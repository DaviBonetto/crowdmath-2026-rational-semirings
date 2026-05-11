# Exercise 1.5

## Status

Solved Offline.

---

## Restatement

A monoid $M$ is a **half-factorial monoid (HFM)** if it is atomic and any two atomic factorizations of the same element have the same number of atoms. Every UFM is an HFM.

(1) Prove the Hilbert monoid $H = \{4n+1 : n \in \mathbb{N}_0\}$ is an HFM that is not a UFM.

(2) Prove a Puiseux monoid is an HFM if and only if it is a UFM.

---

## Definitions Used

- **$\Omega_1(h)$:** number of standard prime factors of $h$ that are $\equiv 1 \pmod{4}$, counted with multiplicity.
- **$\Omega_3(h)$:** number of standard prime factors of $h$ that are $\equiv 3 \pmod{4}$, counted with multiplicity.
- **Atoms of $H$:** by Exercise 1.2, the atoms of $H$ are exactly the standard primes $p \equiv 1 \pmod 4$, and the products $q_1 q_2$ where $q_1, q_2$ are standard primes with $q_i \equiv 3 \pmod 4$.

---

## Part (1): $H$ is an HFM that is not a UFM.

### Step 1: $H$ is atomic.

This was proved in Exercise 1.2, Part (3). $\square$

---

### Step 2: $H$ is an HFM.

Let $h \in H \setminus \{1\}$ and write its standard prime factorization as
$$h = p_1^{a_1} \cdots p_s^{a_s} \cdot q_1^{b_1} \cdots q_t^{b_t},$$
where $p_i \equiv 1 \pmod 4$ and $q_j \equiv 3 \pmod 4$. Set $\Omega_1 := \Omega_1(h) = \sum_i a_i$ and $\Omega_3 := \Omega_3(h) = \sum_j b_j$.

Since $h \equiv 1 \pmod 4$ and each $q_j \equiv 3 \pmod 4$, the product $\prod q_j^{b_j} \equiv 3^{\Omega_3} \pmod 4$ must satisfy $3^{\Omega_3} \equiv 1 \pmod 4$, which forces $\Omega_3$ to be **even**.

**Claim:** Every atomic factorization of $h$ in $H$ has exactly $\displaystyle k = \Omega_1 + \frac{\Omega_3}{2}$ factors.

Let $h = c_1 \cdots c_k$ be any atomic factorization in $H$. Each atom $c_\ell$ is one of two types:

| Type | Form | $\Omega_1(c_\ell)$ | $\Omega_3(c_\ell)$ |
|---:|---|---:|---:|
| 1 | Standard prime $p \equiv 1 \pmod 4$ | 1 | 0 |
| 2 | Product $q_i q_j$ with $q_i \equiv q_j \equiv 3 \pmod 4$ | 0 | 2 |

Since $\Omega_1$ and $\Omega_3$ are additive over products and $h = c_1 \cdots c_k$:
$$\Omega_1(h) = \sum_{\ell} \Omega_1(c_\ell), \qquad \Omega_3(h) = \sum_{\ell} \Omega_3(c_\ell).$$

Let $k_1$ = number of Type-1 atoms and $k_2$ = number of Type-2 atoms. Then:
$$k_1 = \Omega_1(h) = \Omega_1, \qquad 2k_2 = \Omega_3(h) = \Omega_3 \implies k_2 = \frac{\Omega_3}{2}.$$

So the total number of atoms is
$$k = k_1 + k_2 = \Omega_1 + \frac{\Omega_3}{2},$$
which is **completely determined by $h$** and independent of the factorization. Therefore $H$ is an HFM. $\square$

---

### Step 3: $H$ is not a UFM.

The element $441 = 3^2 \cdot 7^2 \in H$ (since $441 = 4 \cdot 110 + 1$) admits two distinct atomic factorizations in $H$:
$$441 = 9 \times 49 = 21 \times 21.$$

Checking:
- $9 = 3^2 \in H$, $49 = 7^2 \in H$, $21 = 3 \cdot 7 \in H$ (since $21 = 4 \cdot 5 + 1$).
- $9, 49, 21$ are atoms of $H$ by Exercise 1.2 Part (2) (each is a product of two primes $\equiv 3 \pmod 4$).
- $\{9, 49\} \neq \{21, 21\}$ as multisets.

Both factorizations have length $2 = 0 + \frac{4}{2}$, consistent with HFM. But they are distinct, so $H$ is not a UFM. $\blacksquare$

---

## Part (2): A Puiseux monoid is an HFM if and only if it is a UFM.

### ($\Leftarrow$) UFM $\Rightarrow$ HFM.

In a UFM, every element has a unique atomic factorization, so all factorizations trivially have the same length. $\square$

---

### ($\Rightarrow$) HFM $\Rightarrow$ UFM.

Let $M$ be an atomic Puiseux monoid (additive submonoid of $(\mathbb{Q}_{\geq 0}, +)$) that is an HFM. We show $M$ is a UFM.

**Key Lemma:** $M$ has at most one atom.

*Proof.* Suppose for contradiction that $M$ has two distinct atoms $a \neq b$, with $a, b \in \mathbb{Q}_{>0}$.

Write $\dfrac{a}{b} = \dfrac{p}{q}$ in lowest terms, with $p, q \in \mathbb{N}$ and $\gcd(p, q) = 1$.

Then $q \cdot a = p \cdot b$ (as rational numbers). Since $a, b \in M$ and $M$ is closed under addition:
$$x := q \cdot a = \underbrace{a + \cdots + a}_{q} \in M \quad \text{and} \quad x = p \cdot b = \underbrace{b + \cdots + b}_{p} \in M.$$

These give two atomic factorizations of $x$:
- Factorization 1: $q$ copies of the atom $a$, length $q$.
- Factorization 2: $p$ copies of the atom $b$, length $p$.

Since $M$ is an HFM, we must have $q = p$.

But $\gcd(p, q) = 1$ and $p = q$ forces $p = q = 1$, giving $a = b$ — a contradiction.

Therefore $M$ has at most one atom. $\square$

**Conclusion:**

If $M = \{0\}$, it is trivially a UFM.

If $M \neq \{0\}$, then $M$ is atomic, so it has at least one atom. By the lemma, it has at most one atom. Hence it has exactly one atom, say $a \in \mathbb{Q}_{>0}$. Every nonzero element of $M$ factors as a sum of copies of $a$, so $M = \mathbb{N}_0 a \cong (\mathbb{N}_0, +)$.

The monoid $(\mathbb{N}_0, +)$ is a UFM: every $n \in \mathbb{N}$ has the unique factorization $n = 1 + \cdots + 1$ ($n$ times). Under the isomorphism, $M = \mathbb{N}_0 a$ is a UFM with unique atom $a$. $\blacksquare$

---

## Summary

| Monoid | Atomic | HFM | UFM |
|---|:---:|:---:|:---:|
| Hilbert monoid $H$ | ✓ | ✓ | ✗ |
| Puiseux monoid $M$ (HFM) | ✓ | ✓ | ✓ |
| Atomic Puiseux monoid with more than one atom | ✓ | ✗ | ✗ |

---

## Notes

The HFM condition is strictly weaker than UFM in general — the Hilbert monoid witnesses this gap. The factorization $441 = 9 \times 49 = 21 \times 21$ is the canonical example: two different atomic factorizations of the same length.

The reason Puiseux monoids cannot exhibit this gap is entirely down to their rational structure. Any two distinct atoms $a \neq b \in \mathbb{Q}_{>0}$ satisfy $q \cdot a = p \cdot b$ for integers $p \neq q$ (since $a/b \in \mathbb{Q}$, $p/q$ in lowest terms gives $p \neq q$ whenever $a \neq b$). This immediately produces factorizations of different lengths, breaking HFM.

In contrast, the Hilbert monoid is multiplicative and its atoms (which are products of two primes $\equiv 3 \pmod 4$) all have the same "weight" $2$ in terms of standard prime counting, so different factorizations always come out the same length.
