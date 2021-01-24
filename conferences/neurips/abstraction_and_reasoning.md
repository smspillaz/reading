# Abstraction and reasoning in modern ML systems (Chollet, Szgedy)

## (1) What is generalization

The ability to handle tasks that differ from previously encountered situations -
ability to deal with novelty and uncertainty.

- System-centric generalization: Ability to adapt to situations not previously
  encountered
 - Developer aware generalization: Ability to adapt to situations that the developer
   that the creater could not have anticipation

The first definition is the one that we usually rely on.

Generalization: Conversion ratio between past experience and potential operating area.
 - rate of operationalization of experience wtih respect to future behaviour.


You can categorize AI system by their level of genearalization
 - No generalization: Task specific algorithms
 - Local generalization: Adaption to known unknowns within a known set of tasks (ML)
 - Flexible AI: Ability to handle a broad domain, ability deal with things that
   the creators could not have anticipated
 - Extreme Generalization: Open-ended AI

Flexible AI - there is nascent interest in this (GPT-3, SDCs, Flexible Robotics)

Another property - mirrors the structure of human cognitive abilities.

 - Task specific skills exhibited by a given system tells you nothing about its
   generalization power.
 - Relationship between what you can do and the information that you have.
 - You can increase skill without increasing generalization power
 - Skill does not characterize intelligence

Shortcut rule:
 - You get what you optimize for
 - If you optimize for task-specific perofrmance
 - Kaggle competitions: kaggle systems optimize for the
   eval metric.

There is no path from the specific to the general.

"If you can solve chess, you can solve anything"
 - We did solve chess eventually
 - But this did not teach us anything about recognition.

You can always use deep learning or a giant hash table. But then
you cannot adapt to new situations.

AI Paradox: solve specific tasks without displaying any intelligence (Descartes).

Intelligent agents can produce their own abstractions.

To compare humans and AI you need to standardize on the same set of priors
 - Abstraction and reasoning corpus
 - 1000 unique tasks - they will only share abstract commonalities.
 - Priors:
   - Objectness
   - Numbers
   - Agentness
   - Elementary geometry and topologyu

 - Core knowledge systems
   - Ancient, shared by humans and other primates, sometimes beyond
   - Innate or emerge very early
   - CK systems guide learning
   - CK is all you need to solve ARC


Nature of abstraction: re-using programs and representations
 - Identify re-usable bits, these are a called abstractions.

How do you identify when things are similar
 - If something is repeated twice, assume a single origin.
 - Sensitivity to abstract analogies

Two poles of abstraction:


 - Comparing and merging

 (a) Value centric

 - Comparing using a distance function
 - Expressing an instance in terms of prototypes.

 (b) Program centric

  - Graph of discrete operators
  - Graph isomorphisms
  - Topologically ground - merge instances that are isomorphic
    into an abstract program


Capabiltiies and limits of deep learning:
 - Excels at the first form of abstraction: DL models are continuous
 - Its intuitive that you can produce abstractions that are an anology between
   two spaces.
   - Learning a smooth geometric morphing.
   - Second engine of abstraction: program analogy (topological)


Interpolation: the origin of generalization in Deep Learning
 - What we care about lies on a low-dimensional manifold of the high dimensional space
 - Within one of these manifolds, you can interpolate between two inputs
 - The ability to interpolate between samples is the key to generalization
   - If you have things that you've never seen before you can start to make
     sense of things that you've never seen before.
   - There will be a point in training between fitting and overfitting
     that moves around the actual latent manifold of the data, so you
     can make sense of latent inputs.
   - The power of the model to generalize is much more a natural consequence of
     the data.
   - But there is a point where distances are not robust to small perturbations
     but structure is robust to small perturbations.
   - You cannot apply deep learning to problems like sorting a list, because
     they have a discrete structure. You could try embedding it in a continuous
     manifold but then you cannot use that for interpolation.

Deep learning can solve problems that require value-centric abstraction, but
not discrete reasoning problems. Anything that requires reasoning, planning,
program-centric abstraction cannot be solved.

How do you solve these sorts of problems?
 - Need ot learn how to reason.
 - Program synthesis
   - Combinatorial search over a graph of operators
   - Feedback signal: correctness check
   - Challenge: combinatorial explosion.

ARC successes:
  JS Wind: Exhaustic iterations of combinations of up to 4 ops out of a DSL
   - Lots of hardcoding priors

Machine Learning and Program Synthesis:
 - Making continuous optimization efficient:
  - Introduction of modularity and hierarchy
  - Introduce module re-use (parameter sharing)
  - Strengthen feedback signal

 - Making program synthesis efficient:
  - Introduce modularity and hierarchy in program space
  - Introduce module re-use (functional abstraction, shared libraries of re-usable
    functions).
  - Limit branding decision space via heuristics

 - Leveraging program-centric abstraction in program synthesis
  - Solve N problems via search over the DSL
  - Start identify sub-graph isomorphisms
  - Abstract these sub-programs away into re-usable functions and you add this
    back into the DSL
    - Very similar to software engineering

  - Leverage deep learning as a way to reduce the program search space
    - Bridging both worlds.
    - All intelligence is a combination of both forms of abstraction.
    - You need to combine both forms of abstraction.

  - Task level vs global timescales
  - Deep learning is great as a perceptual layer
  - You can use deep learning to produce an intuition over the space of tasks


 - Research areas:
   - Using Deep Learning as a part of a synthesized program
   - Using DL tp guide program search

 - Long-term vision:
   - Lifelong learning
   - Global library of abstract subroutines
   - Perceptual meta-learning, capable of quickly growing task-level model across
     a variety of tasks
   - Modular task-level program learned on the fly to solve a specific task

Both forms of abstraction are drive by analogy.

# What is it that Machines are Learning?

 - Task to distinguish photos with animals in them from
   photos that have no animals in them
 - Trained on dataset from national geographic
 - Look under the hood - in many images of animals, the background
   is blurry, but in images where you have no animals, the background
   is clear. The machine was using the low-frequency background as an easy cue.
 - What happens when you photoshop an object into different poses.

Perceptual categories vs model-based concepts

 - Brige: Human concepts of bridges go much deeper
   - Eg, waterbridge: bridge the water, allows boats
     to travel over the highway
   - Ant-bridges
   - Bridging our hands
   - Bridge of a song
   - Concept has been extended in a way that's very human-like,
     but bridge-detectors can't really deal with.

A concept is a package of analogies
 - How can we get machines to learn *concepts* rather than perceptual categories


Survey a few selected AI methods for abstraction and analogy
 - deep learning
 - probabilistic program induction
 - copycat architecture

(1) Deep Learning

 - Raven's progressive matrices
 - You have a matrix of figure that are changing in some way
   across the rows and columsn
 - Fill in the 9th figure, choosing from the candidates.


 - Zhao et al 2020: Solving Raven's Progressive Matrices with Neural Networks
   - 16 images in the problem
   - Tried different neural network methods
   - Learn a probability distribution over the candidate solutions
   - You need some automatic way to create raven's like problems -
     stochastic image grammar
   - You can solve this task better than humans
   - But what do they learn?

 - In the RAVENs dataset there is some bias! The original group generated
   answer candidates by taking the correct answer and modify either zero or one
   attributes.
   - There's a shortcut possibility here - take the candidate answers
     that were created and figure out what the majority across the candidate
     answers for each attribute.
   - Training on the candidate answers only produced as good a result
     as training on the entire dataset - just always pick one answer
     when you have a problem of a particular type
   - Removing the bias results in a performance that is much lower.


 - Lots of people have tried deep learning approaches
 - Limitations:
    - Requires a very large corpus of examples
    - Need to generate examples automatically, suceptibility to shortcuts
    - Networks are not very transparent about what they learn. Hard to tell
      if they're doing the task that you want or if they're finding some other
      way to get the correct answer.
    - If the goal is abstraction, training on 10s or 1000s of examples makes
      very little sense.


(2) Probabilistic Program Induction Approaches

 - Few-shot learning
 - Learning to create programs that represent an abstraction
   or a generalization of a concept.
 - Define a domain specific language for the induction procedure which
   consists of primitives and some kind of grammar for combining
   the primitives to generate the data and generate an abstract
   concept that will explain the data.
 - Given an input, find a program $S$ that generates that input.

   - Define a prior probability $P(s')$ and a likelihood over possible programs
     $P(I|s')$.
   - By Bayes rule, $s = \arg \max_{s\ \in S} P(s'|I) -> P(I|s')P(s')$
 
 - Omniglot challenge- you have multiple examples of handwritten characters
   from different writing systems.
 - DSL: Primitives were different kinds of pen-strokes that you could combine
   in a hierarchical way, then parts that combine the sub-parts in certain ways
   and then relations among the sub-parts
 - Type-level.
 - To create or generate a character, there is variation in how you do the strokes -
   you can create different instantiations of a given character.
 - Now the system that generates these characters has to learn the probabilities

   - Probabilities: learned frm data
   - Different probability distributions that are learned from the type
     and the instantiation.

   - tasks: one-shot classification - I give you a handwritten character and
     20 candidates and which one is the same character
   - one-shot generation - generate a new version of the characters.


 - Classification task: let $I^c$ be the example where $c$ is the character
   class. Let $I^t$ be the candidates for $t = 1, ..., 20$. Approximate $P(I^t|I^c)$
   and choose $I^c$ with maximum conditional probability
 - To generate the prior, approximate it using MCMC to generate a program to represent
   $I^c$. Then re-fit the program to determine which one fits the best.

 - Generation task: We have to find a program to generate $I^c$, then run that
   program to generate a new example.

 - Bayesian Program Models can learn the generation.


 - Limitations:
   - You need a lot of built-in primitives
   - You need enough data to learn prior probabilities
   - Can require quite a lot of search
   - Hard to scale to more complex problems - as domain-specific language
     becomes more expressive, search becomes less tractable.

   - Hybrid symbolic-neuro system.

 - Copycat 
   - Human analogy making: if abc -> abd
                              pqrs -> pqr? (pqrt)
                              ppqqrrss -> ?
                              axxd -> xqxxx -> ?

   - Meant to be a tool for exploring general issues of abstraction and reasoning.

Open questions on how to make progress in this area

 - Community needs a common suite of challenging tasks
 - Advantages:
   - We can be explicit about prior knowledge
   - By avoiding language-based tasks we can avoid anthropomorphizing what a system
     has achieved.
   - Evaluate on hidden human created examples
   - Static test sets tend to get overfitted to.


# Kinds of Reasoning

 - Common sense reasoning:
   - The large ball crahsed through the table because it was made of steel
    - what was made of steel?

 - Probabilistic reasoning
 - Mathematical reasoning
  - Can every planar graph color by 4 colors such that adjacent nodes have a
    different color?

 - Mathematical Reasoning:
   - Use it in a general sense
     - Rule-based reasoning
     - Formal reasoning
     - Deductive reasoning

In mathematical reasoning you have facts that have a discrete truth value. There
are also statements that are unprovable.

Subtasks of mathematical reasoning
 - Foundations: collecting/postulating axioms and logical rules.
 - Deduction
 - Conjecturing - new facts based on evidence.
 - Concept building: creating new concepts based on previous proofs.

Reasoning Primitives by Peirce:

 - Deduction: We have a rule, we can do cause and effect. If this then that.
 - Abduction: "All beans in this bag are white, these bags are white, the beans are from this bag" -> not always true, but depends on our knowledge
 - Induction: Conjecture from correlation.


Logical reasoning systems:
 - $(a \land b \land c) \lor (a \land \lnot c) \implies d$
 - First-order logic: can quantify over arbitrary objects but not functions:
   $\forall (x, y) x + y = y + x$
 - Higher-order logic: $\forall f: \text{COMM} f \iff \forall x, y : f(x, y) = f(y, x)$
   - Allows us to quantify everything as long as everything is type correct.

Representation of a formula:
 - A tree or a graph
 - Use sequences - a sequence represents a statement that $\forall x, x = x$
 - Merge subexpressons that occurr together which lead to an acyclic grpah.

Neural Representations of formulas 
 - Embed them with RNNs or with Transformer
 - Tree-recurrent representations
   - Shape of the neural links describes how the nodes are connected
   - They come with a lot of computation overhead, not such uniform structures.
 - Graph neural networks: attention masks to impose tree structure.
   - All trees are graphs.
 - Sequence of characters

Supervised Learning of Deduction:
 - G: Goal statement ot prove
 - D: database of statements to look up from
 - O: Possible operations to perform

 - How to select a subset of statements from the database such that
   when we perform an operation involving the goal we get a new set of goals

Premise selection from knowledge base:
 - Goal -> Embedding network
 - Potential premise -> embedding
 - Ranking networks
   - DeepMath - DeepSequence models for premise selection
   - Graph Representations for Higher-Order Logic and Theorem Proving
 - Avoid running the whole network for every potential premise
   - Pre-compute the embedding of all the potential premises, then run
     the left part of the network only
   - Then if the combiner network is cheap, we can just run the left hand
     side (only the goals).

 - One can create a search process which results in proof-search trees.
 - Then once one reaches the end of the proof search tree then you reach the
   end of the theorem proving process.

Approximate One-step Reasoning:
 - Assume $f: X \to Y$ that maps from one class of formulas, that is easy
   to compute but the inverse function $F$ is heard.

 - Idea: Generate a lof of $(x, f(x)) = F(f(x)), f(x)) = (F(y), f)$
 - Eg, differentiation/integration - integrating is nontrivial
 - "Deep learning for symbolic mathematics" - generate many candidates, pick the
   one that checks out.
   - Need to generate training data
   - Need to check at inference time whether network produced something correct

Mathematical Reasoning in Latent Space: ICLR 2020
 - Rewrite the formula in the embedding space.
 - Trained on a single-step rewrite, but if you train for several
   steps you get a reasonably good representation.


Open Challenges:
 - Long-term planning for complicated mathematical deductions
 - Reinforcement learning has quite a bit of exploration and planning work
   done, but this is a highly nontrivial problem.
 - Neural theorem-provers already outperform traditional theorem proving but
   long-term planning is not where it could be.
 - Finding far-away connections between different areas.

