---
title: "Explainable Semantic Space by Grounding Language to Vision with Cross-Modal Contrastive Learning."
venue: "CoRR"
volume: "abs/2111.07180"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2111-07180"
ee: "https://arxiv.org/abs/2111.07180"
url: "https://dblp.org/rec/journals/corr/abs-2111-07180"
authors: ["Yizhen Zhang", "Minkyu Choi", "Kuan Han", "Zhongming Liu"]
sync_version: 3
cite_key: "journals/corr/abs-2111-07180/Zhang/2021"
---

Designs a two-stream model for grounding language learning in vision.

1. VGG-based visual stream
2. BERT-based language stream

Merge the two streams into a joint representational space and do cross-modal constrastive learning.

## Context

Humans take a longer time to name a colored word when the color and the word mismatch. Eg, language is learned by grounding, not by reading.

In this paper, train a languaeg model and a vision model jointly and analyze the semantic space to see if there's a match between visual attributes and words.

Distributional Hypothesis: Words occurring in similar contexts carry similar meanings.

Symbol Grounding Hypothesis: A word is connected to tis meaning by relating to its referent in the physical world.

Cross-modal contastive learning is still under-explored for higher-level tasks like VQA, visual reasoning, scene graph generation etc.

## Approach

The visual stream is based on VGG16 with an additional linear transformation and embedded to match the feature dimension of the lanuguage stream and additional MHA to enforce global information aggregation and learn long-range dependencies.

Project both the VGG16 encoding and BERT encodings into a shared space. Take the inner product between $V$ at each location (eg, treat each pixel as a vector of channel states) and $L$ to get a 3D match-map.

Then compute the contrastive loss ujsing temperature-scaled cross-entropy (anchro samples from one modality and positive/negative samples from the other modality), see [[scaling_up_visual_and_vision_language_representation_learning_noisy_text]]


### Visual Grounding of Object Relations

![[visual_object_grounding.png]]

Finetune the model for visual relation prediction.

Remove the linear transformation heads and add MHA cross-attention. Query is an object word embedding from the language stream, keys and values from every location in the feature map output in the visual stream. Take the attention weighted values and concatenate them to generate visually-grounded object representation.

#### Prediction of relationships between objects with such a representation

Apply a "bilinear relation module", pictured above.

Subject times predicate times object:

$$
r_s R_p r^T_o
$$

For example (elephant, in, water pond).

The predicate is a "learnable bilinear operator". The grounded representations are linearly transformed into a subspace (denotes $r_s$ and $r_o$).

Then we can also use contrastive learning here - take the cross-entropy loss between an anchor, a positive sample and a negative sample. Here the negative samples are "other relations" (eg, if the elephant is in the water pond, it is not away from the water pond). The negative samples can also be other objects, (eg, if the elephant is in the water pond, it is not in the fridge).


## Experiments

1. Human rating of concreteness correlated with first principal component of the grounded semantic space.
2. Clustering of word representations. Calculate the silhouette coefficient to measure clustering strength of visually grounded words.
3. Visually informed compositional reasoning
4. Multimodal image search