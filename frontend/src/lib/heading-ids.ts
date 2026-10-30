import { visit } from 'unist-util-visit';

export interface SourceHeading {
  depth: number;
  slug: string;
  text: string;
}

export function slugifyHeading(value: string): string {
  return value
    .normalize('NFKD')
    .replace(/[\u0300-\u036F]/g, '')
    .replace(/[\u0000-\u001f]/g, '')
    .replace(/[\s~`!@#$%^&*()\-_+=[\]{}|\\;:"'“”‘’<>,.?/]+/g, '-')
    .replace(/-{2,}/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/^(\d)/, '_$1')
    .toLowerCase();
}

function plainHeading(value: string): string {
  return value
    .replace(/`([^`]*)`/g, '$1')
    .replace(/\*\*([^*]*)\*\*/g, '$1')
    .replace(/\*([^*]*)\*/g, '$1')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .trim();
}

function withoutCodeFences(source: string): string {
  const lines = source.split('\n');
  let marker = '';
  let length = 0;
  for (let index = 0; index < lines.length; index += 1) {
    const match = /^([ \t]*(?:[-*+]|\d+[.)])?[ \t]*)(`{3,}|~{3,})(.*)$/.exec(lines[index]);
    if (!match) {
      if (marker) lines[index] = ' '.repeat(lines[index].length);
      continue;
    }
    const currentMarker = match[2][0];
    if (!marker) {
      marker = currentMarker;
      length = match[2].length;
      lines[index] = ' '.repeat(lines[index].length);
    } else if (currentMarker === marker && match[2].length >= length) {
      marker = '';
      length = 0;
      lines[index] = ' '.repeat(lines[index].length);
    } else {
      lines[index] = ' '.repeat(lines[index].length);
    }
  }
  return lines.join('\n');
}

export function sourceHeadings(source: string): SourceHeading[] {
  const seen = new Map<string, number>();
  const emptyRanges = emptyConceptSections(source);
  return [...withoutCodeFences(source).matchAll(/^(#{1,6})[ \t]+(.+)$/gm)].flatMap((match) => {
    const text = plainHeading(match[2]);
    const base = slugifyHeading(text);
    if (!base) return [];
    const count = seen.get(base) ?? 0;
    seen.set(base, count + 1);
    if (emptyRanges.some(([start, end]) => match.index! >= start && match.index! < end)) return [];
    return [{ depth: match[1].length, text, slug: count ? `${base}-${count}` : base }];
  });
}

/** Only the fixed concept scaffold may hide empty sections; preserve all source text and IDs. */
export function emptyConceptSections(source: string): [number, number][] {
  const headings = [...withoutCodeFences(source).matchAll(/^##[ \t]+(.+)$/gm)];
  const expected = ['问题情境', '概念界定', '解释与依据', '边界与辨析', '提取与迁移', '关联与来源', 'TL;DR'];
  if (headings.map((h) => h[1].trim()).join('|') !== expected.join('|')) return [];
  // Locate section boundaries without treating fenced examples as headings.
  const lines = source.split('\n');
  const masked = withoutCodeFences(source).split('\n');
  const positions: number[] = [];
  let offset = 0;
  for (let i = 0; i < lines.length; i++) {
    if (/^##[ \t]+/.test(masked[i])) positions.push(offset);
    offset += lines[i].length + 1;
  }
  return positions.flatMap((start, i) => {
    const end = positions[i + 1] ?? source.length;
    const content = source.slice(start, end).replace(/^#{2,6}[ \t]+.*$/gm, '').replace(/<!--[\s\S]*?-->/g, '').trim();
    return content ? [] : [[start, end] as [number, number]];
  });
}

export function remarkStableHeadingIds() {
  return (tree: any, file: any) => {
    const source = String(file.value ?? '');
    const seen = new Map<string, number>();
    visit(tree, 'heading', (node: any) => {
      const start = node.position?.start?.offset;
      const end = node.position?.end?.offset;
      if (typeof start !== 'number' || typeof end !== 'number') return;

      // RAG references were generated from the literal Markdown heading text.
      // Reading the source slice here keeps math commands and inline HTML intact;
      // deriving the id after KaTeX/HTML rendering would silently change old URLs.
      const raw = source.slice(start, end).replace(/^#{1,6}[ \t]+/, '');
      const base = slugifyHeading(plainHeading(raw));
      if (!base) return;
      const count = seen.get(base) ?? 0;
      seen.set(base, count + 1);
      node.data = {
        ...(node.data ?? {}),
        hProperties: {
          ...(node.data?.hProperties ?? {}),
          id: count ? `${base}-${count}` : base,
        },
      };
    });
    const emptyRanges = emptyConceptSections(source);
    tree.children = tree.children.filter((node: any) => !emptyRanges.some(([start, end]) =>
      node.position?.start?.offset >= start && node.position?.start?.offset < end));
  };
}
