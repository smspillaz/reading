---
title: Grounded Language Learning in a Simulated 3D World.
venue: CoRR
volume: abs/1706.06551
year: 2017
type: Informal Publications
access: open
key: journals/corr/HermannHGWFSSCJ17
ee: http://arxiv.org/abs/1706.06551
url: https://dblp.org/rec/journals/corr/HermannHGWFSSCJ17
authors: ["Karl Moritz Hermann", "Felix Hill", "Simon Green", "Fumin Wang", "Ryan Faulkner", "Hubert Soyer", "David Szepesvari", "Wojciech Marian Czarnecki", "Max Jaderberg", "Denis Teplyashin", "Marcus Wainwright", "Chris Apps", "Demis Hassabis", "Phil Blunsom"]
sync_version: 3
cite_key: journals/corr/HermannHGWFSSCJ17/Hermann/2017
---
Presents an agent that learns to interpret langauge in a simulated 3D environment.

The main findings of the paper:
 - The agent "learns to relate linguistic symbols and emergent perceptual representaitons of its physical surroundings and pertinent seuqences of actions"
 - The agent's comprehension "extends beyond prior experience and enables it to apply 'familiar language' to 'unfamiliar situations'"
 - Language leanring is contingent on a combination of reinforcement and unsupervised learning
 - The semantic knowledge gained generalizes zero-shot to "new situations" and "new language".


## Environment

3D world. Multiple episodes in a room containing two objects.

Agent spawned in a position equidistant from both objects. Must go to the object that matches the description.

## Necessity of unsupervised learning
Early simulation results revealed that an initial actor-critic design *does not learn to solve even comparably simple tasks* in the setup.

The reward signal is *too weak* which makes sample efficiency and learning *too difficult*.

Propose to instead use some unsupervised learning to try and boost sample efficiency during RL:

 1. **Temporal Autoencoding**: Predict $o_{t + 1}|o_t, a_t$
 2. **Language Prediction**: Predict $w_{t + 1}|w_t$
 3. **Reward Prediction**
 4. **Value Replay**

The more unsupervised learning tasks you use, the faster the learning. Though the fastest learning method reaches its inflection point of reward change at around 1,000,000 episodes.

## Word learning is much faster if words are already known


Word learning is a lot faster if the agent already knows a certain number of words outside the training set. In this case you can get to convergence at around 100,000 episodes as opposed to 1 million.


## One-shot learning

In natural language you have the ability to "compose" the meanings of known words to intepret otherwise unknown prhases.

Colour-shape composition experiment. 40 shape and 13 colour terms. Some are excluded from the training set. Study done of:

1. **Composition**: All shape and color unigrams and 90\% of possible colour-shape bigrams, test on the remaining 10\% (so you know what a blue object is, you know what a blue ladder is, do you know what a blue box is?)
2. **Decomposition-composition**: No training on unigrams
3. **Lighter/Darker**: Intepret the term "lighter / darker" as it relates to unseen colours
4. **Relative size**: Interpret the term "larger" and "smaller" as it relates to unseen objects


## Curriculum Learning

Applied a curriculum to train the agent on a range of multi-word referring instructions such as "pick the X" where X rpresents a string consisting of either a noun or an adjective-noun.

## Multi-task learning

Follow instructions consisting of many independent subtasks, for example "pick the X object" or "pick all X".

**Selection**: Pick the X or pick all X
**Next to**: Pick up X next to Y
**In room**: Pick the X in Y room

A curriculum is requierd to achieve the best possible agent performance on these tasks.