---
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness."
venue: "CoRR"
volume: "abs/2205.14135"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2205-14135"
doi: "10.48550/ARXIV.2205.14135"
ee: "https://doi.org/10.48550/arXiv.2205.14135"
url: "https://dblp.org/rec/journals/corr/abs-2205-14135"
authors: ["Tri Dao", "Daniel Y. Fu", "Stefano Ermon", "Atri Rudra", "Christopher R\u00e9"]
sync_version: 3
cite_key: "journals/corr/abs-2205-14135/Dao/2022"
---
There are lots of methods trying to reduce compute and memory requirements of attention, but few are actually successful in reducing wall clock time. They also tend to ignore overheads from memory access.

Consider the memory hierarchy!

The whole point is to compute blocks on SRAM

Outer loop copies keys. Inner loop copies copies queries and computes `sm(QK^T)V`.

OK, so we tile the matrices into blocks, then load them into SRAM and compute attention wrt the blocks. Then by scaling the output of each block by the right factor before adding, you get the correct result.

OK some preliminaries:

Softmax can be given by:

$$m(x) = \max(x_i)$$
$$f(x) = [e^{x_1 - m(x)}, ..., e^{x_d} - m(x)]$$
$$l(x) = \sum f(x)$$
$$\text{softmax}(x) = \frac{f(x)}{l(x)}$$

Why the $-m(x)$ ? This is to ensure numerical stability, eg, we don't want to exponentiate huge numbers, so we typically subtract the maximum value of $x_i$ from the exponent. It gets divided out anyway in the end.

Lets say you have a concatenated vector of $[x_1, x_2]$. You can decompose the softmax as:

$$m(x) = \max(m(x_1), m(x_2))$$
$$f(x) = [e^{m(x_1) - m(x)}f(x_1), e^{m(x_1) - m(x)}f(x_2)]$$
$$l(x) = e^{m(x_1) - m(x)}l(x_1) + e^{m(x_1) - m(x)}l(x_2)$$

I.e, why do we multiply by $f(x_1)$? Well, it will add those factors to the exponent: eg:

$$f(x) = [e^{m(x_1) - m(x)}([e^{x_{1_1} - m(x)}, ... e^{x_{1_d} - m(x)}]), e^{m(x_1) - m(x)}([e^{x_{2_1} - m(x)}, ... e^{x_{2_d} - m(x)}])]$$
and

$$f(x) = [([e^{x_{1_1} - m(x) + m(x_1) - m(x)}, ... e^{x_{1_d} - m(x) + m(x_1) - m(x)}]), e^{m(x_1) - m(x) + m(x_1) - m(x)}([e^{x_{2_1} - m(x) + m(x_1) - m(x)}, ... e^{x_{2_d} - m(x) + m(x_1) - m(x)}])]$$

How does the algorithm work?
