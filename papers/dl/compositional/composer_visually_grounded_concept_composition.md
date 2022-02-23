---
title: Visually Grounded Concept Composition.
venue: EMNLP
pages: 201-215
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/emnlp/0002HQSS21
doi: 10.18653/V1/2021.FINDINGS-EMNLP.20
ee: https://doi.org/10.18653/v1/2021.findings-emnlp.20
url: https://dblp.org/rec/conf/emnlp/0002HQSS21
authors: ["Bowen Zhang", "Hexiang Hu", "Linlu Qiu", "Peter Shaw", "Fei Sha"]
sync_version: 3
cite_key: conf/emnlp/0002HQSS21
---

Proposes a "Concept and Relation Graph" which builds pon top of constituency analysis and consists of recursively combined concepts with predicates.

The CRG is a graph-structured database where concept nodes encode language expressions of concepts and their visual denotationes. Predicate nodes define how a concept is semantically composed of its children.

Concept Composition Transformer (Composer). Performs hierarhical learning of visual-semantic alignment.

# The Concept and Relation Graph
![[composer_concept_and_relation_graph.png]]

Concepts are higher level, primitives are lower-level. Concepts come from applying predictes to primitives.

Another way of looking at it - a single image is a concept, but it is linked to many "reference images" through arguments of its predictes.

## How to identify the concepts and relations
1. Parse the sentence into a constituency tree
2. Relations are n-ary functions with placeholders
3. Simpler concepts can be arguments to the predicates.


 Text/image pairs. Group all the images that refer to the same concept to form the image denotation.

 An "image denotation" is a set of images that contain the referred to concept.

 Example: "ball" is all images containing the word "ball".

 ## Composer Architecture
 ![[composer_architecture.png]]

 Main idea: recursively compose primitives into sentences using predicates.

Take the primitive word embeddings as the inputs and perform cross-modal attention to obtain visually grounded word embeddings. Use an object detector to get object-centric features (eg, region proposals and their corresponding embeddings).

Then call the "composition procedure"

![[composer_composition_procedure.png]]

Use the word embeddings to query the viual features.

Represent predicates as "template sentences". Eg, "(NP1) running on (NP2)" and encode them with the predicate transformer.

To do the composition, take the encoded predicates and primitives and put them through some feedforward net. Eg, "a man" gets combined with "NP1". "running" stays the same, "the field" gets combined with NP2 etc.

Then do attention between each piece of the sentence infused with its argument/word information and the object centric visual features and read the output of the classification token to get the object-centric visusal features.

# Alignment score

$$
s(x, y) = \theta^T \cdot v(x, y) \propto p(x, y)
$$

eg, we learn the probability that image x corresponds to sentence y. Minimize the negative log likelihood.

## Multi-Level visual-semantic alignment

We can extend the alignment to learning objectives to all those intermediate concepts

Triplet hinge-loss. Derive negative concepts form negative sentences in the dataset. Negative concepts are a bit noisier than the ones at the sentence level because many common objects presented in the positive image are also common objects in other images and this can lead to ambiguity. Hinge loss is a littlem ore robust to this sort of label noise.

$$
l_{\text{MVSA}} = \sum_i \sum_{c \in C} \max(0, \alpha - s(x_i, c) + s(x_i, c^{-})) + \max(0, \alpha - s(x_i, c) + s(x_i^{-}, c))
$$

Eg, we ensure that we match a positive pair more strongly than a negative one.

## Learning to preserve orders in the tree

$$
l_{\text{order}} = \sum_i \sum_{e_{jk}} \max(0, \beta - s(x_i, c_j) + s(x_i, c_k))
$$

$e_{jk}$ is an edge connecting $c_j$ and $c_{k}$ with $c_j$ as the parent and $c_k$ closer to the predicate. $\beta$ is the margin. $x_i$ is the image.

Basically, this ensures that $c_j$ matches the image more than $c_j$. So as you go up the tree, you have a closer matching score.

# Experiments

Compare Composer with ViLBERT and VSE.

![[composer_zero_shot_cross_dataset_transfer.png]]

They look at Zero-shot cross-dataset transfer and compositional generalization.

They crate 16 test splits wiht different compound divergence. COMPOSER is more robust to distribution shit (25% relative improvement).

## Ablation Study

### Choice of modulator

Use FiLM to combine primitive/relation embeddings.

### MSVA Supervision

This helps a little bit.

## Interpretability
![[composer_interpretability.png]]

