---
title: CoDA: Contrast-enhanced and Diversity-promoting Data Augmentation for Natural Language Understanding.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/QuSSSC021
ee: https://openreview.net/forum?id=Ozk9MrX1hvA
url: https://dblp.org/rec/conf/iclr/QuSSSC021
authors: ["Yanru Qu", "Dinghan Shen", "Yelong Shen", "Sandra Sajeev", "Weizhu Chen", "Jiawei Han"]
sync_version: 3
cite_key: conf/iclr/QuSSSC021
---
# CODA: Contrast Enhanced Diversity Promoting Data Augmentation for NLU

Designing label-preserving transformations for text data is hard.

Propose a novel framework which synthesizes diverse samples.

Contrastive regularization objective is introduced.

Semantic meaning of a sentence is much more sensitive to local perturbations.

Three strategies:

 (a) Random combination
 (b) Mixup
 (c) Sequential stacking.


 ![[label_preserving_transformations_nlp.png]]
 Consistency loss is employed to capture the local inforamtion.

 Contrastive regularization:

  - Incorporate global information.
  - Augmented data should be closer in the original data space. Maximize the similarity to original sample and minimize similarity to other training samples.


Overall objective: take local and global information.

Stacking adversarial training over a back-translation module can give rise to a more diverse and informative augmented samples.