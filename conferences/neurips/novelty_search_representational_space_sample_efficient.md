# Novelty Search in the Representational Space for Sample Efficient Exploration

Basic idea: create intrinsic rewards from low-dimensional representational state space learned from information theoretic principles.

How to explore large state spaces?

 - Count them?
 - Most states have a count of 1 or 0
 - Some states should be counted together
 - Frame-stacking exacerbates this

We need *state abstraction* and *density estimation*.

 - State abstraction: Group states together, so they're more meaningful
	 - Random Network Distillation (Burda) (state abstraction)
		 - Fixed random RNN used as target
		 - Largely affected by pixel similarity
 - Pseudo-counts (Bellemare et al) (density estimation)
	 - estimate a probability density from data
	 - estimate a density of counts given a state


## State abstraction

Information Bottleneck: Compress $X$ to preserve relevant information on relevance variable $Y$:

$L(p(\tilde z|z)) = I[S"|X'] - \beta I[X';\{X, A\}]$

the first term is the encoding rate, the second term is the dynamic model's "predictive ability"

S' is the source message
X' is the encoded state
X is the encoded prev state
A is the action
$\{X, A\}$ is the encoded state/action pair (relevance variable)

We're trying to preserve all the relevant information of our state with respect to the previous tate and action.

Minimizing the encoding rate reduces the representation size - minimize the amount of unnecessary information preserved.

Maximize the dynamics model's predictive power.

Effectively, this is the difference between the entropy of our current state and the entropy of our current state given the previous state and action:

$$
H[X'] - H[X' | X, A]
$$

To do this, minimize entropy of encoding, maximize uncertainty of next state (dynamics loss)


## Tests

4-rooms: encoding trajectories - minimizing the IB function corresponds to relative co-ordinates

Multi-step maze: You have to grab a key that opens the door to the reward.

![[novelty_search_multi_step_maze.png.png]]

You get relative dimensions + whether or not the agent has picked up the key on the third dimension.

You generalize as seen in the overlap.

With these learnt low-dim representations how can you explore.

## Novelty search

$\hat \rho_X(x) = \frac{1}{k} \sum^k_{i  = 1} d(x, x_i)$

A state is considered novel if it is away from its k-nearest neighbours.

Density estimation - this is proportional to counts.

But the problem is that distances are unbounded. How can you ensure that the distance is constrained? Unbounded distances imply unbounded intrinsic rewards. You will get divergent action-values during training.

## Consecutive distance constraint

$L_{\text{csc}}(\theta_{\hat e}) = \max(||\hat e(s_1; \theta_e) - \hat e(s_2;\theta_e||_2 - \omega), 0)$

$\omega$ corresponds to the max consecutive L2 distance.

We allow consecutive states to only be a certain distance away from each other (bounded by $\omega$). Anything more and you're capped at $\omega$(?)


