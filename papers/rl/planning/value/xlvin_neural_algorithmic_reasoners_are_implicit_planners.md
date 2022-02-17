---
title: Neural Algorithmic Reasoners are Implicit Planners.
venue: CoRR
volume: abs/2110.05442
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2110-05442
ee: https://arxiv.org/abs/2110.05442
url: https://dblp.org/rec/journals/corr/abs-2110-05442
authors: ["Andreea Deac", "Petar Velickovic", "Ognjen Milinkovic", "Pierre-Luc Bacon", "Jian Tang", "Mladen Nikolic"]
sync_version: 3
cite_key: journals/corr/abs-2110-05442/Deac/2021
---

[[xlvin_neural_algorithmic_reasoners_are_implicit_planners.pdf]]

Studies implict planning through value iteration.

Prior approaches assume the connectivity structure of the evironment or infer "local neighbourhoods".

They discover an "algorithmic bottleneck effect" caused by explicitly running the planning algorithm based on scalar predictions in every state, which can be harmful to data efficiency if such scalars are improperly predicted.

Proposes XLVIN to perform the computations in *latent space*.

# Related Work

[[value_iteration_networks]] : the original vin formulation

[[mvprop]] : value propagation modules

[[gvin_life_beyond_lattices]] : VIN but with graph networks

All of these assume that the transition table and reward distribution is known.

[[value_prediction_network]]: use a latent transition model to construct a local environment around the current state
[[treeqn_and_atreec_differentiable_tree_structured_models_for_deep_reinforcement_learning]]: similar, but with differentiable tree structure

The problem with these approaches is that if you have insufficient data to predict scalar values for the value function, then your VI algorithm is equally suboptimal.

[[transe_translating_embeddings_for_modelling_multi_relational_data]] : Get some state embeddings via an encdoer and the effect of an action by a translation vector.

The transE loss is given by:

$$
\mathcal{L}_{\text{transE}}((s, a, s'), \bar s) = d(z(s) + T(z(s), a), z(s')) + \max (0, \xi - d(z(\bar s), z(s')))
$$

i.e, the point is that you translate from one state in the latent space to another state in the latent space and try to ensure that points in the latent space which are negative samples are far away.
# Architecture
![[xlvin_architecture.png]]


The main idea: Once you train $T(z(s), a)$, you can induce a local graph by applying $T$ to $z(s)$ with each $a$ to get $z(s')$, the next state in the VIN. Then you can just keep rolling out this process, applying actions to $z(s')$ to get $z(s'')$ and so on.

Now you can train a reward model $R(h_s, a)$ to get a Q-value for latent states.

**The algorithmic bottleneck still remains**: VI's performance depends on having exactly correct parameters of the underlying MDP. In this work, don't project the state embeddings further to a low dimensional space and instead run a graph neural network directly over them.


**Encoder**: Consume state representations $s \in S$ and produce flat embeddigns

**Transition**: This is just the translation function $T$ above.

**Executor**: Produces an embedding $h_s$ of a staet $s$ alongside a neighbourhood set $\mathcal{N}(h_s)$ which contains expected embeddings of states that immediately neighbour $s$.

**Actor and Tail Components**: Consume a state embedding and produce action probabilities (policy) and Q values.

What value of $K$ to use? Since the tree-expansion strategy is breadth first, you have $O(|A|^K$) complexity. Diminishing returns $K > 4$ so just use $K \le 4$, Probably larger values of $K$ will require a rollout policy where you select actions to expand for each staet.

(Note: probably a good rollout policy is picking transitions which are likely to actually exist, eg, things that have been observed in expert trajectories, or some prior or otherwise).

## How to train it?
Without knowledge of the MDP, no easy way to train the exector.

Don't train end-to-end. Pre-train the parameters of $X$ and freeze them using [[graph_neural_induction_of_value_iteration]]. First generate a dataset of synthetic MDPs according to some underlying graph distribution and execute the VI algorithm on these MDPs keeping track of intermediate values at each step until convergence. Supervise a GNN operating over MDP transitions as edges to receive $V_t(s)$ and predict then next value. Retrain the processor as the executor function.

Then training the whole thing corresponds to

1. Sampling policy rollouts
2. Evaluating PPO and TransE + negative samples
3. Updating policy network parameters using the combined loss, which is the PPO loss plus the TransE loss for each timestep.

# Experiments

Question: Do you get gains in data efficiency from XLVIN? Compare in a low-data regime against model-free PPO baseline and abalating against the ATreeC implicit planner.

Environments

 * CartPole
 * Acrobot
 * MountainCar
 * LunarLander

For CartPole you only get 10 trajectories at the beginning and no further interaction beyond the 100 epochs of trinaing.

All other environments are sparse reward,

The authors also look at pixel-space observations on Freeway, Alien, Enduro and HERO.

Use ATreeC as one of hte baselines, capturing the behaviour of a larger class of VI-based implicit planners

How do we do?

![[xlvin_results.png]]
In table 1 we have only 100 episodes of trinaing data. PPO and ATreeC do about as well as each other in most cases, XLVIN beats both of them.

The model is capable of solving Acrobot and MountainCar in only 100 trajectories

## Ablation Study

Success really hinges on $T$ and $X$. Analyse a pre-trained XLVIN agent with a CNN encoder on a randomly generated 8x8 grid-world.

Perform linear regression to test how accurately decodable the ground-truth $V^*(x)$ values are. Compute the $R^2$ score. After applying hte GNN computations, the value function is pretty much perfectly decodable. The encoder maps to a latent space where you can actually perform VI.

# How are the synthetic MDPs generated?

![[xlvin_synthetic_mdps.png]]

Create synthetic graphs.

$|S| = 20$ and $|A| = 8$ . The idea is that we sample the graphs by picking some transition uniformly, setting the probability of that transition to one if sampled?

The rewards are just normally distributed.

For CartPole you have a binary tree.

See [[graph_neural_induction_of_value_iteration]] . The general idea here is to "learn" how to do value iteration in the latent space over lots of different graphs. Its sort of like [[spatial_planning_transformers]] in that sense.