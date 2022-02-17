---
title: XLVIN - eXecuted Latent Value Iteration Nets.
venue: CoRR
volume: abs/2010.13146
year: 2020
type: Informal Publications
access: open
key: journals/corr/abs-2010-13146
ee: https://arxiv.org/abs/2010.13146
url: https://dblp.org/rec/journals/corr/abs-2010-13146
authors: ["Andreea Deac", "Petar Velickovic", "Ognjen Milinkovic", "Pierre-Luc Bacon", "Jian Tang", "Mladen Nikolic"]
sync_version: 3
cite_key: journals/corr/abs-2010-13146/Deac/2020
---
# XLVIN

See also [[xlvin_neural_algorithmic_reasoners_are_implicit_planners]]

[[xlvin_executed_latent_vin.pdf]]

tl;dr:
 - Combines "recent develop ments in contrastive learning, graph representation learning and neural algorithmic reasoning, deploying VIN-style models to generic environments"
 - Contrastive SSL: Mearningfully identify dynamics for the MDP, even when not provided, by embedding states and actions into vector space, such that effect of action embeddigns is consistent with true action dynamics.
 - Graph Representation Learning: Message passing architecture to traverse the partially inferred MDP
 - Use improvement to GVIN to do value iteration on the inferred graph
 - Pretraining of executor and transition model.


## Architecture

![[xlvin_architecture.png]]

The transition model is $z(s) + T(z(s), a)$ where $z$ and $T$ are learnable functions. $z$ is the embedding and $T$ is a function which produces a translation vector for a given state-action pair.

Loss:

$$
\mathcal{L} = d(s(z) + T(z(s), a), z(s')) + \max (0, \epsilon - D(z(\tilde s), z(s')))
$$

$\tilde s$ is a negative sample.

The point being that $z(\tilde s)$ and $z('s)$ should be far away from each other.

Basically, at every step in the rollout, you assign a neighbouring latent state to the previous state.

### Execution Model

$N(h_s) \approx \mathbb{E}_{s' \sim P(s'|s, a) } z(s')$

Basically, you combine the neighbourhood set features to produce an updated embedding of state $s, X_s = X(h_s, N(h_s))$

Actor/tail components: Consume state embedding, produce action distribution.

### Algorithm

1. Initialize input state
2. Initialize depth-0 set of state embeddings, containing $\{h_s\}$
3. For $k = 0$ to $K$
	1. Initialize embedding set
	2. For each depth $k - 1$ embedding set, compute $h' = h + T(h, a)$ for each action
	3. Attach to the embedding set and add edges between prior nodes and successor nodes accordingly.
4. Run execution model over graph by applying the executor function $h_s = X(h_s, N(h_s))$ (so we start again and run $X$ over all the nodes we expanded from applying $z$ and $T$ to each state-action pair)
5. Regress policy and value from $h_0$, eg, the state we started from.


This is sort of like dreamer-style rollouts, where you have to estimate the state space and also execute it at the same time.

### Pretraining


Note that $T$ is pre-trained by sampling the environment using a random policy and you also train transitions in this way.

The GNN executor is also pre-trained using synthetic graphs, where the rewards for taking an action are sampled frm the normal distribution.