---
title: Rabin、RSA 与为何需要后量子
type: lecture
lecture: 6
tags: [rsa, rabin-cryptosystem, trapdoor-function, post-quantum-cryptography]
status: complete
source: 'https://65610.csail.mit.edu/2026/lec/l06-pq.pdf'
---
# Lec 6 Rabin、RSA 与为何需要后量子

> MIT 6.5610 · Lecture 6 · 关键词：陷门单向函数、RSA、Rabin、因子分解、二次剩余、Shor 算法、后量子动机
> *说明：经典材料（RSA 1977 / Rabin 1979 / Shor 1994），以标准处理撰写，要点与本课"Rabin, RSA, Why post-quantum?"一致。*

---

## TL;DR

- 陷门单向函数让公开参数支持正向计算，只有持有陷门者能高效求逆；RSA 与 Rabin 分别建立在 RSA 问题和整数分解/平方根困难上。
- RSA 与 Rabin 的代数映射不是可直接使用的安全加密，仍需随机编码、认证和严格参数；“数学可逆”不等于 IND-CPA/CCA 安全。
- Shor 算法能在量子计算机上高效求解分解与离散对数，使 RSA、DH 和 ECC 同时失效，后量子迁移必须在大规模量子机出现前完成。

## 0. 主线

L5 的公钥基于离散对数；本讲转向**基于因子分解**的陷门函数（RSA、Rabin），再点明：这些经典假设都会被**Shor 量子算法**攻破 → 这正是后量子密码（L7 起的 LWE）的动机。

---

## 1. 陷门单向函数（Trapdoor One-Way Function）

::: definition
**陷门单向函数（*TDF*）**：一族函数 $f_{pk}$，公开 $pk$ 下正向易算、反向难求逆；但持有**陷门** $sk$ 者可高效求逆。
:::

> 🔎 这是公钥加密的通用骨架：用 $pk$ 加密 = 正向计算，用 $sk$ 解密 = 用陷门求逆。

---

## 2. RSA

设 $N=pq$（两大素数之积），$\phi(N)=(p-1)(q-1)$。选 $e$ 与 $\phi(N)$ 互素，$d=e^{-1}\bmod\phi(N)$。

::: theorem
**RSA 陷门置换**
- 公钥 $(N,e)$，私钥 $d$（陷门）。
- 正向 $f(x)=x^e \bmod N$；求逆 $f^{-1}(y)=y^d \bmod N$。
- 正确性：$x^{ed}=x^{1+k\phi(N)}\equiv x\pmod N$（Euler 定理）。
:::

- **RSA 假设**：无 $d$ 时求 $e$ 次根 $x=y^{1/e}\bmod N$ 困难。
- **关系**：能分解 $N$ ⟹ 能算 $\phi(N)$ ⟹ 能算 $d$ ⟹ 破 RSA。反向（破 RSA ⟹ 分解）未知，故 RSA 假设**可能**强于分解。

> ⚠️ **教科书 RSA 不安全**：确定性（不 IND-CPA）、有可乘同态 $f(x_1)f(x_2)=f(x_1x_2)$ 可被滥用。实战必须用 **OAEP 填充**等随机化方案。

---

## 3. Rabin

::: theorem
**Rabin 陷门**：$f(x)=x^2 \bmod N$，$N=pq$。
- **安全等价于因子分解**：求平方根 $\Leftrightarrow$ 分解 $N$（这是"漂亮假设"——win-win）。
- 缺点：平方映射**四对一**（每个二次剩余有 4 个平方根），解密有歧义，需附加冗余/标识来消歧。
:::

> 🔎 **为何平方根 ⟺ 分解**：若能对随机 $a$ 求出 $x$ 满足 $x^2\equiv a^2$ 但 $x\not\equiv\pm a$，则 $\gcd(x-a,N)$ 给出 $N$ 的非平凡因子。这正是把"求根能力"归约到"分解能力"的关键。CRT（中国剩余定理）下，模 $N$ 的平方根由模 $p$、模 $q$ 的根组合而成。

---

## 4. 为何需要后量子

::: example
**Shor 算法（1994）**：量子计算机可在**多项式时间**内分解大整数、求解离散对数。
:::

> ⚠️ 一旦大规模容错量子计算机问世，**RSA、Rabin、DH、ECDLP 全部失效**。即便量子计算机尚未到来，"**先收割、后解密**（harvest-now-decrypt-later）"的威胁意味着今天的长期机密就需要后量子保护。
> 对比对称密码：Grover 算法只提供平方加速（$2^n\to 2^{n/2}$），密钥翻倍即可应对——所以**后量子的痛点在公钥**。
> NIST 后量子标准（如基于格的 ML-KEM/Kyber、ML-DSA/Dilithium）即今日可在经典机上运行、抵御量子敌手的方案。这把我们引向 **LWE**（L7）。

---

## 5. RSA、Rabin 与后量子小结

| 方案 | 陷门基础 | 安全 ⟺ 分解？ | 量子安全？ |
|------|----------|----------------|------------|
| RSA | $x^e\bmod N$ | 否（可能更强） | ❌ Shor |
| Rabin | $x^2\bmod N$ | ✅ 等价 | ❌ Shor |
| ElGamal/DH | 离散对数 | — | ❌ Shor |
| 格 (LWE) | 见 L7 | — | ✅（目前认为） |

- 公钥 = 陷门单向函数；RSA/Rabin 基于因子分解。
- 教科书 RSA 必须随机化填充；Rabin 安全严格等价分解但有四义性。
- Shor 摧毁所有经典数论公钥 → 后量子（格）登场。

::: insight
后量子迁移不是单次替换算法，而是包含资产盘点、混合部署、协议协商与长期密文保密期的生命周期工程。
:::
