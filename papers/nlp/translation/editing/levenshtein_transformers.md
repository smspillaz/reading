---
title: Levenshtein Transformer.
venue: NeurIPS
pages: 11179-11189
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/nips/GuWZ19
ee: https://proceedings.neurips.cc/paper/2019/hash/675f9820626f5bc0afb47b57890b466e-Abstract.html
url: https://dblp.org/rec/conf/nips/GuWZ19
authors: ["Jiatao Gu", "Changhan Wang", "Junbo Zhao"]
sync_version: 3
cite_key: conf/nips/GuWZ19
---

![[levenshtein_transformer.png]]

Basic idea: Predict insertion tokens.

Cast text editing as a markov decision process. Decide what to do, add/edit/delete a token, then feedback observe the new state. Rewards for getting closer to the solution.

Imitation learning (expert policy).