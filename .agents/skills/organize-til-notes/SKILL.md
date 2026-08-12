---
name: organize-til-notes
description: Organize, revise, and validate Korean lecture notes, rough Markdown drafts, or learning summaries as structured TIL documents in this repository. Use when the user asks to summarize, refine, restructure, complete, or verify a TIL note while preserving their questions, examples, and reasoning. Do not use for generic repository maintenance, Git-only work, or read-only conceptual explanations that do not involve organizing a TIL document.
---

# Organize TIL Notes

Turn the author's raw learning record into a readable, verifiable Korean TIL document without replacing their reasoning with a generic textbook summary.

## Establish the task boundary

1. Resolve the exact target with `rg --files`; preserve Korean spelling, spaces, brackets, and parentheses in paths.
2. Read the entire target, `templates/til.md`, and one relevant neighboring document before editing substantially.
3. Distinguish the requested action:
   - For explanation, review, feasibility, or direction checks, inspect and respond without editing.
   - For requests to refine, organize, correct, complete, or apply changes, edit the exact authorized target.
4. Preserve unrelated working-tree files and changes. Never broaden the edit or commit scope silently.

## Preserve the learning record

- Retain the author's original questions, concrete examples, intermediate calculations, and points of confusion.
- Correct factual, mathematical, terminology, spelling, spacing, and rendering errors during an authorized comprehensive pass.
- Start difficult explanations with a small trace or numeric example, show intermediate states or shapes, and then generalize.
- Do not hide beginner-relevant steps behind a finished formula, advanced abstraction, or replacement solution.
- Do not invent a confusion point, reference, experiment, or practical application merely to fill the template.
- Remove empty placeholder sections and template instructions when no meaningful content exists.

## Structure the document

Use the frontmatter fields and defaults from `templates/til.md`:

```yaml
title: "문서 제목"
description: "문서의 핵심 내용을 설명하는 한두 문장"
date: YYYY-MM-DD
updated: YYYY-MM-DD
category: category-name
tags:
  - tag-name
publish: false
```

- Preserve the original `date` when known.
- Update `updated` only for a material content change.
- Do not change `publish` unless the user requests it.
- Use one top-level heading that represents the frontmatter title.
- Prefer `오늘의 질문 → 핵심 결론 → 개념 정리 → 직접 확인 → 헷갈리기 쉬운 부분 → 실제 활용 → 한 문장 요약`.
- Adapt or omit sections when the content requires it; do not impose the sequence mechanically.
- Write primarily in clear Korean. Add an English technical term in parentheses on first use when it helps.
- Keep symbols, terminology, capitalization, and code names consistent throughout the document.

## Explain mathematics and code

- Follow the root `AGENTS.md` rules for GitHub-compatible Markdown, mathematics, emphasis, links, and media.
- For matrix multiplication, state both operand shapes, the contracted dimension, the result shape, and the meaning of each remaining axis.
- Distinguish mathematical operations precisely, such as `@` versus `*`, inner product versus cosine similarity, and raw score versus normalized or scaled score.
- Put executable examples in fenced blocks with a language identifier.
- Run code with `python3` or an appropriate verified virtual environment; never infer recorded output when it can be executed safely.
- Compare displayed numeric values, array contents, and shapes with the actual output.
- State clearly when a visual renderer or external page was not visually inspected.

## Validate the result

Run the bundled validator on every changed TIL document from the repository root:

```bash
python3 .agents/skills/organize-til-notes/scripts/validate_til_markdown.py path/to/changed.md
```

The validator checks frontmatter, final newlines, heading count, fenced code blocks, math delimiters, prohibited macros, Korean bold-emphasis boundaries, placeholder remnants, and relative links.

Then complete the checks the script cannot establish:

1. Read the complete revised document from top to bottom.
2. Execute relevant code and compare its output with the note.
3. Review `git diff --check`, `git diff --name-only`, and `git diff --stat`.
4. If committing was explicitly requested, follow the exact-path staging and commit rules in root `AGENTS.md`.

Report which checks passed and any check that could not be run. Do not claim GitHub rendering success until the committed or pushed page has actually been inspected on GitHub.
