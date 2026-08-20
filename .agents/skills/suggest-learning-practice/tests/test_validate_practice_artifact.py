from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys


SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from validate_practice_artifact import validate  # noqa: E402


def markdown_cell(text: str) -> dict[str, object]:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code_cell(text: str) -> dict[str, object]:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)}


class PracticeArtifactValidatorTests(unittest.TestCase):
    def build_bundle(self, root: Path, *, prefilled: bool = False, global_hint: bool = False) -> Path:
        bundle = root / "practice/dl/tensor-contract"
        (bundle / "src/tensor_contract").mkdir(parents=True)
        (bundle / "tests").mkdir()
        til = root / "til/2026/08/2026-08-20.md"
        til.parent.mkdir(parents=True)
        til.write_text("# TIL\n", encoding="utf-8")
        source = root / "materials/lesson.md"
        source.parent.mkdir()
        source.write_text("# Source\n", encoding="utf-8")
        markdown = """# Tensor contract practice

- 기준 TIL: [2026-08-20](../../../til/2026/08/2026-08-20.md)
- 관련 강의자료: [lesson](../../../materials/lesson.md)

## Practice Coverage Map

| Outcome ID | TIL location | Practice action | Artifact/Exercise | Required evidence |
| --- | --- | --- | --- | --- |
| O01 | 오늘의 학습 > Tensor shape | implement | E01 | passing contracts and interpretation |
"""
        if global_hint:
            markdown += "\n## 점진적 힌트\n\n- 멀리 떨어진 힌트\n"
        exercise = """## E01. Tensor contract

### 실제 사용 맥락

Validate a batch boundary.

### 실행 전 회상·예측

Predict the output shape before running tests.

### 작은 유사 사례와 계약

For `(2, 3)`, return the two dimensions as metadata.

### 구현

Implement the public function in `src/`.

<details>
<summary>힌트 1: 관찰할 상태</summary>

Inspect `shape` before converting it.
</details>

<details>
<summary>힌트 2: 작은 trace</summary>

Trace `(2, 3)` one axis at a time.
</details>

### 테스트와 실패 진단

Run pytest and identify the first contract failure.

### 결과 해석

Explain which boundary the test protects.
"""
        notebook = {
            "cells": [
                markdown_cell(markdown),
                code_cell(
                    "# setup-check: repository-root import\n"
                    "from pathlib import Path\n"
                    "import sys\n"
                    "bundle_src = Path('practice/dl/tensor-contract/src').resolve()\n"
                    "sys.path.insert(0, str(bundle_src))\n"
                    "from tensor_contract import describe\n"
                ),
                markdown_cell(exercise),
                code_cell("# TODO: E01\n"),
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        (bundle / "workbook.ipynb").write_text(json.dumps(notebook), encoding="utf-8")
        implementation = "return tuple(value.shape)" if prefilled else "raise NotImplementedError('learner implementation')"
        (bundle / "src/tensor_contract/__init__.py").write_text("from .core import describe\n", encoding="utf-8")
        (bundle / "src/tensor_contract/core.py").write_text(
            f"def describe(value: object) -> tuple[int, ...]:\n    \"\"\"Return a shape contract.\"\"\"\n    {implementation}\n",
            encoding="utf-8",
        )
        (bundle / "tests/test_core.py").write_text(
            """from tensor_contract import describe


def test_normal_shape_contract():
    assert describe(None) is not None


def test_edge_scalar_contract():
    assert describe(None) is not None


def test_failure_invalid_input_contract():
    assert describe(None) is not None
""",
            encoding="utf-8",
        )
        return bundle

    def codes(self, problems) -> set[str]:
        return {problem.code for problem in problems}

    def test_valid_bundle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(validate(self.build_bundle(root), repo_root=root, check_collection=False), [])

    def test_prefilled_core_and_global_hints_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root, prefilled=True, global_hint=True)
            codes = self.codes(validate(bundle, repo_root=root, check_collection=False))
            self.assertIn("PREFILLED_CORE", codes)
            self.assertIn("GLOBAL_HINT", codes)

    def test_executed_cell_and_unmapped_outcome_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][-1]["execution_count"] = 1
            notebook["cells"][-1]["outputs"] = [{"output_type": "stream", "name": "stdout", "text": ["fake\n"]}]
            notebook["cells"][0]["source"] = [line.replace("| E01 |", "| E02 |") for line in notebook["cells"][0]["source"]]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            codes = self.codes(validate(bundle, repo_root=root, check_collection=False))
            self.assertIn("EXECUTED", codes)
            self.assertIn("COVERAGE", codes)

    def test_missing_adjacent_hint_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][2]["source"] = [
                line.replace("<summary>힌트 1: 관찰할 상태</summary>", "<summary>참고</summary>")
                for line in notebook["cells"][2]["source"]
            ]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "HINT_ADJACENCY",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_empty_explanation_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][2]["source"] = [
                line for line in notebook["cells"][2]["source"] if line != "Validate a batch boundary.\n"
            ]
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "EXERCISE",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_missing_or_broken_setup_import_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"].pop(1)
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "IMPORT_SETUP",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

            notebook["cells"].insert(
                1,
                code_cell(
                    "# setup-check: broken import\n"
                    "from package_that_does_not_exist import missing\n"
                ),
            )
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "IMPORT_SETUP",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )

    def test_broken_course_practice_mapping_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self.build_bundle(root)
            course = root / "materials/private/course"
            practice = course / "course-provided-practice"
            practice.mkdir(parents=True)
            (course / "lesson.md").write_text("# Lesson\n", encoding="utf-8")
            (practice / "practice.md").write_text("# Practice\n", encoding="utf-8")
            (course / "INDEX.md").write_text(
                """# Course

## 강의 자료

| 파일 | 원본 |
| --- | --- |
| `lesson.md` | [원본](https://example.com) |

## 강의 제공 실습

| Practice path | Related lesson path | Variant | Format | Original |
| --- | --- | --- | --- | --- |
| `course-provided-practice/practice.md` | `missing.md` | single | Markdown | [원본](https://example.com) |
""",
                encoding="utf-8",
            )
            path = bundle / "workbook.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            notebook["cells"][0]["source"].extend(
                [
                    "\n",
                    "- mapped lesson: [lesson](../../../materials/private/course/lesson.md)\n",
                    "- mapped practice: [practice](../../../materials/private/course/course-provided-practice/practice.md)\n",
                ]
            )
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertIn(
                "PRACTICE_MAPPING",
                self.codes(validate(bundle, repo_root=root, check_collection=False)),
            )


if __name__ == "__main__":
    unittest.main()
