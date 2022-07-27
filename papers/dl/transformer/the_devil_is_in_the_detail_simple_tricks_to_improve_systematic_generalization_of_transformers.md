---
title: The Devil is in the Detail: Simple Tricks to Improve Systematic Generalization of Transformers
---

Revisit relative position encoding, [[universal_transformers|universal transformer]] variants, embedding scaling.

Test on SCAN, CFQ, COGS, Mathematic, PCFG.

# Universal Transformers - Relevance

Universal Transformers are basically transformers with weight sharing between the layers, without adaptive computation time.

Universal Transformers are important in cases where you don't want to be sensitive to the order of operation that are seen, or you want to re-use the same operation multiple times.

# Improving on Systematic Generalization

## EOS Decision Problem

How to generalize to a longer sequence length? EOS often overfits to a specific position.

Overcome this with relative positional embeddings.

## Model Selection

Early stopping is dangerous, especially on the IID validation set.

![[devil_is_in_the_details_early_stopping.png]]

If you do early stopping too early , you miss out on a lot of generalization accurracy.

## Validation Splits for Generalization

Measuring performance on the IID split does not tell you anything about generalization. Future datasets should have both an IID split and a generalization split.

## Embedding Scaling

1. Token Embedding Upscaling: Sinusoidal PE is in the range -1, 1, but regular embeddings have a different magnitude meaning that positional encoding is irrelevant. To solve this, scale by $\sqrt{d_{\text{modl}}}$
2. No scaling: Initialize word embeddings with normal distribution
3. Position Embedding Downscaling: Scale position embeddings by $\frac{1}{\sqrt{d_{\text{model}}}}$

PED performs best on both PCFG and COGS.

# Overall Results

Universal Transformers with Relative PE helps a lot here. Particularly on SCAN length generalization tasks.