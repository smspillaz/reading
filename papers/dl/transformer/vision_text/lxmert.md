---
title: "LXMERT - Learning Cross-Modality Encoder Representations from Transformers."
venue: "EMNLP/IJCNLP"
pages: "5099-5110"
year: 2019
type: "Conference and Workshop Papers"
access: "open"
key: "conf/emnlp/TanB19"
doi: "10.18653/V1/D19-1514"
ee: "https://doi.org/10.18653/v1/D19-1514"
url: "https://dblp.org/rec/conf/emnlp/TanB19"
authors: ["Hao Tan", "Mohit Bansal"]
sync_version: 3
cite_key: "conf/emnlp/TanB19"
---

Build a large-scale transformer with three encoders:
 - object-relationship
 - language encoder
 - cross-modality encoder

Pre-train the model with large amounts of image-and-sentence pairs with five representative pre-training tasks (MLM, masked object prediction, cross-modality matching and image-question answering). This helps to learn the intra-modality and cross-modality relationships. After fine-tuning, we get SOTA results on VQA and GQA.

The question this paper seeks to answer is "large-scale pretraining and fine-tuning studies for the modality pair of vision and language is still underdeveloped".

The framework is modelled after recent BERt-style innovations. Focuses on learning vision-and-language interactions, esepcailly for representaitons of a single image and its descriptive sentence.


## Architecture

![[lxmert_architecture.png]]

Two inputs: an image and a related sentence.

Each image is represented as a "sequence of objects".

Each sentence is a "sentence of words".

### Input Embeddings

**Word-Level Sentence Embeddings**: Word embeddings for WordPiece tokens, Index embeddings (similar to positional encoding, but learned, then LayerNorm)

**Object-level image embeddings**: Instead of Conv feature maps, run an object detection nework and get the embeddings for each object. These are called "RoI features", plus their positions.

### Self-attention

Over each modality separately

### Cross-Modality Encoders

Cross-attention between encoded object embeddings and encoded word embeddings.

Do self-attention on the outputs of the cross-attention layers.

### Output

The $k$th layer outputs are produced by feed-forward sub-layers.

Use the (cls) token as the embedding