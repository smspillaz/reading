---
title: BabyAI - A Platform to Study the Sample Efficiency of Grounded Language Learning.
venue: ICLR
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/iclr/Chevalier-Boisvert19
ee: https://openreview.net/forum?id=rJeXCo0cYX
url: https://dblp.org/rec/conf/iclr/Chevalier-Boisvert19
authors: ["Maxime Chevalier-Boisvert", "Dzmitry Bahdanau", "Salem Lahlou", "Lucas Willems", "Chitwan Saharia", "Thien Huu Nguyen", "Yoshua Bengio"]
sync_version: 0
---
# BabyAI: A Platform to study the sample efficiency of grounded language learning

Abstract: Simulator with 19 levels of increasing difficulty, subset of English language.
Current deep learning methods are not very sample efficient in the context of learning a language
with compositional properties.

2D gridworld with synthetic natural-looking instructions. Uses curriculum learning. Provides
a bot agent that can be used to generate new demonstrations on the fly and advise the learner on
how to continue acting.

Current methods (Mei et al 2016, Hermann et al 2017) work but require lots of data, in terms of reward
function queries or demonstrations.

Features of BabyAI:
 - Environment manipulation (so having some sort of memory or environment update function would be useful)
 - Partial Observability
 - Systematic definition of synthetic language
 - Human-in-the-loop training


BabyLang:
 - Language is simple but contains 2.48 x 10^19 possible instructions.
 - Verifier to check if the agent's sequence of actions successfully achieves the goal.

BabyLevels:
 - Curriculum of 11 different tasks, each of increasing difficulty. Starts with navigation
   ends with composite instructions.

Bot Agent:
 - Bot knows how to solve all the problems. Baby doesn't know anything.


Baselines:
 - GRU to encode the instructions, CNN to encode the room layout.
 - Proximal Policy Optimization (PPO)
 - Required 20 to 50 GPUs over 2 weeks.

Results:
 - Success rate of 100% on simple tasks. 77% on more complex tasks. 1 Million Samples.
 - Paper comments that this is very inefficient.
 - Another approach: Measure sample efficiency on tasks - how many samples required to get to 99% success rate?
   - Imitation learning is promising here, but still takes 84310-12430 samples to work correctly. RL takes 15.9-18.4k
   - Harder tasks like GoTo required 341-408k samples to reach 99% success rate.
   - Curriculum Learning Helps, but only to an extent. Trying to pretrain using harder tasks doesn't help.
     In fact it makes things much worse than if you had pre-training.

## Related Papers

 - Language Models as Knowledge Bases: https://arxiv.org/abs/1909.01066
 - Language as an Abstraction for Hierarchical Deep RL: http://papers.nips.cc/paper/9139-language-as-an-abstraction-for-hierarchical-deep-reinforcement-learning
 - Working Memory Graphs: https://arxiv.org/abs/1911.07141