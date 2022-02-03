---
title: Replacing Rewards with Examples - Example-Based Policy Search via Recursive Classification.
venue: CoRR
volume: abs/2103.12656
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2103-12656
ee: https://arxiv.org/abs/2103.12656
url: https://dblp.org/rec/journals/corr/abs-2103-12656
authors: ["Benjamin Eysenbach", "Sergey Levine", "Ruslan Salakhutdinov"]
sync_version: 3
cite_key: journals/corr/abs-2103-12656/Eysenbach/2021
---

# RCE: Replacing Rewards with Examples

Basic idea & Motivation: Defining reward functions is difficult. Can we instead give some examples of success states?

The problem then becomes

$$p(e_{t+} = 1|s_t, a_t)$$

where $e_{t+} = 1$ is "we reach the success state at some point the future"

Problem: this is ill-posed if we do not have expert trajectories. By bayes rule: $P(A|B) = \frac{P(B|A)P(A)}{P(B)}$

$$
p(e_{t+} = 1|s_t, a_t) = \frac{p(s_t, a_t|e_{t+} = 1)P(e_{t+})}{p(s_t, a_t)}
$$

To estimate $p(s_t, a_t|e_{t+} = 1)$ we need trajectories.

Define a "classifier" which estimates whether we will be successful given a current state-action:

$$C^{\pi}_{\theta}(s_t, a_t)$$

Three steps to deal with the "don't know the trajectories" problem.

1. $p(s_t, a_t|e_{t+} = 1)p(e_{t+} = 1) = p^{\pi}(e_{t+} = 1|s_t, a_t)p(s_t, a_t)$ (simple flip with bayes rule)
2. $p(s_t, a_t|e_{t+} = 1) = (1 - \gamma)p(e_t = 1|s_t) + \gamma E_{p(s_{t + 1}|s_t, a_t)} [p^{\pi}(e_{t+} = 1|s_{t+1}, a_{t + 1})]$
3. Use samples $s^* \sim p(s_t|e_t = 1)$ with the assumption that the behaviour policy equals the expert policy and assume that $p_U(e_{t+} = 1) = 1$. Then estimate $p^{\pi}(e_{t+} = 1|s_{t + 1}, a_{t + 1})$ using the classifier predictions.


$$
\mathcal{L}^{\pi}(\theta) = (1 - \gamma) E_{p_U(s_t|e_t = 1)} [\log C(s_t, a_t)] + E_{p(s_t, a_t, s_{t + 1})}[\gamma w \log C(s_t, a_t) + \log(1 - C(s_t, a_t))]
$$

Where the weight is the importance weight given by the discriminator.

 - first term trains classifier to predict 1 for success examples
 - second term is the TDL bootstrapping
 - third term train the classifier to predict 0 for random transitions