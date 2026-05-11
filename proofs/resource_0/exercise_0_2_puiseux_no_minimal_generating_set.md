# Exercise 0.2

## Status

Solved Offline.

## Restatement

Prove that the Puiseux monoid $\mathbb{Q}_{\geq 0}$ (the additive monoid of non-negative rationals) has no minimal generating set.

## Definitions Used

- **Generating set:** A subset $S \subseteq M$ of a monoid $M$ such that $\langle S \rangle = M$, i.e., every element of $M$ can be written as a finite sum of elements of $S$.

- **Minimal generating set:** A generating set $S$ such that no proper subset of $S$ is still a generating set. Equivalently, for every $s \in S$, the element $s$ cannot be expressed as a finite sum of elements in $S \setminus \{s\}$; i.e., $s \notin \langle S \setminus \{s\} \rangle$.

- **Puiseux monoid $\mathbb{Q}_{\geq 0}$:** The set of all non-negative rational numbers under addition.

## Proof

We show that no generating set of $\mathbb{Q}_{\geq 0}$ can be minimal, by proving that every element of every generating set is redundant.

Let $S$ be any generating set of $\mathbb{Q}_{\geq 0}$. We will show that for every $s \in S$, we have $s \in \langle S \setminus \{s\} \rangle$, which means $S$ is not minimal.

**Case $s = 0$.**
The element $0$ is the identity of $\mathbb{Q}_{\geq 0}$, so $0$ is always the empty sum and belongs to $\langle S \setminus \{0\} \rangle$ regardless of what $S \setminus \{0\}$ contains.

**Case $s > 0$.**
Consider the element $s/2 \in \mathbb{Q}_{\geq 0}$. Since $S$ generates $\mathbb{Q}_{\geq 0}$, there exist elements $q_1, \ldots, q_k \in S$ (not necessarily distinct) such that

$$
\frac{s}{2} = q_1 + q_2 + \cdots + q_k.
$$

Since each $q_i \geq 0$ and their sum equals $s/2$, each $q_i$ satisfies

$$
0 \leq q_i \leq \frac{s}{2} < s.
$$

In particular, $q_i \neq s$ for all $i$. Therefore every $q_i$ belongs to $S \setminus \{s\}$, which gives

$$
\frac{s}{2} \in \langle S \setminus \{s\} \rangle.
$$

Consequently,

$$
s = \frac{s}{2} + \frac{s}{2} \in \langle S \setminus \{s\} \rangle.
$$

**Conclusion.**
In both cases, $s \in \langle S \setminus \{s\} \rangle$. Since $s \in S$ was arbitrary, every element of $S$ can be expressed using the remaining elements, so $S$ is not minimal.

Since $S$ was an arbitrary generating set of $\mathbb{Q}_{\geq 0}$, no generating set of $\mathbb{Q}_{\geq 0}$ is minimal. $\blacksquare$

## Notes

- The key property exploited here is that $\mathbb{Q}_{\geq 0}$ is **divisible**: for every $q \in \mathbb{Q}_{\geq 0}$ and every positive integer $n$, the element $q/n$ also belongs to $\mathbb{Q}_{\geq 0}$. Divisibility forces every element to be a sum of strictly smaller elements of the monoid, which is precisely what makes minimality impossible.

- The same argument shows that any divisible submonoid of $(\mathbb{Q}_{\geq 0}, +)$ — such as $\mathbb{Q}_{\geq 0}$ itself or $\{r \in \mathbb{Q}_{\geq 0} : r \geq 0\}$ — has no minimal generating set.

- This contrasts sharply with numerical monoids $N \subseteq \mathbb{N}_0$, which always admit a unique minimal generating set (sometimes called the **atoms** or **irreducibles** of $N$). The difference comes from the fact that $\mathbb{N}_0$ is not divisible: for example, $1/2 \notin \mathbb{N}_0$.

- The argument is purely order-theoretic: it uses only that every positive element has a "half" strictly between $0$ and itself that is still in the monoid. No specific properties of $\mathbb{Q}$ beyond this are needed.
