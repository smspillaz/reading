---
title: "Diverse Demonstrations improve In-Context Compositional Generalization"
---
In-context learning works well when the training and test sets are drawn from the same distribution. However in compositional generalization, selecting similar demonstrations isn't sufficient, as no example will be similar enough to the input.

In this work, they select *diverse* demonstrations that aim to cover all the structures required in the output program.

They use "noisy" demonstrations during training to avoid over-reliance on demonstrations.

They test on three semantic parsing datasets and show that with diverse demonsrtations, you improve performance by 23 points. So it does well on SMCalFlow, for example.

The reason why increasing diversity is important is that we want the demonstration to cover all the structures in the expected output program.

# How to select diverse demonstrations.

![[diverse_demonstrations_selection.png]]

Given some input $x_{\text{test}}$, two approaches:
 * Coverage based: Define some set of elements that we want the prgoram to cover and then select examples which contain these elements, called Cover-LS.
	 * Predict and then attempt to cover *local structures* (sub-trees) of the output.
	 * Predict what the local structures are likely to be using an auxiliary model, assuming that predicting the local structures is easier than predicting the entire program. Then iterative select examples taht cover the predicted local structures.
	 * This requires converting the program into an abstract syntax tree and replacing strings and numbers with placeholders.
	 * This also requires that you know what symbols map to local structures, or you can learn it in some way. In this case, they train T5 on the training set and then use beam search to find local utterances.
	 * Once you have all the local structures, you can retrieve examples from the training set which cover that local examples that are not yet covered.
 * Utterance coverage (Cover-Utt):
	 * Covers words in the input utterance as opposed to predicted local structures.
 * Another approach: Determinental Point Processes: select examples which are dissimilar to each other but relevant to the input utterance. You can do this by computing TF-IDF vectors for each demonstration.


Results:
 - Cover-LS gets
	 - 85.4% on the template split of GeoQuery (about the same as fine-tuned T5)
	 - 73.5% on SMCalFlow-CS (better than 50% for tine-tuned T5)
	 - 64.4% on COVR-10 (better than 21.5% on finetuned T5).
 - Cover-Utt gets:
	 - 82.1%
	 - 69.7%
	 - 78.1%

So Cover-Utt, despite just trying to find examples covering the right words, seems to also do OK in these cases.