---
title: "Compositional Semantic Parsing with Large Language Models."
venue: "CoRR"
volume: "abs/2209.15003"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2209-15003"
doi: "10.48550/ARXIV.2209.15003"
ee: "https://doi.org/10.48550/arXiv.2209.15003"
url: "https://dblp.org/rec/journals/corr/abs-2209-15003"
authors: ["Andrew Drozdov", "Nathanael Sch\u00e4rli", "Ekin Aky\u00fcrek", "Nathan Scales", "Xinying Song", "Xinyun Chen", "Olivier Bousquet", "Denny Zhou"]
sync_version: 3
cite_key: "journals/corr/abs-2209-15003/Drozdov/2022"
---

Tries to approach compositional semantic parsing through a least-to-most-prompting approach. Prompting might be sufficiently flexible and with recent advancement it could be an effective and generic approach to address a wide range of language understanding problems.

Least-to-most prompting is promising. In [[least_to_most_prompting_enables_complex_reasoning_in_large_language_models]] they got it working on SCAN. What about harder tasks like CFQ? What about stuff that doesn't fit in the context.

In this paper, they use *dyanmic least-to-most* prompting. What does that mean?

 1. Tree-structured decomposition of language throughLM-predited syntactic parsing
 2. Use the decomposition to dynamically select examples
 3. Linearize the decomposition tree and prompt the model to sequentailly generate answers to subproblems.

On CFQ they get 95% accuracy and on COGS they get 99.2% accuracy.

How does it work?

On SCAN, least-to-most prompting would decompose the problem "look around right thrice and walk twice" into "look right", "look around right", "look around right thrice" and "walk twice".

You can decompose into subproblems, solve each of the subproblems, put them in the prompt and so on. The way you put them in the prompt is to do it sequentially, eg, first you solve "look right", then add the answer to the prompt, then solve "look around right", then "look around right thrice", then "walk twice".

Does this work for CFQ? Challenges are:
 1. Decomposition is hard
 2. Knowledge required for translation is too large to fit into a singel prompt
 3. Translation of consittuents is context-dependent.

Natural language is hard to decompose.

Also a constituent translation is context-dependent. What do we mean by this? Walk twice always translates into WALK WALK. This is not true for CFQ. See this example:
 - (1) Did M1 star M2, start M3 and star an art director and editor of M0? SELECT count(8) WHERE { ?x0 edited M0 . ?x0 art.directed M0 . M1 starred ?x0 . M1 starred M2 . M1 starred M3}
 - (2) What was produced by an art director that M1 and M2 employed? SELECT DISTINCT WHERE { ?x0 produced.by ?x1 . ?x1 a art.director . M0 employed ?x1 . M1 employed ?x1 }

In this case, "an art director" is translated into "?x0 art.directed M0" in (1) and "?x1 a art.director" in (2). This means that you cannot use normal least-to-most prompting here and translate sub-problems in isolation.
![[dynamic_least_to_most_prompting_compositional_semantic_parsing_llms.png]]

How does *dynamic* least-to-most prompting work?

 1. Decomposition using LM-based syntactic parsing: Teach the language model to do a syntactic parse, then do a tree-based decomposition. This requires teaching the model about language.
 2. Select exemplars based on the decompsotion, such that they collectively demonstrate the relevant knowledge needed to trnaslate the input sentences.
	 1. Try to make sure that all the leaf phrases are covered by exemplars.
 3. Sequential solution based on the decomposition: