---
title: Systematic Generalization on gSCAN - What is Nearly Solved and What is Next?
venue: EMNLP
pages: 2180-2188
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/emnlp/QiuH0SS21
doi: 10.18653/V1/2021.EMNLP-MAIN.166
ee: https://doi.org/10.18653/v1/2021.emnlp-main.166
url: https://dblp.org/rec/conf/emnlp/QiuH0SS21
authors: ["Linlu Qiu", "Hexiang Hu", "Bowen Zhang", "Peter Shaw", "Fei Sha"]
sync_version: 3
cite_key: conf/emnlp/QiuH0SS21
---

Analyze grounded scan through a big multi-modal transformer.

They also analyze data efficiency. You need about 40% of the original 360,000 training examples, so sample complexity is important.

# Experimental Setup
![[compositional_generalization_gscan_what_is_nearly_solved_exact_matches.png]]

"Exact match" means that you do exactly what the expert does.

99.90 and 99.25 on splits B and C is very strong performance.

Unsolved splits:

 - D: Novel Direction: Targets are *south west* of the agent. We have seen south, west and other combinations but not *south west*.
 - G: Adverb k = 1: Commands with "cautiously", but you only see a few shots of them. You have to generalize to all other sequences from seeing "cautiously" a few times.
 - H: Adverb-to-verb: In this case you have to "pull while spinning". We know what it means to go to an object "while spinning", but not to pull one while spinning. The errors are not due to errors in visual grounding, they're errors in combining the action sequences.

# Archictecture

![[compositional_generalization_gscan_what_is_nearly_solved_ablations_of_transformer.png]]

ViLBERT. Convolutional cross-attention.

What matters? Ablation study

# Extended Task

"Relative" spatial relations are hard.

"Grounded Spatial Relation" Compositional Generalization Task. Very relational.

Contains language expressions that refer to target objects along with their relations to a referent object.

 - Next to
 - North/west/south/east of

"Blue square next to a red circle" or "blue square north of a red circle".

Also create visual distractors in the environment, eg, blue squares north of other objects.

Splits:

 * I: Random: In-distribution
 * II: Visual: Red squares are the target or reference. Other things have been the target or the referent but not red squares. Transformer: 64% success.
 * III Relational: Green squares and blue circles combinations
 * IV: Referent: Yellow squares are referred to as the target. Eg, "Push a small yellow square west of a green big cylinder". 
 * V: Relative Position 1: Targets are north of their referent. Nothing has ever been "north" before. Transformer 59.29%
 * VI: Relative Position 2: Targets are west of their referent. Nothing has ever been "west" before. Transformer 49.50%

# Sample Complexity

![[compositional_generalization_gscan_transformer_sample_complexity.png]]

The model without cross-modal attention is even more data inefficient, performance drops significantly when using less than 70% of the training data.

With cross-modal attention you start losing performance at 144,000 samples.

Things also get worse when you reduce the number of promitives. Here they removed one noun, one color and one adverb and this reduces the data to 110,000 and 74,000 training samples. In this case you need *an even greater proportion* data to make it work - almost 90-100% for splits B and C.

![[compositional_generalization_gscan_transformer_sample_complexity_removed_objects.png]]