---
title: Do As I Can, Not As I Say - Grounding Language in Robotic Affordances.
venue: CoRR
volume: abs/2204.01691
year: 2022
type: Informal Publications
access: open
key: journals/corr/abs-2204-01691
doi: 10.48550/ARXIV.2204.01691
ee: https://doi.org/10.48550/arXiv.2204.01691
url: https://dblp.org/rec/journals/corr/abs-2204-01691
authors: ["Michael Ahn", "Anthony Brohan", "Noah Brown", "Yevgen Chebotar", "Omar Cortes", "Byron David", "Chelsea Finn", "Keerthana Gopalakrishnan", "Karol Hausman", "Alexander Herzog", "Daniel Ho", "Jasmine Hsu", "Julian Ibarz", "Brian Ichter", "Alex Irpan", "Eric Jang", "Rosario Jauregui Ruano", "Kyle Jeffrey", "Sally Jesmonth", "Nikhil J. Joshi", "Ryan Julian", "Dmitry Kalashnikov", "Yuheng Kuang", "Kuang-Huei Lee", "Sergey Levine", "Yao Lu", "Linda Luu", "Carolina Parada", "Peter Pastor", "Jornell Quiambao", "Kanishka Rao", "Jarek Rettinghouse", "Diego Reyes", "Pierre Sermanet", "Nicolas Sievers", "Clayton Tan", "Alexander Toshev", "Vincent Vanhoucke", "Fei Xia", "Ted Xiao", "Peng Xu", "Sichun Xu", "Mengyuan Yan"]
sync_version: 3
cite_key: journals/corr/abs-2204-01691/Ahn/2022
---

Large language models have lots of embedded knowledge. We could use that embedded knowledge to do planning or just to interpret instructions. However LMs and robots are grounded in different ways.

Eg, if we ask an LM how to clean a spill, it might give us something reasonable, but it won't be something the robot understands.

In this paper, ground the LM to the real world by pretrained skills, constraining it to natural language actions that are both feasible and contextually appropriate.

The main principle is that in addition to asking the LLM to interpret an instruction, score the likelihood that an individual skill makes progress towards comleting the high-level instruction.

The LM scores the probability of taking a particular skill, the affordance model scores the probability that a particular skill will succeed.

A skill in this sense is a policy that performs some short skill $\pi \in Pi$, such as picking up a particular object. There is also an affordance function, $p(c_{\pi}|s, l_{\pi})$ which corresponds to the value function for a skill if we take the reward of 1 to be a success case.

The idea is then that when you generate, you score beams based on this probability. Eg generate many beams with different completions, and take the one that maximizes $p(c_{\pi}|s, l_{\pi})p(l_{\pi}|i)$

![[saycan_architecture.png]]

# How to train the skills

Behaviour Cloning: Use demonstrations , building on top of [[bcz_zero_shot_task_generalization_language]].

Reinforcement Learning: Transform images using RetinaGAN.

551 labelled skills that span set of seven skill families and 17 objects

# Rollouts

"I left out a coke, apple and water, can you throw them away and then bring me a sponge to wipe the table?"

Failure cases:
 - Negatives
 - Early termination
 - Ambiguous references