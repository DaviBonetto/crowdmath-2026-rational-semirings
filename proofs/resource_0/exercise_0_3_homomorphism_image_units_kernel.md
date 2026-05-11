# Exercise 0.3

## Status

Solved Offline

## Restatement

Let $f : M \to N$ be a monoid homomorphism. We want to prove that the following three statements hold:

1. $f(M)$ is a submonoid of $N$.
2. If $M$ is a group, then $f(M)$ is a group.
3. $\ker f := \{ m \in M : f(m) = e_N \}$ is a submonoid of $M$.

## Definitions Used

- **Monoid homomorphism:** A map $f : M \to N$ between monoids satisfying $f(e_M) = e_N$ and $f(ab) = f(a)f(b)$ for all $a, b \in M$.

- **Submonoid:** A subset $K$ of a monoid that contains the identity element and is closed under the monoid operation.

- **Image of $f$:** The set $f(M) := \{ f(m) : m \in M \} \subseteq N$.

- **Kernel of $f$:** The set $\ker f := \{ m \in M : f(m) = e_N \}$.

- **Group:** A monoid in which every element has a two-sided inverse.

## Proof

### Part (1): $f(M)$ is a submonoid of $N$

We verify the two conditions for $f(M)$ to be a submonoid of $N$.

**Identity.** Since $f$ is a monoid homomorphism, $f(e_M) = e_N$. In particular, $e_N \in f(M)$.

**Closure.** Let $x, y \in f(M)$. Then there exist $a, b \in M$ such that $f(a) = x$ and $f(b) = y$. Since $f$ is a homomorphism,

$$
xy = f(a)\,f(b) = f(ab).
$$

Since $ab \in M$, we have $xy = f(ab) \in f(M)$.

Hence $f(M)$ is a submonoid of $N$. $\square$

---

### Part (2): If $M$ is a group, then $f(M)$ is a group

By Part (1), $f(M)$ is already a submonoid of $N$, so it suffices to show that every element of $f(M)$ has a two-sided inverse inside $f(M)$.

Let $x \in f(M)$, so $x = f(a)$ for some $a \in M$. Since $M$ is a group, the inverse $a^{-1}$ exists in $M$, and thus $f(a^{-1}) \in f(M)$. We compute:

$$
x \cdot f(a^{-1}) = f(a)\,f(a^{-1}) = f(aa^{-1}) = f(e_M) = e_N,
$$

$$
f(a^{-1}) \cdot x = f(a^{-1})\,f(a) = f(a^{-1}a) = f(e_M) = e_N.
$$

Therefore $f(a^{-1})$ is the two-sided inverse of $x$ in $f(M)$, and since $x$ was arbitrary, every element of $f(M)$ is invertible. Hence $f(M)$ is a group. $\square$

---

### Part (3): $\ker f$ is a submonoid of $M$

We verify the two conditions for $\ker f$ to be a submonoid of $M$.

**Identity.** Since $f$ is a monoid homomorphism, $f(e_M) = e_N$. Hence $e_M \in \ker f$.

**Closure.** Let $a, b \in \ker f$, so $f(a) = e_N$ and $f(b) = e_N$. Since $f$ is a homomorphism,

$$
f(ab) = f(a)\,f(b) = e_N \cdot e_N = e_N.
$$

Hence $ab \in \ker f$.

Therefore $\ker f$ is a submonoid of $M$. $\square$

## Notes

- In Part (2), the key insight is that $f$ sends inverses to inverses: $f(a^{-1}) = f(a)^{-1}$ in $N$. This is a general fact about group homomorphisms that follows directly from the homomorphism property.

- Part (3) shows that $\ker f$ is a submonoid, but not necessarily a group. For example, let $M = (\mathbb{N}_0,+)$ and let $N = \{0\}$ be the trivial additive monoid. The map $f : M \to N$ given by $f(n)=0$ is a monoid homomorphism, and $\ker f = \mathbb{N}_0$, which is a submonoid of $M$ but not a group.

- If $M$ is itself a group, then $\ker f$ is in fact a **normal subgroup** of $M$ (not just a submonoid), since it is also closed under taking inverses and conjugation. This stronger statement is standard in group theory.

- The three parts together illustrate that monoid homomorphisms behave well with respect to the algebraic structure: they preserve submonoids forwards (via images) and backwards (via kernels).
