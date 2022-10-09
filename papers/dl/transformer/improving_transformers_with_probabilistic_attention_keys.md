---
title: "Improving Transformers with Probabilistic Attention Keys."
venue: "ICML"
pages: "16595-16621"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/NguyenNLNTBHO22"
ee: "https://proceedings.mlr.press/v162/nguyen22c.html"
url: "https://dblp.org/rec/conf/icml/NguyenNLNTBHO22"
authors: ["Tam Minh Nguyen", "Tan Minh Nguyen", "Dung D. D. Le", "Duy Khuong Nguyen", "Viet-Anh Tran", "Richard G. Baraniuk", "Nhat Ho", "Stanley J. Osher"]
sync_version: 3
cite_key: "conf/icml/NguyenNLNTBHO22"
---

For many applications, attention heads learn redundant embeddings and most of them can be removed without degrading most of the performance of the model.

Proposes "Transformer with Mixture of Gaussian Keys", replaces redundant heads with a mixture of keys at each head, following a Gaussian mixture model. Transformer-MGK accelerates training and inference and has fewer parameters. Can also be extended to linear attention methods.

In this paper they establish a correspondence between self-attention in Transfromer and Gaussian Mixture Model and propose "Transformer with Mixture of Gaussian Keys", a novel class of transformer that can avoid the head redundancy.

At its core, Transformer-MGK is replacing attention key $k_j$ with a GMM, which allows the query and its associated token to attend to more diverse positions in the input sequence.
 1. GMM and attention scores in self-attention match share a similar posterior distribution in their model
 2. Mixture of Gaussian Keys can capture diversity of attention patterns and thus alleviate head redundancy.
 3. MGK is extended to linear attention, eg, mixture of linear keys (MLK).
 4. Transformer-MGK and Transformer-MLK are comparable or better than the corresponding baseline transformers, using only half the attention heads.

Why do GMM and attention scores have a similar posterior distribution? Consider a query $q$ and key $k$. $t$ is an n-dimensional binary random variable, which indicates the position $j$ of a key $k_j$.

$$
p(q_i) = \sum^N \pi_j p(q_i|t_j = 1) = \sum^N \pi_j \mathcal{N}(q_i|k_j, \sigma^2I)
$$

The posterior, $p(t_j = 1)$ can be computed with Bayes Rule ($p(A|B) = \frac{p(B|A)p(A)}{p(B)}$) as follows:

$$
p(t_j = 1|q_i) = \frac{\pi_j \mathcal{N}(q_i|k_j, \sigma^2_j)}{\sum_{j'}\pi_{j'} \mathcal{N}(q_i|k_{j'}, \sigma^2_{j'})}
$$

When the query and key are normalized and the prior is uniform, then the posterior can be written as:

$$
\frac{\exp{q_i k_j^T/\sigma^2}}{\sum_{j'} \exp{(q_i k_{j'}^T/\sigma^2)}}
$$

Which is exactly the softmax score for attention when $\sigma^2 = \sqrt{D}$. Therefore we can see that the attention score $q_i$ and key $k_j$ is exactly the posterior $p(t_j = 1|q_i)$, eg, the responsibility that key $j_j$ takes for explaining the query $q_i$ .

How can we translate this into a mixture of Gaussian keys? $z_r$ indicates the $r^{\text{th}}$ gaussian in the mixture.

$$
\pi_{jr} = \sum_r (z_r = 1|t_j = 1)P(q_i|z_r = 1, t_j = 1) = \sum_r \pi_{jr} \mathcal{N}(q_i|k_{jr}, \sigma^2 I)
$$

$$
P(t_j = 1|q_i) = \frac{\sum_r \pi_{jr} \exp {q_i k^T_{jr}/\sigma^2_{jr}}}{\sum_{j'}\sum_r \pi_{j'r} \exp {q_i k^T_{j'r}/\sigma^2_{j'r}}}
$$

This can be relaxed into a gaussian kernel :

$$
P(t_j = 1|q_i) = \frac{\sum_r \pi_{jr} \exp {||q_i -  k_{jr}||^2/2\sigma^2_{jr}}}{\sum_{j'}\sum_r \pi_{j'r} \exp {||q_i - k^T_{j'r}||^2/2\sigma^2_{j'r}}}
$$

Then, the "Transformer MGK" is defined as follows:

$$
h_i = \sum_j \begin{pmatrix} \frac{\sum_r \pi_{jr} \exp {||q_i -  k_{jr}||^2/2\sigma^2_{jr}}}{\sum_{j'}\sum_r \pi_{j'r} \exp {||q_i - k^T_{j'r}||^2/2\sigma^2_{j'r}}} \end{pmatrix} v_j
$$

Then we can do inference and learning with EM.

The E-step makes a soft-assignment, eg:

$$
\gamma_{ir} = \frac{\sum_r \pi_{jr} \exp {||q_i -  k_{jr}||^2/2\sigma^2_{jr}}}{\sum_{j'}\sum_r \pi_{j'r} \exp {||q_i - k^T_{j'r}||^2/2\sigma^2_{j'r}}}
$$

To make a "hard" assignment, replace the sum with a $\max$ and remove the uniform prior.

$$
P(t_j = 1|q_i) = \frac{\max_r \exp {||q_i -  k_{jr}||^2/2\sigma^2_{jr}}}{\sum_{j'}\max_r \exp {||q_i - k^T_{j'r}||^2/2\sigma^2_{j'r}}}
$$

Then instead of an $M$ step, you just learn via gradient descent via the $E$ step, eg, just learn $q_i$ and $k_{jr}$.