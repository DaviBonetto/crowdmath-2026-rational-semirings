# Exercise 0.5

## Status

Solved offline. Posted on AoPS.

## Restatement

Let $M$ be a cancellative monoid. Prove that if $M$ has only finitely many elements, then $M$ is a group.

## Definitions Used

- **Cancellative monoid:** A monoid $M$ in which the cancellation laws hold on both sides, i.e., for all $a, b, c \in M$:
  - _Left cancellation:_ $ab = ac \implies b = c$,
  - _Right cancellation:_ $ba = ca \implies b = c$.

- **Group:** A monoid in which every element has a two-sided inverse.

- **Left multiplication map:** For a fixed $a \in M$, the map $\lambda_a : M \to M$ defined by $\lambda_a(x) = ax$.

- **Right multiplication map:** For a fixed $a \in M$, the map $\rho_a : M \to M$ defined by $\rho_a(x) = xa$.

## Proof

Since $M$ is a monoid, it has an identity element $e_M$. It remains to show that every element of $M$ has a two-sided inverse inside $M$.

Let $a \in M$ be arbitrary. We will find an element $b \in M$ satisfying $ab = ba = e_M$.

---

**Step 1: $\lambda_a$ and $\rho_a$ are injective.**

Suppose $\lambda_a(x) = \lambda_a(y)$, i.e., $ax = ay$. By left cancellation in $M$, we conclude $x = y$. Hence $\lambda_a$ is injective.

Suppose $\rho_a(x) = \rho_a(y)$, i.e., $xa = ya$. By right cancellation in $M$, we conclude $x = y$. Hence $\rho_a$ is injective.

---

**Step 2: $\lambda_a$ and $\rho_a$ are surjective.**

Since $M$ is finite, any injective map from $M$ to itself must also be surjective (by the pigeonhole principle). Therefore, both $\lambda_a : M \to M$ and $\rho_a : M \to M$ are bijections.

---

**Step 3: $a$ has a right inverse and a left inverse in $M$.**

Since $\lambda_a$ is surjective, there exists $b \in M$ such that $\lambda_a(b) = e_M$, i.e.,

$$
ab = e_M.
$$

Since $\rho_a$ is surjective, there exists $c \in M$ such that $\rho_a(c) = e_M$, i.e.,

$$
ca = e_M.
$$

---

**Step 4: The right and left inverses coincide.**

Using associativity and the two equations above:

$$
c = c \cdot e_M = c(ab) = (ca)b = e_M \cdot b = b.
$$

Hence $b = c$, and we conclude:

$$
ab = e_M \quad \text{and} \quad ba = e_M.
$$

Therefore $b$ is the two-sided inverse of $a$ in $M$.

---

**Conclusion.**

Since $a \in M$ was arbitrary, every element of $M$ has a two-sided inverse. Combined with the fact that $M$ is already a monoid (associativity and identity), we conclude that $M$ is a group. $\blacksquare$

## Notes

- The finiteness hypothesis is essential. The additive monoid $\mathbb{N}_0$ is cancellative but infinite, and it is not a group (no element other than $0$ has an additive inverse in $\mathbb{N}_0$).

- The core of the argument is the classical fact that an injective map from a finite set to itself is automatically a bijection (pigeonhole principle). Cancellativity is precisely what guarantees the injectivity of the multiplication maps.

- This result is a special case of a broader phenomenon: a finite cancellative monoid behaves like a finite group. In fact, the Cayley table of such a monoid forms a Latin square, which is another way to see that every element must be invertible.

- The proof works for non-commutative monoids without any modification, since we used both left and right cancellation separately.
