# Practice

TIL에서 배운 내용을 직접 회상하고 구현하며, 실제 테스트 실패와 상태
변화를 해석한 증거를 둡니다.

## 산출물 형태

순수 손계산, 작은 Shape trace, 출력 해석은 단일 Notebook으로 충분합니다.

```text
practice/<area>/<topic>.ipynb
```

코드 중심 ML·DL·LLM·systems 실습은 작은 현업형 bundle을 기본으로 합니다.

```text
practice/<area>/<topic>/
├── workbook.ipynb
├── src/
│   └── <package>/<module>.py
└── tests/
    └── test_<module>.py
```

Notebook은 상황, 실행 전 예측, 작은 계약, 단계별 힌트, 테스트 실행과
결과 해석을 안내합니다. `src/`에는 type hint와 docstring이 있는 public
signature만 제공하고 핵심 learner function은 `NotImplementedError`에서
시작합니다. `tests/`는 normal·edge·failure 계약을 보여주지만 구현 방법은
노출하지 않습니다. 첫 `# setup-check` 셀은 저장소 루트 kernel에서 해당
bundle의 `src/`를 찾고 public interface를 실제로 import합니다.

## 생성 원칙

`$suggest-learning-practice`에는 검토·저장을 마친 날짜별 TIL 경로를
정확히 전달합니다. `til/today.md`나 자동으로 고른 최신 TIL은 입력이
아닙니다. 실습은 TIL의 공백만 고치는 것이 아니라 주요 학습 성과 전체를
다음 action으로 바꿉니다.

- `implement`: 핵심 메커니즘 직접 구현
- `test`: 정상·경계·실패 계약 확인
- `debug`: 의도적으로 깨진 경계나 흐름 진단
- `interpret`: Shape, gradient, metric, output의 의미 설명
- `design`: API, 데이터 계약, 모델 출력이나 실험 조건 설계

설명을 잘했어도 직접 구현한 증거가 없으면 작은 `Core` 실습부터
시작합니다. `Applied`는 작은 현실 조건 하나를, `Advanced`는 기반 구현이
확인됐을 때만 ablation·민감도·실패 분석 같은 연구 질문 하나를 더합니다.

각 exercise는 다음 순서를 유지합니다.

```text
실제 사용 맥락
→ 실행 전 회상·예측
→ 작은 유사 사례와 계약
→ 핵심 로직 직접 구현
→ 바로 옆의 접힌 힌트
→ 테스트와 실패 진단
→ 실제 시스템 의미와 한계 해석
```

힌트를 파일 아래쪽에 몰아두지 않습니다. 각 TODO 바로 앞에 `힌트 1`과
`힌트 2`를 접어 두고, 완성 구현은 넣지 않습니다.

## 강의 제공 실습

강의 제공 원본은 `materials/private/<course>/course-provided-practice/`에
남습니다. 각 과정 `INDEX.md`의 다음 열이 강의와 실습을 정확히 연결합니다.

```text
Practice path | Related lesson path | Variant | Format | Original
```

TIL에 링크된 정확한 강의와 일치하는 행만 자동으로 참고합니다. 원본은
learner evidence가 아니며, 문제 상황·테스트·실패 사례를 설계하는 scaffold로
사용합니다. 답이나 가짜 출력을 복사하지 않습니다.

## 실행과 피드백

bundle은 저장소 루트에서 다음처럼 실행합니다.

```bash
PYTHONPATH=practice/<area>/<topic>/src \
  uv run pytest practice/<area>/<topic>/tests
```

구현 전에는 `NotImplementedError` 실패가 정상입니다. import와 collection은
성공해야 합니다. 막혔을 때 `$suggest-learning-practice`에 정확한 Notebook
또는 bundle 경로를 주면, 저장된 code와 실제 traceback을 기준으로 한 번에
가장 작은 blocker부터 안내합니다. 테스트 통과 뒤에도 결정적인 상태나
출력을 직접 설명해야 완료 증거가 됩니다.

[실습 Notebook 템플릿](./template.ipynb)은 위 구조의 Notebook 기준입니다.
실행하지 않은 결과를 기록하지 않고, 데이터셋·모델 가중치·API 키와 큰
출력 파일은 Git에 올리지 않습니다.
