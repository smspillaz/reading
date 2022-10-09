---
title: "Is Curiousity all you need? On the utility of emergent behaviours from curious exploration"
tags: ["DeepMind"]
---

# Is Curiousity all you need? On the utility of emergent behaviours from curious exploration

- As the agent learns to reach previously unexplored spaces and the objective adapts to reward new areas, behaviours emerge but then are overwritten to do something else.
- Shift the focus to retaining the behaviours which emerge during curiousity based learning.
- Self-discovered behaviours might actually be useful in solving related tasks.


The problem arises in environments with multiple possible tasks (eg, manipulatuon strategies where objects could be interacted with or rearranged in different ways). So you might discover something useful only for it to be overwritten layer.

In contrast to prior work:
 - Implement curiousity based exploration in an off-policy learning setting, which improves upon on-policy implementations in terms of data-efficiecny.
 - Look at the utilisation of self-discovered behaviour for learning new downstream tasks.


Contributions:
 - SelMo: An off-policy realisation of self-motivated curiousity based method for exploration
 - Extend the focus in the application of curiousity learning towards the identification and retention of emerging intermediate behaviours.


SelMo Architecture:
 - Collect trajetories $\tau^k, \tau^{k + 1}$... using the current policy and store in a replay buffer.
 - Dynamics model: Sample uniformly from this buffer and updates parameters for forward prediction using SGD.
 - Sampled predictions are assigned a curiousity reward based on their respective prediction erorr under the current $f^j_{\text{dyn}}$


When transitions are evaluated by the world model, the assigned reward is scaled by the model's current prediction error:

$$
r^{(j)}(s_t, a_t, s_{t + 1}) = \text{tanh}(\eta_r * (f^{(j)_{\text{dyn}}}(s_t, a_t) - s_{t + 1})^2)
$$

When a new match of data is sampled from the model replay, the forward model labels each example in the batch by assigning curiousity rewards and then performs gradient updates by minimizing prediction loss.

**Policy Replay**

Fixed-size pociy replay buffer stores tuples representing trajectories which have been labelled with curiousity rewards by the world model.

Trajectories with the most outdated curiousity rewards get replaced first to reflect changes in the world model.

## What sort of emergent behaviour do we see?

### JACO

 - Agents drawn towards the cubes
 - Then drawn towards picking them up

### OP3

 - 2K episodes spent learning to balance
 - Around 30K epsidoes: swing arms to take bigger steps
 - 70k epsiodes: start revisiting earlier behaviour, but with variations.

## Utilization of emergent behaviour

 - Reguarlized Hierarchical Policy Optimization: Compose mutliple policies in a hierarchical manner
	 - We have some downstream task that we want to learn and we provide five policy snapshots
	 - RHPO samples SelMO sanpshots and utilizes the behaviour exhibited by them to assist the exploration for the desired downsteam task.
 - Findings: SelMo auxiliaries from the mid and late exploration periods give the learning of the lifting policy a boost