---
title: "Learning &quot;What-if&quot; Explanations for Sequential Decision-Making."
venue: "ICLR"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/BicaJHS21"
ee: "https://openreview.net/forum?id=h0de3QWtGG"
url: "https://dblp.org/rec/conf/iclr/BicaJHS21"
authors: ["Ioana Bica", "Daniel Jarrett", "Alihan H\u00fcy\u00fck", "Mihaela van der Schaar"]
sync_version: 3
cite_key: "conf/iclr/BicaJHS21"
---
# Learning "what if" explanations for sequential decisionmaking

 - Integrate counterfactual reasoning into batch inverse RL.
 - Principled way to define reward functions and explain expert behaviour and satisfies the constraints of real-world decisionmaking where active experimentation impossible.
 - Estimating the effects of various actions: counterfactual readily tackle the off-policy nature of policy evaluation in the batch setting and can naturally accomadate settings where expect policies depend on the histories of observations rather than just the current state.


Motivation: healthcare, interpretable parameterization is important. This can reveal trade-offs and preferences in expert actions.

![[learning_what_if_reward_signals.png]]

Parameterize reward signals for actions based on preferences over counterfactuals.

Reward function: Given by weight over expected value if action is taken (given state) + weighted expected value if action is not taken (given state)

$$
R(h_t, \text{take action}) = w_u E[U_{t + 1}|h_t] + w_z E[Z_{t + 1}|\text{take action}, h_t]
$$
$$
R(h_t, \text{no action}) = w_u E[U_{t + 1}|h_t] + w_z E[Z_{t + 1}|\text{no action}, h_t]
$$

We want to recover $w_z$ and $w_u$. We want to make some tradeoff. Consider medicine - treatment has side effects.

Finding that the weight for $u$ is greater than the weight for $z$ means that the expert is preferring to treat more aggressively.

Batch max-margine inverse reinforcement learning.

Aim: Recover expert weights and policy similar to $\pi_E$ (the expert policy) as measured by $||\mu^{\pi_E} - \mu^{\pi}||$, where $\mu$ is the "expected return" given a policy.

Use Counterfactual Inverse Reinforcement Learning

 - What is the potential outcome for taking $a_t$ at time $t$, given $h_t$. We can estimate this based on the historical data.
 - Define reward function in terms of counterfactual outcomes.

To estimate feature expectations, propose a new algorithm which takes advantage of counterfactuals.

Counterfactual $\mu$-learning is a TDL method which estimates feature expectations by using counterfactuals as part of temporal difference learning with 1-step boostraping. Basically take the current mu-values and the ones that you would get with the counterfactual.

Experiment: Disease progression dynamics, side effect dynamics, determine how well you can recover the reward weights.