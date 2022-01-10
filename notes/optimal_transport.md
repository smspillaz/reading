# Optimal Transport

Motivation: moving mass from distribution a to distribution b - what sort of "plan" optimizes the cost of this?

## Kantorovitch - Discrete OT

$$
\alpha = \sum^n a_i \delta_{x_i}
$$

$$
\beta = \sum^m b_j \delta_{y_j}
$$

We have some points $x_i$ and $y_j$

Weights $a_i \ge 0$ and $b_j \ge 0$

![[ot_plan_simple.png]]

Constraint for conservation of mass: $\sum^n a_i = \sum^m b_j = 1$

The optimal transport is the one that miniimizes the cost.

$$
\min {\sum_{i, j}} d(x_i, y_j)^p P_{i, j}
$$
where $P \in U(a, b)$ and $U(a, b) = P \in \mathbb{R}^{n \times m}; P \mathbb{1}_m = a, P^T \mathbb{1}_n = b$

You can replace everything by arbitrary densities. Just replace discrete couplings by continuous couplings.

$$
W_p(\alpha, \beta)^p = \min_{\pi \in \mathcal{M}^1_{+} (\mathcal{X}^2)} \int_{\mathcal{X}^2} d(x, y)^p d \pi (x, y); \pi_1 = \alpha, \pi_2 = \beta
$$

$$W_p$$ is a distance, 0 iff two point clouds are equal.

## Simplification of the problem - Entropy regularization

$$\min_{P \in U(a, b)} \sum_{i, j} d(x_i, y_i)^p P_{i, j} + \epsilon P_{i, j} \log (\frac{P_{i, j}}{a_i b_j})$$

$\epsilon$-penalty introduced for relatively entropy. As $\epsilon$ goes to zero, then you have the optimal transport. Optimal transport is equal to the optimal matching of Monge, solution is a bijection. As the temperature increases you get some diffusion, this makes the algorithm a little more stable in high dimensions.

As you increase $\epsilon$ the solution is more and more blurry, and in the limit you transport mass from everyone to everyone.

## Sinkhorn's Algorithm

Proposion: $P_{i, j} = u_i K_{i, j} v_j$ where $K_{i, j} = e^{-\frac{d(x_i, y_j)^p}{\epsilon}}$

This is like a maximum entropy method. Being a solution to this problem means that you should be able to factor it using a gibbs kernel. You should be able to factor your coupling using a Gaussian blurring. Instead of having to look for a big matrix, you just look for two vectors, just solve for the conservation of mass.

You just need to solve:

$$
u * (Kv) = a
$$

$$
v * (K^Tu) = b
$$

Note that the two depend on each other. Sinkhorn iterations: $u = \frac{a}{Kv}$, $v = \frac{b}{K^T u}$

Just iterate between the two and it converges.

## What can we do with sinkhorn divergence?

The problem is that once you add entropy, this is no longer a distance function anymore. As $\epsilon$ goes to $\inf$, you converge to a single dirac.

Simple hack to fix this problem: Remove the diagonal parts. Eg, subtract $\frac{1}{2} W^p_{p, \epsilon} (\alpha, \alpha) - \frac{1}{2} W^p_{p, \epsilon} (\beta, \beta)$


## For matching

Consider word vectors $w$ and image patch vectors $v$. We want to learn a plan $T \in \mathbb{R}^{T \times K}$ to optimize the alignment.

$(w, v)$ given by distributions $\mu$, $\nu$ where $\mu = \sum^T a_i \delta_{w_i}$ and $v = \sum^K b_j \delta_{v_j}$.

Say further that weights $a \in \mathbb{R}^T$ and $b \in \mathbb{R}^K$ and both weights have a sum of 1, as both $\mu$ and $\nu$ are probability distributions.

Then the optimal transport distance is:

$$
\mathcal{L}_{text{WRA}}(\theta) = \mathcal{D}_{ot} (\mu, \nu) = \min_{T \in \prod (a, b)} \sum^T \sum^K T_{ij} \cdot c(w_i, v_j)
$$

Note: This is the optimal transport plan multiplied with the cosine similarities, elementwise.

where $\prod(a, b) = \{T \in R^{T \times K} | T \mathbb{1}_m = a, T^T \mathbb{1}_n = b \}$.

Then $c(w_i, v_j) = 1 - \frac{w_i^T v_j}{||w_i||_2 ||v_j||_2}$

Solving T is sort of hard, use the IPOT algorithm.

IPOT algorithm:
 - Take $C_{ij}$ as cosine distance matrix, words and image patches.
 - Take $A_{ij}$ as $e^{-\frac{C_{ij}}{\beta}}$
 - Initialize $T$ as ones.
 - Iteratively:
	 - Compute $A * T$
	 - Compute diracs as $\delta = \frac{1}{nQ \sigma}$
	 - Re-compute $\sigma = \frac{1}{mQ%T \delta$
	 - $T = \text{diag}(\delta)Q\text{diag}(\sigma}$



