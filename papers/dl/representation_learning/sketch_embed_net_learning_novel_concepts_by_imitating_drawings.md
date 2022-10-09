---
title: "SketchEmbedNet - Learning Novel Concepts by Imitating Drawings."
venue: "ICML"
pages: "10870-10881"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/WangRZ21"
ee: "http://proceedings.mlr.press/v139/wang21s.html"
url: "https://dblp.org/rec/conf/icml/WangRZ21"
authors: ["Alexander Wang", "Mengye Ren", "Richard S. Zemel"]
sync_version: 3
cite_key: "conf/icml/WangRZ21"
---


# SketchEmbedNet: Representation learning by learning to sketch

Basic idea:
 - Pairs of images / sketches
 - Learn to make parameter to RNN which would produce sketch matching the corresponding sketch
 - Sketch comes from a "sketching program" / rasterizer.
 - Use the learned representations downstream.

The results are the most interesting bit, appears to outperform constrastive learning by a significant margin on both Omniglot and Quickdraw ($77.69 \to 94.88$ and $83.26 \to 96.96$)

Best performance is seen on 5-way 1-shot learning.

"Conceptual composition": Similar to word2vec, snowman - circle = square.

Discussion: Sketches are good for capturing shape in image

Obvious question: What about edge detection?