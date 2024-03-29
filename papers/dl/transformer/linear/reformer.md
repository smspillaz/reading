---
title: "Reformer - The Efficient Transformer."
venue: "ICLR"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/KitaevKL20"
ee: "https://openreview.net/forum?id=rkgNKkHtvB"
url: "https://dblp.org/rec/conf/iclr/KitaevKL20"
authors: ["Nikita Kitaev", "Lukasz Kaiser", "Anselm Levskaya"]
sync_version: 3
cite_key: "conf/iclr/KitaevKL20"
---
# Reformer: The Efficient Transfomer

Transformers are great and performance seems to scale with the number of parameters.
Huge models seem to do ever-better on a number of benchmarks (see, eg, GPT-2 and GPT-3).

Time and space complexity scales with number of layers and sequence size. The state-of-the-art
models are getting so big now that you can't even fine-tune them on a single GPU with
long sequences (lets say that a nice GPU gets you about 16GB of memory and a long sequence is
up to 16K tokens).

But this doens't check out with the math: Lets say that you have 0.5 billion parameters per layer
(floating point). This should be 2GB of memory. The activations, assuming that you have 64K with
embedding size 1024 should be another 2GB of memory. Assuming
that you throw away any calculations that you don't need, it should be possible to fit the model
and activations on a GPU.

Problems:
 - Intermediate computations are huge
 - Need to store the intermediate activations for backprop
 - Attention on sequences length L is O(L^2) in both compute and memory.

## Contributions

 1. Reversible Layers
 2. Splitting activations and processing them in chunks
 3. Approximate attention with LSH (O(L log L))

## Memory-Efficient Attention

Normal attenion is a dot product, eg:

 $$
 \text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}}) V
 $$

If your sequence length is 64K, the $QK^T$ is 64K x 64K which in itself is 16GB of memory. Not feasible on
a normal GPU.

Alternative: Trade memory for space and compute $\text{softmax}(\frac{q_i K^T}{\sqrt{d_k}}) V$ for each $q_i \in Q$
separately. Memory usage is now O(L) instead of O(L^2). The tradeoff is that you lose some parallelism. Also need
to recompute the softmax on the backward pass.

Observation: You could probably chunk this computation to regain some of that parallelism. No need to do each one
separately.

## Locality Sensitive Hashing Attention

First Observation: Q, K and V on most transformer type architectures are entirely artificial. They are linear
projections from the activations that come from the layer before. (We want Q and K to be identical, so use the same
projection for both and a different one for V).

We are interested in the result $\softmax(QK^T)$, not $QK^T$. Can we approximate $\softmax(QK^T)$?

Remember how softmax works: $\frac{e^{x_i}}{\sum_j e^{x_j}}$. In the limit, the smaller elements of
$\mathbf{x}$ go to zero. Power law distribution followed. Experiment: If you find the top 64 elements
and compute softmax over them, then set rest to zero, does it make that much of a difference? Probably not.

```py
>>> def capped_softmax(x, limit):
...     top = np.argsort(x)[-limit:]
...     x_top = x[top]
...     softmax_top = softmax(x_top)
...     result = np.ones_like(x) * np.finfo(float).eps
...     for i, s in zip(top, softmax_top):
...         result[i] = s
...     return result
...
>>> r = np.random.normal(size=64000)
>>> x =  r * r
>>> entropy(softmax(x), capped_softmax(x, 64000))
2.21854306858116e-16
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 2)))
8.40575896079891e-05
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 4)))
0.00017307511733625174
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 8)))
0.00029919649505647785
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 16)))
0.0004995377265998139
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 32)))
0.0008350182494549327
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 64)))
0.0014213964910320875
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 128)))
0.002438563162349844
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 256)))
0.004198809773849821
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 512)))
0.0071744313131057785
>>> entropy(softmax(x), capped_softmax(x, int(64000 / 1024)))
0.01210328539497348
```

Idea: Dot product computes *correlation*. Can we find two vectors
that are correlated with each other quickly?

Locality Sensitive Hashing: Say we have some locality-sensitive-hash
function h(x). Two inputs that are *close* in some space that is interesting
will be hashed into the same bucket if they are close in the space with
high probability.

 - Random Projections: To get b hashes generate a random matrix R of [d_k, b / 2].
   $h(x) = \arg \max ([x R, -x R])$ (eg, multiply vector and negative vector with R, concat),
   then the bucket is the element with maximal value (eg, the column that we were most
   similar to).
 - Works because of triangle inequality property: Two vectors correlated with each other
   are highly likely to be most correlated to the same third vector drawn from a random distribution.

### LSH Attention:

$$
o_i = \sum_{j \in P_i} e^{q_i \cdot k_j - z(i, P_i)} v_j
$$

Where $P_i = {j : h(q_i) = h(k_j)}$ - eg, you only compute the softmax for things that are in your bucket.

How this is used:
 - Assign queries $q_i$ and keys $k_i$ to buckets according to h(x)
 - Sort according to assigned buckets
 - Divide the sorted array into $m$ chunks (which might cross bucket boundaries)
   - Define mapping $i \to s_i$ (argsort)
 - Compute attention within each bucket and the previous bucket (so we might over-compute attention, but never under-compute it). Allows batching.
   - In practice this means that $\tilde P_i = \{j : \floor{\frac{s_i}{m}} - 1 \le \floor{\frac{s_j}{m}} \}$ (this is NOT the complement, but rather an approximation of set $P_i$
   - We want $m < |\tilde P_i|$. Set $m$ to $\frac{1l}{n_{\text{buckets}}}$ - $m$ should on average be the length of a bucket, probability of $m$ growing to 2x that is low (unanalyzed).

How to improve the hashing? Use multi-round hashing. Standard practice in LSH - hash many times with different projections
so we have $P_i = \Cup_r {j : h_r(q_i) = h_r(k_j)}$.

Problem: A bucket can contain many queries but no keys and vice versa. They don't align and are ignored. To alleviate this,
set $k_j = \frac{q_j}{||q_j||}$. In practice this means $W_k = W_q$. In practice this doesn't actually matter so much.

Keep track of original position index to do causal masking as usual.

Complexity:

 - From $bn_hl^2$ to $ln_r(\frac{4l}{nc})^2$ (l  = seq len, b = batch size n_h = num heads, n_r rounds n_c chunks), so we go from being quadratic in length to quadratic in $\frac{4l}{n_c}$. If $n_c$ is large, this is a substantial reduction.

You can do this during both training and eval. The gradients for the important attention elements are kept and the rest are set to zero.

### Experiment on a simple task

Replicate the symbols that you are given. With 4 rounds of LSH you can get good performance (99.9% accuracy).

## Reversible Transformer

Motivation: Still have a constant scalar factor $b n_h l d_k d_{\text{model}} n_l$ in front of the complexity. Can we reduce it?

Main issue: Need to store all the activations at each layer in order to compute the backward pass. For many layers this gets expensive.

Observation about ResNets from Gomez et al: ResNet is f(x) = x + h(x). We can recover the intermediate value by subtracting the residual from the output. No need to keep $x$ around redundantly. Similar thing for attention: Add the attention to the input and pass it to the next layer, don't need to store the input twice.