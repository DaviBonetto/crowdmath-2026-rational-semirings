# Exercise 1.4

## Status

Solved Offline.

---

## Restatement

Let $\rho$ be the positive root of $x^3 - 3x^2 - 3 = 0$. Prove that $(\mathbb{N}_0[\rho], +)$ is atomic and find its atoms.

---

## Setup

**What is $\mathbb{N}_0[\rho]$?**

$$\mathbb{N}_0[\rho] = \{f(\rho) : f \in \mathbb{N}_0[x]\} = \left\{\sum_{i=0}^n a_i \rho^i : n \in \mathbb{N}_0,\, a_i \in \mathbb{N}_0\right\} \subseteq \mathbb{R}_{>0} \cup \{0\}$$

under addition. Since $\rho > 0$ (as the positive root), every element is non-negative.

**Location of $\rho$:** Since $f(3) = 27 - 27 - 3 = -3 < 0$ and $f(4) = 64 - 48 - 3 = 13 > 0$, we have $\rho \in (3, 4)$. The polynomial $x^3 - 3x^2 - 3$ has no rational roots (none of $\pm 1, \pm 3$ are roots), so it is irreducible over $\mathbb{Q}$, and $[\mathbb{Q}(\rho):\mathbb{Q}] = 3$.

**Consequence:** $\{1, \rho, \rho^2\}$ is a $\mathbb{Q}$-basis for $\mathbb{Q}(\rho)$, so every element of $\mathbb{Q}(\rho)$ has a **unique** representation $A + B\rho + C\rho^2$ with $A, B, C \in \mathbb{Q}$.

---

## Key Lemma: Every $\rho^n$ has non-negative coordinates in the basis $\{1, \rho, \rho^2\}$.

Write $\rho^n = a_n + b_n\rho + c_n\rho^2$ for $a_n, b_n, c_n \in \mathbb{Z}$.

**Recurrence.** From $\rho^3 = 3\rho^2 + 3$:
$$\rho^{n+1} = a_n\rho + b_n\rho^2 + c_n\rho^3 = a_n\rho + b_n\rho^2 + c_n(3\rho^2 + 3) = 3c_n + a_n\rho + (b_n + 3c_n)\rho^2.$$

So the recurrence is:
$$a_{n+1} = 3c_n, \qquad b_{n+1} = a_n, \qquad c_{n+1} = b_n + 3c_n.$$

**Initial values:**

| $n$ | $a_n$ | $b_n$ | $c_n$ | Element                 |
| --: | ----: | ----: | ----: | ----------------------- |
|   0 |     1 |     0 |     0 | $1$                     |
|   1 |     0 |     1 |     0 | $\rho$                  |
|   2 |     0 |     0 |     1 | $\rho^2$                |
|   3 |     3 |     0 |     3 | $3 + 3\rho^2$           |
|   4 |     9 |     3 |     9 | $9 + 3\rho + 9\rho^2$   |
|   5 |    27 |     9 |    30 | $27 + 9\rho + 30\rho^2$ |

**Claim:** $a_n, b_n, c_n \geq 0$ for all $n \geq 0$.

_Proof by induction._ Base cases $n = 0, 1, 2$ are clear. If $a_n, b_n, c_n \geq 0$, then $a_{n+1} = 3c_n \geq 0$, $b_{n+1} = a_n \geq 0$, $c_{n+1} = b_n + 3c_n \geq 0$. $\square$

---

## Main Result

### Step 1: $\mathbb{N}_0[\rho] = \{A + B\rho + C\rho^2 : A, B, C \in \mathbb{N}_0\}$.

**($\supseteq$):** Every $A + B\rho + C\rho^2$ with $A, B, C \in \mathbb{N}_0$ equals the polynomial $A + Bx + Cx^2$ evaluated at $\rho$, so it lies in $\mathbb{N}_0[\rho]$.

**($\subseteq$):** Let $f(\rho) = \sum_{i=0}^n \alpha_i \rho^i$ with $\alpha_i \in \mathbb{N}_0$. By the Key Lemma, each $\rho^i = u_i + v_i\rho + w_i\rho^2$ with $u_i, v_i, w_i \geq 0$. Therefore:
$$f(\rho) = \underbrace{\sum_i \alpha_i u_i}_{A} + \underbrace{\sum_i \alpha_i v_i}_{B}\rho + \underbrace{\sum_i \alpha_i w_i}_{C}\rho^2$$
with $A, B, C \in \mathbb{N}_0$ (since $\alpha_i \geq 0$ and $u_i, v_i, w_i \geq 0$). $\square$

---

### Step 2: Isomorphism $\mathbb{N}_0[\rho] \cong \mathbb{N}_0^3$.

Define $\varphi: \mathbb{N}_0[\rho] \to \mathbb{N}_0^3$ by $\varphi(A + B\rho + C\rho^2) = (A, B, C)$.

- **Well-defined:** By Step 1, every element of $\mathbb{N}_0[\rho]$ has the form $A + B\rho + C\rho^2$ with $A, B, C \in \mathbb{N}_0$.
- **Injective:** Since $\{1, \rho, \rho^2\}$ is $\mathbb{Q}$-linearly independent, the representation is unique: $A + B\rho + C\rho^2 = A' + B'\rho + C'\rho^2$ implies $A = A', B = B', C = C'$.
- **Surjective:** Every $(A, B, C) \in \mathbb{N}_0^3$ maps from $A + B\rho + C\rho^2 \in \mathbb{N}_0[\rho]$.
- **Monoid homomorphism:** $\varphi((A_1+B_1\rho+C_1\rho^2)+(A_2+B_2\rho+C_2\rho^2)) = (A_1+A_2, B_1+B_2, C_1+C_2) = \varphi(\cdot)+\varphi(\cdot)$. ✓

So $\varphi$ is an isomorphism of additive monoids. $\square$

---

### Step 3: Atomicity and atoms.

The free commutative monoid $\mathbb{N}_0^3$ is **atomic** with atoms $\{e_1, e_2, e_3\}$: every $(A, B, C) = A \cdot e_1 + B \cdot e_2 + C \cdot e_3$ is a unique atomic factorization.

Since $\mathbb{N}_0[\rho] \cong \mathbb{N}_0^3$, the monoid $\mathbb{N}_0[\rho]$ is atomic, and its atoms are $\varphi^{-1}(e_1), \varphi^{-1}(e_2), \varphi^{-1}(e_3)$:

$$\boxed{\mathcal{A}(\mathbb{N}_0[\rho]) = \{1,\, \rho,\, \rho^2\}.}$$

Every $x \in \mathbb{N}_0[\rho] \setminus \{0\}$ factors uniquely as:
$$x = A \cdot 1 + B \cdot \rho + C \cdot \rho^2 \qquad (A, B, C \in \mathbb{N}_0,\text{ not all zero})$$
which is a sum of $A + B + C$ atoms (with $A$ copies of $1$, $B$ copies of $\rho$, $C$ copies of $\rho^2$). $\blacksquare$

---

### Verification that $1, \rho, \rho^2$ are atoms.

An element $a \in \mathbb{N}_0[\rho] \setminus \{0\}$ is an atom iff $a = b + c$ with $b, c \in \mathbb{N}_0[\rho]$ forces $b = 0$ or $c = 0$.

Under $\varphi$, atoms of $\mathbb{N}_0[\rho]$ correspond to atoms of $\mathbb{N}_0^3$, i.e., elements $(A,B,C)$ with $A+B+C = 1$. These are exactly $e_1 = (1,0,0)$, $e_2 = (0,1,0)$, $e_3 = (0,0,1)$, corresponding to $1, \rho, \rho^2$. $\square$

---

## Notes

The central observation is that the polynomial relation $\rho^3 = 3\rho^2 + 3$ is entirely "additive" the right-hand side has non-negative coefficients. This is what allows $\mathbb{N}_0[\rho]$ to be exactly the set of polynomials of degree at most $2$ in $\rho$ with non-negative integer coefficients. If the relation had introduced negative signs (e.g., $\rho^3 = \rho^2 - 1$), higher powers would escape $\mathbb{N}_0^3$ and the structure would be more subtle.

Numerically, $\rho \approx 3.28$, so the atoms have approximate values $1$, $3.28$, and $10.76$. Any element of $\mathbb{N}_0[\rho]$ decomposes uniquely into non-negative integer multiples of these three atoms.

The factorization is unique because it inherits from $\mathbb{N}_0^3$, which is a UFM (unique factorization monoid). In particular, $\mathbb{N}_0[\rho]$ is not just atomic but also a UFM.
