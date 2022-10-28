---
title: "Masked Siamese Networks for Label-Efficient Learning."
venue: "CoRR"
volume: "abs/2204.07141"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2204-07141"
doi: "10.48550/ARXIV.2204.07141"
ee: "https://doi.org/10.48550/arXiv.2204.07141"
url: "https://dblp.org/rec/journals/corr/abs-2204-07141"
authors: ["Mahmoud Assran", "Mathilde Caron", "Ishan Misra", "Piotr Bojanowski", "Florian Bordes", "Pascal Vincent", "Armand Joulin", "Michael G. Rabbat", "Nicolas Ballas"]
sync_version: 3
cite_key: "journals/corr/abs-2204-07141/Assran/2022"
---

Basic idea: two networks, one gets the masked images and one gets the unmasked image. Both should have the same representation. There is no input reconstruction.

Base architecture is ViT.

How do you avoid representational collapse?

 - training objective: cross-entropy loss between prediction and anchor: $H(p^{+}_i, p_{i, m})$
 - mean entropy maximization regularization: Effectively, $\frac{1}{MB} \sum^B_i \sum^M_m H(p^{+}_{i}, p_{i, m}) - \lambda H(\frac{1}{MB} \sum^B_i \sum^M_m p_{i, m})$
- This basic idea is that you want small cross-entropy between anchors and predicted labels for veiws, and large diversity of predictions.


## Related work

 - DINO
 - [[data2vec_a_general_framework_for_self_supervised_learning_in_speech_vision_and_language]]

There is no patch-level loss in this work, like there is in data2vec.

## Results

Marginally better on 1%-imagenet-1k.

1%-imagenet-1k requires that you take 13 labelled examples per class, then classify the entire dataset and measure the top-1 accurracy.

MSN gets 75.7 with a larger model. MSN can beat other self-supervised models, but not the SOTA on the task.

What if you use 100% of the labels to finetune the linear layer on top? Then you get top-1 accurracy of around 76.9, which is competitive but doesn't vastly surpass others.

What if you use 100% of the labels to fine-tune the whole model? Then you get 83.4, which is competitiev with data2vec's 84.2, but not better.

## Ablations

RandomMask + FocalMask helps a lot.


