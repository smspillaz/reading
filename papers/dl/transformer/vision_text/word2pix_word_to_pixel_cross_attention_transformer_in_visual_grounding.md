---
title: Word2Pix - Word to Pixel Cross Attention Transformer in Visual Grounding.
venue: CoRR
volume: abs/2108.00205
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2108-00205
ee: https://arxiv.org/abs/2108.00205
url: https://dblp.org/rec/journals/corr/abs-2108-00205
authors: ["Heng Zhao", "Joey Tianyi Zhou", "Yew-Soon Ong"]
sync_version: 3
cite_key: journals/corr/abs-2108-00205/Zhao/2021
---

![[word2pix_architecture.png]]

![[word2pix_architecture_2.png]]

Typical methods encode the image and sentence first, which means that you neglect words which are less important for sentence embedding but important for visual grounding.

This paper proposes a network that gives each word from the query an opportunity to attend to the pixels.

This paper examines one-stage methods as opposed to two-stage methods. One stage methods are fast, but one problem with them is that you have to encode the query into a single vector.

Example "cat sitting under the chair". A major component is "cat", "sitting" and "chair". "under" is not so important because it could be replaced with another word that gives the same subsequent word distribution. As a result, information from "under" is lost in the sentence embedding, meaning that you don't change your attention to the cat under the chair in the image above and keep your attention on the cat sitting on the chair.

## Main Contributions

1. Word2Pix
2. Formulation for word-to-pixel attention via an encoder-decoder transformer architecture for visual grounding.
3. Improved performance.


## Architecture

The word2pix attention branch is attention between words and pixels. The way it works is that you first process the image with a backbone CNN, then flatten the pixels such that each pixel is a vector of channels. Each pixel also has a spatial positional encoding attached to it.

Then do multi-head cross-attention.

To predict the targets, regress from the (cls) token.