---
title: "MetAug: Contrastive Learning via Meta Feature Augmentation."
venue: "ICML"
pages: "12964-12978"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/LiQZ0X22"
ee: "https://proceedings.mlr.press/v162/li22r.html"
url: "https://dblp.org/rec/conf/icml/LiQZ0X22"
authors: ["Jiangmeng Li", "Wenwen Qiang", "Changwen Zheng", "Bing Su", "Hui Xiong"]
sync_version: 3
cite_key: "conf/icml/LiQZ0X22"
---

Contrastive Learning relies on "informative" features or "hard" features.

In this paper they propose to directly augment in latent space, by learning discriminative representations without a large amount of input data. They perform meta-learning to build the augmentation generator that updates its parameters with reference to the encoder performance. To prevent collapse a margin-injected regularizer is added in the objective function.

Suppose the input data has $M$ views. Initialize $M$ neural networks as meta-augmentation generators, all of which are used to augment the features of each view. To learn anti-collapse features, there are two ingredients:
 - Margin-injected meta-feature augmenrtation (use the performance of the encoder in one iteration to improve the view-specific features for the next. For original and augmented features, inject a margin of $\mathcal{R}_{\sigma}$ between their similarties)
 - Optimization-driven unified contrast, which contrasts all features in one gradient back propagation step. This also amplifies the impact of instance similarity that deviates far from the optimum and weakens the impact of instance similarity that is close to the optimum.

The meta-learning objective is

$$
\arg \min_{\omega} \mathcal{L}(\{g_{\nu}(f_{\theta}(\tilde X)), a_{\omega}(g_{\nu}(f_{\theta})(\tilde X))\})
$$

The argument to $\mathcal{L}$ is the set of both original features and meta-augmented features and $\theta$ and $\nu$ are the parameters of the encoders and projection heads, computed by backprop.

We do the second derivative over the weights to update $\omega$.

How do you avoid collapsed augmented features? The trick is to inject a margin to encourage $a_{\omega}$ to generate more complex and informative features. What does this look like?

$$
\sigma^+ = \min [\min (\{d(\{z^+\}_{k^+})\}), \max(\{d(\{z^-\}_{k^-})\})]
$$

$$
\sigma^- = \max [\min (\{d(\{z^+\}_{k^+})\}), \max(\{d(\{z^-\}_{k^-})\})]
$$

In other words,