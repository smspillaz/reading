# Compositionality and Out of Distribution Generalization

## Concept of Compositionality

Judith Fan 
 - How has our understanding of compositionality changed?
 - Structure of human language, how does that affect perception. You have a functional pressure to deal with a highly variable world.
 - For problems that involve scene understanding, compositionality has a huge role to play.

Kevin Elllis
 - Knowledge is not a monolith, it comes in pieces, the pieces are re-usable. They have an API. The process doesn't care about what its input is, it just cares that it is compatible.
 - You can imagine a pink elephant on the moon, you can glue those things together.
 - Individual pieces are not necessarily tied to the domains in which you first learned them.

Josh Tenenbaum:
 - Hardest to do for conventional NNs
 - All models have different aspects about how the math breaks down into pieces, linear algebra has compositionality in it.


## Are the neurosymbolic approaches the way to go?

 - Neurosymbolic models are a way to revisit the idea of compositions of simple things.
 - There's not one type of neurosymbolic model, many different flavours.
 - Look at raw data, rediscover the structure.
 - Learning centric: Standard architecture with some additional mechanisms like a key-value memory. Teach the model to be compositional.


## Why do you want to impose compositionality?

 - If you take it as a given that you don't change the underlying architecture, then you might miss a solution that turns out to be very powerful.
 - The most successful methods might use NNs to do more of the work but might use compositionality as a small part.

 - The neurosymbolic approaches provide us with tangible hypotheses.
 - Think about the kind of tasks that we are trying to model and explain
 - Maybe somehthing contraversial: "Lets just hope it emerges" is a mistake. So many examples that it is much better to explore the different possibilities. Includes other things that people think of as "neural networks".
 - Modern architectures are a form of compositionality


## Degrees of compositionality

 - Is there a notion of "good" vs "okay" compositionality.
 - Kevin: Transformations and GNN are compositional in a weaker sense. Artihmetic is compositional in a stronger sense.
 - There may be certain datsets or tasks that push you towards compositonality
 - Real world might not be totally compositional


## Compositional General Models

 - 