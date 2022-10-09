---
title: "On the Learning of Non-Autoregressive Transformers."
venue: "ICML"
pages: "9356-9376"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/HuangTZLH22"
ee: "https://proceedings.mlr.press/v162/huang22k.html"
url: "https://dblp.org/rec/conf/icml/HuangTZLH22"
authors: ["Fei Huang", "Tianhua Tao", "Hao Zhou", "Lei Li", "Minlie Huang"]
sync_version: 3
cite_key: "conf/icml/HuangTZLH22"
---

A non-autoregressive transformer (NAT) tries to predict the whole target sequence all at once in parallel. Having these is nice because then you don't have to run the decoder many times (which is slow in terms of latency).

In this paper, the theoretical and empircal challenges of NAT learning are discussed.

A few things are shown:
 - Simply training NAT by maximizing the likelihood can lead to an approximation of marginal distributions but drops all dependencies between tokens
 - The success of former methods can be seen as maximizing the likelihood on a proxy distribution.

Non-autoregressive Neural Machine Translation by Gu et al 2018 shows that learning NAT is very challenging and directly training NAT via MLE leads to implausible outputs with repeated tokens.

Many training methods have been proposed:
 - Knowledge Distillation: supervise NAT with sequences distilled from autoregressive transformers as a teacher
 - GLAT: Masked LM objective

These can improve the situation regarding generation quality.

#### Why is it hard?

There's a good example in Figure 2 about why training NATs towards higher likelihood does not lead to better generation quality. Consider a joint distribution over two variables, $P(y_1, y_2)$. NAT is forced to assume that $P(y_1, y_2) = P(y_1)P(y_2)$. But $y_2$ could depend on $y_1$! For example, if the two are correlated, like "no problem" and "of course". Instead of learning the proper density, eg, that "of course" happens 50% of the time and "no problem" happens the other 50%, NAT will learn that "no" happens 50% of the time and "of" the other 50% in token 1 and the same for "problem" and "course" in token 2. This means that "no course" has a probability of 25% according to the model, even when in reality it has a probability of 0%.

From a theoretical perspective, NAT's KL divergence with the true data distribution is bounded by a non-negative constant, which corresponds to the information loss in the data distirbution.

$$
\mathcal{D}_{KL}[P_{\text{data}}(Y|X)||P_{\theta}(Y|X)] = -H_{\text{data}}(Y|X) - \mathbb{E}_{P_{\text{data}}(Y|X)} [\sum \log P_{\theta}(y_i|X)]
$$
$$
-H_{\text{data}}(Y|X) - \sum
 \mathbb{E}_{P_{\text{data}}(Y|X)} [\log P_{\theta}(y_i|X)]
$$

$$
\ge -H_{\text{data}}(Y|X) + \sum
 H_{\text{data}}(y_i|X)
$$
(by Gibbs inequality)

The last quantity is called the "conditional total correlation", which measures information dependence between the target tokens. Large values of this quantity in the data are correlated with loss in performance of non-autoregressive models trained on the data in comparison to their autoregressive counterparts.

This quantity is called $\mathcal{C}$ in the paper.

#### Why do the previously proposed methods improve the situation?

The previously proposed training methods (Knowledge Distillation and GLAT) maximize likelihood on a proxy distribution and this proxy distribution usually has a low $\mathcal{C}$.