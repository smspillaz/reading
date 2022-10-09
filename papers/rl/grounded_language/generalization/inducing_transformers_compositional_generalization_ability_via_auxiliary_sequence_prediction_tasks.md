---
title: "Inducing Transformer&apos;s Compositional Generalization Ability via Auxiliary Sequence Prediction Tasks."
venue: "EMNLP"
pages: "6253-6265"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/emnlp/JiangB21"
doi: "10.18653/V1/2021.EMNLP-MAIN.505"
ee: "https://doi.org/10.18653/v1/2021.emnlp-main.505"
url: "https://dblp.org/rec/conf/emnlp/JiangB21"
authors: ["Yichen Jiang", "Mohit Bansal"]
sync_version: 3
cite_key: "conf/emnlp/JiangB21"
---

Motivated by the failure of transformer models on the SCAN challenge, proposes two auxiliary sequence prediction tasks that track the progress of function and argument semantics, as additional training supervision;.

During inference, jointly predict the next action and next tokens in the auxiliary sequences at each step.

Experiments on SCAN show that this method encourages the Transformer to understand compositional structures of the command, improving accuracy on multiple splits. With only 418 samples this approach still achieves 97.8% accuracy on the MCD1 split on SCAN.

# Architecture
![[inducing_transformer_compositional_generalization_architecture.png]]

Bascically a transformer with two prediction heads, conditioned on partially generated aux sequences.

The aux sequences represent the lower level symbolic structures.

AuxSeq 1 (repetiton): Eg, "walk left thrice" -> [2, 2, 1, 1, 0, 0] (three separate segments of "TURNL WALK"). Ignore the content and focus on the repetition.

AuxSeq 2: supervised the correct completion of every single (action sequence). Eg "jump around left twice": -> [1, 0, 1, 0, 1, 0].

## Generalization to gSCAN