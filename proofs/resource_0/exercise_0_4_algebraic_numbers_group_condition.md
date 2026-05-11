# Exercise 0.4

## Status

Solved Offline.

---

## Restatement

Let $\alpha$ be an algebraic number. We want to show that $\mathbb{N}_0[\alpha]$ (the additive monoid of all polynomial evaluations at $\alpha$ with non-negative integer coefficients) is a group under addition if and only if no conjugate of $\alpha$ is a positive real number.

Throughout the proof, we assume $\alpha \neq 0$. If $\alpha = 0$, then $\mathbb{N}_0[\alpha] = \mathbb{N}_0$, which is not a group, while $0$ has no positive conjugate. Thus, as stated with "positive" rather than "nonnegative," the exercise requires this nonzero assumption or a separate clarification of the degenerate case.

---

## Definitions Used

- **$\mathbb{N}_0[\alpha]$**. The set $\left\{\sum_{i=0}^n a_i \alpha^i : n \in \mathbb{N}_0,\, a_i \in \mathbb{N}_0\right\}$. This is a submonoid of $(\mathbb{C}, +)$, and also closed under multiplication (since the product of two polynomials with non-negative integer coefficients again has non-negative integer coefficients).
- **Minimal polynomial.** The monic polynomial $m(x) \in \mathbb{Q}[x]$ of smallest degree with $m(\alpha) = 0$. It is irreducible over $\mathbb{Q}$.
- **Conjugates of $\alpha$.** All roots of $m(x)$ in $\mathbb{C}$, including $\alpha$ itself.

---

## Proof

The key observation is that $\mathbb{N}_0[\alpha]$ is a group if and only if $-1 \in \mathbb{N}_0[\alpha]$.

**Why this is enough.** Since $\mathbb{N}_0[\alpha]$ is closed under multiplication, if $-1 = h(\alpha)$ for some $h \in \mathbb{N}_0[x]$, then for any $p(\alpha) \in \mathbb{N}_0[\alpha]$, the additive inverse $-p(\alpha) = h(\alpha) \cdot p(\alpha) = (h \cdot p)(\alpha)$ also belongs to $\mathbb{N}_0[\alpha]$ (because $h \cdot p \in \mathbb{N}_0[x]$). Conversely, if $\mathbb{N}_0[\alpha]$ is a group, then $1 \in \mathbb{N}_0[\alpha]$ must have an additive inverse, so $-1 \in \mathbb{N}_0[\alpha]$.

Now, $-1 \in \mathbb{N}_0[\alpha]$ is equivalent to: there exists $f \in \mathbb{N}_0[x]$ with $f(\alpha) = 0$ and $f(0) \geq 1$.

Indeed, if $h(\alpha) = -1$ with $h \in \mathbb{N}_0[x]$, set $f(x) = h(x) + 1 \in \mathbb{N}_0[x]$; then $f(\alpha) = 0$ and $f(0) = h(0) + 1 \geq 1$. Conversely, if $f(\alpha) = 0$ with $f \in \mathbb{N}_0[x]$ and $f(0) \geq 1$, set $h(x) = f(x) - 1$; then $h \in \mathbb{N}_0[x]$ (since the constant term drops from $f(0) \geq 1$ to $f(0) - 1 \geq 0$) and $h(\alpha) = -1$.

So we need to prove: **$\alpha$ has no positive conjugate if and only if $\alpha$ is a root of some $f \in \mathbb{N}_0[x]$ with $f(0) > 0$.**

---

### ($\Rightarrow$) If $\mathbb{N}_0[\alpha]$ is a group, then $\alpha$ has no positive conjugate

Suppose for contradiction that $\alpha$ has a positive conjugate $\beta > 0$ (possibly $\beta = \alpha$).

Since $\mathbb{N}_0[\alpha]$ is a group, $-1 \in \mathbb{N}_0[\alpha]$, so there exists $f \in \mathbb{N}_0[x]$ with $f(\alpha) = 0$ and $f(0) > 0$.

Since $\beta$ is a conjugate of $\alpha$, the minimal polynomial $m(x)$ divides $f(x)$ in $\mathbb{Q}[x]$ (because $f(\alpha) = 0$ and $m$ is irreducible). Hence $f(\beta) = 0$.

But $f(x) = c_n x^n + \cdots + c_1 x + c_0$ with all $c_i \geq 0$ and $c_0 \geq 1$. Since $\beta > 0$:

$$f(\beta) = c_n \beta^n + \cdots + c_1 \beta + c_0 \geq c_0 \geq 1 > 0.$$

This contradicts $f(\beta) = 0$. $\square$

---

### ($\Leftarrow$) If $\alpha$ has no positive conjugate, then $\mathbb{N}_0[\alpha]$ is a group

Let $m(x) \in \mathbb{Q}[x]$ be the monic minimal polynomial of $\alpha$ over $\mathbb{Q}$, of degree $d$. None of the roots of $m$ lie in $(0, \infty)$.

**Step 1 — $m(x) > 0$ for all $x \geq 0$.**

Since $\alpha \neq 0$, we have $m(0) \neq 0$. By hypothesis, $m$ has no positive real root. Therefore $m$ has no root in $[0, \infty)$.

Because $m$ is monic, $m(x) \to +\infty$ as $x \to +\infty$. Since $m$ is continuous and has no zero on $[0, \infty)$, its sign is constant on $[0, \infty)$. Hence $m(x) > 0$ for all $x \geq 0$.

**Step 2 — Multiplying by $(1 + x)^N$ to clear negative coefficients.**

We use the following classical result:

> **Pólya's Theorem (one-variable version).** If $p(x) \in \mathbb{R}[x]$ satisfies $p(x) > 0$ for all $x \geq 0$, then there exists $N \in \mathbb{N}_0$ such that $(1 + x)^N p(x)$ has all non-negative coefficients.

Since $m(x) > 0$ for all $x \geq 0$, Pólya's theorem gives $N \in \mathbb{N}_0$ such that $(1 + x)^N m(x)$ has nonnegative rational coefficients. Multiplying by a sufficiently large positive integer $D$, we obtain

$$f(x) := D(1 + x)^N \, m(x) \in \mathbb{N}_0[x].$$

**Step 3 — $f$ does the job.**

- $f(\alpha) = (1 + \alpha)^N \cdot m(\alpha) = (1 + \alpha)^N \cdot 0 = 0$.
- $f(0) = D \cdot 1^N \cdot m(0) = Dm(0) > 0$ because $D > 0$ and $m(0) > 0$.
- $f \in \mathbb{N}_0[x]$ (from Step 2).

By the equivalence established above, $-1 \in \mathbb{N}_0[\alpha]$, so $\mathbb{N}_0[\alpha]$ is a group. $\square$

---

## Notes

- The multiplicative closure of $\mathbb{N}_0[\alpha]$ is what makes the whole argument work: once you have $-1 = h(\alpha)$ in the monoid, you can negate anything by multiplying by $h(\alpha)$. Without this, having $-1$ in an additive monoid wouldn't help.

- The ($\Rightarrow$) direction is very clean: a polynomial with non-negative coefficients and positive constant term can't vanish at a positive real number. That's basically the entire argument.

- Pólya's theorem is the heavy-lifting tool for ($\Leftarrow$). The intuition: multiplying by $(1+x)^N$ "smears out" the coefficients. For large $N$, the binomial coefficients grow fast enough to absorb any finite number of negative coefficients in $m(x)$.

- The $\alpha = 0$ edge case is discussed at the beginning of the proof.

- Examples: $\alpha = -1$ gives $\mathbb{N}_0[-1] = \mathbb{Z}$ (group ✓, no positive conjugate ✓). $\alpha = i$ gives $\mathbb{N}_0[i] = \mathbb{Z}[i]$ (group ✓, conjugates $\pm i$ not positive ✓). $\alpha = 2$ gives $\mathbb{N}_0[2] = \mathbb{N}_0$ (not a group ✓, conjugate $2 > 0$ ✓).

- There's a nice way to see why $\mathbb{N}_0[i] = \mathbb{Z}[i]$: since $i^2 = -1$, we have $-1 \in \mathbb{N}_0[i]$ directly (take $h(x) = x^2$), and then $-\alpha = (-1)\cdot\alpha$ for any $\alpha \in \mathbb{N}_0[i]$.
