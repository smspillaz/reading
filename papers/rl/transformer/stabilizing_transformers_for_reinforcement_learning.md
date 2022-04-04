---
title: Stabilizing Transformers for Reinforcement Learning.
venue: ICML
pages: 7487-7498
year: 2020
type: Conference and Workshop Papers
access: open
key: conf/icml/ParisottoSRPGJJ20
ee: http://proceedings.mlr.press/v119/parisotto20a.html
url: https://dblp.org/rec/conf/icml/ParisottoSRPGJJ20
authors: ["Emilio Parisotto", "H. Francis Song", "Jack W. Rae", "Razvan Pascanu", "\u00c7aglar G\u00fcl\u00e7ehre", "Siddhant M. Jayakumar", "Max Jaderberg", "Rapha\u00ebl Lopez Kaufman", "Aidan Clark", "Seb Noury", "Matthew Botvinick", "Nicolas Heess", "Raia Hadsell"]
sync_version: 3
cite_key: conf/icml/ParisottoSRPGJJ20
---

Applying Transformers to the reinforcement learning setting is hard. This paper discusses some methods for how you could tweak the architecture to improve training stability.

Proposed architecture is called "Gated Transformer XL" (GTrXL). Tries to solve the issue that transformers have poor training stability which makes them ill-suited to reinforcement learning tasks.

![[gtrxl_architecture.png]]

The main idea is to make layer norm optional and replace the residual connection with a gating unit. Many different options were tried but the best one empirically was to use a GRU cell.

Note that this architecture is in use for cases where you have a step-by-step memory agent in POMDP problems. It might not be so relevant for other cases.