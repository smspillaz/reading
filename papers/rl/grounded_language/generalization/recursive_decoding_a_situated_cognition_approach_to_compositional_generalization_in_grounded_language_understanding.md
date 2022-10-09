---
title: "Recursive Decoding - A Situated Cognition Approach to Compositional Generation in Grounded Language Understanding."
venue: "CoRR"
volume: "abs/2201.11766"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2201-11766"
ee: "https://arxiv.org/abs/2201.11766"
url: "https://dblp.org/rec/journals/corr/abs-2201-11766"
authors: ["Matthew Setzler", "Scott Howland", "Lauren A. Phillips"]
sync_version: 3
cite_key: "journals/corr/abs-2201-11766/Setzler/2022"
---

Compositional Generalization is a blind spot for NNLMs.

Less work has focused on generating novel combinations of known outputs. Here we focus on the latter "decode side" of generalization within the context of gSCAN.

Present "recursive decoding", a novel procedure for trianing and using seq2seq models.

Rather than decode all-at-once, predict one token at a time, then the inputs are incrementally updated based on predicted tokens and re-encoded for the next decoder step.

Therefore, RD decomposes a complex ood sequence task to a series of incremental predictions which each resemble what hte model has already seen during training.

In this work, focus on the "novel direction" and "length extrapolation" tasks.

A summary of what happens here is that you take an action, observe the next state, then take another action. Its basically treating the problem as an MDP.