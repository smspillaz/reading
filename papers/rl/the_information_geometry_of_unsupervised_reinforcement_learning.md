---
title: "The Information Geometry of Unsupervised Reinforcement Learning."
venue: "CoRR"
volume: "abs/2110.02719"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2110-02719"
ee: "https://arxiv.org/abs/2110.02719"
url: "https://dblp.org/rec/journals/corr/abs-2110-02719"
authors: ["Benjamin Eysenbach", "Ruslan Salakhutdinov", "Sergey Levine"]
sync_version: 3
cite_key: "journals/corr/abs-2110-02719/Eysenbach/2021"
---
RL agents can prepare to solve unknown downstream tasks by performing unsuperivsed skill discovery.

During pre-training we only learn state-action transitions. Perform pre-training by maximizing mutual information objective.

Not much theoretical analysis on this however. We don't know if these skills are somehow optimal or even efficient. No provably efficient skill-learning algorithms.

2 main results:
 - Unsupervised skill discovery based on MI does not learn skills that are optimal for *every possible reward function*
 - But you can get an optimal initialization against an adversarial reward function.

Objective - maximize the distribution of the latent codes.

In practice, we have some latent codes that we are trying to optimize - learn some $z$ that contains maximal mutual information over the distribution of states. Given some states we want to make the skill identifiable and given some states we want to know where the skil lgoes.

Main result:
 - learned skills fail to cover all possible policies, no matter how many skills are learned. We will just learn duplicates.
 - But when the distribution over skills that maximizes MI is converted into a distribution over states, it is the best initialization for adapting to an adversarilly chosen reward function.

Adaptation is purely idealized, it is in a form that cannot be optimized by any known algorithm.

Adversarilly chosen reward function: The most difficult to learn reward in the states. Given that we have some specified MDP, any type of reward function in this MDP which is the most difficult to learn or solve. Eg, the most difficult with respect to the skills that we have learned.

Some intuition about how we reach this main goal.
 - We can visualize policies wit h a state-occupancy measure.
 - A reward starts as a vector from the origin.  The best policy is the one that maximizes the dot product between the state marginal and the reward vector.
 - Mutual information algorithms fail to discover all the vertices of this polytope.
 - Maximizing mutual information is equivalent to minimizing the maximum divergence between a prior over states and any achieveable state marginal distribution. Maximum number of skills to be learned is the same as the number of states in the state-space.

Questions: So basically a skill tells us how to get to a particular distribution of states, but only defines one particular way of doing it, right? So if we learn to get to C through A then B and the reward requires B, A, C, then we

 - not quite the reward function is markovian

"optimal visitation"

60% state A
20% state B
20% state C

But for example you only want to visit state A to maximize reward. Mutual information based skills and reward maximization are orthogonal problems.