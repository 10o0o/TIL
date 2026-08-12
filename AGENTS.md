# Repository Guidelines

## Purpose and Scope

This repository is a personal Today I Learned (TIL) knowledge base for software engineering, Python, mathematics, machine learning, deep learning, Transformers, and LLM engineering.

Apply these priorities across the repository:

1. Preserve the author's files, learning history, and unrelated work.
2. Keep explanations accurate and readable in Korean.
3. Verify formulas, code output, links, and Markdown structure in proportion to the change.
4. Keep documents compatible with both VS Code preview and GitHub.
5. Make narrow, explicitly authorized changes.

This root file applies to the entire repository. Use a nested `AGENTS.md` or `AGENTS.override.md` only when a subtree requires stricter or different rules.

## Repository Layout

- `content/`: topic-based TIL documents.
- `templates/til.md`: the default TIL structure and frontmatter template.
- `assets/`: repository-local images and other document media.
- `.agents/skills/`: repository-scoped repeatable workflows.
- `.vscode/settings.json`: repository-only editor settings.
- `README.md`: repository purpose and public writing principles.

Use the repository-scoped `organize-til-notes` Skill when a request involves organizing, revising, completing, or validating a lecture-based TIL draft. Keep task-specific authoring procedures in that Skill rather than expanding this file.

## Working Agreements

- Resolve exact paths with `rg --files` before acting. Korean spelling, spaces, brackets, and parentheses in filenames are significant.
- Do not rename or relocate documents, directories, or assets unless the user explicitly requests it.
- Treat explanation, review, diagnosis, and feasibility requests as read-only unless the user also asks for a change.
- When editing is requested, modify the exact authorized target and preserve existing examples and intent.
- Preserve unrelated working-tree changes. If safe separation is impossible, stop and ask the user.
- Do not create references, results, confusion points, or claims that are not supported by the user's material or an identified source.
- Store pasted document media under `assets/` through the repository VS Code settings and use repository-relative links.

## Markdown Compatibility

GitHub rendering is the compatibility target. Rendering correctly in VS Code alone is not sufficient.

- Use `$...$` for inline mathematics and `$$...$$` on separate lines for block mathematics.
- Prefer broadly supported MathJax commands such as `\frac`, `\sqrt`, `\mathbf`, `\mathrm`, `\text`, `\begin{bmatrix}`, and `\begin{aligned}`.
- Do not use the custom operator macro formed by a backslash followed by `operatorname`; GitHub may reject it. Use `\mathrm{softmax}`, `\mathrm{rank}`, `\mathrm{Var}`, or similar roman text.
- Do not define document macros with `\DeclareMathOperator`, `\newcommand`, `\renewcommand`, `\def`, or `\require`.
- Escape underscores inside roman text, for example `\mathrm{cosine\_similarity}`.
- In Markdown tables, use `\lVert` and `\rVert` for norms instead of literal vertical bars that can split cells.
- Do not use `\(...\)` or `\[...\]`; standardize on dollar-sign delimiters.
- Keep math delimiters and fenced code blocks balanced. Give opening code fences a language identifier.
- When Korean text immediately follows bold emphasis, include the particle or ending inside the bold delimiters, or place whitespace or punctuation after the closing marker. Prefer `**지도학습은**` or `**지도학습**: ...` over `**지도학습**은`.
- Use one top-level heading in a finished TIL document and keep relative links resolvable from the document's directory.

## Verification

Run checks in proportion to the change and report any check that could not be run.

For changed TIL documents, run the repository validator with exact paths:

```bash
python3 .agents/skills/organize-til-notes/scripts/validate_til_markdown.py path/to/changed.md
```

Also complete the checks that apply:

1. Inspect the complete changed document or configuration file.
2. Run executable examples with `python3` or an appropriate verified virtual environment.
3. Compare recorded numeric results, shapes, and output with actual execution.
4. Verify changed relative links and repository-local assets exist.
5. Run `git diff --check`.
6. Review `git status --short`, `git diff --name-only`, and `git diff --stat`.

If a Markdown linter is available, run it on changed documents. Do not claim GitHub rendering was visually verified unless the rendered GitHub page was actually inspected.

## Commit Rules

Do not commit or push unless the user explicitly asks. A request to commit does not imply permission to push.

Use `<type>: <concise imperative summary>` with these preferred types:

- `til`: add or substantially develop a learning note.
- `fix`: correct factual, mathematical, link, output, or rendering problems.
- `docs`: update repository-level documentation, instructions, or templates.
- `chore`: change settings, tooling, or maintenance files without changing learning content.

Keep one logical change per commit. Before committing:

1. Run `git status --short`.
2. Stage only explicitly authorized files using exact paths.
3. Confirm scope with `git diff --cached --name-status`.
4. Review `git diff --cached`.
5. Run `git diff --cached --check`.
6. Commit only after required validation succeeds.

Never use `git add .` or `git add -A` when unrelated work exists. After committing, report the commit hash, subject, included files, and remaining uncommitted changes. Do not amend, rewrite, reset, or force-push history unless the user explicitly requests it.

## Code Review Rules

Flag the following during review:

- GitHub-incompatible or unbalanced Markdown and mathematics.
- Formulas, shapes, code results, or prose that contradict executable examples.
- Broken relative links or missing repository-local assets.
- Accidental changes to dates, publication status, filenames, or unrelated notes.
- Placeholder text presented as finished content.
- Unsupported claims or copied material without a necessary source.
- Broad rewrites that remove the author's intent without being requested.

For each issue, explain the concrete failure and recommend the smallest safe correction.
