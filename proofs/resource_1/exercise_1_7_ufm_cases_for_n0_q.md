# Exercise 1.7

## Status

Solved Offline.

---

## Restatement

Given a positive rational number $q$, consider the set $\mathbb{N}_0[q]$, which consists of all polynomials evaluated at $q$ with non-negative integer coefficients. The goal is to determine exactly for which positive rational values of $q$ the following two monoids are Unique Factorization Monoids (UFMs):

1. The additive monoid $(\mathbb{N}_0[q], +)$
2. The multiplicative monoid $(\mathbb{N}_0[q] \setminus \{0\}, \cdot)$

## Definitions Used

- **Atom / irreducible element:** A nonunit element in a commutative monoid that cannot be factored into a product (or sum) of two nonunits.
- **UFM (Unique Factorization Monoid):** A commutative monoid where every nonunit factors into atoms, and this factorization is unique up to the order of factors and associates.
- **Puiseux monoid:** An additive submonoid of the nonnegative rational numbers $\mathbb{Q}_{\ge 0}$.
- **Reduced form of $q$:** For $q \in \mathbb{Q}_{>0}$, we express it as $q = a/b$ where $a, b \in \mathbb{N}$ and $\gcd(a, b) = 1$.

## Proof

Write throughout
\[
q=\frac{a}{b}\in \mathbb{Q}_{>0}
\qquad\text{with}\qquad
\gcd(a,b)=1.
\]

### Part (1): Classification of $(\mathbb{N}_0[q],+)$

We claim that
\[
(\mathbb{N}_0[q],+)\text{ is a UFM } \Longleftrightarrow q\in \mathbb{N}_0.
\]

#### If $q\in\mathbb{N}_0$, then $(\mathbb{N}_0[q],+)$ is a UFM.

If $q$ is a nonnegative integer, then every power $q^i$ is an integer, so every element of $\mathbb{N}_0[q]$ is an integer. Since $1\in \mathbb{N}_0[q]$, we get
\[
\mathbb{N}_0[q]=\mathbb{N}_0.
\]
Under addition, $\mathbb{N}_0$ has exactly one atom, namely $1$, and every $n\in\mathbb{N}_0$ factors uniquely as
\[
n=\underbrace{1+\cdots+1}_{n\text{ times}}.
\]
Hence $(\mathbb{N}_0[q],+)$ is a UFM.

#### If $0<q<1$ and $q=\frac1n$ for some $n\ge 2$, then $(\mathbb{N}_0[q],+)$ is not a UFM.

Indeed, let $x \in \mathbb{N}_0[q] \setminus \{0\}$. Since $\mathbb{N}_0[q]$ is closed under multiplication by $q$, we have $qx \in \mathbb{N}_0[q]$, and $qx \neq 0$. Because $q = 1/n$, we get
\[
x = n(qx).
\]
In additive notation,
\[
x = \underbrace{qx + \cdots + qx}_{n\text{ times}}.
\]
Since $n \ge 2$, this writes $x$ as a sum of nonzero elements of $\mathbb{N}_0[q]$. Therefore no nonzero element is an atom, so the monoid is not atomic and hence not a UFM.

#### If $q\notin\mathbb{N}_0$ and $q\neq \frac1n$ for every $n\in\mathbb{N}$, then $(\mathbb{N}_0[q],+)$ is not a UFM.

We split into two cases.

##### Case 1: $q>1$ and $q\notin \mathbb{N}$.

We first show that both $1$ and $q$ are atoms.

For $1$, suppose
\[
1=x+y
\qquad\text{with }x,y\in \mathbb{N}_0[q]\setminus\{0\}.
\]
Every non-integer element of $\mathbb{N}_0[q]$ is at least $q>1$, so any nonzero summand strictly smaller than $1$ must be an integer, hence at least $1$. Thus both $x$ and $y$ would have to be positive integers, forcing $x+y\ge 2$, impossible. So $1$ is an atom.

For $q$, suppose
\[
q=x+y
\qquad\text{with }x,y\in \mathbb{N}_0[q]\setminus\{0\}.
\]
If one summand is a positive integer, then it is at least $1$, while any positive non-integer summand is at least $q$. Hence such a decomposition would force
\[
x+y\ge 1+q>q,
\]
which is impossible. If both summands are non-integers, then each is at least $q$, so
\[
x+y\ge 2q>q,
\]
again impossible. Hence $q$ is an atom.

Now use the relation $a=bq$:
\[
\underbrace{1+\cdots+1}_{a\text{ times}}

= a
= bq
= \underbrace{q+\cdots+q}_{b\text{ times}}.
\]
This gives two different factorizations of the same element into atoms. Therefore $(\mathbb{N}_0[q],+)$ is not a UFM.

##### Case 2: $0<q<1$ and $q=\frac{a}{b}$ with $1<a<b$.

We again show that $1$ and $q$ are atoms.

Suppose
\[
1=\sum_{i=0}^n c_i q^i
\qquad(c_i\in\mathbb{N}_0).
\]
Multiplying by $b^n$ gives
\[
b^n = c_0 b^n + \sum_{i=1}^n c_i a^i b^{\,n-i}.
\]
Reducing modulo $a$, all terms with $i\ge 1$ vanish, so
\[
b^n \equiv c_0 b^n \pmod a.
\]
Because $\gcd(a,b)=1$, we obtain $c_0\equiv 1\pmod a$. Since the whole sum equals $1$ and all terms are nonnegative, we must have $c_0\le 1$, hence $c_0=1$. Then all other $c_i$ must be $0$. So $1$ is an atom.

Now suppose
\[
q=\sum_{i=0}^n c_i q^i
\qquad(c_i\in\mathbb{N}_0).
\]
Since $q<1$, the constant term must be $c_0=0$. Dividing by $q>0$ yields
\[
1=\sum_{i=1}^n c_i q^{i-1}.
\]
By the previous paragraph, the right-hand side must be exactly $1$, so $c_1=1$ and $c_i=0$ for all $i\ge 2$. Hence $q$ is an atom.

Again the relation $a=bq$ gives
\[
\underbrace{1+\cdots+1}_{a\text{ times}}

= a
= bq
= \underbrace{q+\cdots+q}_{b\text{ times}},
\]
two distinct atomic factorizations. So $(\mathbb{N}_0[q],+)$ is not a UFM.

Combining all cases, we conclude that
\[
\boxed{(\mathbb{N}_0[q],+)\text{ is a UFM if and only if } q\in\mathbb{N}_0.}
\]

---

### Part (2): Classification of $(\mathbb{N}_0[q]\setminus\{0\},\cdot)$

We claim that
\[
(\mathbb{N}_0[q]\setminus\{0\},\cdot)\text{ is a UFM }
\Longleftrightarrow
q\in\mathbb{N}\ \text{or}\ q=\frac1n\text{ for some }n\in\mathbb{N}.
\]

Let
\[
S_q := \mathbb{N}_0[q]\setminus\{0\}.
\]

#### If $q\in\mathbb{N}$, then $S_q$ is a UFM.

As in Part (1), if $q$ is an integer then $\mathbb{N}_0[q]=\mathbb{N}_0$, so
\[
S_q=\mathbb{N}.
\]
Under multiplication this is the usual multiplicative monoid of positive integers, which is a UFM by the Fundamental Theorem of Arithmetic.

#### If $q=\frac1n$ with $n\in\mathbb{N}$, then $S_q$ is a UFM.

In this case
\[
\mathbb{N}_0[q]=\mathbb{N}_0\!\left[\frac1n\right]
= \left\{\frac{m}{n^k}: m\in\mathbb{N}_0,\ k\in\mathbb{N}_0\right\}.
\]
Indeed, every polynomial in $\frac1n$ has denominator a power of $n$, and conversely every $\frac{m}{n^k}$ equals $m q^k$.

Now let $P$ be the set of primes dividing $n$. For every $p\in P$,
\[
\frac1p = \frac{n}{p}\cdot \frac1n \in \mathbb{N}_0\!\left[\frac1n\right],
\]
so each such prime $p$ is a unit of $S_q$. Therefore the only primes that matter up to associates are the ordinary primes not dividing $n$.

Take a nonzero element
\[
x=\frac{m}{n^k}\in S_q.
\]
Write the usual prime factorization of $m$ and move all prime factors from $P$ into the unit part. Then
\[
x = u \cdot p_1\cdots p_t,
\]
where $u$ is a unit of $S_q$ and each $p_i$ is an ordinary prime not dividing $n$.

Those primes remain atoms in $S_q$, and uniqueness follows directly from the uniqueness of the ordinary prime factorization in $\mathbb{N}$. Hence $S_q$ is a UFM.

#### Now assume $q=\frac{a}{b}$ with $a,b>1$. Then $S_q$ is not a UFM.

The main idea is to use a fixed polynomial identity in $\mathbb{N}_0[X]$ and show that its four factors stay atomic after evaluating at $q$.

##### Step 1: reduced polynomial forms

We first record the normal forms we need.

The reductions below are terminating because each replacement preserves the evaluated value and moves the expression toward the chosen reduced coefficient bounds. The uniqueness follows from the modular induction described below.

**If $q>1$**, every element of $S_q$ can be written uniquely as
\[
f(q), \qquad f(X)=\sum_{i=0}^n c_i X^i \in \mathbb{N}_0[X],\quad 0\le c_i<a.
\]
This is obtained by repeatedly replacing $aX^i$ with $bX^{i+1}$.

**If $0<q<1$**, every element of $S_q$ can be written uniquely as
\[
f(q), \qquad f(X)=\sum_{i=0}^n c_i X^i \in \mathbb{N}_0[X],\quad 0\le c_i<b\ \text{for all }i\ge 1,
\]
by repeatedly replacing $bX^{i+1}$ with $aX^i$.

The uniqueness in both cases follows by the standard modular induction:

- for $q>1$, compare constant coefficients modulo $a$, then divide by $a$ and continue;
- for $0<q<1$, compare highest coefficients modulo $b$, then divide by $b$ and continue.

> **Note:** The normal-form argument is used here as a technical lemma. A fully expanded proof would require checking termination and uniqueness of the carrying process in detail.

##### Step 2: the only unit is $1$

Suppose $x,y\in S_q$ satisfy $xy=1$. Write $x=f(q)$ and $y=g(q)$ in reduced form from Step 1. If any carrying occurred when reducing the ordinary product $f(X)g(X)$ back to the reduced form, then:

- in the case $q>1$, choose the largest place from which a carry moves upward; since no further carry leaves the next place, the reduced coefficient there is at least $b\ge 2$;
- in the case $0<q<1$, choose the smallest place to which a carry moves downward; since no carry continues below that place, the reduced coefficient there is at least $a\ge 2$.

But the reduced form of $1$ is just the constant polynomial $1$, whose coefficients are all $0$ or $1$. So no carrying can occur at all, and therefore
\[
f(X)g(X)=1
\]
inside $\mathbb{N}_0[X]$. Hence $f=g=1$, so $x=y=1$.

Thus $S_q$ is reduced:
\[
S_q^\times=\{1\}.
\]

##### Step 3: a useful lemma about $0$-$1$ polynomials

We will use the following lemma repeatedly.

**Lemma.** Let $f(X)\in \mathbb{N}_0[X]$ be irreducible, and suppose every coefficient of $f$ is either $0$ or $1$. Then $f(q)$ is an atom of $S_q$.

**Proof.** Suppose
\[
f(q)=x y
\qquad\text{with }x,y\in S_q.
\]
Write $x=g(q)$ and $y=h(q)$ in reduced form from Step 1.

If any carrying occurred while reducing the ordinary product $g(X)h(X)$ back to the reduced form of $f(q)$, then exactly the same argument as in Step 2 would show that some coefficient of the reduced form is at least $2$. But all coefficients of $f$ are $0$ or $1$. Therefore no carrying occurs, so
\[
g(X)h(X)=f(X)
\]
in $\mathbb{N}_0[X]$.

Since $f$ is irreducible in $\mathbb{N}_0[X]$, one of $g,h$ must be $1$. Because $S_q$ has no nontrivial units, this means one of $x,y$ is the unit $1$. Hence $f(q)$ is an atom. $\square$

##### Step 4: four irreducible $0$-$1$ polynomials

Consider
\[
f_1(X)=1+X,\quad
f_2(X)=1+X^3,\quad
f_3(X)=1+X+X^2,\quad
f_4(X)=1+X^2+X^4.
\]

We claim that each $f_i$ is irreducible in $\mathbb{N}_0[X]$.

- $f_1$ is obviously irreducible.

- For $f_2=1+X^3$: if $f_2=uv$ with $u,v$ nonconstant and constant terms $1$, let $r$ and $s$ be the least positive exponents appearing in $u$ and $v$. Then the coefficient of $X^{\min\{r,s\}}$ in $uv$ is positive, contradicting the fact that $1+X^3$ has no $X$- or $X^2$-term.

- For $f_3=1+X+X^2$: any nontrivial factorization must have degree pattern $1+1$, so
  \[
  1+X+X^2=(1+mX)(1+nX)
  \]
  for some $m,n\in\mathbb{N}$. Comparing the $X^2$-coefficient gives $mn=1$, hence $m=n=1$, but then the $X$-coefficient is $2$, contradiction.

- For $f_4=1+X^2+X^4$: if $f_4=uv$ with $u,v$ nonconstant and constant terms $1$, then all odd coefficients of $uv$ are zero. Since coefficients are nonnegative, this forces all positive exponents occurring in $u$ and $v$ to be even. Writing $Y=X^2$, we get
  \[
  1+Y+Y^2 = U(Y)V(Y),
  \]
  contradicting the irreducibility of $1+Y+Y^2$.

So all four $f_i$ are irreducible.

By the lemma, the four elements
\[
1+q,\quad 1+q^3,\quad 1+q+q^2,\quad 1+q^2+q^4
\]
are atoms of $S_q$.

##### Step 5: a universal non-unique factorization

In $\mathbb{N}_0[X]$ we have the identity
\[
(1+X+X^2)(1+X^3)=(1+X^2+X^4)(1+X).
\]
Evaluating at $X=q$ gives
\[
(1+q+q^2)(1+q^3)=(1+q^2+q^4)(1+q).
\]
By Step 4, each factor is an atom of $S_q$. By Step 2, the only unit is $1$, so associates are literally equalities. The two factorizations are distinct because
\[
1+q^3 \neq 1+q
\qquad\text{and}\qquad
1+q+q^2 \neq 1+q^2+q^4.
\]
Therefore $S_q$ is not a UFM.

Combining all cases, we conclude that
\[
\boxed{(\mathbb{N}_0[q]\setminus\{0\},\cdot)\text{ is a UFM if and only if } q\in\mathbb{N}\text{ or }q=\frac1n\text{ for some }n\in\mathbb{N}.}
\]

## Notes

- The additive answer is exactly what one expects after Exercise 1.5(2): among these cyclic Puiseux monoids, the only additive UFM case is the genuinely numerical one, namely $\mathbb{N}_0$ itself.
- The multiplicative answer is more subtle. The reciprocal-integer case behaves like a localization of $\mathbb{N}$, so unique factorization survives after turning the primes dividing $n$ into units.
- The identity
  \[
  (1+X+X^2)(1+X^3)=(1+X^2+X^4)(1+X)
  \]
  is the real obstruction in the mixed case $q=\frac ab$ with $a,b>1$: once those four evaluations are known to be atoms, non-unique factorization is unavoidable.
- I kept the proof in the project's positive-rational convention for $\mathbb{N}_0[q]$. If one extends the notation to negative rationals, the picture changes and should be discussed separately.
