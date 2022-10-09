---
title: "Systematic Generalization on gSCAN with Language Conditioned Embedding."
venue: "AACL/IJCNLP"
pages: "491-503"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/ijcnlp/GaoHM20"
ee: "https://aclanthology.org/2020.aacl-main.49/"
url: "https://dblp.org/rec/conf/ijcnlp/GaoHM20"
authors: ["Tong Gao", "Qi Huang", "Raymond J. Mooney"]
sync_version: 3
cite_key: "conf/ijcnlp/GaoHM20"
---

Hypothesis: Explicitly modelling the relations between objects in their contexts while learning their representations will help acheive systematic generalization.

Learn objects' contextualized embedding with dynamic message passing conditioned on the input natural language.

One essential step in acheiving the goal of generalization is to obtain good object embeddings to which the language can be grounded.

1. Learning good representations of attributes whose actual meanings are contextualized
2. Learning good representations for attributes so that conceptually similar attributes ("yellow" and "red" have similar represnetaitons)

# Architecture
![[systematic_generalization_with_language_conditioned_embeddings_gnn_architecture.png]]
At a high level:

1. Treat the grid world as a collection of objects whose semantic meanings are contextualized by their neighbours

## Input Extraction

BiLSTM with attention weighted outputs over a sequence.

## GridWorld

Extract one-hot represnetaitons of color, shape and orientation and embed each property with a 16 dimensional vector, concatenating them back into one vector and using this for the local embedding.

## Language Conditioned Message Passing

Perform iterative message passing for $T$ rounds, eg, every node has a hidden state and trades messages and updates its own internal state.

Each object in the gridworld is a node and together they form a complete graph (everything connected to everything).

## Encoding the entire gridworld

Graph convolutions with different kernel sizes to get a multiscale representation. Do attention between the LSTM word encodings and the gridworld contexts.

# Experiments

Split B: Novel direction: Succeeds sometimes, but mostly fails

Split C, G: "small circle"

Split D, E: Novel combinations: This model is able to do the red square split with 80% success.