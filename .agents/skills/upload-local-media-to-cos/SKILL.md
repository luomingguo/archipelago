---
name: upload-local-media-to-cos
description: Upload images and videos referenced by Markdown from local absolute paths, file:// URLs, or explicitly selected relative paths to the user's Tencent COS object storage (bucket tc-1258979383), verify public accessibility, and replace Markdown and HTML media links in place. Use when encountering local image/video paths (/Users/..., file://, relative media, typora-user-images), or when the user asks to upload note images/videos to COS/图床/对象存储.
---

# Upload local Markdown images and videos to COS

Use the bundled script for the fragile scan, collision check, upload, verification, and rewrite sequence. Keep Markdown unchanged until every object is available and publicly readable.

## Storage contract

- Treat “对象存储”, “COS”, and “图床” as Tencent COS bucket `tc-1258979383` in `ap-guangzhou`, unless the user names another service.
- Upload every object to the bucket root using its filename only. Never add a directory prefix.
- Build public URLs from `https://tc-1258979383.cos.ap-guangzhou.myqcloud.com/<encoded-filename>`.
- Use `~/.local/venvs/cos/bin/coscmd` with `~/.cos.conf`. Never print, copy, or commit the credentials.
- Treat upload as an external write. Use it only when the user requested or approved the upload.

## Supported media formats

- **Images**: `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.gif`, `.avif`, `.ico`, `.bmp`, `.tiff`
- **Videos**: `.mp4`, `.webm`, `.mov`, `.m4v`, `.ogg`, `.avi`, `.mkv`, `.flv`
- Media references can be Markdown images `![alt](path)`, Markdown links to media `[text](path.mp4)`, HTML `<img>`, `<video>`, or `<source>`.
- Code blocks (fenced code blocks and inline code spans) are automatically ignored so syntax examples are never modified.

## Workflow

1. Inspect the Markdown targets and repository status. Preserve unrelated changes.
2. Run a dry scan first:

   ```bash
   python3 <skill-directory>/scripts/migrate_markdown_media.py path/to/note.md
   ```

   Pass a directory to scan its Markdown recursively. Absolute paths and `file://` URLs are included by default. Add `--include-relative` only when the user also wants portable relative images/videos moved to COS.

3. Review every resolved local file and proposed URL. Stop on missing files or basename collisions.
4. Apply only after the targets are correct:

   ```bash
   python3 <skill-directory>/scripts/migrate_markdown_media.py --apply path/to/note.md
   ```

   The script performs exact-name remote checks, reuses an object only when its MD5 matches, refuses a different same-name object, uploads absent objects, verifies remote MD5 and public HTTP access (checking HTTP 200 and image/video content-type), then atomically rewrites references.

5. Use `--overwrite` only after the user explicitly approves replacing a different existing object. Prefer a new unique filename otherwise.
6. Inspect the Markdown diff, search the scope for residual `/Users/`, `file://`, and `typora-user-images`, and confirm each new URL returns HTTP 200 with an image or video content type.

## Safety and failure handling

- Do not replace a local link with a predicted URL before upload and public verification succeed.
- Do not bulk-upload the entire Typora image directory unless the user explicitly asks for that scope.
- If a run fails after uploading some objects, leave the Markdown unchanged. Rerun safely; matching objects are reused.
- Use `--backup-suffix=.before-cos` for non-Git files when a local backup is useful. Do not leave backups inside a Git repository without reporting them.
- Report uploaded, reused, updated, missing, and skipped items separately. Never report an unverified URL as complete.
