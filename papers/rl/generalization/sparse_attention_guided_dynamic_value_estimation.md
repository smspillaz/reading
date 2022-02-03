---
title: Sparse Attention Guided Dynamic Value Estimation for Single-Task Multi-Scene Reinforcement Learning.
venue: CoRR
volume: abs/2102.07266
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2102-07266
ee: https://arxiv.org/abs/2102.07266
url: https://dblp.org/rec/journals/corr/abs-2102-07266
authors: ["Jaskirat Singh", "Liang Zheng"]
sync_version: 3
cite_key: journals/corr/abs-2102-07266/Singh/2021
---

# Sparse Attention Guided Dynamic Value Estimation for Single-Task Multi-Scene Reinforcement Learning

Training DRL agenst on evnrionments with multiple levels and scenes from the same task has become "essential for many applications aiming to achieve generaliation and domain transfer from sim2real".

Multiple scenes increases the variance of samples collected for policy graident.

Current methods learn a single value funciton but the sample variance is best minimized by treating each scene as a distinct MDP and then learning a joint value function $V(s, \mathcal{M})$ depending on both the state and the relevant MDP.

The true value function follows a multi-modal distribution and this is not well captured by the traditional CNN/LSTM based critic networks. To fix this problem, propose a dynamic value estimation which approximates the true joint value function thorugh a *sparse attention mechanism* over multiple value funciton hypotheses and nodes.


Contributions of this paper:

1. Enhanced Variance Reduction
2. Clustering Hypothesis
3. Novel Critic Module using sparse attention mechanism over multiple value function hypotheses and modes.
4. Implicit state space decomposition: Learned sparse attention divides the overall state space into distinct sets of game skills.
5. Navigation efficiency

The proposed solution to the value prediction error problem in the multi-scene case is to approximate the value funciton as the *mean value of the cluster of observations to which the current MDP belongs*. This can be implemented through a sparse attentiong mechanism over the value funciton modes, where teh attention parameters are 1 for the closest parameters and 0 otherwise.

A novel loss funciton is proposed which *progressively enforces sparsity in the attention as the training continues*


## Sparsity-enforcing loss

Define two metrics to describe the attention parameter distribution:

**Confusion $\delta$**: This is a measure of uncertainty as to which cluster the current state trajectory pair ($s_t, \tau^{t_-}$) belongs to.

$$
\delta(s_t, \tau^{t_-}) = \frac{1}{N_b \sum_i \alpha^2_i(s_t, \tau^{t_-})}
$$


**Contribution $\rho$**: The measure of how much a particular cluster contributes to the overall function value estimation across a general trajectory sequence $\tau : \{s_0, a_0, s_1, a_1, ..., s_T\}$

$$
\rho_i(\tau) = \frac{1}{T} \sum^T \delta(s_t, \tau^{t_-}) \alpha_i(s_t, \tau^{t_-})
$$

In this case $\alpha_i$ is the attention weight.

An increase in the sparsity of cluster assignments is equivalent to the maximization of their $l_2$ norm, which corresponds to a minimization of the confusion metric $\delta$. We also want to ensure that each cluster *contributes equally* in the $(s, \mathcal{M})$ space as opposed to the attentions all collapsing on to a single value. To achieve this, propose the *confusion-contribution loss*

$$
L^{CC} = k_1 E_{s_t, \tau^{t_-}} [\log \delta(s_t, \tau^{t_-})] + k_2 E_{\tau} [\log (\sum^{N_b}_i \rho^2_i (\tau))]
$$

Caveat: For this to work, the state space must have been well explored by the agent. Otherwise, the sparse cluster assignment will incorrectly generalize across the entire state space and everything collapses down to one cluster.

## Experiments

1. CNN LSTM baseline
2. Dynamic: Requires only a few changes to the critic network, eg, the attention parameters.
3. Sparse Dynamic: Addition of the $L_{CC}$ loss function during the training process.


DVE is able to outperform the baseline CNN/LSTM/PPO baseline on most of the environments, but the performance really shines when you introduce sparsity.