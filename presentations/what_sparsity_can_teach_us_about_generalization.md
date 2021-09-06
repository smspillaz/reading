# What sparsity can teach us about generalization properties

 - Going beyond test-set accuracy
 - Training models that satisfy multiple criteria.


## Intriguing relationship between capacity and generalization

We are in a stage of ML research is throwing more parameters at a problem.

Bu the relationship between weights and generalization properties is not well understood. Diminishing returns.

Many redundancies between weights are observed.

Puzzling ability to remove the majority of the weights with minimal degradation to test set accuracy, even at extremely high levels of sparsity.

A model can fulfil an objective an many ways while violating the spirit of the objectives.

Can we do better than our current representations - if most weights are redundant, why do we need them in the first place?

### Experimental framework

Train populations of mdoels with minimal differences in test-set accuracy to different end sparsities (0 - 99%).

We can also precisely vary how much the weight representation differs.

Top-level metrics high critical differences in generalization.

 1. Sparse models amplify sensitive to adversarial examples and common corruption
 2. Varying sparsity disproportionately impacts and systematically impacts a small subset of classes and exemplars


If we look at the brittleness to corruptions, sparsity amplifies the sensitivity to brittleness.

 - Why?
 - You cannabalize performance on a small subset of classes to improve performance on others.
 - Number of classes impacted grows at high level of sparsity.


PIEs are challenging for a human to classify and also challenging for an algorithm to classify too. When you compress, you're eroding performance on the most challenging examples.

PIEs over-index on two main groups
 - Noisy examples (improperly structured, where multiple labels could apply
 - Corrupted or incorrectly labelled data
 - This is a misuse of parameters to represent these data points. We spend a lot of capacity learning the "edge cases".

Atypical data points (challenging examples)
 - Unusual vantage points of the class category
 - PIEs also over-index on the long-tail of underrepresented attributes.


## Moving beyond "algorithmic bias is a problem"

 - Characterizing bias in compressed models


"Shortcut learning" is due to relative / overrepresented training features.

The way that the model treats underrepresented features on the long tail often coincides with notions of fairness.

Geographic bias: Models perform far worse on locales that are undersampled in the training set.

Most natural image, NLP etc datasets follow zipfs law.


## Measuring the impact of compression on algorithmic bias

Celeb-A: spurious correlation between gender, age, hair color

Sparsity disproportionately impacts these underrepresented groups.

Civil comments dataset - toxic comments only in 8% of the training set. Sparsity sharply degraded model ability to detect toxic comments. Most impacts sub-groups are the least represented.

Models are spending the majority of capacity learning small subsets of the data. Whether or not this is well-spent depends on what is the long tail.

## Optimizing models that fulfil multiple desirable objectives , compact, robust, fair

Much of the literture treats these objectives as siloes

Having a formal framework to measure trade-offs creates a roadmap for training models that fulfill multiple objectives.

![[iron_triangle_fairness_fragility_compression.png]]

Iron triangles.

Distillation objectives obtain a 4.1x reduction in the number of PIEs and up to 5.7x in cases where baseline non-sparse model makes the correct prediction (from "Going beyond classification accuracy: Accuracy metrics in Model Complexity")

Knowledge distillation coupled with pruning and effectively improve t radeoff between compressed networks and disparate harm (from "Simon Says: Evaluating and mitigating bias in pruned neural networks with knowledge distillation", Blakeney et al 2021).

Not all pruning approaches are created equal ("A winning hand: compression deep networsk can improve out of distribution robustness")

 ## Open Questions
 
 1. Difference between impact of sparsity on IID settings vs OOD settings
	 1. There's an assumption of IID in the test set, in that it is sampled from the same population as the training set
	 2. In an OOD setting sparse models benefit performance for models traine don the specialized dataset. JW300 (Jehova's Witness parallel corpora - sparsity benefits generalization). Curbs memorization of artefacts that don't generalize.
 2. Spending the majority of our weights on a small fraction of the training distribution.
	 1. We're just adding more weights to solve these problems.
	 2. Is this a problem solved more cheaply else where.
	 3. If we could figure out which examples require additional constraints and adapt the training based on that feedback, then there is a promising direction we could make.




