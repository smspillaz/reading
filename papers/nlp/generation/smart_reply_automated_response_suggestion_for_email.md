---
title: Smart Reply - Automated Response Suggestion for Email.
venue: KDD
pages: 955-964
year: 2016
type: Conference and Workshop Papers
access: closed
key: conf/kdd/KannanKRKTMCLGY16
doi: 10.1145/2939672.2939801
ee: https://doi.org/10.1145/2939672.2939801
url: https://dblp.org/rec/conf/kdd/KannanKRKTMCLGY16
authors: ["Anjuli Kannan", "Karol Kurach", "Sujith Ravi", "Tobias Kaufmann", "Andrew Tomkins", "Balint Miklos", "Greg Corrado", "L\u00e1szl\u00f3 Luk\u00e1cs", "Marina Ganea", "Peter Young", "Vivek Ramavajjala"]
sync_version: 3
cite_key: conf/kdd/KannanKRKTMCLGY16
---
Challenges:

 - How do we ensure that the individual response options are always high quality in language and content?
 - How to select multiple options to show a user so as to maximize likelihood of chosen options
 - Process millions of messages and remain within latency requirements
 - How to design the system without ever training on user data except aggregate statistics?

Architecture:

 - Response selection: LSTM computation is expensive, find only approximate best repsonses
 - Select responses from response space which is generated offline
 - Choose a small set to maximize utility
 - Triggering model: Don't show suggestions if no suggestions likely to be used

Related, but not what this paper does:

 - Predicting the full response
 - Identifying the target response space (close to what this paper does, but applied in different problem settings)

Inference: Feed in an original message and then use the output of the softmax distributions to get a distribution of vocab.

 - Draw random sample
 - Greedy decding
 - Computing likelihood of known responses

Addressing the challenges:
 - Use SSL to construct a target response space $R$ consisting only of high quality responses, then use the model to pick the best response in $R$.
 - Penalize responses which are too applicable to everything (high positive bias)
 - Scoring every response candidate would require $O(|R|l)$ steps, where $l$ is the length of the longest sequence. $R$ could be very large.
	 - Organize elements into a trie.
	 - Conduct left-to-right beam search, but retain hypotheses that appear in the trie.
	 - Has complexity $O(bl)$.


Generating the Response Set:

 - Canonicalization: If things convey the same information, they should be merged
 - Semantic intent clustering: Partition responses by meaningful response intent
 - Graph construction:Edge from $u$ to $v$ if they share feature sets.
 - SSL: Label propagation

Suggestion diversity:

 - Omit redundant responses (no two responses with same intent)
 - Enforce negatives and positives (fix unbalanced replies dataset)