---
title: "Attention Score의 내적과 QKᵀ Shape 추론"
description: "Attention에서 내적을 관련도 점수로 사용하는 이유와 QKᵀ의 shape을 벡터, 행렬, 배치, Multi-Head 단계로 확장하며 정리합니다."
date: 2026-08-10
updated: 2026-08-10
category: linear-algebra
tags:
  - mathematics
  - linear-algebra
  - attention
  - transformer
  - NumPy
publish: false
---

# Attention Score의 내적과 $QK^\top$ Shape 추론

## 오늘의 질문

- Attention은 왜 Query와 Key의 내적을 관련도 점수로 사용할까?
- 하나의 Query를 여러 Key와 비교할 때 왜 $qK^\top$을 계산할까?
- $QK^\top$의 각 원소와 전체 shape은 무엇을 의미할까?
- 배치와 Multi-Head 차원이 추가되면 어떤 축을 전치해야 할까?
- 왜 내적 점수를 $\sqrt{d_k}$로 나눈 뒤 Softmax를 적용할까?
- Key와 Value는 각각 어떤 역할을 할까?

## 핵심 결론

Query와 Key의 마지막 차원이 모두 $d_k$라면, 원점수(raw score) $R$과 스케일된 점수 $S$는 다음과 같이 계산한다.

$$
R=QK^\top,
\qquad
S=\frac{R}{\sqrt{d_k}}
  =\frac{QK^\top}{\sqrt{d_k}}
$$

각 원소는 다음과 같다.

$$
R_{ij}=Q_i\cdot K_j,
\qquad
S_{ij}=\frac{Q_i\cdot K_j}{\sqrt{d_k}}
$$

이므로, $i$번째 Query가 $j$번째 Key와 얼마나 잘 맞는지를 나타낸다.

$$
Q\in\mathbb{R}^{L_q\times d_k},
\qquad
K\in\mathbb{R}^{L_k\times d_k}
\quad\Longrightarrow\quad
QK^\top\in\mathbb{R}^{L_q\times L_k}
$$

> $QK^\top$은 새로운 종류의 연산이 아니라, 모든 Query와 모든 Key 사이의 내적을 한 번의 행렬곱으로 묶은 것이다. 행은 “누가 찾는가(Query)”, 열은 “누구를 평가하는가(Key)”를 뜻한다.

## 기호와 Shape 먼저 정리하기

| 기호 | 의미 | 대표 shape |
| --- | --- | --- |
| $L_q$ | Query 토큰 수 | 스칼라 |
| $L_k$ | Key와 Value 토큰 수 | 스칼라 |
| $d_{\text{model}}$ | 입력 토큰 표현의 차원 | 스칼라 |
| $d_k$ | Query와 Key 벡터의 차원 | 스칼라 |
| $d_v$ | Value 벡터의 차원 | 스칼라 |
| $X$ | 입력 토큰 표현 | $(L, d_{\text{model}})$ |
| $Q$ | Query 행렬 | $(L_q, d_k)$ |
| $K$ | Key 행렬 | $(L_k, d_k)$ |
| $V$ | Value 행렬 | $(L_k, d_v)$ |
| $QK^\top$ | 모든 Query-Key 점수 | $(L_q, L_k)$ |

Self-Attention에서는 Query, Key, Value가 같은 시퀀스에서 만들어지므로 보통 $L_q=L_k=L$이다. 이때 score 행렬의 shape은 $(L,L)$이 된다.

## 1. 먼저 내적을 정확하게 이해하자

두 벡터가 다음과 같다고 하자.

$$
q=
\begin{bmatrix}
2 & 1
\end{bmatrix},
\qquad
k=
\begin{bmatrix}
1.5 & 1
\end{bmatrix}
$$

내적은 같은 위치의 원소끼리 곱한 뒤 모두 더하는 연산이다.

$$
q\cdot k
=2\times1.5+1\times1
=4
$$

NumPy에서는 `@` 연산자로 같은 계산을 할 수 있다.

```python
import numpy as np

q = np.array([2.0, 1.0])
k = np.array([1.5, 1.0])

print(q @ k)
# 4.0
```

### 왜 내적을 관련도 점수로 사용할 수 있을까?

내적은 다음 식으로도 표현할 수 있다.

$$
q\cdot k
=\lVert q\rVert\lVert k\rVert\cos\theta
$$

따라서 내적은 두 요소의 영향을 함께 받는다.

- **방향**: 두 벡터가 비슷한 방향일수록 $\cos\theta$가 커진다.
- **크기**: 벡터의 norm이 클수록 내적의 절댓값도 커질 수 있다.

모델은 학습을 통해 관련 있는 Query와 Key의 내적이 커지도록 $W_Q$와 $W_K$를 조정할 수 있다. 그래서 Attention의 내적은 단순한 기하학적 유사도보다는 **학습된 적합도 점수(compatibility score)**로 이해하는 편이 정확하다.

### 내적과 코사인 유사도는 다르다

코사인 유사도는 내적을 두 벡터의 크기로 나눈 값이다.

$$
\mathrm{cosine\_similarity}(q,k)
=\frac{q\cdot k}{\lVert q\rVert\lVert k\rVert}
$$

| 구분 | 내적 | 코사인 유사도 |
| --- | --- | --- |
| 식 | $q\cdot k$ | $\dfrac{q\cdot k}{\lVert q\rVert\lVert k\rVert}$ |
| 방향의 영향 | 있음 | 있음 |
| 크기의 영향 | 있음 | 정규화로 제거 |
| Attention에서의 해석 | 학습된 적합도 점수 | 일반적으로 직접 사용하지 않음 |

코사인 유사도는 방향만 비교하며, 둘 중 하나가 영벡터이면 분모가 $0$이므로 정의할 수 없다. 반면 Scaled Dot-Product Attention은 일반적으로 정규화하지 않은 내적을 사용한다.

## 2. 하나의 Query와 여러 Key를 한 번에 비교하기

하나의 Query $q$를 세 개의 Key $k_1,k_2,k_3$와 비교한다고 하자.

$$
q=
\begin{bmatrix}
2 & 1
\end{bmatrix}
$$

각 Key를 **행으로 쌓아** 행렬 $K$를 만든다.

$$
K=
\begin{bmatrix}
1.5 & 1 \\
-1 & 2 \\
-2 & -1
\end{bmatrix}
$$

이때 $K$의 shape은 $(3,2)$다.

- 행 3개: 후보 Key가 3개
- 열 2개: Key 하나의 feature가 2개

우리가 원하는 값은 다음 세 내적이다.

$$
q\cdot k_1,
\qquad
q\cdot k_2,
\qquad
q\cdot k_3
$$

### 왜 $qK$가 아니라 $qK^\top$일까?

현재 shape은 다음과 같다.

$$
q:(2,),
\qquad
K:(3,2)
$$

`q @ K`는 안쪽 차원 $2$와 $3$이 맞지 않아 계산할 수 없다. $K$를 전치하면 각 Key가 열에 놓인다.

$$
K^\top=
\begin{bmatrix}
1.5 & -1 & -2 \\
1 & 2 & -1
\end{bmatrix}
$$

따라서 shape은

$$
(2,)@(2,3)\longrightarrow(3,)
$$

이 되고, 행렬곱을 펼치면 다음과 같다.

$$
\begin{aligned}
qK^\top
&=
\begin{bmatrix}
2 & 1
\end{bmatrix}
\begin{bmatrix}
1.5 & -1 & -2 \\
1 & 2 & -1
\end{bmatrix} \\
&=
\begin{bmatrix}
2(1.5)+1(1) & 2(-1)+1(2) & 2(-2)+1(-1)
\end{bmatrix} \\
&=
\begin{bmatrix}
4 & 0 & -5
\end{bmatrix}
\end{aligned}
$$

결과의 세 원소가 각각 $q\cdot k_1$, $q\cdot k_2$, $q\cdot k_3$다. $K^\top$은 단순히 shape을 억지로 맞추는 것이 아니라, $K$의 각 **행**과 $q$가 내적되도록 Key를 배치한다.

## 3. 모든 Query와 모든 Key를 비교하기

이제 각 토큰에 Query가 하나씩 있다고 하자. Query를 행으로 쌓으면 $Q$, Key를 행으로 쌓으면 $K$가 된다.

토큰이 4개이고 각 Query와 Key가 8차원이라면

$$
Q:(4,8),
\qquad
K:(4,8),
\qquad
K^\top:(8,4)
$$

이므로

$$
QK^\top:(4,8)@(8,4)\longrightarrow(4,4)
$$

이다. 안쪽의 $8$은 내적에 사용되고, 바깥쪽의 $4$와 $4$가 결과 shape으로 남는다.

### Score 행렬의 각 원소가 뜻하는 것

$$
R=QK^\top
$$

라고 하면, 행렬곱의 정의에 따라

$$
\begin{aligned}
R_{ij}
&=\sum_{r=1}^{d_k}Q_{ir}(K^\top)_{rj} \\
&=\sum_{r=1}^{d_k}Q_{ir}K_{jr} \\
&=Q_i\cdot K_j
\end{aligned}
$$

이다. 즉 `S[i, j]`는 $i$번째 Query와 $j$번째 Key의 적합도 점수다.

```text
                         Key
                 k0    k1    k2    k3
              ┌────────────────────────┐
Query      q0 │ s00   s01   s02   s03 │
           q1 │ s10   s11   s12   s13 │
           q2 │ s20   s21   s22   s23 │
           q3 │ s30   s31   s32   s33 │
              └────────────────────────┘
```

- 행 $i$: 정보를 찾는 $i$번째 Query
- 열 $j$: 평가 대상인 $j$번째 Key
- 원소 $s_{ij}$: $Q_i\cdot K_j$

### Score 행렬은 일반적으로 대칭이 아니다

벡터의 내적은 $a\cdot b=b\cdot a$이지만, Attention에서는 비교하는 벡터 쌍 자체가 다르다.

$$
R_{ij}=Q_i\cdot K_j,
\qquad
R_{ji}=Q_j\cdot K_i
$$

$Q_i\cdot K_j$와 $Q_j\cdot K_i$는 같은 두 벡터의 순서만 바꾼 식이 아니다. 일반적으로 $Q=XW_Q$, $K=XW_K$이고 $W_Q\ne W_K$이므로 두 점수는 같을 필요가 없다.

## 4. Query, Key, Value는 어디에서 만들어질까?

데이터셋에 Query, Key, Value가 별도 열로 들어 있는 것은 아니다. 모델이 입력 토큰 표현 $X$에 서로 다른 학습 가능한 가중치를 곱해 생성한다.

$$
Q=XW_Q,
\qquad
K=XW_K,
\qquad
V=XW_V
$$

한 시퀀스에 대한 단순화한 shape은 다음과 같다.

$$
\begin{aligned}
X &: (L,d_{\text{model}}) \\
W_Q &: (d_{\text{model}},d_k) \\
W_K &: (d_{\text{model}},d_k) \\
W_V &: (d_{\text{model}},d_v)
\end{aligned}
$$

따라서

$$
Q:(L,d_k),
\qquad
K:(L,d_k),
\qquad
V:(L,d_v)
$$

가 된다.

| 요소 | 직관적인 질문 | 역할 |
| --- | --- | --- |
| Query | 나는 무엇을 찾고 있는가? | 어떤 정보가 필요한지 표현 |
| Key | 나를 어떤 기준으로 찾을 수 있는가? | Query와 비교할 선택 기준 |
| Value | 나를 선택했다면 어떤 정보를 전달할 것인가? | 가중합에 실제로 사용되는 정보 |

예를 들어 “나는 사과를 먹었다”에서 “먹었다”의 Query가 목적어와 관련된 방향을, “사과를”의 Key가 목적어와 관련된 방향을 학습했다면 두 벡터의 내적이 크게 나올 수 있다. 다만 실제 벡터의 각 차원이 사람이 읽을 수 있는 문장 하나에 그대로 대응하는 것은 아니며, 이는 역할을 이해하기 위한 비유다.

### 왜 $XX^\top$ 대신 $QK^\top$을 사용할까?

$XX^\top$도 입력 벡터 사이의 내적을 계산할 수 있다. 하지만 $W_Q$와 $W_K$를 따로 학습하면 모델은 다음 두 역할을 서로 다르게 표현할 수 있다.

- 정보를 **찾는 방식**
- 정보를 **찾을 수 있게 표시하는 방식**

따라서 원래 임베딩 공간에서 단순히 비슷한 토큰을 찾는 데 그치지 않고, 각 Attention head가 학습한 관계를 기준으로 적합도를 계산할 수 있다.

### Key는 선택 기준이고 Value는 가져올 정보다

Query와 Key로 계산한 Attention weight가 특정 위치에서 $0.8$이라고 하자. 이때 결과에 더하는 값은 $0.8K_j$가 아니라 $0.8V_j$다.

```text
Query와 Key 비교  → 누구를 얼마나 참고할지 결정
Attention weight @ Value → 선택한 위치의 실제 정보 결합
```

도서관에 비유하면 Query는 검색어, Key는 검색용 색인, Value는 실제 책 내용에 가깝다. 검색어와 색인을 비교해 책을 찾은 뒤에는 색인이 아니라 본문을 가져온다.

## 5. Scaled Dot-Product Attention 전체 식

Attention의 핵심 계산은 다음과 같다.

$$
\mathrm{Attention}(Q,K,V)
=\mathrm{softmax}\left(
\frac{QK^\top}{\sqrt{d_k}}+M
\right)V
$$

여기서 $M$은 mask 행렬이다. 허용된 위치에는 $0$, 보지 못하게 막을 위치에는 매우 작은 값 또는 $-\infty$를 넣는다.

| 단계 | 계산 | 의미 |
| --- | --- | --- |
| 1 | $QK^\top$ | 모든 Query-Key 적합도 계산 |
| 2 | $\dfrac{QK^\top}{\sqrt{d_k}}$ | 차원 증가에 따른 점수 분산 보정 |
| 3 | $+M$ | 보면 안 되는 위치 차단 |
| 4 | $\mathrm{softmax}(\cdot)$ | 각 Query 행을 합이 1인 가중치로 변환 |
| 5 | $AV$ | Value의 가중합으로 새 토큰 표현 생성 |

Attention weight를 $A$라고 쓰면

$$
A=\mathrm{softmax}\left(
\frac{QK^\top}{\sqrt{d_k}}+M
\right)
$$

이고, 최종 출력은

$$
O=AV
$$

이다. $A:(L_q,L_k)$이고 $V:(L_k,d_v)$이므로

$$
O:(L_q,L_k)@(L_k,d_v)\longrightarrow(L_q,d_v)
$$

가 된다.

### 왜 $\sqrt{d_k}$로 나눌까?

Query와 Key의 각 원소가 서로 독립이고 평균이 $0$, 분산이 $1$이라고 단순화해 보자.

$$
q\cdot k=\sum_{r=1}^{d_k}q_rk_r
$$

각 곱 $q_rk_r$의 분산을 약 $1$로 보면, 독립인 항 $d_k$개를 더한 내적의 분산은 대략 다음과 같다.

$$
\mathrm{Var}(q\cdot k)\approx d_k
$$

따라서 표준편차는 약 $\sqrt{d_k}$가 된다.

$$
\mathrm{Std}(q\cdot k)\approx\sqrt{d_k}
$$

$\sqrt{d_k}$로 나누면 분산이 다시 약 $1$이 된다.

$$
\mathrm{Var}\left(
\frac{q\cdot k}{\sqrt{d_k}}
\right)
=\frac{\mathrm{Var}(q\cdot k)}{d_k}
\approx1
$$

정확히 말하면 $d_k$가 커질수록 내적의 평균이 계속 양수 방향으로 커지는 것이 아니다. 평균은 $0$ 근처일 수 있지만 **분포의 퍼짐과 점수의 절댓값 규모**가 커진다.

| $d_k$ | 내적의 대략적인 분산 | 내적의 대략적인 표준편차 |
| ---: | ---: | ---: |
| $16$ | $16$ | $4$ |
| $64$ | $64$ | $8$ |

우리가 보정하려는 것은 표준편차이므로 $d_k$가 아니라 $\sqrt{d_k}$로 나눈다. $d_k=64$일 때 일반적인 점수 규모는 약 $8$배 커지므로 $8$로 나누는 것이 자연스럽다. $64$로 나누면 점수를 지나치게 작게 만든다.

### 큰 점수가 Softmax에서 문제가 되는 이유

Softmax는 다음과 같다.

$$
\mathrm{softmax}(x_i)
=\frac{e^{x_i}}{\sum_j e^{x_j}}
$$

예를 들어

$$
\mathrm{softmax}([1,2,3])
\approx[0.09,0.24,0.67]
$$

이지만, 점수 차이가 열 배 커지면

$$
\mathrm{softmax}([10,20,30])
\approx[0,0.00005,0.99995]
$$

처럼 매우 뾰족해진다. 이 영역에서는 작은 점수를 받은 위치의 gradient가 작아져 학습이 불안정해질 수 있다. $\sqrt{d_k}$ 스케일링은 점수의 순서를 바꾸지 않으면서 차이를 줄여 Softmax가 지나치게 일찍 포화되는 것을 완화한다. 온도를 높여 분포를 부드럽게 만드는 것과 비슷한 효과다.

## 6. Shape을 단계별로 확장하기

### 문장 하나

토큰이 4개이고 각 토큰 표현이 8차원이라고 하자.

$$
X:(4,8),
\qquad
W_Q:(8,4)
$$

그러면

$$
Q=XW_Q:(4,8)@(8,4)\longrightarrow(4,4)
$$

이다. 결과의 첫 번째 $4$는 토큰 수, 두 번째 $4$는 Query 하나의 차원 $d_k$다.

> $d_{\text{model}}$, $d_k$, $d_v$는 항상 같지 않다. $d_{\text{model}}$은 입력 표현의 차원, $d_k$는 Query와 Key의 차원, $d_v$는 Value의 차원이다.

### 배치가 추가된 경우

문장 3개를 동시에 처리하고, 각 문장에 토큰이 4개, 각 Query와 Key가 8차원이라고 하자.

$$
Q:(3,4,8),
\qquad
K:(3,4,8)
$$

축의 의미는 다음과 같다.

```text
(batch, seq_len, d_k)
   3        4      8
```

우리는 batch 축은 유지하고 마지막 두 축만 바꿔야 한다.

$$
(3,4,8)\longrightarrow(3,8,4)
$$

NumPy에서는 다음과 같이 계산한다.

```python
K_transposed = np.swapaxes(K, -1, -2)
scores = Q @ K_transposed
```

shape의 흐름은

$$
(3,4,8)@(3,8,4)\longrightarrow(3,4,4)
$$

이다. 각 batch에서 독립적으로 $(4,8)@(8,4)\to(4,4)$ 행렬곱이 수행된다. 더 일반적으로 `@`는 마지막 두 축을 행렬로 취급하고, 앞쪽 축에는 브로드캐스팅 규칙을 적용한다.

### 3차원 이상에서 `.T`를 주의해야 하는 이유

2차원 배열에서 `.T`는 두 축을 교환한다.

$$
(a,b)\xrightarrow{\texttt{.T}}(b,a)
$$

하지만 NumPy에서 3차원 배열에 `.T`를 적용하면 모든 축의 순서가 뒤집힌다.

$$
(3,4,8)\xrightarrow{\texttt{.T}}(8,4,3)
$$

원하는 결과인 $(3,8,4)$가 아니다. 따라서 배치 행렬에서는 마지막 두 축만 바꾸는 `np.swapaxes(K, -1, -2)` 또는 `K.transpose(0, 2, 1)`을 사용한다.

### 1차원 NumPy 벡터에서 `.T`를 주의하자

```python
q = np.array([1, 2, 3])

print(q.shape)    # (3,)
print(q.T.shape)  # (3,)
```

1차원 배열 `(3,)`에는 행과 열을 구분하는 두 개의 축이 없으므로 `.T`를 적용해도 shape이 바뀌지 않는다.

```python
row_q = q.reshape(1, 3)     # (1, 3): 행벡터
column_q = q.reshape(3, 1)  # (3, 1): 열벡터
```

$$
(3,)\ne(1,3),
\qquad
(3,)\ne(3,1)
$$

세 shape은 NumPy에서 서로 다른 배열 구조다.

### Multi-Head Attention

Multi-Head Attention에서는 보통 Query와 Key를 다음 shape으로 정리한다.

$$
Q,K:(B,H,L,d_h)
$$

예를 들어

$$
B=2,
\qquad
H=8,
\qquad
L=100,
\qquad
d_h=64
$$

라면

$$
Q,K:(2,8,100,64)
$$

이다. $K$의 마지막 두 축만 교환하면

$$
K^\top:(2,8,64,100)
$$

이므로

$$
(2,8,100,64)@(2,8,64,100)
\longrightarrow(2,8,100,100)
$$

이 된다. 즉 각 batch의 각 head마다 $100\times100$ Attention score 행렬이 하나씩 생긴다.

일반적인 Transformer에서는 $d_{\text{model}}$을 여러 head로 나누어 $d_h=d_{\text{model}}/H$로 두는 경우가 많다. 예를 들어 $d_{\text{model}}=4096$, $H=32$라면 $d_h=128$이다.

### Self-Attention과 Cross-Attention

Self-Attention에서는 $Q$, $K$, $V$가 같은 입력 $X$에서 만들어진다.

$$
Q=XW_Q,
\qquad
K=XW_K,
\qquad
V=XW_V
$$

따라서 Query 길이와 Key 길이가 같아 score shape이 보통 $(L,L)$이다.

Cross-Attention에서는 Query와 Key가 서로 다른 시퀀스에서 올 수 있으므로 길이가 다를 수 있다.

$$
Q:(10,64),
\qquad
K:(20,64)
$$

이면

$$
QK^\top:(10,64)@(64,20)\longrightarrow(10,20)
$$

이다. 따라서 가장 일반적인 shape 공식은 다음과 같다.

$$
\boxed{
Q:(L_q,d_k),
\quad
K:(L_k,d_k)
\quad\Longrightarrow\quad
QK^\top:(L_q,L_k)
}
$$

## 7. Tensor Shape을 읽는 습관

shape을 외우기보다 각 축이 무엇을 가리키는지 말로 읽는 편이 좋다.

$$
Q:(B,L_q,d_k)
$$

에서

$$
Q[b,i,r]
$$

은 “$b$번째 문장의 $i$번째 토큰 Query가 가진 $r$번째 feature”다. 마찬가지로

$$
K[b,j,r]
$$

은 “$b$번째 문장의 $j$번째 토큰 Key가 가진 $r$번째 feature”다.

따라서 score는 자연스럽게 다음과 같이 읽힌다.

$$
\mathrm{score}[b,i,j]
=\sum_{r=1}^{d_k}Q[b,i,r]K[b,j,r]
$$

즉 $b$번째 batch에서 Query 토큰 $i$와 Key 토큰 $j$의 모든 feature를 같은 위치끼리 곱해 더한 값이다.

## 8. 전체 흐름을 한 장으로 보기

```text
입력 토큰 표현 X
(seq_len, d_model)
        │
        ├── @ W_Q ──→ Q (seq_len, d_k)
        ├── @ W_K ──→ K (seq_len, d_k)
        └── @ W_V ──→ V (seq_len, d_v)

Q (seq_len, d_k) @ Kᵀ (d_k, seq_len)
        │
        ▼
QKᵀ (seq_len, seq_len)
        │
        ├── ÷ √d_k
        ├── + mask
        └── softmax
        │
        ▼
Attention Weights (seq_len, seq_len)
        │
        └── @ V (seq_len, d_v)
        │
        ▼
Output (seq_len, d_v)
```

이 흐름은 다음처럼 확장된다.

```text
벡터 하나와 벡터 하나 비교
q · k
  ↓
벡터 하나와 여러 벡터 비교
q @ Kᵀ
  ↓
모든 벡터와 모든 벡터 비교
Q @ Kᵀ
  ↓
점수 분산 보정
QKᵀ / √d_k
  ↓
Softmax로 참고 비율 결정
  ↓
Attention Weights @ V
  ↓
실제 정보 결합
```

## 9. 시퀀스가 길어지면 왜 $L^2$이 될까?

Self-Attention에서 토큰이 $L$개라면 Query도 $L$개, Key도 $L$개다. 각 Query가 모든 Key와 비교하므로 score 개수는 다음과 같다.

$$
L\times L=L^2
$$

| 시퀀스 길이 $L$ | Score 개수 $L^2$ |
| ---: | ---: |
| $4$ | $16$ |
| $100$ | $10{,}000$ |
| $1{,}000$ | $1{,}000{,}000$ |
| $100{,}000$ | $10{,}000{,}000{,}000$ |

$QK^\top$을 계산하는 시간 복잡도는 feature 차원까지 포함해 대략 $O(L^2d_k)$이고, score 행렬 자체의 메모리 복잡도는 $O(L^2)$이다. 그래서 긴 context를 처리할 때 Attention이 주요 병목 중 하나가 된다.

## 직접 확인

다음 코드는 하나의 Query, 전체 Query 행렬, 배치 Attention의 shape을 차례로 확인한다.

```python
import numpy as np

# 1. 하나의 Query와 여러 Key 비교
q = np.array([2.0, 1.0])
K_small = np.array([
    [1.5, 1.0],
    [-1.0, 2.0],
    [-2.0, -1.0],
])

small_scores = q @ K_small.T
print("small_scores:", small_scores)
print("small_scores.shape:", small_scores.shape)

# 2. 배치가 있는 Scaled Dot-Product Attention
rng = np.random.default_rng(0)

Q = rng.normal(size=(3, 4, 8))
K = rng.normal(size=(3, 4, 8))
V = rng.normal(size=(3, 4, 6))

K_transposed = np.swapaxes(K, -1, -2)
scores = (Q @ K_transposed) / np.sqrt(Q.shape[-1])

# 행별로 수치적으로 안정적인 Softmax 계산
shifted_scores = scores - scores.max(axis=-1, keepdims=True)
exp_scores = np.exp(shifted_scores)
weights = exp_scores / exp_scores.sum(axis=-1, keepdims=True)

output = weights @ V

print("K_transposed.shape:", K_transposed.shape)
print("scores.shape:", scores.shape)
print("weights.shape:", weights.shape)
print("output.shape:", output.shape)
print("row sums are 1:", np.allclose(weights.sum(axis=-1), 1.0))

# 3. 1차원 배열은 전치해도 shape이 바뀌지 않음
print("q.shape, q.T.shape:", q.shape, q.T.shape)
```

실행 결과:

```text
small_scores: [ 4.  0. -5.]
small_scores.shape: (3,)
K_transposed.shape: (3, 8, 4)
scores.shape: (3, 4, 4)
weights.shape: (3, 4, 4)
output.shape: (3, 4, 6)
row sums are 1: True
q.shape, q.T.shape: (2,) (2,)
```

## 헷갈리기 쉬운 부분

| 헷갈리기 쉬운 생각 | 정확한 이해 |
| --- | --- |
| Attention의 내적은 코사인 유사도다. | 내적은 방향과 크기의 영향을 모두 받으며, Attention에서는 학습된 적합도 점수로 사용한다. |
| $K^\top$은 shape만 억지로 맞추기 위한 것이다. | $K$의 각 행을 Query와 내적할 수 있도록 Key들을 열 방향으로 배치한다. |
| Score 행렬은 내적을 사용하므로 대칭이다. | $R_{ij}=Q_i\cdot K_j$와 $R_{ji}=Q_j\cdot K_i$는 서로 다른 벡터 쌍이므로 일반적으로 다르다. |
| Query, Key, Value는 원본 데이터에 들어 있다. | 입력 표현 $X$와 학습 가능한 $W_Q,W_K,W_V$로 모델이 계산한다. |
| Key와 내적했으므로 최종 결과에도 Key를 더한다. | Key는 선택 기준이고, 실제로 가중합하는 정보는 Value다. |
| 배치 텐서에도 무조건 `.T`를 쓰면 된다. | NumPy의 `.T`는 모든 축을 뒤집으므로 마지막 두 축만 `swapaxes(-1, -2)`로 교환한다. |
| $d_k$가 커지면 내적의 평균이 계속 커진다. | 평균보다 분산과 표준편차, 즉 점수 분포의 퍼짐이 커지는 것이 핵심이다. |
| 분산이 $d_k$만큼 커지므로 $d_k$로 나눠야 한다. | 점수의 일반적인 규모는 표준편차인 $\sqrt{d_k}$만큼 커지므로 $\sqrt{d_k}$로 나눈다. |

## 이해 점검

### 1. `q.shape == (8,)`, `K.shape == (5, 8)`이면 결과 shape은?

$$
(8,)@(8,5)\longrightarrow\boxed{(5,)}
$$

후보 Key 5개에 대한 점수가 하나씩 나온다.

### 2. `Q.shape == (4, 8)`, `K.shape == (4, 8)`이면 결과 shape은?

$$
(4,8)@(8,4)\longrightarrow\boxed{(4,4)}
$$

Query 4개와 Key 4개 사이의 총 16개 내적이 담긴다.

### 3. 배치에서 `K.T` 대신 `swapaxes`를 사용하는 이유는?

원하는 변환은

$$
(B,L,d_k)\longrightarrow(B,d_k,L)
$$

이기 때문이다. NumPy의 `.T`는 모든 축을 뒤집어 $(d_k,L,B)$로 만든다.

### 4. $\sqrt{d_k}$ 스케일링을 생략하면?

$d_k$가 커질수록 내적 점수의 분산이 커져 Softmax가 지나치게 뾰족해지기 쉽다. $\sqrt{d_k}$로 나누면 score scale을 안정화해 Softmax의 조기 포화를 완화할 수 있다.

### 5. Self-Attention에서 score shape이 $(L,L)$인 이유는?

같은 길이 $L$의 시퀀스에서 Query와 Key를 만들기 때문에 $L_q=L_k=L$이다.

$$
Q:(L,d_k),
\qquad
K^\top:(d_k,L)
\quad\Longrightarrow\quad
QK^\top:(L,L)
$$

## 실제 활용

- **Self-Attention**: 한 시퀀스의 모든 토큰이 서로를 참고한다.
- **Causal Attention**: 미래 토큰 위치를 mask 처리해 현재 토큰이 이전 토큰만 보게 한다.
- **Cross-Attention**: 한 시퀀스의 Query가 다른 시퀀스의 Key와 Value를 참고한다.
- **Multi-Head Attention**: 여러 head가 서로 다른 관계를 병렬로 학습한다.
- **긴 Context 최적화**: $L^2$ 크기의 score 행렬이 만드는 계산량과 메모리 병목을 줄이는 것이 핵심 과제가 된다.

## 한 문장 요약

> Attention의 $QK^\top$은 모든 Query와 Key의 내적을 한 번에 계산한 $(L_q,L_k)$ 적합도 행렬이며, 이를 $\sqrt{d_k}$로 스케일링하고 Softmax를 적용한 가중치로 Value를 결합한다.
