# Testing ability of language models to interpret figurative language
(Emmy Liu, Chenxuan)

Presents FigQA, Winograd style benchmark task.

Most NLP focuses on concrete question answering.

Language is interesting because its figurative sometimes too.

Metaphors and similes.  "The development of the steam engine was like the discovery of fire by cavement". - Question - what does this tell us about the impact of steam engines on society? 

Understanding metaphores is important not only for language comprehension but also the frame of mind that you start with.

LMs might be considerably weaker about generating appropraite figurative language.

Can LMs correctly make inferences about creative language used by humans?

 - Winogra style task - you have to pick the correct answer.

Forward and backward accuracies, eg, correct answer given the metaphor, choosing the metaphor for a literal meating.

Generation: Generate a metaphor for a statement and then see if humans like it.

"The new mattress is just as comfortable as sleeping on rocks"

Dataset characteristics:
 - Object metaphores
 - Visual metamores
 - Social/cultural metaphors

Results:
 - How well pre-trained LMs do in the zero-shot context.
 - Can strong LMs perform well on interpreting metaphors zero shot? No. Human does significantly better than all models.
 - Backwards directly is much worse.

What helps to improve performance:
 - Fine tuning helps, but not scaleable. Novel phrases might not follow the pattern found in the dataset.
 - Prompting? Doesn't help much.

How well do LMs do at generating interpretations for metaphors?
 - Out of 4 completions - GPT-3 Davinci
 - Correct: 50.8%
 - Contradictory completions: 37.7%

Usually completions are overly literal. Eg "it was a fortress that appeared like a pebble. That is, it is a fortress that was a pebble"


Cultural knowledge is actually easy for the models in the zero-shot setting. Training improves object, visual and social knowledge.

# Compositional Task-Oriented Parsing as Abstractive Question Answering

Wenting Zhao.

Input: Utterance
Output: An unambigupus tree of intents

Each utterance has a top-level intent. Each intent has slots which has arguments specifying the important aspects of the task.

Prior work:
 - Just linearize the parse tree and use that as the output of a sequence-to-sequence model. Each node is enclosed with brackets, brackets indicate parent relationship.
 - Limitations: Linearlized trees have a mixture of natural language and symbolic tokens. Pretrained models are only trained on pure natural language.
 - Can we reformulate such that input and output is natural language.

Proposes a general reduction from TOP to abstractive QA.

To handle few-shot setting, train QA models with the masked span prediction objective.

Step-by-step:
 - Find out the intent. Eg, just ask the model "what did the user intend to do?" -> get directions
 - Find out the slots associated with the intent. Eg, just ask "What are the slots?"
 - Find out the values corresponding to each slot -> Ask "what is the X", eg, what is the destination for each slot.

Tricks to improve accuracy
 - Incorporate answers to previous quesrtions as context. So you basically have a dialogue.
 - Incorporate domain's metadata. Eg, give a literal description of what the question is about in the context for each questions.
 - Turn QA into masked span prediction. We turn the QA pairs into declarative sentences

# Lingusitic Framework Models go Toe-to-Toe at Neuro-symbolic Language Modelling


Symbolic Linguistic Representation - these were the dominant paradigm in CL.

Comparison by comibnation - would the sum of two representations be redundant or symbiotic? You could also convert between different formalisms etc.

Comparison by conditioning.

7 sentence-structure SLR (symbolic linguistic representations) with different properties
 - Semantic constituencies
 - Syntactic constitutencies
 - Semantic dependencies
 - Synatctic dependencies

There is a corpus.

Right now we use ground truth graphs at training and test time which controls for parser performance.

Two questions - how can we compare different representations frameworks. We do that by conditioning.

1. Compare by conditioning next token predictions on different SLRs
2. Compare by combining with pretrained incremental transformer

Mechanism: We do some factoring - split up the graph into subgraphs. Encode token-relevant sugraphs and including preceding contexts

Marked improvement over baseline purely neural transformer LM. Subtle differences in linguistic representation really do matter.

# Improving Compositional Generalization with Latent Structure and Data Augmentaiton

[[improving_compositional_generalization_with_latent_structure_and_data_augmentation]]



# DiFFCSE: Difference-based Contrative Learning for Sentence Embeddings

Yung-Sung Chaing

SimCSE is basically SimCLR for NLP. Produces augmentations by changing the dropout mask in transformers.

In SimCSE the only thing that is helpful is changing the dropout mask.

Why do we need positive pairs in contrastive learning?
 - To make the presentations invariant to augmentations
 - But the thing is that sometimes we want the representation *not* to be invariant to the augmentation. Sometimes doing masking actually changes the meaning of the sentence!
 - Can we make the representations be *aware* of the augmentations but not necessarily invariant to them?


The discriminator is conditioning on the sentence embedding. The gradient of the discriminator will be propagated to the sentence encoder and we can force it to compress the information of the input sentence as much as possible. This enables the discriminator to detect the tiny difference.

Qualitative study:

SimCSE-BERT base:
 - Query: this is not a problem
	 - This is a big problem
	 - You have a problem
	 - I don't see why that should be a problem

DiffCSE-BERT base:
 - Query: This is not a problem
	 - I don't see why this could be a problem
	 - I don't see why that should be a problem
	 - This is a big problem

Augmentations in natural language are not really useful.

DiffCSE is a new unsupervised sentence embedding framework that is awakre of but not invariant to MLM based augmentation.

DiffCSE can achiecve SOTA on STS and transfer tasks.

Extensive abalation studies demonstrate that DiffCSE is useful.

Question: Equivariance is not just about sensitivity right? Are there symmetries other than contrast?

# Bilingual Tabluar Inference


