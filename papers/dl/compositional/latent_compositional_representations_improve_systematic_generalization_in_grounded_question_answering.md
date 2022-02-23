---
title: Latent Compositional Representations Improve Systematic Generalization in Grounded Question Answering.
venue: Trans. Assoc. Comput. Linguistics
volume: 9
pages: 195-210
year: 2021
type: Journal Articles
access: open
key: journals/tacl/BoginSGB21
ee: https://transacl.org/ojs/index.php/tacl/article/view/2489
url: https://dblp.org/rec/journals/tacl/BoginSGB21
authors: ["Ben Bogin", "Sanjay Subramanian", "Matt Gardner", "Jonathan Berant"]
sync_version: 3
cite_key: journals/tacl/BoginSGB21
---

In this work, a model that computes representations and denotation for all question spans in a bottom-up compositional manner using a CKY style parser.

The model induces latent trees driven by answer supervision only.

This bias towards tree structures "dramatically improves systematic generalization on out of distribution examples".

Some possible reasons for bad systematic generlization is the expressivity of architectures of LSTMs and transformers which compute a global representaiton depending on the entire input, resulting in a collapse of reasoning (Jiang and Bansal 2019, Subrramanian 2019, 2020)

Approach evaluated on arithmetic expressions and [[closure_assessing_systematic_generalization_of_clevr_models|CLOSURE]] (which is a split of [[clevr_a_diagnostic_dataset_for_compositional_language_and_elementary_visual_reasoning]]).

![[glt_latent_compositional_represnetation_split_points.png]]

The goal is to compute a representation $h_{ij}$ and denotation $d_{ij}$ . $_{ij}$ here refers to "question spans", eg,e very question is made up of many spans. In this sense, its basically the powerset of the question's contiguos spans.

The aim is to output an "answer" $a \in \mathcal{A}$

Pass the question representation $h_{0n}$ and weighted sum of visual representations $d_{0n}{V}$ through softmax to get the final distribution.

To compute $h_{ij}$ split all points and compose pairs of sub-spans using $f_h$. Then $h_{ij}$ is the weighted sum of all subspan representations. You can take a dynamic programming approach to this.

How to compute the weight over the split points? Use $a^{k}_{ij} = \exp(s^T h^k_{ij})$  . Basically attention where $s^T$ is a parameter vector.

To compute $d_{ij}$, compute the expected value for the left and right subspans usin the attention weights, then use $d_{ij} = f_d(d_{ij_L}, d_{ij_R}, h_{ij})$

### How should $f_d$ and $f_h$ look like?

$f_h$: Compute softmax weighted linear combination of two sub-spans for $h_{ij}$ at split point $k$ and pass through feedforward net.

$f_d$: Define four modules for computing denotations and learn when to use each module:

 - Skip
 - Intersection
 - Union
 - Visual (only this one uses the visual representations).

![[latent_compositional_representaitons_f_d.png]]

The idea is that you then have a weighted average of the four modules. This is like [[deep_compositional_question_answering_with_neural_module_networks|neural module networks]] . See the paper for how each one is defined.

## Grounding

How do you ground the sentence parts to the image?

1. Co-references: Simple pointer network, if something one one sentence grounds and co-refers in another sentence, the thing in the other sentence grounds too.
2. Visual representaitons: Two approaches: FiLM or object detection. Use object detection.

# Experiments

## Arithmetic

GLT gets a small drop in accurracy, but much better compared to transformer on the OOD split.

## CLEVR/CLOSURE

Compare against MAC and FiLM.

on closure we get 96.1 compared to 72.4 for MAC and 60.1 for FiLM.

## Ablation Study

Removing union/intersect modules loses 5 points of performance.

Removing skip drops about 8 points.

With non-compositional representations (eg, just replace $h_{ij}$ with a sequence encoder), you drop about 13 points on the OOD case.