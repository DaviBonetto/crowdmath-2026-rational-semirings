# Exercise 0.6

## Status

Solved offline. Posted on AoPS.

## Restatement

Prove that a monoid $M$ is cancellative if and only if it is isomorphic to a submonoid of a group.

## Definitions Used

- **Cancellative monoid:** A monoid $M$ in which both left and right cancellation hold, i.e., for all $a, b, c \in M$: $ab = ac \implies b = c$ and $ba = ca \implies b = c$.

- **Submonoid of a group:** A subset of a group that contains the identity and is closed under the group operation, viewed as a monoid in its own right.

- **Monoid isomorphism:** A monoid homomorphism that is also a bijection (with a homomorphism inverse).

- **Grothendieck group $\mathcal{G}(M)$:** Given a commutative cancellative monoid $M$, the abelian group formed by equivalence classes $a/b$ of pairs $(a,b) \in M \times M$ under the relation $(a,b) \sim (c,d) \iff ad = bc$, with operation $(a/b)\cdot(c/d) = ac/bd$ and identity $e_M/e_M$.

- **Canonical embedding:** The monoid homomorphism $i : M \to \mathcal{G}(M)$ defined by $i(a) = a/e_M$.

## Proof

We prove both directions of the biconditional.

---

### ($\Leftarrow$) If $M$ is isomorphic to a submonoid of a group, then $M$ is cancellative.

Let $G$ be a group and $S \leq G$ a submonoid with $M \cong S$ via some monoid isomorphism $\varphi : M \xrightarrow{\sim} S$.

**Step 1: Every submonoid of a group is cancellative.**

Since $G$ is a group, every element of $G$ is a unit, hence cancellative. In particular, every element of $S \subseteq G$ is cancellative in $G$. Since the operation on $S$ is inherited from $G$, $S$ is cancellative as a monoid.

**Step 2: Cancellativity is preserved under isomorphisms.**

By the proposition in Resource 0, if $\varphi : M \to S$ is a monoid isomorphism and $S$ is cancellative, then $M$ is cancellative. (Concretely: suppose $ab = ac$ in $M$. Applying $\varphi$, we get $\varphi(a)\varphi(b) = \varphi(a)\varphi(c)$ in $S$. By cancellativity of $S$, $\varphi(b) = \varphi(c)$. By injectivity of $\varphi$, $b = c$. The right cancellation argument is symmetric.)

Hence $M$ is cancellative. $\square$

---

### ($\Rightarrow$) If $M$ is cancellative, then $M$ is isomorphic to a submonoid of a group.

Assume first that $M$ is commutative (the general case is addressed in the Notes). We use the Grothendieck group construction from Resource 0.

**Step 1: Construct $\mathcal{G}(M)$.**

Since $M$ is a commutative cancellative monoid, we form the Grothendieck group $\mathcal{G}(M)$, whose elements are equivalence classes $a/b$ for $(a,b) \in M \times M$ under

$$
(a,b) \sim (c,d) \iff ad = bc.
$$

With the operation $(a/b) \cdot (c/d) = ac/bd$, identity $e_M/e_M$, and inverses $(a/b)^{-1} = b/a$, the set $\mathcal{G}(M)$ is an abelian group.

**Step 2: The canonical embedding is an injective monoid homomorphism.**

Define $i : M \to \mathcal{G}(M)$ by $i(a) = a/e_M$. We verify:

- _Homomorphism:_ $i(ab) = ab/e_M = (a/e_M)(b/e_M) = i(a)\,i(b)$, and $i(e_M) = e_M/e_M$, the identity of $\mathcal{G}(M)$.

- _Injectivity:_ If $i(a) = i(b)$, then $a/e_M = b/e_M$, so $(a, e_M) \sim (b, e_M)$, which means $a \cdot e_M = b \cdot e_M$, i.e., $a = b$. The cancellativity assumption is part of the Grothendieck group construction used in Resource 0; in this particular injectivity check, the equality reduces directly to $a = b$.

**Step 3: $i(M)$ is a submonoid of $\mathcal{G}(M)$ isomorphic to $M$.**

The image $i(M) = \{ a/e_M : a \in M \}$ is a submonoid of $\mathcal{G}(M)$: it contains the identity $e_M/e_M = i(e_M)$ and is closed under the operation since $i(a)\,i(b) = i(ab) \in i(M)$. Since $i$ is an injective homomorphism onto $i(M)$, it is a monoid isomorphism $M \xrightarrow{\sim} i(M)$.

Therefore $M$ is isomorphic to $i(M)$, a submonoid of the group $\mathcal{G}(M)$. $\square$

---

**Conclusion.**

A monoid $M$ is cancellative if and only if it is isomorphic to a submonoid of a group. $\blacksquare$

## Notes

- The ($\Leftarrow$) direction requires no commutativity assumption and works for all monoids.

- The ($\Rightarrow$) direction above is written for the commutative setting, which is the setting of Resource 0 and the Grothendieck group construction used there. In the non-commutative setting, cancellativity alone is not generally enough to guarantee an embedding into a group; additional hypotheses are needed. Therefore, this proof should be read in the commutative context of the resource.

- The proposition in Resource 0 states the ($\Leftarrow$) direction explicitly: "the property of being cancellative is preserved under isomorphisms," so that direction can also be cited directly.

- Example 14 in Resource 0 illustrates the construction concretely: $\mathcal{G}(\mathbb{N}_0) = \mathbb{Z}$, and $i(\mathbb{N}_0) = \{n/0 : n \in \mathbb{N}_0\}$, which corresponds to $\mathbb{N}_0$ sitting inside $\mathbb{Z}$ as a submonoid.
