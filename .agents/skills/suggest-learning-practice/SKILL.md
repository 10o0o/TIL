---
name: suggest-learning-practice
description: Assess one explicitly supplied, finalized dated TIL and its linked learning sources, optionally adapt explicitly annotated instructor-provided practice, and create one tailored unexecuted .ipynb workbook only when useful. Use only when the user invokes $suggest-learning-practice with the exact til/YYYY/MM/YYYY-MM-DD.md path and wants a practice decision, Notebook, Kaggle task, implementation, project, ablation, or benchmark. Accept additional exact files under materials/private/{course}/course-provided-practice/ as optional source scaffolds to refine, supplement, or extend; never infer the latest TIL or a matching practice file. Choose Core, Applied, or Advanced from demonstrated understanding, and create no file when reteaching, more evidence, or no additional practice is the better outcome.
---

# Build an Adaptive Practice Workbook

Use the learner's finalized TIL as the entry point. Practice is optional; creating a useful workbook is the default action when the evidence supports practice. When the user explicitly annotates instructor-provided practice, use it as an optional design scaffold rather than as learner evidence or a workbook to copy verbatim.

## Require one finalized TIL and resolve optional practice

1. Require the user to name exactly one repository file at `til/YYYY/MM/YYYY-MM-DD.md`.
2. Do not infer “today,” select the newest TIL, accept `today.md`, or substitute the current conversation for the required file.
3. Read the whole TIL and validate it with:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py til/YYYY/MM/YYYY-MM-DD.md
```

4. If validation fails, stop and ask the learner to repair that exact TIL. Do not issue a provisional practice outcome or scope a workbook from an invalid TIL.
5. Resolve and read the relevant source links under `관련 기록`, especially `materials/` links. Follow only knowledge and practice links that bear on today's concepts.
6. For a source-based lesson, require at least one resolvable source link. If it is missing or broken, stop and ask the learner to identify or repair the source instead of guessing.
7. When the invocation explicitly annotates one or more files under `materials/private/<course>/course-provided-practice/`, resolve and read each file completely. Require exact file paths; do not infer a same-numbered lesson, select a nearby file, or load the whole directory.
8. If an annotated practice path is missing, broken, or materially unrelated to the TIL target, stop and ask for the correct file instead of forcing it into the workbook.
9. Treat the TIL as learner evidence, not as an infallible source. Do not turn copied text, tutor prose, lecture completion, confidence, or note length into proof of understanding.
10. Treat instructor-provided practice, its worked answers, and its sample output as source material only. They do not demonstrate that the learner can perform or interpret the task.

Leave source auditing and misconception correction to `$coach-llm-research-study`, adaptive teaching to `$teach-course-material`, and durable concept writing to `$update-learning-knowledge`.

## Decide before creating

Look for the learner's own explanation, correct notation and shapes, a worked calculation, interpreted output, and transfer to a changed example. Supplying instructor practice changes how a workbook may be designed, not whether understanding has been demonstrated or which depth is justified. Choose exactly one outcome:

- **재학습 우선**: a prerequisite or misconception blocks meaningful implementation. Create no Notebook and name the first concept to revisit.
- **증거 확인 우선**: the TIL does not show enough understanding to scope useful practice. Create no Notebook and ask one small diagnostic question.
- **추가 실습 없음**: the learner can already explain, apply, and interpret the target, or the next lesson will exercise it naturally. Create no file and state the evidence.
- **워크북 생성**: a specific gap can be tested through calculation, code, comparison, transfer, or interpretation. Create one Notebook without asking for a second confirmation.

If the user explicitly asks for a decision only, report the decision without creating a file.

## Adapt annotated instructor practice

When instructor-provided practice is supplied and `워크북 생성` is the outcome:

1. Use the supplied practice as a draft exercise design. Compare its objective, prerequisites, sequence, starter code, dependencies, expected checks, worked answers, and interpretation prompts against the exact TIL evidence and target gap.
2. Classify its parts internally as `유지`, `다듬기`, `보충`, or `제외`. Do not create a separate audit artifact unless the user asks for one.
3. Preserve a useful baseline and exercises that directly test the gap. Improve unclear ordering, repeated setup, fragile instructions, variable or Shape descriptions, TODO boundaries, reproducibility controls, observable checks, and completion criteria.
4. Add only what produces useful new evidence: a short non-blocking prerequisite bridge, one changed condition, an edge or failure case, a comparison, or a concept-specific interpretation prompt. Do not add complexity merely to make the workbook longer.
5. Remove or convert complete solutions, prefilled reflections, and sample outputs into starter code, TODOs, checks, or progressive hints. Never expose a full answer indirectly by leaving every required line in place with only cosmetic blanks.
6. Keep the original file unchanged. Link it from the workbook and briefly distinguish the retained course scaffold from the tailored supplement.
7. If the supplied practice already covers the target gap well, keep it compact and improve only the parts that help this learner. If it contains a suspected substantive error, do not silently bless or rewrite the claim; flag it for `$coach-llm-research-study` and avoid building the task on it.

## Choose the depth

Use the smallest depth that produces new evidence, not automatically the shortest task.

- **Core**: verify one mechanism with a hand calculation, tiny Tensor, or minimal implementation. Use when the gap is between explanation, shapes, calculation, and code.
- **Applied**: include a baseline and one changed condition on small realistic data. Use when mechanics are understood but data handling, metrics, validation, or result interpretation needs evidence.
- **Advanced**: include a baseline plus one research-style question such as an ablation, sensitivity test, failure-case analysis, efficiency trade-off, or reproducibility check. Use only when Core foundations are already demonstrated and the added investigation serves the learner's LLM Research Engineer goal.

Applied and Advanced workbooks are cumulative: preserve a simple baseline before adding complexity. Do not choose Advanced merely because it sounds more valuable.

Match the activity to the domain:

- mathematics or Tensor shapes: small NumPy/PyTorch calculation and interpretation;
- classical ML: controlled dataset experiment, validation, metrics, or error analysis;
- deep learning or Transformer mechanics: minimal implementation, ablation, or debugging task;
- LLM systems: controlled latency, throughput, memory, batching, or KV-cache comparison;
- post-training: small controlled SFT, preference, or LoRA comparison.

Use Kaggle only when an end-to-end data workflow, validation, metrics, or error analysis is the learning target. Verify a named current competition, dataset, library, or tool before putting it in a workbook. Never optimize for leaderboard rank as the learning objective.

## Create one Notebook workbook

When `워크북 생성` is the outcome:

1. Search `practice/` for an existing workbook on the same task. Never overwrite learner code, outputs, or reflections.
2. Create one primary artifact at `practice/<area>/<topic>.ipynb`, using `practice/template.ipynb` as the structural baseline. Keep the filename stable and descriptive; add a narrower focus when the generic path already exists.
3. Put these items in the Notebook:
   - links to the exact TIL and the source materials followed from it;
   - when supplied, a link to each exact `course-provided-practice` file and a concise note on what was retained and what was supplemented;
   - selected level: Core, Applied, or Advanced;
   - the learner evidence and gap that make the task useful now;
   - one learning question, prerequisites, and observable completion criteria;
   - an execution-before-prediction prompt;
   - ordered instructions, starter code or TODO cells, and a progressive hint section;
   - prompts to compare prediction with observation, explain what the result demonstrates, and identify one limitation;
   - an optional prompt for one specific unresolved point when it would help later teaching; omit it when none remains;
   - concept-specific interpretation prompts instead of redundant catch-all wording such as `내 말로 다시 설명`; do not ask the learner to nominate `knowledge/` updates because `$update-learning-knowledge` owns that decision;
   - for Advanced only, one explicit hypothesis and one controlled extension such as an ablation or error analysis.
4. Keep the target concept larger than setup and data wrangling. A Notebook may reference a supporting `.py` file only when accurate benchmarking or repeatable jobs require one; the workbook remains the primary artifact.
5. Do not include a complete solution, invented output, hidden answer, fabricated metric, or claimed result. Leave all code cells unexecuted with `execution_count: null` and empty `outputs` unless the user separately asks to run the experiment.
6. Do not enroll in Kaggle, download data, start paid compute, or use credentials unless the user explicitly requests that external action.

## Validate and report

Validate a created workbook with:

```bash
python3 -m json.tool practice/<area>/<topic>.ipynb >/dev/null
git diff --check -- practice/<area>/<topic>.ipynb
```

Read the final Notebook and confirm that every source link resolves, all code cells are unexecuted, and no answer or result was invented.

When instructor practice was used, compare the final Notebook against it and confirm that the source remains unchanged, the tailored additions address the TIL gap, complete solutions or sample outputs were not copied into learner-facing cells, and unrelated exercises were not carried over by default.

Report concisely:

1. **판단**: no practice, reteaching first, evidence first, or workbook created;
2. **근거**: the exact learner evidence and gap from the TIL;
3. **강의 제공 실습 활용**: the exact supplied path and the main retained or supplemented element, only when one was used;
4. **워크북**: path and selected depth when created;
5. **시작점**: the first prediction or task the learner should complete.

Do not provide a menu, backlog, numeric mastery score, or mandatory schedule. Do not commit or push unless the user separately asks.
