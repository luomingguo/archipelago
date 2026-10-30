// Integration checks for the concept contract, using isolated temporary notes.
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { spawnSync } from 'node:child_process'
import { CONCEPT_HEADINGS, splitFrontmatter } from './notes-lib.mjs'
import { sourceHeadings, remarkStableHeadingIds } from '../frontend/src/lib/heading-ids.ts'
import { chunkDocument } from '../rag/src/chunk.ts'
import { createMarkdownProcessor } from '../frontend/node_modules/@astrojs/markdown-remark/dist/index.js'

const root = fileURLToPath(new URL('../', import.meta.url))
const scratch = await fs.realpath(await fs.mkdtemp(path.join(os.tmpdir(), 'concept-contract-')))
const course = path.join(scratch, 'docs/zh/cs/testing/example')
const file = path.join(course, 'concept/sample.md')
const run = (name, args = []) => {
  const result = spawnSync(process.execPath, [path.join(root, 'tools', name), ...args], { cwd: scratch, encoding: 'utf8' })
  return { ...result, output: `${result.stdout}${result.stderr}` }
}
const lint = () => run('notes-lint.mjs', ['--strict-concept', '--max-errors=0', file])
try {
  await fs.mkdir(course, { recursive: true })
  await fs.symlink(path.join(root, 'NOTESTYLE.md'), path.join(scratch, 'NOTESTYLE.md'))
  await fs.symlink(path.join(root, 'tools'), path.join(scratch, 'tools'))
  await fs.writeFile(path.join(course, 'index.md'), '---\ntitle: Example\ntype: course\ncourse: Example\nstatus: draft\n---\n# Example\n')
  assert.equal(run('notes-new.mjs', ['--course', 'example', '--type', 'concept', '--slug', 'sample', '--title', '样例']).status, 0)
  const original = await fs.readFile(file, 'utf8')
  const { fm, body } = splitFrontmatter(original)
  assert.equal('tags' in fm, false)
  assert.deepEqual([...body.matchAll(/^## (.+)$/gm)].map((m) => m[1]), CONCEPT_HEADINGS)
  assert.equal(lint().status, 0, lint().output)
  assert.match(lint().output, /0 warning/)
  assert.equal(run('notes-fix.mjs', [file]).status, 0)
  assert.equal('tags' in splitFrontmatter(await fs.readFile(file, 'utf8')).fm, false)
  const audit = spawnSync(process.execPath, [path.join(root, '.agents/skills/course-notes-audit/scripts/audit-course.mjs'), course, '--json'], { encoding: 'utf8' })
  const report = JSON.parse(audit.stdout)
  assert.ok(!report.issues.some((issue) => issue.file === 'concept/sample.md'), audit.stdout)

  const renderer = await createMarkdownProcessor({ remarkPlugins: [remarkStableHeadingIds] })
  const emptyHtml = (await renderer.render(body)).code
  assert.equal(sourceHeadings(body).filter((h) => h.depth === 2).length, 0)
  assert.doesNotMatch(emptyHtml, /<h2/)

  const definition = '这是用于检验契约的定义。'
  const filled = body.replace('## 概念界定', `## 概念界定\n\n${definition}`)
    .replace('## 解释与依据', '## 解释与依据\n\n### 子节依据\n\n依据内容。\n\n```text\n## 伪标题\n```')
    .replace('## TL;DR', '## TL;DR\n\n- 问题。\n- 定义。\n- 依据。')
  const html = (await renderer.render(filled)).code
  const headings = sourceHeadings(filled)
  assert.deepEqual(headings.filter((h) => h.depth === 2).map((h) => h.text), ['概念界定', '解释与依据', 'TL;DR'])
  for (const heading of headings) assert.ok(html.includes(`id="${heading.slug}"`), heading.slug)
  assert.doesNotMatch(html, /<h2[^>]*>边界与辨析/)
  const doc = { path: 'sample.md', url: '/sample', lang: 'zh', course: 'Example', title: '样例', docType: 'concept', tags: [], body }
  assert.equal(chunkDocument(doc).length, 0)
  const chunks = chunkDocument({ ...doc, body: filled })
  assert.equal(chunks.filter((c) => c.blockKind === 'summary').length, 1)
  assert.ok(chunks.every((c) => c.content.trim() && c.tags.length === 0))

  await fs.writeFile(file, original.slice(0, original.indexOf('# 样例')).replace('status: draft', 'status: complete') + filled.replace('依据内容。', '依据内容。\n\n::: insight\n作者对案例的判断。\n:::'))
  assert.equal(lint().status, 0, lint().output)

  await fs.writeFile(file, original.replace('status: draft', 'status: complete'))
  assert.notEqual(lint().status, 0)
  await fs.writeFile(file, original.replace('## 概念界定', '## 错误标题'))
  assert.notEqual(lint().status, 0)
  await fs.writeFile(file, original.replace('status: draft', 'tags: [Bad_Tag]\nstatus: draft'))
  assert.notEqual(lint().status, 0)
  const lecture = path.join(course, 'lec1.md')
  await fs.writeFile(lecture, '---\ntitle: 样例\ntype: lecture\nstatus: draft\ntags: [sample, testing]\n---\n# Lec 1 样例\n\n## 正文主题\n\n正文。\n\n## TL;DR\n\n- 一。\n- 二。\n- 三。\n')
  assert.equal(run('notes-lint.mjs', ['--max-errors=0', lecture]).status, 0)
  await fs.appendFile(lecture, '\n## 后续主题\n\n正文。\n')
  assert.notEqual(run('notes-lint.mjs', ['--max-errors=0', lecture]).status, 0)
  console.log('Concept contract: template, lint/fix, rendered HTML/TOC, RAG and TL;DR placement passed.')
} finally {
  await fs.rm(scratch, { recursive: true, force: true })
}
