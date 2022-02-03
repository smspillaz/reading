# Attention over Learned Object Embeddings Enabled Complex Visual Reasoning

https://neurips.cc/virtual/2021/session/44815

Causal inference task - ACRE

Confounding variables. Cannot infer that the gray cylinder caused the activation of the platform.

Object permanence - trakcing objects across frames.

Dynamics Prediction - CLEVERER. What will happen next in a video.

Counterfactual reasoning - what would have happened without object X?

Previously required bespoke models or inductive biases.

## Contribution (ALOE)

Attention over learned object embeddings

Combines:
 - Self-attention
 - Learned object embeddings
 - Self-supervision

Objects are "words" for visual tasks.

 - What's the right level of abstraction to attend over?
	 - Image patches
	 - Frame level information bundles?

Use attention on objects. Use MONet - an unsupervised object segmentation moel, to obtain objects for each video.

## Architecture

 - Use MoNET to get the object word embeddings
 - Get word inputs + embeddings
 - Transformer + position encoding
 - Answer from classification token
 - Universal-transformer style architecture

Training:
 - Self-masking
 - Different masking schemes
	 - Frames
	 - Objects
	 - Words


Self-supervision improves data efficiency. Auxiliary loss is the masking loss.