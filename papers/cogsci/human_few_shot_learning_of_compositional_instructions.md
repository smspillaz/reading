---
title: "Human few-shot learning of compositional instructions."
venue: "CogSci"
pages: "611-617"
year: 2019
type: "Conference and Workshop Papers"
access: "open"
key: "conf/cogsci/LakeLB19"
ee: "https://mindmodeling.org/cogsci2019/papers/0123/index.html"
url: "https://dblp.org/rec/conf/cogsci/LakeLB19"
authors: ["Brenden M. Lake", "Tal Linzen", "Marco Baroni"]
sync_version: 3
cite_key: "conf/cogsci/LakeLB19"
---
Generate a completely new "pseudo language" and test compositional generalization on humans.

"zup blicket lug".

Must learn the meaning of each function from just a small number of demonstrations, then generalize to new primitives.

Phrases form orders that are not natural in english.

"fep" -> repeat prev token three times ("dax fep" -> red red red)
"blicket" -> take both preceding primitives and following primitives and produce outputs in alternating sequence ("wif blicket dax" -> green red green)
"kiki" -> concatenate previous and next strings in reverse order ("dax kiki lug" -> blue red, flipped from red blue).

You can also compose these: "wif blicket dax kiki lug" -> blue green red green, from red green blue -> green red green blue -> blue green red green.

Average performance across 25 participants in the study was 84.3%.

# What inductive biases exist?

Study the "one-to-one", "iconic concatenation" and "mutual exclusivity" biases.

On each trial, you are given a set of study instructions and then you have to make a judgment about a single new test instruction.

The pseudoword and colors were re-randomized for each trial. Must provide a reasonable guess.

Three trials on iconic concatenation: how you concatenate instructions together in the absence of demonstrations

Three trials on how to weigh ME vesus one-to-one judgments.
Mutual exclusivity: words mean something other than what another word is known by. Eg, if "dax" means RED, then "zup" should mean BLUE if RED and BLUE are the only choices.

There was strong evidence for each of the three inductive biases.

ME: 81.8%