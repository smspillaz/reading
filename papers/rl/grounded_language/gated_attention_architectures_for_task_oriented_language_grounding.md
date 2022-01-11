---
title: Gated-Attention Architectures for Task-Oriented Language Grounding.
venue: AAAI
pages: 2819-2826
year: 2018
type: Conference and Workshop Papers
access: open
key: conf/aaai/ChaplotSPRS18
ee: https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/17425
url: https://dblp.org/rec/conf/aaai/ChaplotSPRS18
authors: ["Devendra Singh Chaplot", "Kanthashree Mysore Sathyendra", "Rama Kumar Pasumarthi", "Dheeraj Rajagopal", "Ruslan Salakhutdinov"]
sync_version: 0
---
# Gated Attention architectures for generalization in task-oriented language grounding

Similar to FiLM - weight the channels by the components of the language encoding.

Flatten the output and pass to the policy model (with an LSTM in between).

They claim zero-shot generalization of 0.81 in the "easy" case.

Test set:

 * smallest red object
 * armor
 * short green pillar
 * green short pillar
 * pillar
 * tall blue torch
 * blue tall torch
 * blue short torch
 * blue keycard
 * yellow keycard
 * keycard
 * yellow skullkey
 * skullkey


All other combinations in training set