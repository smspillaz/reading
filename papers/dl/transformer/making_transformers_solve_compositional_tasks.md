---
title: Making Transformers Solve Compositional Tasks.
venue: CoRR
volume: abs/2108.04378
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2108-04378
ee: https://arxiv.org/abs/2108.04378
url: https://dblp.org/rec/journals/corr/abs-2108-04378
authors: ["Santiago Onta\u00f1\u00f3n", "Joshua Ainslie", "Vaclav Cvicek", "Zachary Fisher"]
sync_version: 3
cite_key: journals/corr/abs-2108-04378/Ontanon/2021
---
In this paper, explore the design space of transforemr models showing that certain design decisions impact compositional generalization.

Some transformer configurations generalize compositionally better than others.

Eg, "jump" -> "jump twice". "jax" -> "jax twice".

There are several different design decisions that can result in different inductive biases, including:
 - Weight sharing
 - Hyperparameter configurations
 - Formulation of the target task

Use a collection of twelve compositional generalization datasets, including SCAN, PCFG, COGS, CFQ and basic algorithmic tasks.

A key contribution of this paper is to challenge the common assumption that Transformer's *dont* generalize compositionally.

# Datasets and Tasks

 - Add: Add two numbers and carry
 - AddNegative: Add two numbers but some are negative
 - Reverse: Output is expected in reverse order, where training and test sets are disjoint and test sets are a little longer
 - Duplication: Input is a string and the output should be the same sequence repeated twice
 - Cartesian product: Input is two sequences, output is cartesian product
 - Intersetion: Output is 1 if they have a non-empty intersection
 - SCAN-length
 - SCAN-add-jump
 - PCFG-productivity
 - PCFG-systematicity
 - COGS
 - CFG-mcd1

# Architecture

![[making_transformers_solve_compositional_tasks_architecture.png]]

## Positional Encodings
 - rel-e: Relative positional encodings, where the "relative label" defines a learnable mebedding that is added to the key during the attention process
 - rel-b: Relative positional encodings, where you have a learnable bias added to the attention
 - rel-eb: Both wieght and bias

Result: Any time of relative positional encodings help, but using embeddings helps mroe than using bias terms. Allows the model to learn a position invariant pattern that generalizes better.

## Decoder Type

Copy Decoder: Mix probability of generated tokens times probability of just copying the input at that position.

## Model Size

Size helps for more complex datasets, but you don't need big models for simple probl;ems.

## Weight Sharing

Share weights across layers in the encoder and decoder.

Weight sharing boosts compositional generalization accurracy. This is good for operations where you have to repeat operations over and over again.

## Immediate representation

Framing the task differently - instead of sequence-to-sequence, sequence-tagging.