---
title: "Learning to Interpret Natural Language Navigation Instructions from Observations."
venue: "AAAI"
year: 2011
type: "Conference and Workshop Papers"
access: "open"
key: "conf/aaai/ChenM11"
ee: "http://www.aaai.org/ocs/index.php/AAAI/AAAI11/paper/view/3701"
url: "https://dblp.org/rec/conf/aaai/ChenM11"
authors: ["David L. Chen", "Raymond J. Mooney"]
sync_version: 3
cite_key: "conf/aaai/ChenM11"
---

Presents a system that learns to trnasform natural language navigational instructions into a formal plan by observing expert demonstrations. Uses a learned leixcon to refine inferred plans and a supervised learner to induce a semantic parser.

They have to learn a lexicon, a set of phrase-meaning parts:

 - For each n-gram that appears in a plan, add the navigation plan to the meanings for a given n-gram.
 - They use a scoring funciton to evaluate a pair of an n-gram $w$ and a graph $g$
	 - $\text{score}(w, g) = p(g|w) - p(g|\lnot w)$
	 - Measures how much more likely a graph $g$ appears when $w$ is present compared to when it is not.
	 - Estimate probabilities using a count-based estimator.