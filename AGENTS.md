# Repository Guidelines

## Purpose

This repository is a personal Today I Learned (TIL) knowledge base for growing from software engineering into AI and LLM engineering. It records Python, mathematics, machine learning, deep learning, Transformer, evaluation, fine-tuning, and post-training concepts in a form that can be understood and verified later.

Prioritize the following outcomes:

1. Preserve what the author actually learned and questioned.
2. Explain concepts accurately in clear Korean.
3. Verify formulas, hand calculations, shapes, and code outputs.
4. Keep Markdown readable in both VS Code preview and GitHub.
5. Make narrow changes that do not overwrite unrelated learning work.

This root file applies to the entire repository. Add a nested `AGENTS.md` or `AGENTS.override.md` only when a subtree needs more specific rules.

## Repository Layout

- `content/`: topic-based TIL documents.
- `content/mathematics/linear-algebra/`: current linear-algebra learning notes.
- `templates/til.md`: default structure and frontmatter for a new TIL document.
- `assets/`: repository-local images and other media referenced by documents.
- `.vscode/settings.json`: repository-only editor settings, including pasted-media paths.
- `README.md`: repository purpose, topic index, and public writing principles.

Do not rename or relocate Korean filenames, topic directories, or assets unless the user explicitly requests it. Always resolve an exact filename with `rg --files` because Korean spelling, spaces, brackets, and parentheses are significant.

## Working Principles

- Inspect the named file, `templates/til.md`, and one relevant neighboring document before making a substantial edit.
- Treat requests to explain, review, or assess as read-only unless the user also asks for changes.
- When the user asks to edit a named file or section, modify that exact target and preserve their learning flow and existing examples.
- Prefer a small concrete example, intermediate calculations, and shape annotations before a general formula.
- Do not replace beginner-oriented reasoning with an advanced derivation that hides the steps being learned.
- Fix clear spelling, spacing, terminology, formula, and rendering errors during an authorized comprehensive editing pass.
- Remove unused template sections instead of leaving placeholder text. Do not invent references, confusion points, or project applications merely to fill a template.
- Preserve unrelated working-tree changes. If the target overlaps edits that cannot be safely separated, stop and ask the user.

## TIL Document Conventions

Use the frontmatter fields from `templates/til.md`:

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

- Set `date` to the original creation date when known.
- Update `updated` only when the document content changes materially.
- Do not change `publish` unless the user requests publication-status work.
- Use one top-level `#` heading that matches the frontmatter title.
- Prefer the learning flow `오늘의 질문 → 핵심 결론 → 개념 정리 → 직접 확인 → 헷갈리기 쉬운 부분 → 실제 활용 → 한 문장 요약`.
- Keep only sections that have meaningful content; section names may be adapted to the topic.
- Write primarily in Korean. On first use, add an English technical term in parentheses when it improves clarity.
- Keep notation and capitalization consistent within a document, including `shape`, `Query`, `Key`, `Value`, `NumPy`, and matrix symbols.
- For matrix multiplication, state operand shapes, the contracted dimension, result shape, and what each remaining axis means.
- Put executable examples in fenced code blocks with a language identifier. Keep recorded output synchronized with the code.
- Store pasted images under `assets/` through the repository VS Code settings and use repository-relative Markdown links.
- Add a source link when a claim, quotation, diagram, or example depends on external material.

## GitHub-Compatible Mathematics

GitHub rendering is the compatibility target. A formula rendering correctly in VS Code alone is not sufficient.

- Use `$...$` for inline mathematics.
- Use `$$...$$` on separate lines for block mathematics.
- Prefer broadly supported MathJax commands such as `\frac`, `\sqrt`, `\mathbf`, `\mathrm`, `\text`, `\begin{bmatrix}`, and `\begin{aligned}`.
- Do not use the custom operator macro formed by a backslash followed by `operatorname`; GitHub may render it as “The following macros are not allowed.” Use roman text instead, for example `\mathrm{softmax}`, `\mathrm{rank}`, `\mathrm{Var}`, or `\mathrm{proj}`.
- Avoid document-defined or unsafe macros such as `\DeclareMathOperator`, `\newcommand`, `\renewcommand`, `\def`, and `\require`.
- Escape underscores inside roman text, for example `\mathrm{cosine\_similarity}`.
- Inside Markdown tables, avoid literal vertical bars in formulas because they can split cells. Use `\lVert` and `\rVert` for norms.
- Do not use `\(...\)` or `\[...\]`; this repository standardizes on dollar-sign delimiters for VS Code and GitHub compatibility.
- Keep opening and closing math delimiters balanced, and do not place block delimiters inside fenced code blocks unless demonstrating raw Markdown.

After changing any mathematics, scan all Markdown documents for the prohibited operator form. This command should produce no output:

```bash
rg -n '\\operator(name)' -g '*.md' -g '!AGENTS.md' .
```

Also scan for custom macro definitions:

```bash
rg -n '\\(DeclareMathOperator|newcommand|renewcommand|def|require)\b' -g '*.md' -g '!AGENTS.md' .
```

## Verification

Run checks in proportion to the change. A document-editing task is complete only after the relevant checks pass.

1. Inspect the complete changed document, not only the edited paragraph.
2. Search for template remnants, malformed delimiters, prohibited macros, stale outputs, and obvious typos.
3. Run executable code examples with `python3` or the appropriate project virtual environment.
4. Compare displayed numeric results and shapes with actual output.
5. Verify every new or changed relative link points to an existing repository file.
6. Run whitespace validation:

   ```bash
   git diff --check
   ```

7. Review the final changed-file list and diff:

   ```bash
   git status --short
   git diff --name-only
   git diff --stat
   ```

If a Markdown linter is available, run it on the changed documents. Do not claim GitHub rendering was visually verified unless the rendered GitHub page was actually inspected. Report any check that could not be run.

## Commit Rules

Do not commit or push unless the user explicitly asks. A request to commit does not imply permission to push.

Use this commit-message format:

```text
<type>: <concise imperative summary>
```

Preferred types:

- `til`: add or substantially develop a learning note.
- `fix`: correct factual, mathematical, link, code-output, or rendering problems.
- `docs`: update repository-level documentation such as `README.md`, `AGENTS.md`, or templates.
- `chore`: change repository settings, tooling, or maintenance files without changing learning content.

Examples:

```text
til: add attention score and shape notes
fix: make math expressions GitHub-compatible
docs: add repository agent guidelines
chore: configure Markdown image assets
```

Keep one logical change per commit. Before committing:

1. Run `git status --short`.
2. Stage only explicitly authorized files using exact paths.
3. Run `git diff --cached --name-status` and confirm the scope.
4. Review `git diff --cached`.
5. Run `git diff --cached --check`.
6. Commit only after all required validation succeeds.

Never stage unrelated user work with broad commands such as `git add .` or `git add -A`. After committing, report the commit hash, subject, files included, and whether anything remains uncommitted. Do not rewrite, amend, reset, or force-push history unless the user explicitly requests it.

## Code Review Rules

When reviewing changes in this repository, flag the following:

- GitHub-incompatible or unbalanced mathematical syntax.
- A formula, matrix shape, code result, or explanation that contradicts the executable example.
- Broken relative links or missing repository-local assets.
- Missing or malformed frontmatter in a new TIL document.
- Accidental changes to `date`, `publish`, filenames, or unrelated notes.
- Placeholder template text presented as completed content.
- Unsupported claims or copied material without a necessary source.
- Large rewrites that remove the author's questions, intermediate reasoning, or beginner-friendly examples without being requested.

For each issue, explain the concrete failure and suggest the smallest safe correction.
