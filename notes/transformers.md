## Basic idea

$$
\text{Att}(x) = \frac{\text{softmax}(Qx(Kx)^T)}{\sqrt{d}} Vx
$$

Transformers:
 - Mutiple attention "heads"
 - Concatenate them together
 - Project back by MLP + residual connection

## Variants

### Routing Transformer

[[routing_transfomer.pdf]]

tl;dr: Use k-means to cluster things queries and keys together, only attend within the same cluster.

Some proofs which show that being close by L2 distance means having high attention weight.

### Reformers

[[reformer]]
[[reformer.pdf]]

Two main contributions:
 1. LSH attention (project queries and keys against a random hyperplane, sort into buckets)
 2. Storage optimization for computing residuals
