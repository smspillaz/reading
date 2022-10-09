---
title: "ReaSCAN - Compositional Reasoning in Language Grounding."
venue: "CoRR"
volume: "abs/2109.08994"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2109-08994"
ee: "https://arxiv.org/abs/2109.08994"
url: "https://dblp.org/rec/journals/corr/abs-2109-08994"
authors: ["Zhengxuan Wu", "Elisa Kreiss", "Desmond C. Ong", "Christopher Potts"]
sync_version: 3
cite_key: "journals/corr/abs-2109-08994/Wu/2021"
---

gSCAN's constrained design means that it does not reqire compositional interpretation and many details of its instructions are actually not required for task success.

Proposes ReaSCAN, which requires reasoning about entities and reliations. Shows that ReaSCAN is much harder for both a multi-modal baseline and a GCN.

gSCAN has three major limitations

1. Its set of instructions is so constrained that preserving the linguistic structure of the command is not required. You can scramble the order of the words and it will still work.
2. The distractor objects are mostly not relevant to accurate understanding. For example in "go to the yellow square", the color and shape feature is only required in 62.7% of test samples. In the other stratum, it is sufficient to go to a yellow object or a square. There's also "go to a red square" where "red" is never seen with "square", but you only need both "red" and "square" to solve 62.5% of test examples.
	1. Also the distractor sampling is biased. Eg, if hte utterance mentions "blue circle", then you have all possible objects that aren't blue circles. Due to the distractor sampling, simple descriptions will have only one distractor whereas more complex descriptions have more distractors.
	2. Too few effective distractors
3. In many examples, not all modifiers in the command are actually required

# Differences to gSCAN
![[reascan_differences_to_gscan.png]]

ReaSCAN is similar to gSCAN but the structure of the gridworld differs.

Eg, "walk to the small square that is inside of a yellow box cautiously". or "pull the square that is in the same column as a blue cylinder and the same row as a small red circle while spinning".

ReaSCAN requires both compositional language interpretation and also complex reasoning about entities and relations.

The models that work well on gSCAN solve some of hte simpler splits on ReaSCAN but not all of them.

ReaSCAN extends gSCAN while maintaining two desiderata:

1. Word order permutations will lead to ambiguities.
2. Identity of the referent depends on reasoning about multiple distractor objects in the world.


## Distractor Sampling

Distractors must reliably introduce uncertainty about the identity of the target.

Eg, target is a small red circle. A large red circle would compete in the size dimension. Distractors that have little in common are weak distractors.

1. Attribute based distractors: Compete with a target if the model struggles with size, color and shape features
2. Isomorphism based distractors: Become potential targets after word order permutations of the command
3. Relation based distractors: ensure that relative clauses are required, because there are other objects which match the object description exactly.

# Splits

![[reascan_splits.png]]

A2 Novel color: Red squares are never targets, red squares are also not referents. But different sized red squares are seen as non-targets. Also make sure that the color attribute is necessary for identifying the target referent.

This split is "sligtly harder" for both models

Novel size: Same thing, but with size.

B1 Novel co-occurrence of concepts: First collect all objects mentioned in the training set, then construct commands with known objects that don't co-occur during training.

C1: Novel conjunctive clause length

C2: Novel relative clauses

# Baselines

[[think_before_you_act_a_simple_baseline_for_compositional_generalization]]

[[gscan_grounded_language_benchmarks]]

