 - Question: Have you looked at semantic representation in a compositional sense?
	 - If you took the alchemy dataset and saw that the third beaker is never full at training time and it is a test time, it would probably fail, alongside all the very similar failure cases.
 - Question: How confident are you that you can disentangle things? You could imagine finer-grained semantic information, such as a negation.
	 - To the extent that these things are not perfect, do the mistakes reflect the fact that everything else is just statistics, or can you identify cases in which the representation is right or wrong.
 - Question: With probing you know what you're looking for apriori. Can you get the model to generate this state information out of a fine-tuned model in an unsupervised way?

## How can we use this understanding of models to fix things?

 - LM fails to genreate in a context that looks like this:
 - $p(\text{world}|\text{text})$
 - Failure mode
	 - State inference
	 - Generation errors - you have the correct text, but can't generate correctly
	 - Some models cannot even use ground-truth states. If you make available to the model in all cases the ground truth representation, you still get errors sometimes!
A lot of the errors that are happening right now seem to be things that can't be fixed with the right kind of targeted supervision.

### Semantic Supervision

 - Auxiliary loss, joint training and backpropagating through the probe in the training set to ensure that we capture all the information that we want.
 - This works pretty well, it can make things a little better. Eg, it can help sample efficiency.


### Inferring latent semantic states

Eg, hindsight methods, if we know what the states are in the future, we could infer the latent states in the past. We can do inference in this model.

Knowing what will be said *next* makes it easier to guess what happens *now*.

Step 1: Guess the latent sttae based on context and completion

Step 2: fine-tune the model for both language modelling and state prediction tasks

State supervision: By understanding where and how representations of world state are encoded in text, we can identify sources of errors and sometimes fix them with targeted supervision.

What problem are LM's solving?
 - Lots of mutually incompatible beliefs about the world which produce text
 - When we train LMs we're just modelling the mixture distribution
 - There is no meaningful sense in which a model has a belief about which facts are true or false.

There's a lot of literature on using LMs as knowledge bases, but whose knowledge and whose priors?

BUT. The story is pretty different once we think about prediction-in-context. A good enough LM might infer bleiefs and goals in context. We might expect the LM to represent things contextually.

What if we took the view that language models are somewhat smart but are just failing to model.

What kind of prompts should you right? One that indexes as a precisely as possibel the author I want to simulate.

What kind of grounded / linguistically informed supervision should you get - what

What kind of modelling improvements manner - one that makes it easier to reason about the internal representations.

A Mathematical Framework for Transformer Circuits

in compositional generalization all these fancy models and data augmetentation techniques which don't quite solve the problem are beaten by pretrained models which also don't solve the problem.