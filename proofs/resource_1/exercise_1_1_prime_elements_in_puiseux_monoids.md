# Exercise 1.1

## Status

Solved Offline.

---

## Restatement

Let $M$ be a Puiseux monoid (an additive submonoid of $(\mathbb{Q}_{\geq 0}, +)$). We want to show that $M$ contains a prime element if and only if $M = \mathbb{N}_0 q$ for some $q \in \mathbb{Q}_{>0}$, in which case $q$ is the unique prime of $M$.

---

## Definitions Used

- **Puiseux monoid:** An additive submonoid of $(\mathbb{Q}_{\geq 0}, +)$.
- **Divisibility in $M$:** For $a, b \in M$, we say $a \mid b$ if there exists $c \in M$ such that $b = a + c$.
- **Prime element:** A nonzero element $p \in M$ such that for all $a, b \in M$, $p \mid (a + b)$ implies $p \mid a$ or $p \mid b$.
- **$\mathbb{N}_0 q$:** The submonoid $\{nq : n \in \mathbb{N}_0\} = \{0, q, 2q, 3q, \ldots\}$.

---

## Proof

### ($\Leftarrow$) If $M = \mathbb{N}_0 q$, then $q$ is the unique prime of $M$.

Write $M = \{0, q, 2q, 3q, \ldots\}$. For any $a = mq, b = nq \in M$, divisibility $q \mid a$ is equivalent to $a \geq q$, i.e., $m \geq 1$.

**$q$ is prime:** Suppose $q \mid (a + b) = (m+n)q$. Then $m + n \geq 1$, so $m \geq 1$ or $n \geq 1$, i.e., $q \mid a$ or $q \mid b$. ✓

**$q$ is the only prime:** Let $nq$ with $n \geq 2$. Take $a = q$ and $b = (n-1)q$; then $nq \mid a + b = nq$, but $nq \nmid a = q$ (since $q < nq$) and $nq \nmid b = (n-1)q$ (since $(n-1)q < nq$). So $nq$ is not prime. ✓

---

### ($\Rightarrow$) If $M$ contains a prime $p$, then $M = \mathbb{N}_0 p$ and $p$ is the only prime.

#### Preliminary Lemma: Primality propagates through sums.

**Lemma.** If $p \in M$ is prime and $p \mid (a_1 + \cdots + a_n)$ for $a_i \in M$, then $p \mid a_i$ for some $i$.

*Proof.* By induction on $n$. The base case $n = 1$ is trivial. For $n \geq 2$: $p \mid (a_1 + (a_2 + \cdots + a_n))$, so by the definition of prime, $p \mid a_1$ or $p \mid (a_2 + \cdots + a_n)$. Applying the induction hypothesis to the second case gives $p \mid a_i$ for some $i \geq 2$. In either case, some $a_i$ is divisible by $p$. $\square$

**Corollary.** If $p \mid nx$ for some $x \in M$ and $n \in \mathbb{N}$, then $p \mid x$.

*Proof.* Apply the Lemma to $a_1 = \cdots = a_n = x$. $\square$

---

#### Step 1: $p$ is the minimum positive element of $M$.

Suppose for contradiction that there exists $x \in M$ with $0 < x < p$.

Write $x/p = m/n \in \mathbb{Q}_{>0}$ in lowest terms. Then $nx = mp$, so $p \mid nx$ (since $nx = mp = p + (m-1)p \in M$ and $(m-1)p \in M$). By the Corollary, $p \mid x$, meaning there exists $c \in M$ with $x = p + c$.

But $M \subseteq \mathbb{Q}_{\geq 0}$, so $c = x - p \geq 0$, which forces $x \geq p$. This contradicts $x < p$.

Therefore, $M$ has no element strictly between $0$ and $p$. $\square$

---

#### Step 2: $p \mid x$ for every $x \in M$ with $x > 0$.

Let $x \in M$, $x > 0$. By Step 1, $x \geq p$. Write $x/p = m/n$ in lowest terms. Then $nx = mp$, so $p \mid nx$. By the Corollary, $p \mid x$, i.e., $x - p \in M$. $\square$

---

#### Step 3: Every positive element of $M$ lies in $\mathbb{N}_0 p$.

Let $x \in M$, $x > 0$. We show $x \in \mathbb{N}_0 p$ by descent.

Since $x$ and $p$ are positive rational numbers, there exists a unique integer $k \geq 0$ such that
$$0 \leq x - kp < p.$$

By the repeated application of Step 2, each positive remainder $x - jp$ (for $0 \leq j \leq k$) belongs to $M$ (starting from $x \in M$, Step 2 gives $x - p \in M$, then $x - 2p \in M$, and so on). Therefore $x - kp \in M$.

But Step 1 says $M$ has no element strictly between $0$ and $p$. Since $0 \leq x - kp < p$ and $x - kp \in M$, we must have $x - kp = 0$, and so $x = kp \in \mathbb{N}_0 p$. $\square$

---

#### Conclusion: $M = \mathbb{N}_0 p$.

- $\mathbb{N}_0 p \subseteq M$: since $p \in M$ and $M$ is closed under addition.
- $M \subseteq \mathbb{N}_0 p$: by Step 3, every positive element is a multiple of $p$, and $0 \in \mathbb{N}_0 p$.

Hence $M = \mathbb{N}_0 p$.

That $p$ is the unique prime of $M = \mathbb{N}_0 p$ was shown in the ($\Leftarrow$) direction. $\blacksquare$

---

## Notes

What surprised me about this proof was how much work the Corollary does. The argument "$p \mid nx \Rightarrow p \mid x$" is essentially the statement that in an additive monoid, primality behaves like it does in $\mathbb{Z}$ — but the proof here is elementary and doesn't require any ring structure.

The descent in Step 3 is satisfying: once you know $p$ is the minimum positive element and every element is divisible by $p$, the monoid has no room to be anything other than $\mathbb{N}_0 p$. The rational structure of a Puiseux monoid is what makes the descent terminate (a strictly decreasing sequence of non-negative rationals with steps of size $p > 0$ must be finite).

It's also worth noting that this gives a complete characterization: among all Puiseux monoids, exactly those of the form $\mathbb{N}_0 q$ — the "simplest" ones, isomorphic to $(\mathbb{N}_0, +)$ — admit a prime element.
