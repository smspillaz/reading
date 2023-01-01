---
title: "Compositional Learning of Image-Text Query for Image Retrieval."
venue: "WACV"
pages: "1139-1148"
year: 2021
type: "Conference and Workshop Papers"
access: "closed"
key: "conf/wacv/AnwaarLK21"
doi: "10.1109/WACV48630.2021.00118"
ee: "https://doi.org/10.1109/WACV48630.2021.00118"
url: "https://dblp.org/rec/conf/wacv/AnwaarLK21"
authors: ["Muhammad Umer Anwaar", "Egor Labintcev", "Martin Kleinsteuber"]
sync_version: 3
cite_key: "conf/wacv/AnwaarLK21"
---

Multi-mdoal queries. the query test prompts some modification in the query image and the task is to find images which are modified according to the query.

Proposes ComposeAE, to learn the composition of image and text query for retrieval.

Also proposes a symmetry constraint on the optimization problem.

Tries to improve upon [[tirg_composing_text_and_image_for_image_retrieval_an_empircal_odyssey|TIRG (text-image residual gating)]].

Use pre-trained BERT + ResNet17.

Proposes that target image representation is an "element-wise rotation of the representation of the source image". The information about the degree of rotation is specified by the text features.

Use a Deep Metric Learning approach. The text feautres take a central role here.

Also propose a rotational symmetry constraint on the optimization problem. Require that multiplication of the target image features with the complex conjugate of the query text features should give a representaiton similar to the query image. Basically, you should be able to rotate back from the target to the source.

This builds upon [[attributes_as_operators_factoring_unseen_attribute_object_compositions]]

# Architecture
![[compose_ae_architecture.png]]

Works by encoding both images and text as vectors.

In order to make the text query a rotation, you learn a mapping $\gamma : \mathbb{R}^k \to \{D \in \mathbb{R}^{k \times k}\}$ where $D$ is diagonal to get a coordinate-wise complex rotation: $\delta = \exp(j\gamma (q))$ where $q$ is the text features and $j$ is the imaginary number.

Learn a mapping function that maps the image features $z$ to the complex space.

## Composition Function

Let $f(z,q)$ denote a composition function which leanrs how to compose extracted image and text features for target image retrieval.

The function is given by:

$$
f(z, q) = \alpha \rho(\phi) + b \rho_{\text{conv}}(\phi, z, q)
$$

where $a$ and $b$ are learnable parameters and $\phi$ and $\rho_{\text{conv}}$ transformation functions specified in the paper ($\phi$ is basically $\delta \eta$ where $\eta$ maps the image into the same space as the rotations, and $\rho_{\text{conv}}$ picks some features from the image.)

## Training

Triplet loss, base loss.

Use contrastive loss function with similarity kernels.

Also two reconstruction losses to ensure that we can reonstruct the query and text.

### Rotational Symmetry Loss

The rotational symmetry constraint translates to maximizing the similarity kernel $K(\nu, z)$ .

# Experiments

Compare with Show and Tell, Parameter Hashing, Attribute as Operator, Relationship, FiLM and TIRG.

## Ablation Study

Mapping to the complex space is important.