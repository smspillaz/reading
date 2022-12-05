---
title: "Offline RL Policies Should be Trained to be Adaptive."
venue: "CoRR"
volume: "abs/2207.02200"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2207-02200"
doi: "10.48550/ARXIV.2207.02200"
ee: "https://doi.org/10.48550/arXiv.2207.02200"
url: "https://dblp.org/rec/journals/corr/abs-2207-02200"
authors: ["Dibya Ghosh", "Anurag Ajay", "Pulkit Agrawal", "Sergey Levine"]
sync_version: 3
cite_key: "journals/corr/abs-2207-02200/Ghosh/2022"
---

The main idea is that for a given trajectory, there are many possible MDPs that the trajectory could be optimal for. So we don't actually know the "true" value function.

One idea is to predict many different value functions at the same time, each one being based on being in a different MDP.

We form beliefs about which MDP we're in based on past state-action trajectories.

The belief is not updated directly as a parameter, but rather gets estimated by a neural network based on the previous transitions.

Because the choice of beliefs affects the value function that we prioritize, we want to choose beliefs whose value functions align with our observations.

Train the policy to maximize the Q-value across all belief-weighted MDPs.

At test time, we do belief updates, which shifts our Q function and we act accordingly.

Algorithm: APE-V