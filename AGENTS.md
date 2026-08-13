# Repository Guidelines

## Purpose

This is a lightweight personal TIL repository for studying toward an LLM Research Engineer role. Keep learning notes easy to write, find, and revisit. Do not turn the repository into a learning-management system.

## Layout

- `materials/`: source files. Copyrighted or private files belong in ignored `materials/private/`.
- `til/`: short learning notes organized by area and date.
- `practice/`: code, Kaggle work, model experiments, and benchmarks that were actually run.
- `ROADMAP.md`: broad learning direction, not a status tracker.
- `content/`: previous long-form notes; preserve them.
- `templates/`: lightweight TIL and practice templates.

The normal flow is:

```text
study -> write a short TIL -> optionally get feedback
-> save substantial practice separately
```

No daily streak, promotion status, separate review log, progress table, or canonical-note gate is required.

## Working rules

- Resolve exact paths with `rg --files`; Korean spelling, spaces, brackets, and parentheses are significant.
- Preserve unrelated working-tree changes.
- Treat review and explanation requests as read-only unless the user asks for edits.
- Use `apply_patch` for text edits.
- Do not rename, relocate, delete, or rewrite existing `content/` notes in bulk.
- Never invent sources, learner claims, code output, experiments, or results.
- Verify current recommendations such as Kaggle competitions, libraries, models, and tools.

## Tutoring

- Start from the learner's note when they provide one.
- Say what is correct, what needs correction, and what useful idea is missing.
- Compress ordinary programming basics unless they affect shapes, gradients, numerical behavior, or model meaning.
- For difficult topics, connect intuition, a small example, formulas and shapes, code, and actual ML/LLM use.
- Suggest one fitting exercise instead of a long task list.
- Use Kaggle when data handling, validation, metrics, or error analysis is the point; use local code or benchmarks for mechanics and systems topics.

## Notes and practice

- Keep TIL files short. Delete unused template sections.
- Short code may stay in a TIL; create `practice/` only when the work deserves separate files.
- Record only observed results from code that actually ran.
- Keep datasets, model weights, credentials, and large generated files out of Git unless explicitly authorized and appropriate.
- Treat PDFs as sources, not public notes. Include toggle children, figures, code, tables, and formulas when exporting Notion pages.

## Markdown and verification

- Target GitHub Markdown.
- Use `$...$` and `$$...$$` for math.
- Give fenced code blocks a language identifier.
- Keep relative links resolvable and use one top-level heading in finished notes.
- Run the TIL validator when applicable:

```bash
python3 .agents/skills/organize-til-notes/scripts/validate_til_markdown.py path/to/changed.md
```

- Read changed files, run relevant code, and check `git diff --check` before finishing.
- For PDFs, render and visually inspect the relevant pages.

## Git

Do not commit or push unless the user explicitly asks. A request to commit does not imply permission to push. Stage only exact authorized paths, review the staged diff, and never rewrite history or force-push without explicit authorization.
