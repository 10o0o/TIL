from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from validate_practice_index import validate  # noqa: E402


class PracticeIndexValidatorTests(unittest.TestCase):
    def build_course(self, root: Path, *, practice_row: str | None = None) -> Path:
        course = root / "materials/private/course"
        practice = course / "course-provided-practice"
        practice.mkdir(parents=True)
        (course / "01-01_lesson.md").write_text("# Lesson\n", encoding="utf-8")
        (practice / "01-01_practice.md").write_text("# Practice\n", encoding="utf-8")
        row = practice_row or "| `course-provided-practice/01-01_practice.md` | `01-01_lesson.md` | single | Markdown | [원본](https://example.com) |"
        index = course / "INDEX.md"
        index.write_text(
            """# Course

## 강의 자료

| 파일 | 원본 |
| --- | --- |
| `01-01_lesson.md` | [원본](https://example.com) |

## 강의 제공 실습

| Practice path | Related lesson path | Variant | Format | Original |
| --- | --- | --- | --- | --- |
"""
            + row
            + "\n",
            encoding="utf-8",
        )
        return index

    def codes(self, problems) -> set[str]:
        return {problem.code for problem in problems}

    def test_valid_explicit_mapping_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(validate(self.build_course(Path(directory))), [])

    def test_unmapped_file_and_broken_lesson_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = self.build_course(
                root,
                practice_row="| `course-provided-practice/missing.md` | `02-01_missing.md` | single | Markdown | [원본](https://example.com) |",
            )
            codes = self.codes(validate(index))
            self.assertIn("INDEX_PARITY", codes)
            self.assertIn("LESSON_LINK", codes)
            self.assertIn("SOURCE_MISSING", codes)

    def test_invalid_variant_and_duplicate_mapping_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            index = self.build_course(Path(directory))
            with index.open("a", encoding="utf-8") as stream:
                stream.write("| `course-provided-practice/01-01_practice.md` | `01-01_lesson.md` | expert | Markdown | [원본](https://example.com) |\n")
            codes = self.codes(validate(index))
            self.assertIn("DUPLICATE", codes)
            self.assertIn("VARIANT", codes)


if __name__ == "__main__":
    unittest.main()
