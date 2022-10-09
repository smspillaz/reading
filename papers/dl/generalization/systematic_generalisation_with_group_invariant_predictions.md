---
title: "Systematic generalisation with group invariant predictions."
venue: "ICLR"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/AhmedBSC21"
ee: "https://openreview.net/forum?id=b9PoimzZFJ"
url: "https://dblp.org/rec/conf/iclr/AhmedBSC21"
authors: ["Faruk Ahmed", "Yoshua Bengio", "Harm van Seijen", "Aaron C. Courville"]
sync_version: 3
cite_key: "conf/iclr/AhmedBSC21"
---

Considers situations hwere the presence of "dominant simpler correlations with the target variable" in a training set can cause NNs to be less reliant on more persistently correlating complex features. When these non-persistnet simpler corelations correlate to background factors, NNs trained on this data exhibit failure on encountering systematic distributional shift when those correlating features appear on other objects.

What helps is "group invariance methods" across inferred partitionings of the trianing set. Also suggest a simple invariance penalty and show that it can perform better than the alternatives.

If the training set is biased such that an easy-to-learn feature correlates with the target variable, SGD uses that factor to perform predictions and ignores the complex true predictive features. Arguably this is desirable absent other criteria.

Example: All chairs are red, redness ought to be a predictive rule for "chairhood". But if some chairs are not red and all chairs have backs and legs, then redness is less relevant.

Example: Biased MNIST: Digits are generally also correlated with some colour, but not in all cases.

 - This work: Biased training data, where objects correlate strongly with simpler non-semantic background information *for the majority of images* but *not* for some minority group.
 - Testcase: replace the correlating factor (eg, the color of the digit) with another correlating factor. Does the model still do "the right thing"? Usually no.

Data from Table 1: Colored MNIST dataset with every digit correlated with a colour 80% of the time.

 - When unseen colors are used, performance drops significantly (99% -> 53.26%).
 - When seen colors are recobmined with other digits, performance drops nontrivially (98.67% -> 85.05%)
 - In a "systematic shift", performance drops to 38.72% from 99.60%.

Finding: If we color the minority group digits with colours used to bias different digits in the majority group, find "marked improvement at systematically shifted tests" over teh case when the colours in the minority group are just different.


Recently proposed method "Environment Inference for Invariant Learning" can be effective in inferring the majroity and minority groups and we can use this partition to provide groups in the trianing set.

Also suggest a new method for encouraging predictions that rely on *persistent correlations across groups* with the intution that similar preditive behaviour across the grouos should be promoted throughout training.


## What is systematic vs nonsystematic generalization?

Data generated from a compostion $C$ of semantic factors $h_s$ and non-semantic factors $h_n$, then $x = C(h_s, h_n)$ and we can use this to generate test datasets to capture different scenarios. $h_n$ shall be independent of $y$, but might be *correlated* with $y$.

![[systematic_generalization_mnist_traning_set.png]]

A few definitions:

1. In-distribution generalization: $h_s \sim p(h_s|y)$ and $h_n \sim p(h_n|y)$. Validation and test sets possess the same biases as the training set and the class-conditional distributions match.
2. Non-systematic shift generalization: $h_s \sim p(h_s|y)$ and $h_n \not \sim p(h_n)$ . In this case, non-semantic factors are sampled from outside $p(h_n)$, eg, they are completely different.
3. Systematic shift generalization: $h_s \sim p(h_s|y)$ and $h_n \sim p(h_n|y')$ where $y' \sim p(y), y' \ne y$. In this case, the non-semantic factors are "adversarial". They come from a class-conditional distribution but $y'$ is a permutation of $y$ so the class-conditional probabilities of $h_n$ are completely different.
4. Semantic anomaly detection: $h_s \not \sim p(h_s)$ and $h_n \sim p(h_n)$. In this case, we *dont* want to classify $x \sim C(h_s, h_n)$ as a known $y$, because that would be relying on $h_n$, the irrelevant factor. The predictive confidence here should go down.

How does that apply to Colored MNIST?
* $T_r$ Training set
* $T_g$: In-distribution set. The coloring scheme is the same as $T_r$
* $T_s$: Systematic shift generalization: Color the test set with biasing colors from other digits
* $T_n$: Non-systematic generalization: Color the test set with random colors different from anything seen in the training set.
* $T_a$: Anomaly detection: We have never seen the digit "0" and don't even have a label for it, but we have seen the colours in use before. We shouldn't assign a high confidence to any label here because "0" is an anomaly, and assigning a high confidence to any label means that we are predicting numbers based on their correlated colour and not their number feature.

What's the trade-off?
 - "Improving performance for such scenarios involving distributional shift might come at the cost of in-distribution performance ... in real-world deployments, where one is likely to encounter unexpected situations, this is probably preferable."

## Predictive Group Invariance across inferred splits


We do not expect to have direct knowledge of the majority and minority groups corresponding to the biasing non-semantic features in a dataset. BUT assuming that we have such groups, can we come up with an "invariance" penalty?

We can ask for the class-conditioned distributions of featues to match in the sense that they lead to the same softmax distributions on average as training progresses without modifying the last linear layer.

This is called *predictive group invariance*.

This acts as a feature-reweighting in both groups (which in the MNIST case demotes the importance of colour).

A classifier extracts some feature vector $f_{\theta}(x)$ and the predictive distribution is $p_w(y|x) = \sigma(w^T f_{\theta}(x))$ where $\sigma$ is softmax.

Given a partition scheme for splitting images $x$ such that every $i$th image is associated iwth a partition label $\alpha$, define $\mathbb{P}^c$ and $\mathbb{Q}^c$:

$$
x^{(i)} \sim \mathbb{P}^c, \alpha^{(i)} = 0, y^{(i)} = c
$$


$$
x^{(i)} \sim \mathbb{P}^c, \alpha^{(j)} = 0, y^{(j)} = c
$$

We want the minimize empirical risk such that the predictions on both distributions are the same:

$$
L(w, \theta|\mathcal{D}, \alpha) = l(\theta, w|\mathcal{D}) + \lambda [\sum_c d(\mathbb{E}_{x \sim \mathbb{P}^c} [p_w(y|x)], \mathbb{E}_{x \sim \mathbb{Q}^c} [p_w(y|x)])]
$$

where $d$ is some distance function, for example, the KL divergence

$$
L(w, \theta|\mathcal{D}, \alpha) = l(\theta, w|\mathcal{D}) + \lambda [\sum_c \text{KL}(\mathbb{E}_{x \sim \mathbb{Q}^c} [p_w(y|x)]||\mathbb{E}_{x \sim \mathbb{P}^c} [p_w(y|x)])]
$$

Note, $Q||P$ and not $P||Q$ because $\mathbb{P}$ consists of "easy" example sdue to the bias, so $\mathbb{P}$ tend sto be low-entropy, whereas $\mathbb{Q}$ is high-entripy and inaccurate.


## How to partition the dataset?

Above we said that we don't assume that we have access to such a partition. Can we learn it?

The key observation is that an "invariant learning objective" formualted by IRM is maximally violated by splitting along a spurious correlation where predictions rely exclusively on it.

How do you do this? Use a soft-partition network:

$$
\hat \beta = \max_{\beta} \sum_{e \in \{0, 1\}} \frac{1}{\sum_{i'} \beta^{(i)} (e)} \sum_i \beta^{(i)}(e) l(\sigma(\phi(x^{(i)})), y^{(i)}) + \sum_{e \in \{0, 1\}} \gamma || \triangledown_{\mu|\mu = 1.0} \frac{1}{\sum_{i'} \beta^{(i)} (e)} \beta^{(i)}(e) l(\sigma(\phi(x^{(i)})), y^{(i)})||^2_2
$$

$\phi(x_i)$ are the logtis from the reference model.

$e \in \{0, 1\}$ indexes the partition.

$\beta^{(i)}(e) \in [0, 1]$ signifies the predicted probability for the $i$th example being in partition $e$, such that $\beta^{(i)}(e = 0) + \beta^{(i)}(e = 0) + \beta^{(i)}(e = 1) = 1$ and $\gamma$ is a hyperparameter.

Then we compute the partition $\alpha^{(i)} = \arg \max_e \beta^{(i)}(e)$.


## Other related baselines

1. IRMv1: Encourage reliance on features that obey stable correlations with the target variable across data from difference environments. Gradient penalty with respect to a dummy multiplier on the logits, scaling up or shrinking hte logits in different environments can only result in local improvements
2. REx: Match training risks across environments by imposing a penalty that minimises the variance of risks across environments
3. GroupDRO: Online algorithm for group-based distributionally robust optimisation, re-weights group-losses as a function evolving magnitudes.
4. Reweight: Reweight the majority group with $\frac{1}{\lambda + 1}$ and find a good $\lambda$ from the validation set.
5. Maximum mean discrepancy feature matching: Use a group-invariance penalty: $||\mathbb{E}[\phi(f_{\theta}(x_{\text{group}_0}))] - \mathbb{E}[\phi(f_{\theta}(x_{\text{group}_1}))]||^2_2$ where $\phi$ is a kernel function, eg, a mixture of three Gaussians with different bandwidths.


## Experiments

* Coloured MNIST
* COCO-on-colours
* COCO-on-places (superimpose COCO objects on to scenes from the Places dataset (eg, just cut out from the segmentation mask))


PGI beats many of the other baselines and maintains good performance in the "non-systematic shift" and "systematic shift" cases.