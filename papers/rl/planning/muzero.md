---
title: "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model."
venue: "CoRR"
volume: "abs/1911.08265"
year: 2019
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-1911-08265"
ee: "http://arxiv.org/abs/1911.08265"
url: "https://dblp.org/rec/journals/corr/abs-1911-08265"
authors: ["Julian Schrittwieser", "Ioannis Antonoglou", "Thomas Hubert", "Karen Simonyan", "Laurent Sifre", "Simon Schmitt", "Arthur Guez", "Edward Lockhart", "Demis Hassabis", "Thore Graepel", "Timothy P. Lillicrap", "David Silver"]
sync_version: 3
cite_key: "journals/corr/abs-1911-08265/Schrittwieser/2019"
---
# MuZero

"Mastering Go, chess, shogi and Atari without rules"

Problem:
 - Exhaustive search - trying to search all possible to states to find the best trajectory.
 - They start this as alphazero for a go game. This is kind of hard due to combinatorial explosion.


Planning algorithms based on lookahead are good, but they require you to know the dynamics of the environment.

Doesn't work on visually rich envirnments though, best to just use model-free.

Basic idea: Predict aspects of the future that are relevant for planning. Via a recurrent process predict the
policy, value function and immediate reward. Don't need to recnostruct the original observation - hidden
states just represent whatever is relevant. Kind of like game tree search with alpha-beta pruning, **except that
you use an RNN to pick a policy at each turn.**

 - Basic idea: Reduce search depth with value network - terminate search at depth N and just use the value function.
 - To reduce the breadth, use a policy network - choose only reasonable actions at each branch.

Deep RL has mostly been just about predicting the value function or optimal policy directly without any lookahead.

Formal definition:
 * Given previous hidden state $s^{k - 1}$, candidate action $a^k$ and dynamics $g(s, a) \to h \to [r^k, s^k]$, you get
   reward $r^k$ and new hidden state.
 * Compute policy and value function from hidden state.
 * Initial hidden state comes from past observations into encoder.
 * Do MTCS at each iteration:
   * Sample action from search policy
   * Store trajectory data into replay buffer.


MCTS:

 - U(s, a): scoring function to choose action
	 - Choose actions that are either promising (high prior and/or high value)
	 - Not well known (visit counts)
	 - Upper regret bound


For Atari: $U(s, a) = r(s, a) + \gamma \cdot v(s') + c \cdot p(s, a)$

How do you evaluate the notes?
 - collect statistics on each node:
	 - calculate the number of visits
	 - mean Q
	 - policy P
	 - reward R,
	 - state transition S
 - How do you assign an observation to a node? Probably only works if the states are discrete?


State representations: - just encoded representations with convnet. We don't preserve the pixel information. No reconstruction loss.

How to make the search more random?
 - Use Dirichlet Noise - boosts prior of around one random action high enough to be explored. Doesn't interfere with other priors.
 - Temperature parameter to control how much you explore. Actions selected based on visit counts.

Updating the learned model towards the MCTS:
 - Polciy is the distillation of the MCTS
 - Reward is the distillation of $u_t$ from MCTS
 - Value is from n_step bootstrapping, eg, discounted rewards down the MCTS tree.

Nicola comment:
 - $s_1$ is trained only by backpropagating through the losses of the value and reward function.
 - Compare DREAMER paper: Using only this policy/value/reward losses doesn't work as well as the reconstruction loss. Dramatic improvement if you use the representation to predict the dynamics.

Difference between alphaZero and muZero:
 - in alphaZero: use the simulator for the MCTS
 - in muZero: use the model for the MCTS. But evaluate the path taken using the simulator.



Reanalyze strategy:
 - Learn one policy - update that policy using the old episodes.
 - 100x fewer frames. More sample efficiency.