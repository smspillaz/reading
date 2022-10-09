---
title: "Compositional Networks Enable Systematic Generalization for Grounded Language Understanding."
venue: "EMNLP"
pages: "216-226"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/emnlp/KuoKB21"
doi: "10.18653/V1/2021.FINDINGS-EMNLP.21"
ee: "https://doi.org/10.18653/v1/2021.findings-emnlp.21"
url: "https://dblp.org/rec/conf/emnlp/KuoKB21"
authors: ["Yen-Ling Kuo", "Boris Katz", "Andrei Barbu"]
sync_version: 3
cite_key: "conf/emnlp/KuoKB21"
---

Given a command, a command specific network is assembled from previously trained modules. Modules are discovered from the training set without annotation. Then you combine these modules from the lingusitic structure of the command.

The model proposed achieves similar training set performance but it is able to generalize. better in a number of ways, including few shot learning and longer action sequences.

Another benefit of compositional networks is that they open the door to naturally including other linguistic principles, for example, incorporating the lexical semantics of words like antoynms.

## Contributions

1. A class of compositional networks
2. Replace data augmentation with compositionality
3. Incorporate lexical semantics of words into compositional networks
4. Address generalization tasks in gSCAN

# Architecture
![[compositional_networks_gscan_architecture_diagram.png]]

The basic idea is to create a parse tree using a dependency parser. Then each token becomes an RNN and the recurrent networks are connected with each other via attention maps. Every node has its own observation. Then the state of the root model is decoded into actions.

## Parsing Natural Language Commands

Three kinds of parsers:
1. Constituency parser
2. Dependency parser
3. Semantic parser

The point being that you arrange the nodes in a tree.

## Compositional Networks

Given a parse, the parse tree nodes get replaced iwth RNNs connected to each other thoruhg the structure of the parse.

1) Recurrent Word Modules: Each word corresponds to an RNN
2) Connecting word modules: Information that flows follows a reverse direction.
3) Attention mechanism: Each RNN maintains a state and this state is used to predict an attention map before being accessed by toher words. You get the observations and attention maps from children from the previous timestep. Then compute the attention for hte current node. Use the attention-weighted inputs to update the hidden state

The attention maps are the way that the nodes communicate with each other.

## How to train the networks?

The input consists of pairs of commands and corresponding trajectories. Use a pre-trained parser. Command is parsed and corresponding network instantiated. Words that haven't been seen yet get a random intialization for their weights. Words that have been seen get their old weights back. Predict actions.

## Experiments
![[compositional_networks_gscan_results.png]]

Again:

a. Random split
b. Yellow squares
c. Red squares
d. Novel direction
e. Relativitiy
f. Class inferenc
g. Adverbs
h. Adverb to verb
i. Sequence length.

On the yellow squares split, this method does OK, 67.72 with high variance. It does much better on split F (class inference) and D (novel direction).

## Interpretability

![[compositional_networks_gscan_interpretability.png]]

Interpretability in two ways:

1. Struture of network overtly encodes the structure o hte sentence
2. Internal reasoning of the network proceeds by passing attention maps

You can inspect the attention maps directly to see what different words actually refer to. If the agent picks the wrong object this will show up in the attention map.