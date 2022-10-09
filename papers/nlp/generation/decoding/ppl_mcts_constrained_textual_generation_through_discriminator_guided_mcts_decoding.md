---
title: "PPL-MCTS: Constrained Textual Generation Through Discriminator-Guided MCTS Decoding."
venue: "NAACL-HLT"
pages: "2953-2967"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/naacl/ChaffinCK22"
doi: "10.18653/V1/2022.NAACL-MAIN.215"
ee: "https://doi.org/10.18653/v1/2022.naacl-main.215"
url: "https://dblp.org/rec/conf/naacl/ChaffinCK22"
authors: ["Antoine Chaffin", "Vincent Claveau", "Ewa Kijak"]
sync_version: 3
cite_key: "conf/naacl/ChaffinCK22"
---

Formulate controlled generation as a tree exploration process guided by a discriminator
indicating how well an associated sequence respects the constraint.

Evaluation:
 - Review polarity
 - Emotion control in French and English

The process:
 - Selection: Choose children from the root to a node that has not been expanded yet. Use
    $p_{\theta}(x_i, x_{1:t - 1})$ to guide selection, then use PUCT to rank nodes:
 - $\text{PUCT}(i) = \frac{s_i}{n_i} c_{\text{puct}} p_{\theta}(x_i|x_{1:t - 1})$ \frac{\sqrt{N_i}}{i + n_i}$, $s_i$ is the aggreigated score of the node and $n_i$ is the number of simulations played after the node and $N_i$ is the number of simulations after the parent. $c_{\text{puct}}$ is an exploration/exploitation tradeoff
 - Expansion: If not terminal, use LM to expand it
 - Simulation: Sample children according to probability and go to terminal node by random walk
   (eg, continually sample from the LM)
 - Backprop: Aggregate final score obtained at terminal node to each parent until root.


Datasets:
 - Amazon polarity
 - CLS from FLUE
 - Emotion


Experiments: Compare accurracy/self-blue/perplexity with:
 - PPLM
 - PPL-MCTS
 - Beam Sampling

Future work:
 - How to set the $\alpha$ parameter to tradeoff accuracy and perplexity
 - Rollout size?