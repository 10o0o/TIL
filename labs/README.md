# Labs

`labs/`는 개념을 실제 코드와 숫자로 확인한 증거를 보관합니다.

## 좋은 실험의 조건

- 한 가지 가설 또는 질문만 검증한다.
- 실행 전에 예상 결과와 shape을 적는다.
- 실제로 실행한 결과만 기록한다.
- 예상과 실제가 다르면 원인을 분석한다.
- 수식의 어느 부분이 코드의 어느 줄인지 연결한다.
- 관련 canonical note를 링크한다.

## 권장 구조

```text
labs/
└── <domain>/
    └── <concept>/
        ├── README.md
        ├── experiment.py
        └── requirements.txt  # 필요할 때만
```

Notebook을 사용해도 되지만, 핵심 실험은 가능하면 다시 실행 가능한 작은 `.py` 파일로 남깁니다.

## 예시

```text
labs/llm/attention-score/
├── README.md
└── attention_score.py
```

README에는 다음을 기록합니다.

```text
질문
→ 실행 전 예상
→ 입력과 shape
→ 실행 방법
→ 실제 결과
→ 해석
→ 무엇을 이해했는가
```

[templates/lab.md](../templates/lab.md)를 사용합니다.
