---
title: "Causal Attention for Vision-Language Tasks."
venue: "CVPR"
pages: "9847-9857"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/cvpr/YangZQ021"
ee: "https://openaccess.thecvf.com/content/CVPR2021/html/Yang_Causal_Attention_for_Vision-Language_Tasks_CVPR_2021_paper.html"
url: "https://dblp.org/rec/conf/cvpr/YangZQ021"
authors: ["Xu Yang", "Hanwang Zhang", "Guojun Qi", "Jianfei Cai"]
sync_version: 3
cite_key: "conf/cvpr/YangZQ021"
---

Proposes a novel attention mechanism, Causal Attention (CATT) to remove confounding effect in existing attention-based vision-language models, which causes attention to focus on spurious correlations in the training data.

CATT implemented as:
1. In-Sample Attention (IS-ATT)
2. Cross-Sample Attention (CS-ATT), mimicking causal intervention.


## Introduction

Due to the fact that the attention weights are unsupervised, eg, there is no word-region grounding for top-down attention or relationship dependency - the weihts may be mislead by dataset bias.

For example, "person riding horse", self-attention will learn "riding" by focusing on "person" and "horse", so it will also pass as "person riding carriage".

The dataset bias causing this is caused by a confounder. Eg, there is a common cause.

If you only train the model based on $P(Y|X)$, then no matter how large the training data, the model can never identify the true causal effect.

## Proposal

Causal Attention "helps the model to identify the causal effect between $X$ and $Y$ and thus mitigate the bias based on confounders". Based on the *front door adjustment* principle and does not require obseration of the confounder.

Light LXMERT+CATT outperforms UNITER on VQA2.0 and NLVR2

### Causal Attention

We can split the attention mechanism into two parts, a selector which sleects suitable knowledge $Z$ from $X$ and a predictor which exploits $Z$ to predict $Y$.

Eg, in VQA, X is a multi-modality set containing an image and question, then attention uses the question to pick $Z$ from the image and predict $Y$.

$$
P(Y|X) = \sum_z(Z = z|X)P(Y|Z = z)
$$

This is "IS-sampling", eg, in-sample sampling since $z$ comes from the current sample $X$.

To eliminate the spurious correlation, block the backdoor pathbetween $Z$ and $Y$. Then we can determine the true causal effect $P(Y|\text{do}(Z))$, eg, stratify the input variable into different cases and measuring the average causal effect of $Z$ on $Y$:

$$
P(Y|\text{do}(Z)) = \sum_x P(X = x)P(Y|X = x, Z)
$$

Notice that in this case we are summing over all $x$ in the possible inputs. This is called *Cross-Sample Sampling* (CS-Sampling), since it comes from other samples.

Once you have that, you can calculate the true causal effect between $X$ and $Y$:

$$
P(Y|\text{do}(X)) = \sum_z P(Z = z|X) \sum_x P(X = x)P(Y|Z = z, X = x)
$$

### How to implement Causal Attention

Parameterize $P(Y|Z, X)$ as a network followed by a softmax $\text{softmax}(g(Z, X))$

Apply normalized weighted geometric mean approximation to absorb the outer sampling into the feature level and thus only need to forward the "absorbed input" into the network for once. Eg:

$\hat Z = \sum_z P(Z = z|h(X))z$

$\hat X = \sum_x P(X = x|f(X))x$

eg, $h$ and $f$ are query functions that transform $X$ into independent query sets

So how does this tie into "in-sampling" and "cross-sampling"? Say in-sampling looks like this:

$$
\hat Z = \text{Softmax}(Q_I^T K_I) V_I
$$

Then cross-sampling would be:

$$
\hat X = \text{Softmax}(Q_C^T K_C) V_C
$$

where $K_C$ and $V_C$ come from other samples in the training set and $Q_C$ comes from $f(X)$. In that sense, you "query" other images using features from the current image for self-attention and "query" other images using features from the text for the current image and encode that as $\hat X$. Then make the prediction using information from both, or stack layers.

$V_C$ comes from the global dictionaries compressed from the whole training set using k-means.

### Using this in LXMERT or Transformers

![[catt_transformer.png]]

The inputs of the encoder include the embedding set of the current image and global image embedding dictionary. There's an image encoder and a language decoder.

![[catt_lxmert.png]]