# Concepts

`concepts/`는 개념별 **단일 기준 문서(canonical note)** 를 보관합니다.

## 핵심 원칙

1. 강의 번호나 날짜가 아니라 개념 이름으로 작성합니다.
2. 같은 개념 문서를 두 개 만들지 않고 기존 문서를 갱신합니다.
3. 설명과 최소 한 번의 적용을 통과하기 전에는 완성 문서로 만들지 않습니다.
4. PDF 문장을 옮기는 대신 학습자가 자료 없이 설명한 내용을 기반으로 작성합니다.
5. 수식, Tensor shape, 코드가 있는 경우 서로 1:1로 연결합니다.
6. 실제로 실행한 코드는 `labs/`에 두고 여기서는 핵심만 링크합니다.

## 권장 구조

```text
concepts/
├── math/
├── ml/
├── dl/
├── llm/
├── evaluation/
└── systems/
```

빈 디렉터리는 Git이 보존하지 않으므로 첫 문서가 생길 때 만듭니다.

## 문서 생성 조건

다음을 만족하면 `concepts/` 문서를 생성하거나 갱신합니다.

- 자료 없이 핵심을 설명했다.
- 작은 숫자 또는 새로운 사례에 적용했다.
- 실제 오개념이 있었다면 식별하고 교정했다.
- 수식이나 shape이 있다면 의미를 설명했다.

구현이 중요한 개념은 `implemented`까지 요구할 수 있습니다.

## 문서 구조

[templates/concept.md](../templates/concept.md)를 사용합니다.

핵심 섹션:

```text
해결하려는 문제
→ 직관
→ 작은 숫자 예제
→ 정확한 정의·수식·shape
→ 코드 또는 lab
→ ML/LLM 연결
→ 헷갈리기 쉬운 부분
→ 자료 없이 설명한 최종 요약
```

## 파일명

새 파일은 가능한 한 안정적인 영문 kebab-case를 사용합니다.

```text
concepts/ml/bias-variance.md
concepts/llm/attention-score.md
concepts/systems/kv-cache.md
```

문서 본문과 제목은 한국어로 작성해도 됩니다.
