---
title: "Plannable Approximations to MDP Homomorphisms: Equivariance under Actions."
venue: "AAMAS"
pages: "1431-1439"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/atal/PolKOW20"
doi: "10.5555/3398761.3398926"
ee: "https://dl.acm.org/doi/10.5555/3398761.3398926"
url: "https://dblp.org/rec/conf/atal/PolKOW20"
authors: ["Elise van der Pol", "Thomas Kipf", "Frans A. Oliehoek", "Max Welling"]
sync_version: 3
cite_key: "conf/atal/PolKOW20"
---
# Plannable Approximatiosn to MDP Homomorphisms: Equivariance under Actions

tl;dr:
 - Symmetries may exist in MDPs
 - Introduces a contrastive loss function which enforces action equivariance on the learned representations
 - When the loss is zero, you have a homomorphism of a deterministic MDP


Equivalence classes: Is there some mapping that you can do of states and actions such that there is a symmetry, eg, taking a class of actions in a class of states and its the same as taking some other class of actions in some other class of states.

 - Basic idea: Use a neural network to map states to latent states, actions to latent actions
 - Should collapse according to the homomorphism

Bisimulation Metrics: Matching reward and transition functions, allowing states to be compared with each other:

 - $d(s, s') = \max_d (c_R|R(s, a) - R(s', a)| + c_T d_P(T(s, a), T(s', a)))$
	 - $R(s, a)$ is the reward of taking $a$ in $s$
	 - $T(s, a)$. is the transition probability
	 - $d_P$ is wasserstein or KL divergence
	 - $c_R$, $c_T$ are constants

Loss function:

$$
\mathcal{L}(\theta, \phi, \xi) = \frac{1}{N} \sum^TN [d(Z_{\theta}(s'_n), T_{\phi})(z_n, \bar A_{\phi})(z_n, a_n)] + d(R(s_n), \bar R_{\xi} (z_n))]
$$

$Z_{\theta}$ is a neural network mapping states to latent sates.

$d(z, z')$ is MSE.

$\bar T_{\phi}$ maps $z$ to $z'$, by predicting some action-effect., eg $T_{\phi}(z, \bar a)) = z + \bar A_{\phi}(z, a)$ where $\bar A_{\phi}$ is a neural network.

$R_{\xi}$ predicts the reward from $z$

Preventing the trivial solution: if you map everything to zero, then all the distance terms also go to zero. This is no-good.

A trick to prevent this outcome is a contrastive loss which you tack on the end:

$$
\max (0, \epsilon - \sum_{s \not \in S} d(Z_{\theta} (s), \bar T_{\theta} (z_n, \bar A_{\phi} (z_n, a_n))))
$$

the idea being that you want to maximize distances between latents for unrelated states.

## Finding an abstract MDP from the structured latent space

Discretization: Construct a discrete set $\mathcal{X}$ of prototype latent states, as well as discrete rtansitions and reward functions. To sample all the states, use the replay memory and encode the states, pruning duplicates.

Reward function: During planning, you can use the predicted reward $R_{\xi}$

Transition function: If two states are connected by an action in the state space, then they should be close after applying the latent space action. Transition function is a distribution over next latent states, use a temperature softmax:

$$
\hat T_{\phi} (z_j| z_i, a) = \frac{e^{-d(z_j, z_i + A_{\phi}(z_i, a))/ \tau}}{\sum_{k \in \mathcal{X}} e^{-d(z_k, z_i + A_{\phi} (x_i, a)) / \tau}}
$$

If an action moves two states close to each other, the nthe weight of their connection increases.

## Proof that this converges to an MDP homomorphism

![[mdp_homomorphisms_latents.png]]

if the loss converges, all the individual loss terms also go to zero.
 - $d(\bar T_{\phi}(z, \bar a), z')$
 - $-d (T\phi(z, \bar a), \tilde z))$
 - $d(R(s), \bar R_{\xi}(z))$

Positive samples: $d(\bar T_{\phi}(z, \bar a), z')})$ has gone to zero and so $d_{+} \lt \tau$, so $e^{-d_{+} / \tau} \approx 1$

Negative examples: $-d(\bar T_{\phi} (z, \bar a), \tilde z)$ goes to zero, meaning that distance to all negative samples ($d_{-}$) $\ge \epsilon$, meaning that $\tau < \epsilon < d_{-}$, meanign that $1 \le \frac{d_{-}}{\tau}$ meaning that $e^{-d_{-} / \tau} \approx 1$

So since $M$ is deterministic, $T(s'|s, a)$ transitions to one state with probability 1 and 0 for the otehrs.