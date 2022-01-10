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
