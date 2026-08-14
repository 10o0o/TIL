---
name: update-learning-knowledge
description: Create or update this repository's durable knowledge notes from understanding the learner has demonstrated in their own TIL, answers, calculations, or interpreted experiment results, then commit only the validated knowledge changes. Use only when the user explicitly invokes $update-learning-knowledge or asks to reflect, promote, or save verified learning into knowledge/. Create or update zero to three concept notes, revise existing notes in place, and return no knowledge change when evidence is insufficient or nothing durable changed. Do not use for teaching, source auditing, TIL formatting, or copying tutor prose into the knowledge base.
---

# Update Learning Knowledge

Maintain `knowledge/` as the learner's current demonstrated understanding, not as a transcript of what a lecture or tutor said.

## Resolve the requested scope

1. Work from the repository root and read `knowledge/template.md` and `knowledge/README.md`.
2. Use the TIL, lesson, concepts, or date named by the user. If no source is named, use the current learning conversation and the most recently finalized relevant TIL; do not scan unrelated history.
3. Read only related existing `knowledge/` notes and executed `practice/` artifacts. Search by concepts and relationships before deciding that no note exists.
4. Use source material and `$coach-llm-research-study` findings to check accuracy, but never treat source text or tutor feedback as evidence that the learner understands it.

## Separate evidence from instruction

Accept learner-authored evidence such as:

- an explanation of purpose and mechanism in the learner's own words;
- a correct calculation, notation or Tensor-shape account;
- an answer that applies the idea in a slightly changed situation;
- an interpretation of code output, an experiment, an error, or a limitation;
- an explicit correction the learner can now explain, rather than a correction supplied only by the tutor.

Do not count copied definitions, lecture completion, tutor-generated summaries, unexecuted code, confidence, or note length as understanding. Treat a correction from the evaluator as a guardrail, not as learner evidence.

If one short diagnostic answer would materially determine whether a concept is ready, ask only that question and wait before writing. Otherwise defer the concept. Do not manufacture a complete note from partial evidence.

## Choose what belongs in the knowledge base

Select zero to three concepts with the highest reuse value. A concept belongs when it is durable, relevant to the roadmap or future lessons, and supported by the learner's own evidence.

Return zero changes when:

- no new or corrected understanding was demonstrated;
- the material is a one-day observation rather than reusable knowledge;
- the only accurate explanation came from the tutor;
- an unresolved misconception affects the core idea;
- an existing note already represents the demonstrated understanding.

Do not create one knowledge file per TIL, a progress record, an evidence log, a review file, or an index merely to record that learning happened.

## Locate or create the canonical concept note

1. Search `knowledge/` for an existing note covering the same concept or relationship.
2. Update that note in place when it exists. Merge aliases into one note instead of creating duplicates.
3. Otherwise choose the narrowest useful area such as `math`, `ml`, `deep-learning`, `llm`, or `systems`, and create `knowledge/<area>/<concept>.md` from `knowledge/template.md`.
4. Use a stable, date-free, lowercase kebab-case filename when English terminology is natural. Do not encode course name, lesson number, or study date in the filename.
5. Set `updated` to the current date in `Asia/Seoul`. Keep a few useful tags, not an exhaustive taxonomy.

## Write only the demonstrated range

Use the template headings in order:

- `한 줄 설명`: the shortest accurate account the learner can support;
- `현재 이해`: why the concept is needed and how it works, limited to demonstrated understanding;
- `예제와 연결`: a learner-worked example, shape, interpreted result, or a useful connection the learner actually made;
- `아직 헷갈리는 것`: only explicit uncertainty or a supported boundary; omit when empty;
- `관련 기록`: only resolvable links worth revisiting; omit when empty.

Preserve the learner's way of explaining where it remains accurate, but edit for clarity and factual consistency. If part of their account is wrong, include only the verified portion and leave the unresolved part explicit or defer the update. Do not paste whole TIL passages, lecture text, evaluator reports, or long tutor explanations.

Revise outdated knowledge in place so the file represents the current best understanding. Keep the chronological record in TIL unchanged. Do not claim calculations, code output, experiments, or transfer that did not occur.

## Write and validate safely

- Use `apply_patch` and preserve unrelated content and links.
- Never edit `archive/`, the source PDF, the finalized TIL, or a practice result as part of this skill.
- Do not create a practice task or push as part of this skill.
- Validate every changed knowledge note from the repository root:

```bash
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py path/to/knowledge-note.md
git diff --check -- path/to/knowledge-note.md
```

## Commit the knowledge update

After every nonzero knowledge change, commit only the knowledge notes created or updated by the current run:

1. Read every final note once more and ensure that all validators and `git diff --check` pass.
2. Run `git status --short` and preserve all unrelated worktree and staged changes.
3. Stage only the exact changed `knowledge/` paths from the current run.
4. Inspect `git diff --cached --name-status -- <knowledge-paths>` and run `git diff --cached --check -- <knowledge-paths>`.
5. Commit only those paths with the message `knowledge: YYYY-MM-DD 학습 내용 반영`, using the current date in `Asia/Seoul`. Use a path-limited commit so unrelated staged changes cannot enter the commit.
6. If there is no justified knowledge change or the selected notes have no change to commit, do not create an empty commit.
7. Do not push.

Report which notes were created, updated, or deliberately skipped, the learner-authored evidence used, the commit hash and committed paths. If there was no justified change, say so plainly without creating a placeholder or commit.
