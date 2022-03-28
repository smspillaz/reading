---
title: Emerging Properties in Self-Supervised Vision Transformers.
venue: ICCV
pages: 9630-9640
year: 2021
type: Conference and Workshop Papers
access: closed
key: conf/iccv/CaronTMJMBJ21
doi: 10.1109/ICCV48922.2021.00951
ee: https://doi.org/10.1109/ICCV48922.2021.00951
url: https://dblp.org/rec/conf/iccv/CaronTMJMBJ21
authors: ["Mathilde Caron", "Hugo Touvron", "Ishan Misra", "Herv\u00e9 J\u00e9gou", "Julien Mairal", "Piotr Bojanowski", "Armand Joulin"]
sync_version: 3
cite_key: conf/iccv/CaronTMJMBJ21
---

Cool plots showing unsupervised segmentation / salience maps.

Method for self-supervised learning. The basic idea is self-supervised learning with ViT.

ViT should really shine with unsupervised learning beacuse that's what NLP transformers do. Remember MLM with BERT.

Vision Transformers are preferable to convnets because ... ?

Self-supervised strategy:

 - Augment data with different views, SimCLR style.
 - Two global views, more local views.
 - Train a student network to match a teacher network. Each network has the same architecture and different weights. EMA-based weight update. Barlow-twins style?
 - Centering: Prevents the teacher network from being too dominant in one dimension.
 - Something weird: why do you do cross-entropy of a softmax?
 - This framework has no concept of negative samples.

What to do downstream?
 1. Image Retrieval (can train on arbitrary collectiosn of images to learn embeddings to retrieve most similar images in another dataset)
 2. Copy detection: Can you recognize pairs of images where one is a distortion of another.


Attention maps:
![[dino_attention_maps.png]]

Transformer has different heads and different heads look at different parts of the image.

