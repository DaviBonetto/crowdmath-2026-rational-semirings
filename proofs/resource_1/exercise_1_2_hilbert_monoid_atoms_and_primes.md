# Exercise 1.2

## Status

Solved Offline.

---

## Restatement

The **Hilbert monoid** is $H := \{4n+1 : n \in \mathbb{N}_0\} = \{1, 5, 9, 13, 17, 21, 25, \ldots\}$ under multiplication. We prove three facts about its prime and atomic structure.

---

## Definitions Used

- **$H$-divisibility:** $a \mid_H b$ means $b = a \cdot h$ for some $h \in H$.
- **Atom of $H$:** An element $a \in H \setminus \{1\}$ that cannot be written as $a = xy$ with $x, y \in H \setminus \{1\}$.
- **Prime element of $H$:** An element $p \in H \setminus \{1\}$ such that $p \mid_H ab$ implies $p \mid_H a$ or $p \mid_H b$.
- **Standard prime:** A prime in $\mathbb{Z}$.
- **Atomic monoid:** Every non-identity element factors as a product of atoms.

Note: $H$ is closed under multiplication since $(4a+1)(4b+1) = 4(4ab+a+b)+1 \in H$.

---

## Proof

### Part (1): Every standard prime $p \equiv 1 \pmod{4}$ is a prime element of $H$.

Let $p$ be a standard prime with $p \equiv 1 \pmod{4}$, so $p \in H$.

Suppose $p \mid_H ab$ for $a, b \in H$. Then $ab = p \cdot h$ for some $h \in H$, so $p \mid ab$ in $\mathbb{Z}$. Since $p$ is a standard prime, $p \mid a$ or $p \mid b$ in $\mathbb{Z}$.

Without loss of generality, suppose $p \mid a$ in $\mathbb{Z}$, so $a = p \cdot k$ for some $k \in \mathbb{Z}_{>0}$.

**Claim:** $k \in H$.

Since $a \in H$, we have $a \equiv 1 \pmod{4}$. Since $p \equiv 1 \pmod{4}$, we get
$$k \equiv a \cdot p^{-1} \equiv 1 \cdot 1 \equiv 1 \pmod{4}.$$
(More explicitly: $a = pk$ and $p \equiv 1$, so $1 \equiv a \equiv k \pmod{4}$.) Also $k > 0$. So $k \in H$.

Therefore $a = p \cdot k$ with $k \in H$, i.e., $p \mid_H a$. Hence $p$ is a prime element of $H$. $\blacksquare$

---

### Part (2): If $q = p_1 p_2$ with $p_1, p_2$ standard primes in $4\mathbb{N}_0 + 3$, then $q$ is an atom of $H$ that is not prime.

**Setup:** Since $p_1, p_2 \equiv 3 \pmod{4}$, we have $q = p_1 p_2 \equiv 9 \equiv 1 \pmod{4}$, so $q \in H$. Note that $p_1, p_2 \notin H$ (as $3 \not\equiv 1 \pmod 4$).

---

#### $q$ is an atom.

Suppose $q = xy$ with $x, y \in H$. Then $x, y \in \mathbb{Z}_{>0}$ and $x \mid q$ in $\mathbb{Z}$.

The positive integer divisors of $q = p_1 p_2$ are:
- If $p_1 \neq p_2$: $\{1, p_1, p_2, p_1 p_2\}$.
- If $p_1 = p_2 = p$: $\{1, p, p^2\}$.

In both cases, $p_1 \notin H$ and $p_2 \notin H$ (since $p_1, p_2 \equiv 3 \pmod{4}$). Therefore the only divisors of $q$ that lie in $H$ are $1$ and $q$ itself.

So $x = 1$ (and $y = q$) or $x = q$ (and $y = 1$). Either way, $q$ is an atom of $H$. $\square$

---

#### $q$ is not prime.

We exhibit $a, b \in H$ with $q \mid_H ab$ but $q \nmid_H a$ and $q \nmid_H b$.

**Case 1: $p_1 \neq p_2$.** Take $a = p_1^2$ and $b = p_2^2$. Since $p_i \equiv 3 \pmod 4$, $p_i^2 \equiv 1 \pmod 4$, so $a, b \in H$.

We have $ab = p_1^2 p_2^2 = (p_1 p_2)^2 = q \cdot q$, and $q \in H$, so $q \mid_H ab$. ✓

Suppose $q \mid_H a = p_1^2$. Then $p_1^2 = p_1 p_2 \cdot h$ for some $h \in H$, giving $p_1 = p_2 h$. Since $p_1$ is prime and $h \geq 1$, this forces $p_2 \mid p_1$, hence $p_2 = p_1$, contradicting $p_1 \neq p_2$. So $q \nmid_H a$.

By symmetry, $q \nmid_H b$. ✓

**Case 2: $p_1 = p_2 = p$, so $q = p^2$.** Choose a standard prime $r \equiv 3 \pmod 4$ with $r \neq p$; for instance, take $r = 3$ if $p \neq 3$, and take $r = 7$ if $p = 3$. Set $a = b = pr$. Since $p, r \equiv 3 \pmod 4$, $pr \equiv 9 \equiv 1 \pmod 4$, so $a = b \in H$.

We have $ab = p^2 r^2 = q \cdot r^2$, and $r^2 \equiv 1 \pmod 4$ so $r^2 \in H$. Thus $q \mid_H ab$. ✓

Suppose $q \mid_H a = pr$. Then $pr = p^2 h$ for some $h \in H$, giving $r = ph$. Since $r$ is prime, either $p = 1$ (impossible) or $h = 1$ and $r = p$, contradicting $r \neq p$. So $q \nmid_H a$, and by symmetry $q \nmid_H b$. ✓

In both cases $q$ is not a prime element of $H$. $\blacksquare$

---

### Part (3): $H$ is atomic.

Let $h \in H \setminus \{1\}$. We must write $h$ as a finite product of atoms of $H$.

**Step 1: Standard prime factorization of $h$.**

Since $h \geq 5$ is a positive integer, factor it in $\mathbb{Z}$:
$$h = p_1^{a_1} \cdots p_s^{a_s} \cdot q_1^{b_1} \cdots q_t^{b_t},$$
where each $p_i \equiv 1 \pmod 4$ and each $q_j \equiv 3 \pmod 4$ are standard primes.

Since $h \equiv 1 \pmod{4}$, the total number of standard prime factors congruent to $3 \pmod{4}$, counted with multiplicity, must be **even**.

Indeed, each such prime contributes a factor $\equiv 3 \pmod 4$, and $3^k \equiv 1 \pmod 4$ if and only if $k$ is even. Hence $\sum_j b_j$ is even. (Note: individual $b_j$ may be odd; only the total needs to be even.)

**Step 2: Atoms of $H$.**

- Each $p_i$ is an atom of $H$: $p_i \in H$ (since $p_i \equiv 1 \pmod 4$), and if $p_i = xy$ in $H$ then $x \mid p_i$ in $\mathbb{Z}$, so $x \in \{1, p_i\}$, both in $H$. ✓
- For primes $q_j \equiv 3 \pmod 4$: we will group them into pairs. Each pair $q_i q_k$ (with $q_i \equiv q_k \equiv 3 \pmod 4$) is an atom of $H$ by Part (2), and lies in $H$ since $q_i q_k \equiv 1 \pmod 4$. ✓

**Step 3: Writing $h$ as a product of atoms.**

List all prime factors of $h$ that are $\equiv 3 \pmod 4$, with multiplicity: this gives a list $r_1, r_2, \ldots, r_{2m}$ of $\sum_j b_j = 2m$ primes (an even count). Pair them consecutively: $(r_1 r_2), (r_3 r_4), \ldots, (r_{2m-1} r_{2m})$. Each pair $r_{2i-1} r_{2i}$ is an atom of $H$ by Part (2).

Together with the $\sum_i a_i$ copies of the atoms $p_1, \ldots, p_s$, we obtain:
$$h = \underbrace{p_1 \cdots p_1}_{a_1} \cdots \underbrace{p_s \cdots p_s}_{a_s} \cdot (r_1 r_2) \cdots (r_{2m-1} r_{2m}),$$
a finite product of atoms of $H$.

Therefore every $h \in H \setminus \{1\}$ is a product of atoms, so $H$ is atomic. $\blacksquare$

---

## Notes

Part (2) is the heart of the exercise: it shows atoms and primes genuinely differ in $H$. The factorization $441 = 9 \times 49 = 21 \times 21$ (with $9, 49, 21 \in H$) is the canonical illustration — both $9 = 3^2$ and $49 = 7^2$ are atoms that fail to be prime, since neither divides $21$ inside $H$.

What makes $H$ unusual is that the factorization into atoms is not unique (it fails to be a UFM), yet atoms still exist in abundance. The reason primes $\equiv 3 \pmod 4$ "disappear" from $H$ — they are not elements of $H$ — is precisely what allows atoms like $q_1 q_2$ to be irreducible inside $H$ while not being prime.

For Part (3), the key insight is that the standard prime factorization in $\mathbb{Z}$ transfers to an atomic factorization in $H$ once you recognize that primes $\equiv 3 \pmod 4$ must appear an even number of times (forced by $h \equiv 1 \pmod 4$), allowing them to be paired into atoms.
