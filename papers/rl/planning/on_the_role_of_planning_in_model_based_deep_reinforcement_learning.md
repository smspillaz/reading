---
title: On the role of planning in model-based deep reinforcement learning.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/HamrickFBGVWABV21
ee: https://openreview.net/forum?id=IrM64DGB21
url: https://dblp.org/rec/conf/iclr/HamrickFBGVWABV21
authors: ["Jessica B. Hamrick", "Abram L. Friesen", "Feryal Behbahani", "Arthur Guez", "Fabio Viola", "Sims Witherspoon", "Thomas Anthony", "Lars Holger Buesing", "Petar Velickovic", "Theophane Weber"]
sync_version: 3
cite_key: conf/iclr/HamrickFBGVWABV21
---
# On the Role of Planning in MBRL

Research questions:
 - How does planning help?
 -  Within planning, what algorithmic choices drive performance?
 -  To what extent does planning improve zero-shot generalization?


MuZero: Different ways of utilizing search or to compute targets.

 - This is an important driver of performance over a one-step method. Most useful for constructing targets for learning and taking actions for training. Search at test time adds very little. It constructs better learning targets and data distributions.


What algorithmic choices in planning drive performance?

 - Search tree depth: In muZero we allow it to get as deep as it once, relatively shallow depth of 2 gives good enough performance
 - UCT depth to balance exploration and exploitation: A depth of 1, a much simpler and easier to implement form of planning
 - Budget, how many simulations: A moderate amount, say around 10, gives the best performance. Number of simulations is the most important hyperparameter

Generalizaton?
 - Additional search at test time doesn't help.
 - Does deeper planning make things worse? Even with a perfect model, we see only small benefits. Its not just the fact that you get compounding error from planner inaccuracy.
 - Other learned components besides the model could be affecting performance
 - Try breadth first search: Any amount of planning hurts performance, evaluating the value function outside the data distribution doesn't work.
 - New mazes: Randomly generated mazes. Test it on a hand-crafted test level - with a learned model, planning too deep actually makes things worse.


Conclusions:
 - Simple shallow forms of planning are sufficient in many existing domains
 - We need different and more diverse environments to evaluate MBRL
 - Planning bottlenecked by failure of learned components such as policy and value models