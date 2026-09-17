#!/usr/bin/env python3
"""Upload local Markdown images and videos to Tencent COS and replace their links safely."""

from __future__ import annotations

import argparse
import hashlib
import html
import os
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlparse
from urllib.request import Request, urlopen


DEFAULT_COSCMD = Path.home() / ".local/venvs/cos/bin/coscmd"
DEFAULT_BASE_URL = "https://tc-1258979383.cos.ap-guangzhou.myqcloud.com"

IMAGE_EXTENSIONS = {
    ".avif", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".svg", ".tiff", ".webp"
}
VIDEO_EXTENSIONS = {
    ".avi", ".flv", ".m4v", ".mkv", ".mov", ".mp4", ".ogg", ".webm", ".wmv"
}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

MARKDOWN_IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]\n]*)\]\((?P<target>[^)\n]+)\)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[(?P<text>[^\]\n]*)\]\((?P<target>[^)\n]+)\)")
HTML_MEDIA_RE = re.compile(
    r"<(?:img|video|source)\b[^>]*?\bsrc\s*=\s*(?P<quote>['\"])(?P<target>.*?)(?P=quote)",
    re.IGNORECASE,
)
TITLE_SUFFIX_RE = re.compile(r"\s+(?:\"[^\"]*\"|'[^']*')\s*$")
MD5_RE = re.compile(r"(?:x-cos-meta-md5\s+|ETag\s+\")([0-9a-fA-F]{32})")

FENCED_CODE_RE = re.compile(r"(?:```|~~~)[^\n]*\n[\s\S]*?(?:```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


class MigrationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Reference:
    markdown: Path
    start: int
    end: int
    line: int
    local: Path
    raw_target: str
    is_video: bool


@dataclass
class Document:
    path: Path
    text: str
    digest: str
    references: list[Reference]


@dataclass(frozen=True)
class ObjectPlan:
    name: str
    local: Path
    md5: str
    size: int
    url: str
    is_video: bool


def file_md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text_exact(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def target_path_slice(raw: str) -> tuple[str, int, int]:
    leading = len(raw) - len(raw.lstrip())
    core = raw.strip()
    if core.startswith("<"):
        close = core.find(">")
        if close > 1:
            return core[1:close], leading + 1, leading + close

    title = TITLE_SUFFIX_RE.search(core)
    path_part = core[: title.start()].rstrip() if title else core
    return path_part, leading, leading + len(path_part)


def resolve_local_path(markdown: Path, target: str, include_relative: bool) -> Path | None:
    value = html.unescape(target.strip())
    lowered = value.lower()
    if lowered.startswith(("http://", "https://", "data:", "//")) or value.startswith("#"):
        return None

    if lowered.startswith("file://"):
        parsed = urlparse(value)
        if parsed.netloc not in ("", "localhost"):
            return None
        candidate = Path(unquote(parsed.path))
    elif value.startswith("~"):
        candidate = Path(value).expanduser()
    elif os.path.isabs(value):
        candidate = Path(unquote(value))
    elif include_relative:
        candidate = markdown.parent / unquote(value)
    else:
        return None

    candidate = candidate.resolve(strict=False)
    if candidate.suffix.lower() not in MEDIA_EXTENSIONS:
        return None
    return candidate


def find_code_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for match in FENCED_CODE_RE.finditer(text):
        spans.append((match.start(), match.end()))
    for match in INLINE_CODE_RE.finditer(text):
        spans.append((match.start(), match.end()))
    return spans


def is_inside_code(start: int, end: int, code_spans: list[tuple[int, int]]) -> bool:
    return any(start < c_end and end > c_start for c_start, c_end in code_spans)


def discover_references(path: Path, text: str, include_relative: bool) -> list[Reference]:
    references: list[Reference] = []
    occupied: list[tuple[int, int]] = []
    code_spans = find_code_spans(text)

    # 1. Images and HTML media
    for pattern in (MARKDOWN_IMAGE_RE, HTML_MEDIA_RE):
        for match in pattern.finditer(text):
            m_start = match.start("target")
            m_end = match.end("target")
            if is_inside_code(m_start, m_end, code_spans):
                continue
            raw = match.group("target")
            path_text, relative_start, relative_end = target_path_slice(raw)
            local = resolve_local_path(path, path_text, include_relative)
            if local is None:
                continue
            start = m_start + relative_start
            end = m_start + relative_end
            if any(start < old_end and end > old_start for old_start, old_end in occupied):
                continue
            occupied.append((start, end))
            references.append(
                Reference(
                    markdown=path,
                    start=start,
                    end=end,
                    line=text.count("\n", 0, start) + 1,
                    local=local,
                    raw_target=path_text,
                    is_video=local.suffix.lower() in VIDEO_EXTENSIONS,
                )
            )

    # 2. Markdown links pointing directly to media files (e.g. [video](demo.mp4))
    for match in MARKDOWN_LINK_RE.finditer(text):
        m_start = match.start("target")
        m_end = match.end("target")
        if is_inside_code(m_start, m_end, code_spans):
            continue
        raw = match.group("target")
        path_text, relative_start, relative_end = target_path_slice(raw)
        local = resolve_local_path(path, path_text, include_relative)
        if local is None:
            continue
        start = m_start + relative_start
        end = m_start + relative_end
        if any(start < old_end and end > old_start for old_start, old_end in occupied):
            continue
        occupied.append((start, end))
        references.append(
            Reference(
                markdown=path,
                start=start,
                end=end,
                line=text.count("\n", 0, start) + 1,
                local=local,
                raw_target=path_text,
                is_video=local.suffix.lower() in VIDEO_EXTENSIONS,
            )
        )

    return sorted(references, key=lambda ref: ref.start)


def markdown_files(inputs: list[str]) -> list[Path]:
    found: set[Path] = set()
    for raw in inputs:
        path = Path(raw).expanduser()
        if not path.exists():
            raise MigrationError(f"target does not exist: {path}")
        if path.is_dir():
            found.update(item.resolve() for item in path.rglob("*.md") if item.is_file())
        elif path.is_file() and path.suffix.lower() == ".md":
            found.add(path.resolve())
        else:
            raise MigrationError(f"target is not a Markdown file or directory: {path}")
    return sorted(found)


def build_documents(inputs: list[str], include_relative: bool) -> list[Document]:
    documents: list[Document] = []
    for path in markdown_files(inputs):
        text = read_text_exact(path)
        references = discover_references(path, text, include_relative)
        if references:
            documents.append(Document(path, text, text_digest(text), references))
    return documents


def build_object_plans(documents: list[Document], base_url: str) -> dict[Path, ObjectPlan]:
    missing = sorted({ref.local for doc in documents for ref in doc.references if not ref.local.is_file()})
    if missing:
        raise MigrationError("missing local media files:\n" + "\n".join(f"  {path}" for path in missing))

    by_local: dict[Path, ObjectPlan] = {}
    by_name: dict[str, ObjectPlan] = {}
    for local in sorted({ref.local for doc in documents for ref in doc.references}):
        is_video = local.suffix.lower() in VIDEO_EXTENSIONS
        plan = ObjectPlan(
            name=local.name,
            local=local,
            md5=file_md5(local),
            size=local.stat().st_size,
            url=f"{base_url.rstrip('/')}/{quote(local.name)}",
            is_video=is_video,
        )
        existing = by_name.get(plan.name)
        if existing and existing.md5 != plan.md5:
            raise MigrationError(
                f"local basename collision: {existing.local} and {plan.local} both map to {plan.name}"
            )
        by_name[plan.name] = plan
        by_local[local] = plan
    return by_local


def run_cos(coscmd: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [str(coscmd), *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise MigrationError(f"coscmd {' '.join(arguments[:1])} failed: {detail}")
    return result


def remote_exists(coscmd: Path, name: str) -> bool:
    result = run_cos(coscmd, "list", name, "-n", "5")
    return any(line.split() and line.split()[0] == name for line in result.stdout.splitlines())


def remote_md5(coscmd: Path, name: str) -> str | None:
    result = run_cos(coscmd, "info", name)
    match = MD5_RE.search(result.stdout)
    return match.group(1).lower() if match else None


def verify_public(plan: ObjectPlan, timeout: int) -> None:
    request = Request(plan.url, method="HEAD", headers={"User-Agent": "antigravity-cos-media-migrator/1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = response.status
            content_type = response.headers.get("Content-Type", "")
            content_length = response.headers.get("Content-Length")
    except Exception as exc:
        raise MigrationError(f"public verification failed for {plan.url}: {exc}") from exc
    if status_code != 200:
        raise MigrationError(f"public verification returned HTTP {status_code}: {plan.url}")

    lowered_type = content_type.lower()
    valid_prefixes = ("image/", "video/", "application/octet-stream", "application/ogg")
    if not any(lowered_type.startswith(prefix) for prefix in valid_prefixes):
        raise MigrationError(f"public object has unexpected content type ({content_type!r}): {plan.url}")

    if content_length and int(content_length) != plan.size:
        raise MigrationError(
            f"public size mismatch for {plan.name}: local={plan.size}, remote={content_length}"
        )


def prepare_remote(
    plans: list[ObjectPlan], coscmd: Path, overwrite: bool, timeout: int
) -> tuple[list[ObjectPlan], list[ObjectPlan]]:
    if not coscmd.is_file() or not os.access(coscmd, os.X_OK):
        raise MigrationError(f"coscmd is not executable: {coscmd}")

    to_upload: list[ObjectPlan] = []
    reused: list[ObjectPlan] = []
    for plan in plans:
        if not remote_exists(coscmd, plan.name):
            to_upload.append(plan)
            continue
        digest = remote_md5(coscmd, plan.name)
        if digest == plan.md5:
            reused.append(plan)
        elif overwrite:
            to_upload.append(plan)
        else:
            detail = digest or "unknown"
            raise MigrationError(
                f"remote collision for {plan.name}: local md5={plan.md5}, remote md5={detail}; "
                "rename the file or explicitly use --overwrite"
            )

    for plan in to_upload:
        run_cos(coscmd, "upload", str(plan.local), plan.name)
        digest = remote_md5(coscmd, plan.name)
        if digest != plan.md5:
            raise MigrationError(
                f"remote MD5 verification failed for {plan.name}: local={plan.md5}, remote={digest}"
            )

    for plan in [*reused, *to_upload]:
        verify_public(plan, timeout)
    return reused, to_upload


def updated_text(document: Document, plans: dict[Path, ObjectPlan]) -> str:
    text = document.text
    for reference in reversed(document.references):
        url = plans[reference.local].url
        text = text[: reference.start] + url + text[reference.end :]
    return text


def atomic_write(path: Path, text: str, backup_suffix: str | None) -> None:
    if backup_suffix:
        backup = path.with_name(path.name + backup_suffix)
        if backup.exists():
            raise MigrationError(f"backup already exists: {backup}")
        shutil.copy2(path, backup)
    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        os.chmod(temp_name, mode)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def apply_documents(documents: list[Document], plans: dict[Path, ObjectPlan], backup_suffix: str | None) -> None:
    for document in documents:
        current = read_text_exact(document.path)
        if text_digest(current) != document.digest:
            raise MigrationError(f"Markdown changed during upload; refusing to rewrite: {document.path}")
    for document in documents:
        atomic_write(document.path, updated_text(document, plans), backup_suffix)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload locally referenced Markdown images and videos to Tencent COS and replace links."
    )
    parser.add_argument("paths", nargs="+", help="Markdown files or directories to scan")
    parser.add_argument("--apply", action="store_true", help="upload, verify, and rewrite; default is dry-run")
    parser.add_argument(
        "--include-relative",
        action="store_true",
        help="also migrate relative media paths; absolute paths and file:// URLs are always included",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace a same-name remote object with different content; requires explicit user approval",
    )
    parser.add_argument(
        "--backup-suffix",
        help="copy each Markdown file before rewriting, for example .before-cos",
    )
    parser.add_argument("--coscmd", type=Path, default=DEFAULT_COSCMD, help="path to the configured coscmd")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="public COS base URL")
    parser.add_argument("--timeout", type=int, default=20, help="public HEAD timeout in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        documents = build_documents(args.paths, args.include_relative)
        if not documents:
            print("No local media references found.")
            return 0
        plans_by_local = build_object_plans(documents, args.base_url)
        plans = sorted(set(plans_by_local.values()), key=lambda plan: plan.name)

        for document in documents:
            for reference in document.references:
                plan = plans_by_local[reference.local]
                kind = "VIDEO" if plan.is_video else "IMAGE"
                print(f"PLAN [{kind}] {document.path}:{reference.line} {reference.local} -> {plan.url}")
        if not args.apply:
            image_count = sum(1 for p in plans if not p.is_video)
            video_count = sum(1 for p in plans if p.is_video)
            print(f"Dry run: {image_count} image(s), {video_count} video(s), {sum(len(doc.references) for doc in documents)} link(s).")
            return 0

        reused, uploaded = prepare_remote(plans, args.coscmd.expanduser(), args.overwrite, args.timeout)
        apply_documents(documents, plans_by_local, args.backup_suffix)
        for plan in reused:
            print(f"REUSED {plan.name} {plan.url}")
        for plan in uploaded:
            print(f"UPLOADED {plan.name} {plan.url}")
        for document in documents:
            print(f"UPDATED {document.path} ({len(document.references)} link(s))")
        print(
            f"Complete: uploaded={len(uploaded)} reused={len(reused)} "
            f"files={len(documents)} links={sum(len(doc.references) for doc in documents)}"
        )
        return 0
    except MigrationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
