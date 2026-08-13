# Repository Guidelines

## Purpose and Scope

This repository is a personal AI/ML/LLM learning record. Its goal is not to maximize the number or length of lecture summaries, but to preserve durable understanding and evidence that the author can recall, explain, apply, implement, and later reproduce what was learned.

Apply these priorities across the repository:

1. Preserve the author's files, learning history, assets, and unrelated work.
2. Treat lecture PDFs and existing notes as sources, not automatic proof of mastery.
3. Keep explanations accurate and readable in Korean.
4. Verify formulas, Tensor shapes, code output, links, and Markdown structure in proportion to the change.
5. Keep documents compatible with both VS Code preview and GitHub.
6. Make narrow, explicitly authorized changes.

This root file applies to the entire repository. Use a nested `AGENTS.md` or `AGENTS.override.md` only when a subtree requires stricter or different rules.

## Repository Layout

- `content/`: preserved lecture-order and concept-oriented legacy notes; do not reorganize in bulk.
- `concepts/`: one current, canonical note per concept after learning evidence exists.
- `til/`: short daily logs of changed understanding, not lecture transcripts.
- `labs/`: executable experiments, observed outputs, and interpretations.
- `curriculum/`: source inventory, prerequisite map, progress, and migration planning.
- `reviews/`: delayed recall and spaced-review records.
- `templates/`: concise TIL, concept, lab, and review templates.
- `assets/`: repository-local images and other document media.
- `.agents/skills/organize-til-notes/`: existing workflow for an explicitly requested note revision or consolidation.
- `.vscode/settings.json`: repository-only editor settings.
- `README.md`: concise public entry point.
- `GUIDE.md`: the learner's operating manual.

Do not add a repository Skill, prompt wrapper, or agent configuration to imitate the ChatGPT Work UI or its execution mode. The repository stores learning artifacts and instructions only.

Use the repository-scoped `organize-til-notes` Skill only when a request involves organizing, revising, consolidating, or validating a specific learning document. It is not a repository implementation of the ChatGPT UI or an autonomous learning mode.

## Working Agreements

- Resolve exact paths with `rg --files` before acting. Korean spelling, spaces, brackets, and parentheses in filenames are significant.
- Do not rename, relocate, delete, or rewrite existing learning documents or assets in bulk.
- Record suspected misclassification or duplication in `curriculum/note-inventory.md` before considering a move.
- Do not move a legacy file until its relative links and inbound references have been checked.
- Treat explanation, review, diagnosis, and feasibility requests as read-only unless the user also asks for a change.
- When editing is requested, modify the exact authorized target and preserve existing questions, examples, calculations, confusion points, and intent.
- Preserve unrelated working-tree changes. If safe separation is impossible, stop and ask the user.
- Do not invent references, results, confusion points, experiments, applications, or mastery evidence.
- Store pasted document media under `assets/` through the repository VS Code settings and use repository-relative links.

## Learning Evidence

Use these terms consistently:

- `seen`: encountered in a source or legacy note.
- `recognized`: understandable while looking at an explanation.
- `explained`: accurately explained without the source.
- `applied`: used to solve a new numeric, shape, interpretation, or debugging problem.
- `implemented`: implemented or debugged in a minimal executable example.
- `retained`: explained and applied again after a delayed review.

A Markdown file, polished prose, commit, or long study session is not by itself evidence of understanding.

Before creating or materially expanding a canonical concept note, require evidence for both `explained` and `applied`. Code-heavy concepts may also require `implemented`. If the evidence is missing, keep the progress status honest and leave the unresolved question visible.

Prefer this learning order:

```text
closed-book recall
→ diagnostic questions
→ explanation of identified gaps
→ small numeric example
→ formula and Tensor shapes
→ code or application problem
→ learner teach-back
→ minimum justified documentation
→ spaced review
```

## Artifact Boundaries

- Keep one canonical concept per file and search for an existing note before creating another.
- Keep TIL entries focused on a changed mental model: prior misunderstanding, corrected understanding, evidence, remaining question, and next review date.
- Create a lab only for code that was actually executed. Record the command, relevant environment assumptions, observed output, and interpretation.
- Use `curriculum/` for PDF-wide mapping and progress, not long concept explanations.
- Use `reviews/` for delayed recall results, including failures and status downgrades.
- Do not backfill missed dates or create a file merely to satisfy a template.
- Preserve `content/` as source history. Migrate one concept at a time only when it becomes relevant and the learner has revalidated it.

## Teaching, Mathematics, and Code

For difficult ML, DL, mathematics, or LLM concepts, prefer:

```text
problem
→ motivation
→ intuition
→ small numeric example
→ exact definition and formula
→ Tensor shapes and axis meanings
→ code mapping
→ actual ML/LLM use
→ learner teach-back
```

- Compress ordinary programming basics unless they affect broadcasting, shape, gradient flow, numerical behavior, or model semantics.
- When using a metaphor, distinguish it from the actual Tensor, operation, learned parameter, and output.
- When explaining library internals, distinguish the mathematical object, a small hand calculation, and the numerical algorithm used by the library.
- For matrix or Tensor operations, state operand shapes, contracted or broadcast dimensions, result shape, and the meaning of every remaining axis.
- Distinguish `@` from `*`, inner product from cosine similarity, raw scores from normalized scores, and pedagogical simplification from actual implementation.
- Run executable examples when safe. Never present inferred output as executed output.

## Markdown Compatibility

GitHub rendering is the compatibility target. Rendering correctly in VS Code alone is not sufficient.

- Use `$...$` for inline mathematics and `$$...$$` on separate lines for block mathematics.
- Prefer broadly supported MathJax commands such as `\frac`, `\sqrt`, `\mathbf`, `\mathrm`, `\text`, `\begin{bmatrix}`, and `\begin{aligned}`.
- Do not use the custom operator macro formed by a backslash followed by `operatorname`; use `\mathrm{softmax}`, `\mathrm{rank}`, `\mathrm{Var}`, or similar roman text.
- Do not define document macros with `\DeclareMathOperator`, `\newcommand`, `\renewcommand`, `\def`, or `\require`.
- Escape underscores inside roman text, for example `\mathrm{cosine\_similarity}`.
- In Markdown tables, use `\lVert` and `\rVert` for norms instead of literal vertical bars that can split cells.
- Do not use `\(...\)` or `\[...\]`; standardize on dollar-sign delimiters.
- Keep math delimiters and fenced code blocks balanced. Give opening code fences a language identifier.
- When Korean text immediately follows bold emphasis, include the particle or ending inside the bold delimiters, or place whitespace or punctuation after the closing marker.
- Use one top-level heading in a finished learning document and keep relative links resolvable from the document's directory.

## Verification

Run checks in proportion to the change and report any check that could not be run.

For changed TIL or concept documents compatible with the existing schema, run the repository validator with exact paths:

```bash
python3 .agents/skills/organize-til-notes/scripts/validate_til_markdown.py path/to/changed.md
```

Also complete the checks that apply:

1. Inspect every changed file from top to bottom.
2. Check heading hierarchy, fenced code blocks, frontmatter/YAML, and relative links.
3. Run executable examples and compare recorded values, shapes, and output with actual execution.
4. Run `git diff --check`.
5. Review `git status --short`, `git diff --name-only`, and `git diff --stat`.

If a Markdown linter is available, run it on changed documents. Do not claim GitHub rendering was visually verified unless the rendered GitHub page was actually inspected.

## Commit Rules

Do not commit or push unless the user explicitly asks. A request to commit does not imply permission to push.

Use `<type>: <concise imperative summary>` with these preferred types:

- `til`: add a short changed-understanding log.
- `learn`: add an evidence-backed concept artifact.
- `lab`: add or revise an executable experiment.
- `review`: record delayed recall.
- `fix`: correct factual, mathematical, link, output, or rendering problems.
- `docs`: update repository-level documentation, instructions, curriculum, or templates.
- `chore`: change settings or tooling without changing learning content.

Keep one logical change per commit. Before committing:

1. Run `git status --short`.
2. Stage only explicitly authorized files using exact paths.
3. Confirm scope with `git diff --cached --name-status`.
4. Review the complete staged diff.
5. Run `git diff --cached --check`.
6. Commit only after required validation succeeds.

Never use `git add .` or `git add -A` when unrelated work exists. After committing, report the commit hash, subject, included files, and remaining uncommitted changes. Do not amend, rewrite, reset, or force-push history unless the user explicitly requests it.

## Code Review Rules

Flag:

- polished notes without learning evidence
- duplicate canonical concepts
- lecture-order organization that hides prerequisites
- formulas, shapes, code results, or prose that contradict executable examples
- broken relative links or missing repository-local assets
- accidental changes to dates, publication status, filenames, or unrelated notes
- placeholder text presented as finished content
- unsupported claims or copied material without a necessary source
- broad rewrites that remove the author's intent

For each issue, explain the concrete failure and recommend the smallest safe correction.
