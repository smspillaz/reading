---
title: "Understanding Robust Generalization in Learning Regular Languages."
venue: "ICML"
pages: "4630-4643"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/DanBR22"
ee: "https://proceedings.mlr.press/v162/dan22a.html"
url: "https://dblp.org/rec/conf/icml/DanBR22"
authors: ["Soham Dan", "Osbert Bastani", "Dan Roth"]
sync_version: 3
cite_key: "conf/icml/DanBR22"
---
Looks at robust generalization in the context of using RNNs to learn a regular language.

Map strings to labels with a compositional strategy that predicts the structure of the deterministic finite state automaton accepting the regular language.

Compositional Strategy via an auxiliary task where the goal is to predict the intermediate states visited by the DFA when parsing a string.