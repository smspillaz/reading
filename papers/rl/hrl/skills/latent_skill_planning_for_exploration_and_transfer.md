---
title: Latent Skill Planning for Exploration and Transfer.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/XieBHGS21
ee: https://openreview.net/forum?id=jXe91kq3jAq
url: https://dblp.org/rec/conf/iclr/XieBHGS21
authors: ["Kevin Xie", "Homanga Bharadhwaj", "Danijar Hafner", "Animesh Garg", "Florian Shkurti"]
sync_version: 3
cite_key: conf/iclr/XieBHGS21
---
# Latent Skill Planning for Exploration and Transfer

Partial amortization for fast adaption at test time. Actions are produced by a policy that is learned over time while the skills it conditions on are chosen using online planning.

How can we efficiently integrate reusuable skill models?

Prior work:
 - Learned world models (Chua, Charma, Wnag & Ba, Hafner), even in the latent space.
 - Online planning (PETS, CEM) - learn only the dynamics and use online search
 - Amortized policy methods (Dreamer, Hafner et al) - reactive policy with many imagined rollouts

Benefit of amortized policy methods is that they improve with experience and perform faster.

Plan latent skills, learn skill-conditioned policies

## Usage of CEM

![[latent_skill_planning_cem.png]]

Use CEM to plan over the latent skill distribution. A low-level policy is conditioned on those skills and we train with imaginary rollouts.

Mutual information skill objective.

$$MI(z, s|s_0) \ge \int p(z, s, s_0) \log \frac{q(z|s, s_0)}{p(z|s_0)}$$

Which is the expected value of $\log q(z|s, s_0) + E_{\s_0}[H(p(z|s_0))]$ - eg, the log-probability of z on distribution $q$ given the state parameters, plus the entropy of the $p$ distribution given the starting state.

Baseline against Dreamer and HIRO (model-free hierarchical RL method). Random skills: LSP but with random skils.

On dm-control we do a little bit better than everyone else.

Learned skills are good enough to be re-composed.

in an environment with obstacles, its really hard to get to the goal with random rollouts, Our method LSP with fixed policy is able to efficiently explore the state space. Dreamer fails completely because it doesn't get a reward.



