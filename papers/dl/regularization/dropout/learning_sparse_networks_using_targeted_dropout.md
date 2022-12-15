---
title: "Learning Sparse Networks Using Targeted Dropout."
venue: "CoRR"
volume: "abs/1905.13678"
year: "2019"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-1905-13678"
ee: "http://arxiv.org/abs/1905.13678"
url: "https://dblp.org/rec/journals/corr/abs-1905-13678"
authors: ["Aidan N. Gomez", "Ivan Zhang", "Kevin Swersky", "Yarin Gal", "Geoffrey E. Hinton"]
tags: "['cohere']"
sync_version: 3
cite_key: "journals/corr/abs-1905-13678/Gomez/2019"
---

Standard training does not make you amenable to pruning. Introduces *targeted dropout* which selects a set of weights to be dropped using a self-reinforcing sparsity criterion.

-   In targeted dropout, we want to find optimal parameters such that our loss is low and we kee ponly k weights of the highest magnitude in the network.
-   If we were deterministic, we would just drop the low weights during training, but it might be necessary to increase them.
-   Introduce stochastiscity into the process by using a targeting proportion and drop probability. Select some bottom percentage and drop them with probability alpha.
-   Some analysis on the dependence between important and unimportant subnetworks.