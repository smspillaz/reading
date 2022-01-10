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