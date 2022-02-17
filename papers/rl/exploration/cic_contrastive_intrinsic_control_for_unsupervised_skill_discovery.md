---
title: CIC - Contrastive Intrinsic Control for Unsupervised Skill Discovery.
venue: CoRR
volume: abs/2202.00161
year: 2022
type: Informal Publications
access: open
key: journals/corr/abs-2202-00161
ee: https://arxiv.org/abs/2202.00161
url: https://dblp.org/rec/journals/corr/abs-2202-00161
authors: ["Michael Laskin", "Hao Liu", "Xue Bin Peng", "Denis Yarats", "Aravind Rajeswaran", "Pieter Abbeel"]
sync_version: 3
cite_key: journals/corr/abs-2202-00161/Laskin/2022
---

The basic issue they were trying ot solve is how to perform unsupervised skill discovery from unlabelled data.

Maximize the mutual information between skills and state transitions.

General idea: Mutual information is a good idea, all the previous approaches to approximate it have been flawed. We need a new lower bound. use a particle estimator for state entropy and contrastive learning to distill behaviours into skills.


Idea: if we have $z_1$ then we move in one direction, $z_2$, another direction, etc.

## Unsuperivsed Reinforcement Learning

1. Pre-training with self-supervised intrinsic rewards. Internal motivation.
2. Fine-tuning to downstream tasks with skills.


Several methods:
 - Knowledge-based methods (error or uncertainty) (ICM, Disagreement, RND, Plan2Explore => $\max ||x - f(x)||$)
 - Data-based (maximize entropy of state visitations) (APT, ProtoRL, Count-based, pseudocounts) => $\max \mathcal{H}$
 - Competence based: Learn skills that generate diverse behaviour. => $\max \mathcal{I}$

Competence based algorithms simultaneously address both the exploration challenge as well as distilling the generated experience in the form of reusable skills.

Two options, both equal but generate different beahvours

Entropy of skills and make skills easy to distinguish
$$
\mathcal{H}(z) - \mathcal{H}(z|\tau)
$$

Ensure diverse behaviours (state visitations) and make the states easy to distinguish based on the skills:
$$
\mathcal{H}(\tau) - \mathcal{H}(\tau|z)
$$

**Skill**: Latent variable that conditions the policy.

## Unsupervised RL Benchmark

Pre-train the agent for 2M steps in each of the three domains.
 - Walker
 - Quadruped
 - Jaco arm

Then fine-tune agents for 100k steps to solve various downstream tasks within domains.

Works in theory, doesn't work in practice.

Do you have to freeze the skills before transferring? Not necessarily.

### Downstream Tasks

Walker: Stand, walk, run, flip
Quadruped: Stand, walk, move.


## Why do competence based methods perform poorly?
The very simple methods that try to optimize the entropy of state visitations tend to do the best (competence based methods perform poorly).

Most mutual-information based algorithms try to maximize a variant of the variational lower bound: $\mathcal{H}(z) + E[\log q(z|\tau)]$

Inorder to produce usable skills, estimators must:

1. Explicitly encourage diverse behaviour
2. Have the capacity to discrimiante between high-dimensional continuous skills

In practice you get diverse skills but not diverse behaviour. The skill space is in practice too limited (eg, very low rank).


If you use the other decomposition, eg, maximizing the entropy of the state visits vs entropy of the skills, then you actually get diverse behaviour.

This is a problem for training the discriminator, you need lots of data to learn $q(z|\tau)$ if the skills are very high dimensional - requires a high number of samples.

Other problem: You leak extrinsic rewards by terminating episodes when the agent falls over

# How does it work in oractice?

Novel sample-based lower-bound. Tighter bound than CPC.

$$
\mathbb{F}_{\text{CIC}} (\tau_1, \tau_2) = \mathcal{H}_{\text{particle}}(\tau_1) + \mathbb{E}[f(\tau_1, \tau_1) - \log \frac{1}{N} \sum^N \exp(f(\tau_j, z_i))]))]
$$

This particle based esitmator is computing the distance between each particle. It is a postprocessed state transition $h_i$ and its $k$th nearest neigbhour..
$$
\mathcal{H}_{\text{particle}}(\tau) \propto \sum^n \log ||h_i -h_i^i||
$$

This encourages exploration through max-entropy and distilling behaviours into skills through contrastive representation learning.

## Architecture

![[cic_unsupervised_skill_discovery_architecture.png]]

The particle-based entripy is hte intrinsic reward.

Noise contrastive loss should learn to maximize mutual information between trajectory query and skill k.

$z_i$ is sampled during training.

### Noise Contrstive Loss

SimCLr list inner product with neural encoders $g$. Exploration with intrinsic rewards.

$$
\mathcal{H}_{\text{APT}} \propto \frac{1}{N_k} = \sum^{N_k}_{h^*_i \in N_k} \log ||h_i - h_i^*||
$$

where $h_i$ is an embedding of $\tau_i$ and $h^*_i$ is a kNN embedding.

The CPC loss is then:

$$
F_{\text{CPC}}. q_{\psi_i} (\tau_i)^T g_{\psi_2} (z_i) - \log \frac{1}{N} \sum^N \exp(g_{\psi_i}(\tau_j)^T g_{\psi_2}(z_i))
$$

## Algorithm

Unsupervised pre-training:
 - Encode states and samples actions, observe next states, add transitions, then ample minibatches and compute contrastive loss to update encoders and compute CIC intrinsic reward

fine-tuning:
 - Take random actions, select skills and sample minibatches to update actor and critic.off-policy training. (n = 4000)
 - Then Encode state and sample actions from policy, observe next state and reward (from extrinsic reward), and update actor and critic.

## Ablaton

 - Skiill prorjection is necessary
 - Skill dimension is necessary - if you use too low dimensions, scores won't work so well.
 - Skill-adaptation: What skill selection mechanism is the best (should we pick skill zero, random skills, or sweed?).