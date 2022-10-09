---
title: "A simple neural network module for relational reasoning."
venue: "NIPS"
pages: "4967-4976"
year: 2017
type: "Conference and Workshop Papers"
access: "open"
key: "conf/nips/SantoroRBMPBL17"
ee: "https://proceedings.neurips.cc/paper/2017/hash/e6acf4b0f69f6f6e60e9a815938aa1ff-Abstract.html"
url: "https://dblp.org/rec/conf/nips/SantoroRBMPBL17"
authors: ["Adam Santoro", "David Raposo", "David G. T. Barrett", "Mateusz Malinowski", "Razvan Pascanu", "Peter W. Battaglia", "Tim Lillicrap"]
sync_version: 3
cite_key: "conf/nips/SantoroRBMPBL17"
---
Proposes "Relation Networks" to solve problems that rely on relational reasoning.

Tested on VQA, bAbI, dynamical systems and Sort-of-CLEVR.

Relational Reasoning: "are there any rubber things that have the same size as the yellow metallic cylinder?". This requires looking at all the objects in-relation-to the Yellow Cylinder.

# Architecture

In its simplest form:

$$
\text{RN}(O) = f_{\phi} (\sum_{ij} g_{\theta}(o_i, o_j))
$$

where the input is a set of objects $o_1, ..., o_n$ and the parameters are $\phi$ and $\theta$. Essentially, $g_{\theta}$ is some sort of pairwise relation function and $f_{\phi}$ takes the sum of relations and returns some answer.

1. RNs learn to infer relations: The input is a complete and directed grpah, nodes are objects whose edges denote the object pairs.
2. RNs are data efficient: $g_{\theta}$ is encouraged not ot overfit to any particular object pair.
3. RNs operate on a set of objects.

## Models

![[relnet_architecture.png]]

RNs operate on objects, not images or natural language. How to convert images and language into objects?

1. Images: Use a CNN to parse pixel inputs into a set of objects. Each of the $d^2$ k-dimensioanl cells in the $d \times d$ feature map is an "object". This means that objects can be background or something else. Obviously this depends on pooling.
2. Conditioning RNs with question embeddings: Use the final state of an LSTM that processes question words. Questions are assigned unique integers and you use that to lookup their encoding. At each timestep, get a single word embedding for each word in the question and relate that to the objects .