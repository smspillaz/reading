---
title: "How Modular should Neural Module Networks Be for Systematic Generalization?"
venue: "NeurIPS"
pages: "23374-23385"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/nips/DAmarioSB21"
ee: "https://proceedings.neurips.cc/paper/2021/hash/c467978aaae44a0e8054e174bc0da4bb-Abstract.html"
url: "https://dblp.org/rec/conf/nips/DAmarioSB21"
authors: ["Vanessa D&apos;Amario", "Tomotake Sasaki", "Xavier Boix"]
sync_version: 3
cite_key: "conf/nips/DAmarioSB21"
---

In this paper, they investigate what sub-tasks a module should perform to faciliated systematic generalization, at least on VQA. Different degrees of modularity could b :

 1. A unique module for all subtasks
 2. Modules tacking groups of subtasks
 3. Many modules, each one tackling one-subtask

Results:
 - Intermediate degree of modularity by grouping sub-tasks leads to much higher systematic generalization than for NMN modules introduced in previous works
 - Modularity most effective when defined at the image encoder stage

In an NMN you have a program generator (which decomposes the input sentence into some sort of "program" to be executed), then you have modules which can answer sub-questions according to that program.

Eg in the most de-composed NMN, for the question "is the green object left of 2", you would decompose the question into `left_of(encoder_green_object(image), encoder_2(image))`

In a "group-decomposed NMN", you would decompose into `relation(encoder_color(image, 'green'), encoder_object(image, '2'), 'left_of')`

In an "all" NMN, you still decompose the program, but one module handles everything.

Findings:
 - Libraries with intermediate degree of modularity, especially at image encoder stage substantially improve systematic generalization. Eg, the "group-decomposed NMN". It seems that they usually do about as well as subtask (the most decomposed), but they really shine when it comes to attribute extraction from multiple objects.
 - More training examples doesn't give you more systematic generalization.