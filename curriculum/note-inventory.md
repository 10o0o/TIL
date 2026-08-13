# Existing Note Inventory and Migration Plan

이 문서는 2026-08-13 기준 `content/`의 기존 학습 노트를 조사한 결과입니다. 목적은 파일을 당장 옮기거나 다시 쓰는 것이 아니라, **어떤 자료를 어떤 개념에서 다시 검증할지** 안전하게 결정하는 것입니다.

## 조사 범위와 기준

- 대상: `content/` 아래 학습 노트 18개 (`content/README.md` 제외)
- 강의 순서형: 파일명에 `[n-n]` 강의 번호가 있고 한 강의의 여러 개념을 묶은 문서
- 개념형: 하나의 수학·ML 개념을 제목으로 삼은 문서
- 장문 후보: 500줄 이상 또는 공백 단위 2,000단어 이상. 500줄 미만이어도 여러 개념이 섞였으면 통합 검토 대상이 될 수 있음
- placeholder 후보: 템플릿 기본 제목·설명·안내 문장 또는 예시 링크가 남은 파일
- 오분류 후보: 본문 주제와 frontmatter category가 현재 디렉터리 의미와 명백히 다른 파일

줄 수는 정리 우선순위를 정하기 위한 신호일 뿐, 품질이나 이해도를 판정하는 점수가 아닙니다.

조사 결과 18개 학습 노트는 총 7,983줄이며, 위 장문 기준에 해당하는 8개가 6,040줄을 차지합니다. 현재 `concepts/`, `til/`, `labs/`, `reviews/`에는 README 외 실제 학습 산출물이 없으므로 새 구조는 아직 비어 있는 시작점입니다.

## 전체 파일 목록

| 유형 | 줄 수 | 현재 파일 | 주요 주제 | 현재 판단 |
|---|---:|---|---|---|
| 강의 순서형 | 931 | [`[1-1]_문제_유형_데이터_분리_평가지표_리마인드.md`](../content/linear-algebra/%5B1-1%5D_%EB%AC%B8%EC%A0%9C_%EC%9C%A0%ED%98%95_%EB%8D%B0%EC%9D%B4%ED%84%B0_%EB%B6%84%EB%A6%AC_%ED%8F%89%EA%B0%80%EC%A7%80%ED%91%9C_%EB%A6%AC%EB%A7%88%EC%9D%B8%EB%93%9C.md) | 문제 유형, split, leakage, 회귀·분류 지표 | ML 오분류·장문, 보존 |
| 강의 순서형 | 830 | [`[1-2]_핵심_모델과_선택_기준_압축_정리.md`](../content/linear-algebra/%5B1-2%5D_%ED%95%B5%EC%8B%AC_%EB%AA%A8%EB%8D%B8%EA%B3%BC_%EC%84%A0%ED%83%9D_%EA%B8%B0%EC%A4%80_%EC%95%95%EC%B6%95_%EC%A0%95%EB%A6%AC.md) | 선형모델, KNN, tree, K-Means, PCA | ML 오분류·장문, 보존 |
| 강의 순서형 | 717 | [`[2-1]_배깅과_랜덤포레스트_1.md`](../content/linear-algebra/%5B2-1%5D_%EB%B0%B0%EA%B9%85%EA%B3%BC_%EB%9E%9C%EB%8D%A4%ED%8F%AC%EB%A0%88%EC%8A%A4%ED%8A%B8_1.md) | bootstrap, OOB, random forest | ML 오분류·장문, canonical 후보 |
| 강의 순서형·혼합 초안 | 828 | [`[3-1]_편향_분산_트레이드오프와_과적합_과소적합_진단_1.md`](../content/linear-algebra/%5B3-1%5D_%ED%8E%B8%ED%96%A5_%EB%B6%84%EC%82%B0_%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%98%A4%ED%94%84%EC%99%80_%EA%B3%BC%EC%A0%81%ED%95%A9_%EA%B3%BC%EC%86%8C%EC%A0%81%ED%95%A9_%EC%A7%84%EB%8B%A8_1.md) | bias-variance, learning curve, leakage | ML 오분류·장문·placeholder 혼합, 보존 |
| placeholder | 72 | [`til copy.md`](<../content/linear-algebra/til copy.md>) | 구 TIL 템플릿 사본 | 임시 파일 후보, 지금은 보존 |
| 강의 순서형 | 647 | [`[4-1]_특이값_분해(SVD)의_구조와_원리.md`](<../content/mathematics/linear-algebra/[4-1]_특이값_분해(SVD)의_구조와_원리.md>) | SVD, rank, low-rank approximation | 장문, canonical 후보 |
| 강의 순서형 | 659 | [`[4-2]_SVD와_PCA의_연결_및_저랭크_응용.md`](<../content/mathematics/linear-algebra/[4-2]_SVD와_PCA의_연결_및_저랭크_응용.md>) | SVD, PCA, recommendation, LoRA | 장문·중복, canonical 후보 |
| 강의 순서형 | 879 | [`[6-1]_Attention_score_내적과_QK_t_Shape_추론.md`](<../content/mathematics/linear-algebra/[6-1]_Attention_score_내적과_QK_t_Shape_추론.md>) | attention score, scaling, masking, shape | 장문·복합, canonical/lab 후보 |
| 개념형 | 237 | [`고유값_고유벡터의_정의와_기하학적_의미.md`](../content/mathematics/linear-algebra/%EA%B3%A0%EC%9C%A0%EA%B0%92_%EA%B3%A0%EC%9C%A0%EB%B2%A1%ED%84%B0%EC%9D%98_%EC%A0%95%EC%9D%98%EC%99%80_%EA%B8%B0%ED%95%98%ED%95%99%EC%A0%81_%EC%9D%98%EB%AF%B8.md) | eigenvalue, eigenvector | canonical 후보, 보존 |
| 개념형 | 271 | [`벡터공간과_선형_독립.md`](../content/mathematics/linear-algebra/%EB%B2%A1%ED%84%B0%EA%B3%B5%EA%B0%84%EA%B3%BC_%EC%84%A0%ED%98%95_%EB%8F%85%EB%A6%BD.md) | span, independence, basis, rank | canonical 후보, 보존 |
| 개념형 | 102 | [`벡터의_내적과_코사인_유사도.md`](../content/mathematics/linear-algebra/%EB%B2%A1%ED%84%B0%EC%9D%98_%EB%82%B4%EC%A0%81%EA%B3%BC_%EC%BD%94%EC%82%AC%EC%9D%B8_%EC%9C%A0%EC%82%AC%EB%8F%84.md) | inner product, cosine similarity | canonical 후보, 이미지 링크 보존 |
| 개념형 | 79 | [`벡터의_수학적_정의와_기하학적_해석.md`](../content/mathematics/linear-algebra/%EB%B2%A1%ED%84%B0%EC%9D%98_%EC%88%98%ED%95%99%EC%A0%81_%EC%A0%95%EC%9D%98%EC%99%80_%EA%B8%B0%ED%95%98%ED%95%99%EC%A0%81_%ED%95%B4%EC%84%9D.md) | vector, norm, normalization | canonical 후보, 보존 |
| 개념형 | 234 | [`선형_변환의_기하학적_해석.md`](../content/mathematics/linear-algebra/%EC%84%A0%ED%98%95_%EB%B3%80%ED%99%98%EC%9D%98_%EA%B8%B0%ED%95%98%ED%95%99%EC%A0%81_%ED%95%B4%EC%84%9D.md) | linear transformation | canonical 후보, 보존 |
| 개념형 | 154 | [`연립선형방정식과 _행렬_해법.md`](<../content/mathematics/linear-algebra/연립선형방정식과 _행렬_해법.md>) | linear systems, rank, least squares | inbound link가 있어 경로 보존 |
| 개념형 | 437 | [`직교성과_최소제곱법.md`](../content/mathematics/linear-algebra/%EC%A7%81%EA%B5%90%EC%84%B1%EA%B3%BC_%EC%B5%9C%EC%86%8C%EC%A0%9C%EA%B3%B1%EB%B2%95.md) | orthogonality, projection, least squares | 복합·중복, canonical 후보 |
| 개념형 | 210 | [`특수_행렬과_행렬_연산_성질.md`](../content/mathematics/linear-algebra/%ED%8A%B9%EC%88%98_%ED%96%89%EB%A0%AC%EA%B3%BC_%ED%96%89%EB%A0%AC_%EC%97%B0%EC%82%B0_%EC%84%B1%EC%A7%88.md) | special matrices, transpose, inverse | 보존 |
| 개념형 | 549 | [`행렬_대각화와_PCA_구현.md`](../content/mathematics/linear-algebra/%ED%96%89%EB%A0%AC_%EB%8C%80%EA%B0%81%ED%99%94%EC%99%80_PCA_%EA%B5%AC%ED%98%84.md) | diagonalization, PCA, executable code | 장문·중복, canonical/lab 후보 |
| 개념형 | 147 | [`행렬_연산과_딥러닝_레이어.md`](../content/mathematics/linear-algebra/%ED%96%89%EB%A0%AC_%EC%97%B0%EC%82%B0%EA%B3%BC_%EB%94%A5%EB%9F%AC%EB%8B%9D_%EB%A0%88%EC%9D%B4%EC%96%B4.md) | matrix multiplication, affine layer | canonical/lab 후보, 보존 |

## 중요한 후보군

### 잘못 분류된 경로

`content/linear-algebra/`의 `[1-1]`, `[1-2]`, `[2-1]`, `[3-1]`은 본문과, 앞의 세 파일에서는 frontmatter까지 머신러닝 주제입니다. 하지만 네 파일을 지금 옮기면 이미지와 향후 inbound link를 함께 조사해야 하므로, 이번 작업에서는 이동하지 않습니다. `[6-1]` Attention 문서는 선형대수 prerequisite를 포함하지만 canonical 목적지는 향후 `concepts/llm/`이 자연스럽습니다.

### 중복 개념

- **PCA**: `[1-2]`, `[4-2]`, `행렬_대각화와_PCA_구현.md`
- **SVD와 low-rank**: `[4-1]`, `[4-2]`, `행렬_대각화와_PCA_구현.md`
- **내적**: `벡터의_내적과_코사인_유사도.md`, `[6-1]` Attention 문서
- **최소제곱·선형회귀**: `연립선형방정식과 _행렬_해법.md`, `직교성과_최소제곱법.md`, `[1-2]`
- **데이터 분리·누수**: `[1-1]`, `[3-1]`
- **편향-분산**: `[3-1]`, `[2-1]`의 앙상블 분산 설명

중복은 삭제 사유가 아닙니다. 해당 개념을 다시 학습할 때 여러 문서의 유효한 설명과 예제를 비교하는 검색 목록입니다.

그 밖에 고유값·대각화·PCA, rank·선형계·최소제곱, PCA 전처리의 중심화·표준화도 서로 겹칩니다. 실제 통합 시에는 각각 `eigenpair`, `diagonalization`, `PCA`; `rank/column space`, `least squares as projection`처럼 핵심 질문을 분리합니다.

### Placeholder와 임시 파일

- `til copy.md`는 구 템플릿 안내 문장과 예시 링크가 남은 사본입니다.
- `[3-1]`은 기본 title/description, 안내 문장, 예시 상대 링크가 남아 있지만 그 사이에 약 750줄의 실질 학습 내용과 이미지 두 개가 있습니다.

따라서 `til copy.md`도 별도 승인 전에는 삭제하지 않고, `[3-1]`은 절대로 placeholder 파일로 보고 통째로 삭제하지 않습니다. 두 파일의 기존 오류는 향후 좁은 cleanup에서 처리합니다.

### 그대로 보존해야 하는 이유

- 기존 질문, 중간 계산, 혼동 기록이 학습 변화의 근거입니다.
- `[3-1]`과 내적 문서는 `assets/`의 이미지 세 개를 상대경로로 참조합니다.
- `직교성과_최소제곱법.md`가 공백이 포함된 `연립선형방정식과 _행렬_해법.md`를 링크합니다.
- 현재의 긴 문서는 아직 `explained`, `applied`, `retained` 증거로 재평가되지 않았습니다.

## 점진적 Migration 순서

1. 현재 학습 개념 하나를 고르고 관련 파일만 검색합니다.
2. PDF와 노트를 닫고 closed-book 설명을 먼저 남깁니다.
3. 기존 파일에서 유효한 예제, 충돌, 중복 후보를 추출합니다.
4. 작은 숫자·shape·새 적용 문제와 필요한 코드를 검증합니다.
5. `explained`와 `applied`를 통과했을 때만 기존 `concepts/`를 갱신하거나 하나를 생성합니다.
6. 실제 실행이 핵심이면 코드를 `labs/`로 분리합니다.
7. 그날 바뀐 이해만 짧은 TIL에 남깁니다.
8. 원본 `content/` 파일은 보존하고 canonical note에서 source history로 링크합니다.
9. 물리적 이동은 모든 상대 링크와 inbound reference를 확인한 별도 변경에서만 검토합니다.

우선 통합 후보는 학습 목표와 중복도가 함께 높은 `Attention score`, `SVD → PCA → low-rank`, `편향-분산`, `데이터 분리·누수`입니다. 다만 현재 progress는 모두 `seen`이므로 즉시 canonical로 승격할 파일은 없습니다. 우선순위는 실제 diagnostic 결과에 따라 바뀔 수 있습니다.
