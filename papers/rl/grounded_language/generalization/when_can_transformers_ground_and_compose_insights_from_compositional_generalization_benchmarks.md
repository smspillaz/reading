---
tags: ["gSCAN"]
title: "When Can Transformers Ground and Compose: Insights from Compositional Generalization Benchmarks."
venue: "CoRR"
volume: "abs/2210.12786"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2210-12786"
doi: "10.48550/ARXIV.2210.12786"
ee: "https://doi.org/10.48550/arXiv.2210.12786"
url: "https://dblp.org/rec/journals/corr/abs-2210-12786"
authors: ["Ankur Sikarwar", "Arkil Patel", "Navin Goyal"]
sync_version: 3
cite_key: "journals/corr/abs-2210-12786/Sikarwar/2022"
---

They say that identifying the target location is the main challenge in these types of transformer models.

They also propose this RefEx task and show that a single self-attention layer can compositionally generalize to novel attributes (similar to [[compositional_generalization_in_grounded_language_learning_via_induced_model_sparsity]]).

Three contributions:
 - Grounded Compositional Transformer (which does just as well on GSRR and ReaSCAN).
 - The main difficulty is in identifying the target location rather than sequence generalization.
 - Why can transformers generalize? They propose RefEx to demonstrate how this happens.


## The Grounded Compositional Transformer

Encoder: Multi-scale CNN

Decoder: N transformer decoder blocks.

To improve the spatial representation, they tokenize the grid cells and project them to a higher dimension. Also include learnable positional encodings. They interleave self-attention with co-attention layers to allow intra-modal interaction before cross-modal interaction. So basically, they take [[systematic_generalization_on_gscan_what_is_nearly_solved_and_what_is_next]] and add self-attention.

Modified world state encoding: They modify the world state for ReaSCAN to disambiguate.

Basically it fixes the problem that Qiu had with the transformer on the GSRR and GroCoT splits.

The only hard splits that remain are B2, C1 and C2 from ReaSCAN.

## Analysis

 1. Target Identification from Encoder Representations: This is hard. Especially for C2, C1 and B2.
 2. Sequence identification from gold targets: This is easy. If you know the targets, navigating to them is trivial.
 3. Transformers can generalize to higher depths of relative clauses. Train on commands of depth 2 and test on commands of depth 3. They et 85.6% accurracy. That's actually pretty good, considering that depth recursion is a hard problem (see [[cogs_a_compositional_generalization_challenge_based_on_semantic_interpretation]]).


## RefEx

 - For two-attr task (eg, you have to compose color and shape attributes), a one-layer transformer can solve it. Same result as in [[compositional_generalization_in_grounded_language_learning_via_induced_model_sparsity]]
 - For three-attr task (color, size, shape): One-layer, one-head can still do it.
 - three-attr-rel task: you need at least 2 layers.


## References

 - On probing:
	 - [[a_mathematical_framework_for_transformer_circuits]]
	 - [[attention_is_not_only_a_weight_analyzing_transformers_with_vector_norms]]