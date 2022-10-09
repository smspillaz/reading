---
title: "DeepAveragers: Offline Reinforcement Learning by Solving Derived Non-Parametric MDPs."
venue: "CoRR"
volume: "abs/2010.08891"
year: 2020
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2010-08891"
ee: "https://arxiv.org/abs/2010.08891"
url: "https://dblp.org/rec/journals/corr/abs-2010-08891"
authors: ["Aayam Shrestha", "Stefan Lee", "Prasad Tadepalli", "Alan Fern"]
sync_version: 3
cite_key: "journals/corr/abs-2010-08891/Shrestha/2020"
---
# DeepAveragers: Offline RL by solving derived non-parametric MDPs

tl;dr: Optimally solve finitely represented MDPs derived from a static dataset of experience. Can be applied on top of any learned representation and has the potential to easily support multiple solution objectives and zero-shot adjustment to changing environments and goals.

Deep Averagers with Costs MDP: Non-parametric model that leverages deep rperesentaitons and accounts for limited data by introducing costs for exploiting under-represented parts of the model.

Promise of model based RL: once we train a suitable model, an optimal planner can produce a range of policies optimizing for different reward structures and safety constraints.

Most model-based approaches fail to deliver as the learned model is not exactly plannable. Have to use MCTS or model-free algorithms.

Use tabular models compared with VI.

Start with a set of state-action tuples. Build a finite MDP using the dataset and the non-parametric. This is a "core-MDP". This uses the states to define the transition model. Then solve this using exact value iteration. By definition all the states in the non-parametric MDP have one-step transitions.  Hence we can get the true values by one-step lookup to the finite q-values.

To scale this, we have a fast GPU enabled VI solver. DAC.

We use deep networks for state represtation learnings and derive the ideas from Gordon and Fontaneau to create a finite non-parametric MDP that is pessimistic in the face of data sparsity. Derive from simple kernel regression from transitions and rewards.

We have kNN -> set of k-nearest neighbours to $s, a$ in the dataset and $d(s, a, s_i, a_i)$ distances between $(s, a)$ and $(s_i, a_i, s'_i, r_i)$. Add additional cost in sparse data regions. The smoothness parameter $k$ and $C$ are the two main hyperparameters.

Oracle experiments in CartPole - we have oracle features. The datasets are collected using different behavioural policies, mied bag, optimal.

There is a sweet spot for the cost-parameter C to ensure the pessimism in the model. If we set it to 0 and it will lead to exploitation, but setting it too high leads to behavioural cloning (ok for optimal dataset, bad for others), $k$ helps to smoothen.

For evaluation, we introduce a softer approach which limits interactions with environment. Collect data with one or more policies and store rollouts. Learn several policies from buffer using different parameters.

Once a representaiton is learned, it is frozen and used to build and solve the DAC-MDPs.

This is the first time it has been shown that such an approach can be scaled to a complex stochastic domain like atari.

### Flexibility of optimal plnaners (first-person view)

An agent sees the first person view and gets a reward of positive 1 for reaching the goal. A DAC policy can solve this well.

Potential benefits for one-shot transfer of different tasks.