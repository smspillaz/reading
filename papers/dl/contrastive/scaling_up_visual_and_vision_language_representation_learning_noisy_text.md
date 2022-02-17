---
title: Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision.
venue: ICML
pages: 4904-4916
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/icml/JiaYXCPPLSLD21
ee: http://proceedings.mlr.press/v139/jia21b.html
url: https://dblp.org/rec/conf/icml/JiaYXCPPLSLD21
authors: ["Chao Jia", "Yinfei Yang", "Ye Xia", "Yi-Ting Chen", "Zarana Parekh", "Hieu Pham", "Quoc V. Le", "Yun-Hsuan Sung", "Zhen Li", "Tom Duerig"]
sync_version: 3
cite_key: conf/icml/JiaYXCPPLSLD21
---

Vision-language datasets rely on curated training datasets that are expensive or reqire expert knowledge.

In this paper, leverage a noisy dataset over one-billion image alt-text pairs.

Use a simple dual-encoder architecture to align vision and language representaitons of an image and use the scale of the corpus to make up for the fact that there's noise in the labels.

To train the model, use a vision/language alignment objective with a simple dual-encoder architecture.

The model is called ALIGN (A Large Scale Image and Noisy Text Embedding).

Learn the encoders via a contrastive loss pushing matching examples together and non-matching examples apart. The key difference is that the text encoder generates the "label" weights. Then do zero-shot transfer.

## Related Work

[[clip_learning_transferable_visual_models_nl_supervision]] . The main difference to CLIP is that CLIP filters their data, in this work they do not filter their data and permit then noisy labels.

Visual Semantic Embeddings.


## Dataset

Trade quality for scale by relaxing most of the cleaning steps. Apply only "minimal frequency-based filtering".

Remove porn, remove small images, remove weird aspect ratio images. Remove equal images with more than 1000 associated alt-texts. Remove any images that are in the zero-shot test sets.

Remove alt-texts shared by more than 10 images or rare tokens.

## Pre-training

Pair of image and text encoders with a cosine similarity combination function at the top. EfficientNet for images and BERT for text.

Minimize image-to-text cross-entropy contrastive loss and text-to-image cross-entropy contrastive loss.

Use normalized embeddings.

## Transfer

- Visual classification on ImageNet
- Image retrieval
- Zero-shot visual classification