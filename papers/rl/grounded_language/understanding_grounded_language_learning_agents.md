---
title: "Understanding Grounded Language Learning Agents."
venue: "CoRR"
volume: "abs/1710.09867"
year: 2017
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-1710-09867"
ee: "http://arxiv.org/abs/1710.09867"
url: "https://dblp.org/rec/journals/corr/abs-1710-09867"
authors: ["Felix Hill", "Karl Moritz Hermann", "Phil Blunsom", "Stephen Clark"]
sync_version: 3
cite_key: "journals/corr/abs-1710-09867/Hill/2017"
---
# Understanding Grounded Language Learning Agents

Studies why it is that models with no meaningful prior knowlege can overcome the obstacle of symbol grounding.

Address the question in a way of achieving a clearer general understanding of grounded language leanring, both to inform future research and to improve confidence in model predictions.

This paper seeks to get a better undrestanidng of neural network mdoels of grounded language learning.

Principal findings are as follows:

 1. Shape/colour bias: When the agent is trained on an equal number of shape and colour words, agents identify using colour as opposed to shape.
 2. Learning negation: If trained on small amounts of data, does not generalize
 3. Curriculum efffects for vocabulary growth: More words learned more quickly if the range of words to which the agent is exposed is limited at first and then expanded gradually.
 4. Semantic processing and representaiton differences: Agents learn words of different semantic classes at different speeds and represents them with features that require different degrees of visual processing depth.