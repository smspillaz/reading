---
title: Plan Arithmetic: Compositional Plan Vectors for Multi-Task Control.
venue: CoRR
volume: abs/1910.14033
year: 2019
type: Informal Publications
access: open
key: journals/corr/abs-1910-14033
ee: http://arxiv.org/abs/1910.14033
url: https://dblp.org/rec/journals/corr/abs-1910-14033
authors: ["Coline Devin", "Daniel Geng", "Pieter Abbeel", "Trevor Darrell", "Sergey Levine"]
sync_version: 3
cite_key: journals/corr/abs-1910-14033/Devin/2019
---
# Plan Arithmetic

Compositional Plan Vectors: Enalbe a policy to perform compositions of tasks without additional supervision.

CPVs represent compositions of the sum of subtasks.

Basic Idea: Similar to word2vec. In this case, learn a compositional feature space of skills,
such that you can make a plan by composing skills. Learn an embedding space so that you can compose tasks
by adding their embeddings. Condition the policy based ont he difference between the embedding and the
reference trajectory and the partially completed trajectory.

Evaluated in one-shot imitation learning on a discrete action environment.

Hierarchical RL learns representation of sub-tasks explicitly, or combines multiple Q functions. In
this approach you don't learn explicit primitives or skills, but instead aim to summarize the task via
a compositional task embedding. Many other prior works have sought to learn policies that are
conditioned on a goal or a task but without explicitly considering compositionality

  - Learning omnidirectional path following using dimensionality reduction
  - Data efficient generalization of robot skills with contextual policy search
  - Multi-task policy search for robotos
  - Learning parameterized skills
  - Learning compact parameterized skills with single regression

This work: Generalize to new compositions of tasks that are out of the distribution of tasks
seen during training.

## Compositional Plan Vectors

Example: Red out, yellow in . Take a red cube out, put a yellow cube in.
 - To make a plan vector, you should encode the task as the sum of its parts
 - The plan vector for red out, yellow in - yellow in should = red out.
 - The idea is that once you've finished one sub-task, you remove that from
   the plan vector.

 - Limitation: cannot represent ordering, since addition is commutative. Policy
   needs to decode which component you do first. The idea that hopefully this
   doesn't matter because the policy won't put the yellow box in if it isn't possible.


One-shot imitation learning setup: Agent is given a reference trajectory of observations
and you perform an action conditioned on the first observation and the reference.

Plan vectors: Define $g_{\phi}(O_{k:l})$ parameterized by $\phi$ which takes a trajectory
and outputs a plan vector. The idea is that the plan vector encodes the sequence. Plan vector
of a partially accomplished trajectory should encode the steps already taken.

Instead of encoding the entire trajectory in the policy, you're only conditioned on the difference
between the initial state and the end state.

$\pi = \pi_{\theta}(a_t|o_t, g(o^{\text{ref}}_0, o^{\text{ref}}_T) - g(o_0, o_t))\$

Training the policy: Demonstrations include the action, the reference trajectories do not.

To improve compositionality, triplet loss: enforce that the sum of the embeddings is
close to the embedding of the full trajectory.

$l_{\text{tri}}(a, p, n) = \max\{||a -p||_2 - ||a - n||_2 + 1, 0 \}$

$L_{\text{hom}}(D, \phi) = \sum^N_i \sum^H_t l_{\text{tri}}(g_{\phi}(o_0^i, o^i_t) + g(o^i_t, o^i_T), g(o^i_0, o^i_T), g(o^j_0, o^j_T))$

Regularize as well that embeddings of paired trajectories should be close in
the embedding space, enforces that embeddings are a function of the
behaviour within a trajectory rather than the appearance of a state.

### How to measure compositionality

Condition the policy on the sum of plan vectors from multiple tasks and measure the policy's success rate.