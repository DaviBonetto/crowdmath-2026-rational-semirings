# Exercise 1.6

## Status

Solved Offline.

---

## Restatement

Let $R = \{a + ib\sqrt{5} : a, b \in \mathbb{Z}\} = \mathbb{Z}[i\sqrt{5}] = \mathbb{Z}[\sqrt{-5}]$. Let $M = R \setminus \{0\}$ be the multiplicative monoid of nonzero elements of $R$.

(1) $M$ is a cancellative commutative monoid under multiplication.
(2) $M$ is atomic.
(3) $M$ is an HFM.
(4) $M$ is not a UFM.

---

## Setup and Key Tool: The Norm

Define the **norm** $N : M \to \mathbb{N}_0$ by
$$N(a + ib\sqrt{5}) = a^2 + 5b^2 = |a + ib\sqrt{5}|^2.$$

Since $N$ is the complex absolute value squared, it is **multiplicative:** $N(\alpha\beta) = N(\alpha)N(\beta)$.

The **units** of $M$ are elements $u \in M$ with $uv = 1$ for some $v \in M$. Since $N(uv) = N(u)N(v) = N(1) = 1$ and $N \geq 0$, units satisfy $N(u) = 1$, i.e., $a^2 + 5b^2 = 1$, which forces $b = 0$ and $a = \pm 1$. So $M^\times = \{\pm 1\}$.

---

## Part (1): $M$ is a cancellative commutative monoid.

**Closure:** $(a+ib\sqrt{5})(c+id\sqrt{5}) = (ac-5bd) + i(ad+bc)\sqrt{5} \in M$, since $ac-5bd,\, ad+bc \in \mathbb{Z}$.

**Associativity and commutativity:** Inherited from $(\mathbb{C}, \times)$.

**Identity:** $1 = 1 + i \cdot 0 \cdot \sqrt{5} \in M$.

So $M$ is a commutative monoid.

**Cancellative:** If $\alpha, \beta, \gamma \in M$ and $\alpha\beta = \alpha\gamma$, then $\alpha(\beta - \gamma) = 0$ in $\mathbb{C}$. Since $\mathbb{C}$ is a field and $\alpha \neq 0$, we get $\beta = \gamma$. $\blacksquare$

---

## Part (2): $M$ is atomic.

Let $\alpha \in M$ be a non-unit, so $N(\alpha) \geq 2$.

If $\alpha$ is not an atom, write $\alpha = \beta\gamma$ with $\beta, \gamma$ both non-units. Then $N(\alpha) = N(\beta) \cdot N(\gamma)$ with $N(\beta), N(\gamma) \geq 2$, so $N(\beta) < N(\alpha)$ and $N(\gamma) < N(\alpha)$.

Since $N$ takes values in $\mathbb{N}$, this descent terminates: inducting on $N(\alpha)$, every non-unit factors into finitely many atoms. $\blacksquare$

---

## Part (3): $M$ is an HFM.

We use the standard ideal-theoretic fact that $R = \mathbb{Z}[\sqrt{-5}]$ is the ring of integers of $\mathbb{Q}(\sqrt{-5})$, is a Dedekind domain, and has class number $2$. Thus its ideal class group has order $2$.

> **External input:** $R = \mathbb{Z}[\sqrt{-5}]$ is a Dedekind domain with class number $2$. This is a standard result in algebraic number theory and is used here without proof.

### Ideal classification of atoms.

Every nonzero ideal of $R$ factors uniquely into prime ideals. The class group of $R$ is $\text{Cl}(R) \cong \mathbb{Z}/2\mathbb{Z} = \{[\mathcal{O}], [\mathfrak{c}]\}$, where $[\mathcal{O}]$ is the principal class and $[\mathfrak{c}]$ is the unique non-trivial class.

For an atom (irreducible) $\alpha \in M$, the ideal $(\alpha)$ is principal. Write its prime ideal factorization as $(\alpha) = \mathfrak{p}_1 \cdots \mathfrak{p}_k$. Since $(\alpha)$ is principal, $[\mathfrak{p}_1] \cdots [\mathfrak{p}_k] = [\mathcal{O}]$ in $\text{Cl}(R)$.

Since the class group has order 2, this means the number of non-principal prime ideals among $\mathfrak{p}_1, \ldots, \mathfrak{p}_k$ is **even**.

**Type A atoms:** atoms whose principal ideal factors as a single principal prime ideal:
$$
(\alpha)=\mathfrak{p},
$$
where $\mathfrak{p}$ is principal.

**Type B atoms:** atoms whose principal ideal factors as a product of two non-principal prime ideals:
$$
(\alpha)=\mathfrak{p}\mathfrak{q},
$$
where $[\mathfrak{p}]=[\mathfrak{q}]=[\mathfrak{c}]$.

These are exactly the two minimal ways to obtain a principal product of prime ideals when the class group has order $2$: either one principal prime ideal, or two non-principal prime ideals whose classes multiply to the principal class.

### Fixed length of factorization.

Fix $\alpha \in M$ and write the unique prime ideal factorization:
$$(\alpha) = \mathfrak{p}_1 \cdots \mathfrak{p}_n, \qquad n = \Omega_{\text{id}}(\alpha) \text{ (fixed by }\alpha\text{)}.$$

Let:
- $n_{\text{p}}$ = number of principal prime ideals among $\mathfrak{p}_1, \ldots, \mathfrak{p}_n$;
- $n_{\text{np}} = n - n_{\text{p}}$ = number of non-principal ones (always even, since $(\alpha)$ is principal).

In **any** atomic factorization $\alpha = \alpha_1 \cdots \alpha_r$, we have $(\alpha) = (\alpha_1) \cdots (\alpha_r)$. By uniqueness of ideal factorization, each $(\alpha_i)$ contributes a subset of the prime ideals:

| Atom type | Prime ideals contributed | $n_{\text{p}}$ contribution | $n_{\text{np}}$ contribution |
|---|---|---:|---:|
| Type A | $\mathfrak{q}$ (principal) | 1 | 0 |
| Type B | $\mathfrak{q}_1\mathfrak{q}_2$ (both non-principal) | 0 | 2 |

Let $k_A$ = number of Type A atoms and $k_B$ = number of Type B atoms in the factorization. Then:
$$n_{\text{p}} = k_A \cdot 1 + k_B \cdot 0 = k_A, \qquad n_{\text{np}} = k_A \cdot 0 + k_B \cdot 2 = 2k_B.$$

Solving: $k_A = n_{\text{p}}$ and $k_B = n_{\text{np}}/2$. Therefore the total number of atoms is
$$r = k_A + k_B = n_{\text{p}} + \frac{n_{\text{np}}}{2},$$
which is **completely determined by $\alpha$** (via its ideal factorization) and **independent of the choice of atomic factorization**. Hence $M$ is an HFM. $\blacksquare$

### Verification on examples.

| Element | $n_{\text{p}}$ | $n_{\text{np}}$ | HFM length |
|---|---:|---:|---:|
| $6$ | 0 | 4 | $0 + 4/2 = 2$ |
| $2$ | 0 | 2 | $0 + 2/2 = 1$ |
| $3$ | 0 | 2 | $0 + 2/2 = 1$ |

Consistent: $6 = 2 \cdot 3$ and $6 = (1+i\sqrt{5})(1-i\sqrt{5})$ both have length 2. ✓

---

## Part (4): $M$ is not a UFM.

The element $6 \in M$ has two distinct atomic factorizations:

$$6 = 2 \cdot 3 = (1 + i\sqrt{5})(1 - i\sqrt{5}).$$

**Verification that all four factors are atoms:**

- $N(2) = 4$. Any factorization $2 = \alpha\beta$ gives $N(\alpha)N(\beta) = 4$. Since $a^2+5b^2=2$ has no integer solution, $N(\alpha) \notin \{2\}$, so $N(\alpha) \in \{1, 4\}$, meaning one factor is a unit. So $2$ is an atom.
- $N(3) = 9$. Similarly, $a^2+5b^2=3$ has no solution, so $3$ is an atom.
- $N(1+i\sqrt{5}) = 1+5 = 6$. Any factorization gives $N(\alpha)N(\beta) = 6$. We need $N(\alpha) \in \{2,3\}$, but $a^2+5b^2=2$ and $a^2+5b^2=3$ have no solutions. So $1+i\sqrt{5}$ is an atom.
- $N(1-i\sqrt{5}) = 6$: same argument.

**The two factorizations are distinct as multisets:** $\{2, 3\} \neq \{1+i\sqrt{5},\, 1-i\sqrt{5}\}$.

Therefore $M$ is not a UFM. $\blacksquare$

---

## Notes

The key structure behind Parts (3) and (4) is that $\mathbb{Z}[\sqrt{-5}]$ has class number 2. This is precisely large enough to allow multiple atomic factorizations of the same element (breaking UFM), but small enough that all factorizations have the same length (HFM). With class number 1 (i.e., a PID), every Dedekind domain is a UFD; the jump to class number 2 introduces exactly the kind of non-uniqueness seen in $6 = 2 \cdot 3 = (1+i\sqrt{5})(1-i\sqrt{5})$.

The HFM counting argument — tracking principal vs. non-principal prime ideals — is a clean application of the fact that non-principal prime ideals always appear in pairs in any element-level factorization (since otherwise the product would not be principal).
