---
title: Data Determines Distributional Robustness in Contrastive Language Image Pre-training (CLIP).
venue: ICML
pages: 6216-6234
year: 2022
type: Conference and Workshop Papers
access: open
key: conf/icml/FangIWWSDS22
ee: https://proceedings.mlr.press/v162/fang22a.html
url: https://dblp.org/rec/conf/icml/FangIWWSDS22
authors: ["Alex Fang", "Gabriel Ilharco", "Mitchell Wortsman", "Yuhao Wan", "Vaishaal Shankar", "Achal Dave", "Ludwig Schmidt"]
sync_version: 3
cite_key: conf/icml/FangIWWSDS22
---
Why are CLIP/ALIGN/BASIC robust to distribution shifts? This paper attempts to answer that question through systematic experimental investigation.

There are five possible causes:
 - Training set size
 - Traiing distribution
 - Language supervision at training time
 - Language supervision at test time
 - Constrastive loss function

The experiments show that the most diverse the training distribution, the more robust the model. The other factors don't really contribute all that much.

There's a couple of image distribution shifts:
 - ImageNet V2 (a reproduction of ImageNet with distribution shift in the validation set due to changes in the crowdsourcing process)
 - ImageNet-Sketch: Blach/white sketches of ImageNet
 - ImageNet-R: Renditions of 200 ImageNet classes
 - ObjectNet: Real-world objects from ImageNet with random backgrounds
 - Image-Net-A: Filtered examples so that they are misclassified.