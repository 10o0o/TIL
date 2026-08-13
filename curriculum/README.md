# Curriculum

이 디렉터리는 강의 날짜가 아니라 **개념의 선수지식과 현재 이해 상태**를 기준으로 학습 순서를 관리합니다.

## 파일

- [source-index.md](./source-index.md): 프로젝트에 업로드한 PDF와 강의 자료 인덱스
- [course-map.md](./course-map.md): 개념 dependency graph와 우선순위
- [progress.md](./progress.md): 개념별 학습 상태와 다음 행동

## 갱신 원칙

1. PDF가 추가되면 `source-index.md`에만 먼저 등록합니다.
2. 새 개념이나 연결이 확인되면 `course-map.md`를 갱신합니다.
3. 설명·적용·구현·복습 결과가 생겼을 때만 `progress.md` 상태를 변경합니다.
4. 문서가 존재한다는 이유로 학습 상태를 올리지 않습니다.
5. 전체 PDF 분석 단계에서는 `concepts/` 문서를 대량 생성하지 않습니다.

## 우선순위

| 우선순위 | 의미 |
|---|---|
| `P0` | 이후 ML/DL/LLM 이해를 막는 핵심 선수지식 |
| `P1` | 원리와 실전 사용까지 이해할 내용 |
| `P2` | 현재는 검색해 사용할 수 있으면 충분한 세부사항 |

LLM Systems / Inference Optimization, Post-training, Evaluation 목표와의 연결성을 기준으로 우선순위를 정합니다.
