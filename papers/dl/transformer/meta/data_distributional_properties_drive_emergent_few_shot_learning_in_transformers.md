---
title: "Data Distributional Properties Drive Emergent Few-Shot Learning in Transformers"
tags: ["DeepMind"]
---

Large Transformers models can do in-context learning without being explicitly trained for it. This paper tries to look into why that is. The main finding is that in-context learning emerges when teh training data exhibits particular distibutional properties (eg, clusters as opposed to being uniform) and emerges even more strongly when meanings or interpretations are dynamic and context dependent.

Natural datasets differ from typical supervised datasets due to a few features, namely:

 - *bursty*: A given entity does not have a distribution which is uniform over time. The upshot of this is that if you see an entity in the context, its much more likely to appear in the same sequence being predicted (eg, language modelling).
 - *zipfian*: Marginal distribution across entities is hgihly skewed, there is a very long tail of infrequent items.
 - *dynamic*: Meanings are often dynamic as opposed to fixed. So a single entity can have multiple possible interpretations (polysemy and homonymy) and multiple entities can map to the same interpretation (synonymy), usually in some context dependent way. So the training data  is somewhere between classic supervised learning and few-shot meta-learning.

# Experiment Design

Use the Omniglod Dataset.

1623 different character classes from various international alphabets, with each class containing 20 handwritten examples. Few-shot challenge to classify examples that were never seen in training.

Training data is the first 16 elements of a sequence as "context", then a query image. Images can recur throuhgout training and the integer label for each image class is fixed (which is a pretty big depature from conventional few shot training where the labels vary).

Trained the model on "bursty" vs "non-bursty" sequences. So in bursty sequences the query appears in the context. In non-bursty sequences the query does not appear. There is also a distractor image appearing the same number of times. Non-bursty is basically just uniform sampling.

Then we want to measure in-context learning and in-weights leanring. How do we do this?

 - In-context learning: Use the few-shot setup, so you have 2 different image classes with 4 examples each, with randomized labels (note that this is quite different from the training setup). So you have to use the context to predict the result. We're looking for better than random performance (50%).
 - In-weights learning: Image classes selected uniformly without replacement with the same labels used in training. There is no context - you have to use only the weights. Better than at-chance is (1/1600).


Findings:

 - Burstiness helps, especially when it is there in training. However, there is a tradeoff - more burstiness means less weights learning and more in-context learning.
 - Improvements in in-context learning come from a long-tail distribution. Otherwise the weights overfit.
 - Multiplicity of labels: Increasing label multiplicity increases in-context learning (not a surprise given that you're basically doing few-shot meta-learning).
 - Within-class variation: Varying whether the classes contain a single image or a lot of different images. Greater within class variatio nleads to greater in-context learning. Making the generalization problem harder increases the likelihood of in-context learning.


How to get in-context learning and in-weights learning to co-exist?

They say that the main thing you need is a zipfian distribution of labels. So some things happen very often and other things don't happen often at all.

Architecture also matters. If you do the same thing with an RNN it won't work.

# Discussion with the Author

Even if the label is always the same, if it shifts at test time, in context learning still works?

In training you never see x or z. They get a random label

If you evaluate on a or b with different labels: author's intuition is that it will not work. They do sort of look at it in the "multiolicity of item label mappings" experiment.