---
title: "Interpreting Graph Neural Networks for NLP With Differentiable Edge Masking."
venue: "ICLR"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/SchlichtkrullCT21"
ee: "https://openreview.net/forum?id=WznmQa42ZAx"
url: "https://dblp.org/rec/conf/iclr/SchlichtkrullCT21"
authors: ["Michael Sejr Schlichtkrull", "Nicola De Cao", "Ivan Titov"]
sync_version: 3
cite_key: "conf/iclr/SchlichtkrullCT21"
---
# Interpreting Graph Neural Networks for NLP with Differentiable Edge Masking

tl;dr: There has been little work on intepreting GNNs. Introduces a method for interpreting the predictions of GNNs which identifies unnecessary edges. Learn a simple classifier that, for every edge in every layer, predicts if that edge can be dropped. Use this as an attribution method to analyze GNN models for two tasks - question answering and semantic role labeling. We can drop a large proportion of the edges without deteriorating performance.

GNNs are black boxes - difficult to understand which graph elements resulted in a prediction.

NLP, GNNs are used to encode syntatic or semantic structures. Important to understand which parts are used.

Requirements:
 - Faithful as possible
 - Able to identify relevant *paths* in addition to edges
 - Fast enough for dataset level analysis.


Erasure Search: Find the smallest possible sub-graph of the input that produces the same predictions. Try every possible combination of subgraphs. Explanations are completely binary. High complexity.

![[graphmask.png]]

GraphMask: Instead find the smallest necessary subgraph by gradient descent.

For every edge in every layer we sample something which tells us whether to enable or disable that edge.

L0 penalty to promote sparsity. If an edge is disabled, replace it with a learned baseline. Preserve the statistics of each neighbourhood in the graph - only disable the messages, not the aggregation function.

Hindsight bias: Don't want the optimizer to cheat by using information from the future. If you know what the predictions are supposed to be ahead of time, the interpretation technique doesn't need to preserve all the informaton - just need to preserve one bit, but then the explanations aren't faithful anymore.

GraphMask: Small local classifier that sees only the message and source/target embeddings. Amortises parameters over the entire dataset. We don't have access to information from the future. When deciding whether a message is useful or not, you only see the source and target embeddings. Interpreter can't exploit the shape of any sample.

Algorithm:

 - Run the original model to get vertex embeddings and messages
 - Use these as futures for local probes
 - Masked messages replaced by learned baseline
 - Minimize divergence between predictions from original and masked model + L0 penalty.

Case study: Question Answering - real world NLP problems, starting with question answering. Too complex for human-defined gold standard on faithfulness.

One of the four edge types used in the model (COREF) is almost entirely superfluous.

COMPLEMENT is used only in the bottom layer - it is used in the majority of edges in that layer.

Case study: Semantic role labelling

 - Only 4% of the edges actually necessary, but those 4% are crucial. Those that describe the relationshop between the predicate and the predicted label.