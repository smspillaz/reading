---
title: Generative Language-Grounded Policy in Vision-and-Language Navigation with Bayes&apos; Rule.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/KuritaC21
ee: https://openreview.net/forum?id=45uOPa46Kh
url: https://dblp.org/rec/conf/iclr/KuritaC21
authors: ["Shuhei Kurita", "Kyunghyun Cho"]
sync_version: 3
cite_key: conf/iclr/KuritaC21
---

There are two possible approaches for building a VLN agent, discriminative and generative.

In this paper, use a language model to compute the distribution over all possible instructions.

The generative language-grounded policy considers what is available at each timeste and chooses one of the potential actions which generates the instruction, then applies Bayes rule to obtain the posterior distribution over actions given the instruction. Basically, score the instruction given the action and not the other way around, then use that to get the action scores.


The hypothesis is that the generative parameterization works better than the discriminative one due to the existence of a richer training signal.

The generative approach outperforms the discriminative one on both the R2R and R4R datasets, esepcailly in unseen environments.


## Discriminative vs Generative Approaches

$$
p(a_t|h_t, X) = \frac{p(X|a_t, h_t) p'(a_t|h_t)}{\sum_{a'_t} p(X|a'_t, h_t) p'(a'_t|h_t)} = \frac{p(X|a_t, h_t)}{\sum_{a'_t} p(X|a'_t, h_t)}
$$

Here we eliminate the second term from each fraction by assuming that $p'(a_t|h_t) = \frac{1}{|A|}$.

$p(X|a_t, h_t) = \Pi_k p(w_k|a_t, h_t, w_{:k - 1})$ is a language model conditioned on thea ction, hidden state and outputs the distribution over all possible sequences of vocabulary tokens.

Learning is then equivalent to solving:

$$
\max_{\theta} \sum^N \sum^{T_n} (\log p(X^n|a^n_t|h^n_t) - \log \sum_{a'^{n}_t \in A} p(X^n|a'^n_t, h^n_t))
$$

where $\log p(X^n|a^n_t, h^n_t)$ is the language model loss conditioned on the reference action, whereas the second term penalizes all the actions.

If we train with only the first term, the resulting network does not learn how to distinguish between the actions and rather learns to just generate the sintruction from the observation.


## Training and Dataset

**R2R**: Let each policy navigate the environment and give the action that leads to the shortest path at each timestep as supervision.

**R4R**: We train both the generative and the discriminative policies to maximize the log-probability of hte correct action from the trianing set.


Observations:
 - Data augmentation has a bigger effect on the validation-unseen split than on the validation-seen split. It discourages overfitting.
 - Discriminative policies are easy to overfit seen environments.
 - Generative policy always performs better than the discriminative one in both success rate and success path length.