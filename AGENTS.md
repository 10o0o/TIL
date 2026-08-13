# Repository Guidelines

## Purpose

This repository is an active-learning knowledge system for the author's transition from software engineering to AI/ML/LLM research engineering.

The primary outcome is not a large number of lecture summaries. The primary outcome is evidence that the author can:

- explain a concept without notes
- apply it to a new numeric, tensor-shape, or interpretation problem
- connect formulas to Python, NumPy, or PyTorch
- implement or debug code when implementation matters
- reproduce the knowledge after a delayed review

Read `GUIDE.md` before substantial learning-system changes.

## Repository Sources of Truth

- `curriculum/`: concept inventory, prerequisites, priority, and learning status
- `concepts/`: one canonical document per mastered concept
- `til/`: short logs of changed understanding
- `labs/`: executed code and experiments
- `reviews/`: delayed recall and weekly review
- `content/`: preserved v1 lecture and concept notes; treat as legacy source material
- `archive/README.md`: migration policy
- `templates/`: document templates
- `.agents/skills/kant-learning-cycle/`: primary active-learning workflow
- `.agents/skills/organize-til-notes/`: secondary single-document maintenance workflow

## Default Workflow

Use `$kant-learning-cycle` for:

- analyzing multiple lecture PDFs
- curriculum and dependency mapping
- prerequisite diagnosis
- adaptive concept tutoring
- numeric and Tensor-shape exercises
- teach-back assessment
- progress tracking
- selective legacy migration
- creation of minimal TIL, concept, lab, and review artifacts

Use `$organize-til-notes` only for an explicitly named existing document or a verified one-concept migration.

Do not create a long lecture summary by default.

## Learning Evidence Rules

Use these status meanings consistently:

- `seen`: encountered
- `recognized`: understandable with support
- `explained`: explained accurately without notes
- `applied`: solved a new example
- `implemented`: implemented or debugged
- `retained`: reproduced after delayed review

A file's existence, length, polish, or commit date is not evidence of mastery.

Before creating or materially expanding a canonical note, obtain `explained` and `applied` evidence. Code-heavy topics may require `implemented`.

When evidence is missing:

- update only `curriculum/progress.md`
- keep the status honest
- leave the unresolved question visible
- do not fill templates with plausible-sounding content

## Writing Boundaries

- Preserve the author's original questions, examples, intermediate calculations, and learning history.
- Do not invent confusion points, experiment results, citations, or practical uses.
- Keep one canonical concept per file.
- Search for an existing concept file before creating a new one.
- Keep TIL files to changed understanding rather than lecture transcription.
- Do not backfill missed dates for completeness.
- Keep executed code and outputs in `labs/`.
- Keep large PDF-wide mapping work in `curriculum/`.
- Preserve `content/` paths unless relocation is explicitly requested and all affected links are repaired.

## Teaching and Explanation Rules

For difficult ML, DL, mathematics, or LLM concepts, prefer:

```text
problem
→ motivation
→ intuition
→ small numeric example
→ formula and term meanings
→ Tensor shapes and axis meanings
→ code mapping
→ actual ML/LLM use
→ learner teach-back
```

Compress ordinary programming basics unless they affect broadcasting, shape, gradient flow, numerical behavior, or model semantics.

When using a metaphor, distinguish it from the actual Tensor, operation, learned parameter, and output.

When explaining library internals, distinguish:

1. the mathematical object being computed
2. a hand calculation for a small example
3. the numerical algorithm used by the library

## Markdown Compatibility

GitHub rendering is the compatibility target.

- Use `$...$` for inline mathematics.
- Use `$$...$$` on separate lines for block mathematics.
- Prefer supported commands such as `\frac`, `\sqrt`, `\mathbf`, `\mathrm`, `\text`, `\begin{bmatrix}`, and `\begin{aligned}`.
- Do not define custom MathJax macros.
- Do not use `\(...\)` or `\[...\]`.
- Escape underscores inside roman math text.
- In Markdown tables, use `\lVert` and `\rVert` rather than literal norm bars.
- Keep math delimiters and fenced code blocks balanced.
- Give each fenced code block a language identifier.
- Use one top-level heading in finished learning documents.
- Keep relative links resolvable from the file's directory.

## Mathematics and Tensor Rules

For matrix or Tensor operations, include:

- each operand shape
- the dimension being contracted or broadcast
- the result shape
- the semantic meaning of each remaining axis
- the mapping between the formula and code

Distinguish precisely:

- element-wise multiplication and matrix multiplication
- inner product and cosine similarity
- logits, raw scores, probabilities, and normalized weights
- statistical bias and a neural-network bias parameter
- derivative, partial derivative, gradient, and Jacobian
- pedagogical simplification and actual model implementation

## Code and Experiment Rules

- Run executable examples when safe.
- Do not record inferred output as executed output.
- Compare displayed values, array contents, and shapes with the actual result.
- Use a small reproducible script when a notebook is unnecessarily large.
- Record environment-specific assumptions.
- Put substantial experiments under `labs/` and link them from concept notes.

## Verification

Run checks in proportion to the change.

For applicable Markdown learning documents:

```bash
python3 .agents/skills/organize-til-notes/scripts/validate_til_markdown.py path/to/changed.md
```

Also complete the checks that apply:

1. read the complete changed file
2. execute relevant code and compare output
3. verify changed relative links and repository-local assets
4. run `git diff --check`
5. review `git status --short`, `git diff --name-only`, and `git diff --stat`

Do not claim GitHub rendering was visually verified unless the committed page was actually inspected on GitHub.

## Git and Commit Rules

Do not modify unrelated files.

Use these commit prefixes:

- `learn`: add evidence-backed learning artifacts
- `til`: add a short changed-understanding log
- `lab`: add or revise an experiment
- `review`: record delayed recall
- `docs`: update repository-level guidance or curriculum
- `fix`: correct factual, mathematical, code, link, or rendering errors
- `chore`: tooling or maintenance without learning-content changes

Before committing:

1. inspect status and diff
2. stage only authorized exact paths
3. run applicable validation
4. keep one logical change per commit

Do not force-push, rewrite, reset, or delete learning history unless explicitly requested.

## Review Priorities

Flag:

- a polished note without learning evidence
- duplicate concept documents
- lecture-order organization that hides prerequisites
- incorrect formulas, shapes, axes, or code outputs
- unsupported claims or fabricated experiments
- broken links or missing assets
- placeholders presented as finished content
- accidental changes to dates, publication state, or unrelated notes
- a TIL that has become a full lecture transcription

Recommend the smallest safe correction.
