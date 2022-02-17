---
title: Explicit Sparse Transformer - Concentrated Attention Through Explicit Selection.
venue: CoRR
volume: abs/1912.11637
year: 2019
type: Informal Publications
access: open
key: journals/corr/abs-1912-11637
ee: http://arxiv.org/abs/1912.11637
url: https://dblp.org/rec/journals/corr/abs-1912-11637
authors: ["Guangxiang Zhao", "Junyang Lin", "Zhiyuan Zhang", "Xuancheng Ren", "Qi Su", "Xu Sun"]
sync_version: 3
cite_key: journals/corr/abs-1912-11637/Zhao/2019
---

Self-attention suffers from the problem of extracting irrelevant information from the context.

Proposes Explicit Sparse Transformers. Select explicitly the most relevanat segments. This can do well on a variety of tasks.

The problem is illustrated quite well in Figure 1 - regular transformers give lots of weight to irrelevant words.

# Model Architecture

![[explicit_sparse_transformer_architecture.png]]

Attention is degenerated to sparse attention through top-k selection. The masking function is basically just adding -inf to the log-attention if the attention weight is smaller than the kth-largest.

### Comparison with other sparse attention mehtods

Top-k is much faster in terms of inference tspeed than other methods like sparsemax, entmax .

### Selecting $k$

Somewhere between 8 and 16.

## Related Work

 - [[from_softmax_to_sparsemax_a_sparse_model_of_attention_and_multi_label_classification|Sparsemax]]
 - [[entmax_sparse_sequence_to_sequence_models|Entmax]]
 - [[sact_learning_when_to_concentrate_or_divert_attention_self_adaptive_attention_temperature_for_neural_machine_translation|SaCT]] - learnable temperature parameter 

