# Big picture

Trends:

 - Generation is all you need
 - Scale is all you need

Text editing advantages:
 - Data efficiency
 - Latency
 - Faithfulness
 - Control (eg, how much new text is inserted)

Questions:
 - Suvid: Are there any works in correcting factual errors? Is this text editing?
	 - In the text editing world not really, but it could be a nice fit. Eg, property of having high overlap between source and target (eg, tag facts, look up in database)
 - Irfan: You mentioned limited vocab.
	 - It applies to some text editing methods, will cover this later.

# Commonalities and differences

Example model: LaserTagger [[lasertagger]]

 - Sentence fusion application. Given two or more answers and you want to fuse them into one sentence.
	 - Phrase vocabulary: Set of phrases that the model can add which counters hallucination. They did some studies in the paper about how big a vocab you need.
	 - Tagging model: BERT + 1 layer decoder
 - Limitations: Realized text is sometimes unnatural since only editor is pretrained, limited phrase vocab, reordering words is hard (deleting from one place, then inserting in some other place).
	 - These are all things that later methods have addressed.

## Model landscape

 - Encoder
	 - What edit operations to use
	 - Tagging architecture
	 - Autoregressive vs feedforward
 - Pointer (how to reorder words)
 - Decoder
	 - How to insert new words/phrases

### Edit operation-types

1. KEEP
2. DELETE
3. REPLACE
	1. REPLACE_X
	2. REPLACE with placeholder, then decode placeholder (EditNTS, Felxi, LEWIS (Levensthein Editing for Unsupervised Text Style Transfer))
4. APPEND / PREPEND: Insert new tokens next to current token [[levenshtein_transformers]]


#### REPLACE_X

Counters hallucinations, ut X can become very large when having to do multi-word insertions. Hard to leverage pre-trained LMs to determine a good insertion.

The usual phrases might look like articles and prepositions that people tend to get wrong.

Pronominalize, noun number singular. Eg, defer to a knowledge base, defer to an algorithm that does it.

Swap order of sentences.

#### Replace with placeholder

## Different tagging architectures and autoregressiveness

### Autoregressive

Condition on previous tags, slower, but higher quality because you can have conditional probability.

Treat the tagging problem as a seq2seq problewm.

### Nonautoregressive

Predict all the tags at the same time using a feedforward NN.

$$P(y|x) = \prod P(y_i|x)$$

For each token predict a label. You have ground-truth tags.

Encoder use a pretrained transformer encoder, to predict the tags apply a FF layer on top of the encoded tokens.

Hard to generate arbitrary outputs. You're limited to the tags that you predefined.

Tags might not always agree as well. Eg, "We have an apples". FF would do both at the same time, eg, "we have some apple", whereas AR tagging will say "we have an apple" or "we have some apples", because it conditions on the previous word.


### Iterative Refinement

 - Apply the model to its own output
 -  - Each iteration increases performance but adds latency
 - GECToR (2022) paper: You really only need to run it for 3 steps to get maximum performance. [[gector_grammatical_error_correction_tag_not_rewrite]]

### Study: LaserTagger

[[lasertagger]] has both both AR and FF modes. Up to 7% difference is as little 1%. At a 40% increase in latency on a GPU. TO between speed and performance.


### Reordering

 - "Last year I read the book that is authored by Jane"
 - "Jane wrote a book, I read it last year"

Tagging model cannot benefit from the overlap because the tokens are in the wrong order. We want to reorder things


#### Pointer Network

At each step of the AR decdoer, predict a distribution over input tokens. Then at each decoder step, take the max probability of an input token and copy it to the output, then repeat the decoder.

Same token can be copied many times.

How would you do it non-autoregressively? Use self-attention in the encoder to do the same thing. Each input token predicts where it goes simultaneously. Each token predicts its successor, then chain them together.

 - Question: What happens if there's a loop?


### Decoder

How to insert arbitrary text?

 - Have the tagger predict where to insert and a seperate component to predict what to insert.
 - Different insertion architectures (RNN, BERT MLM)

### Case Study: FELIX

[[felix_flexible_text_editing_through_tagging_and_insertion]]
Idea 1: Separate insertion frm tagging
Idea 2: Pointer network for reordering.


Eg, "The hearts consist of  layers"

"DEL KEEP KEEP KEEP (INS 2) MASK MASK KEEP"

Then stage 2 replaces the mask tokens with something better. We have to fine-tune this model.

#### Case Study: EdiT5 (2022)

Idea 1: Join insertion and tagging
Idea 2: Insertion mdoel tells us where it wants to insert.

Decoder first predicts the location of the new text and then decode sthe new tokens.

### Seq2Edits: A model that can rewrite and explain (Mallinson 2022)

[[seq2edits_sequence_transduction_using_span_level_edit_operations]]
contains 3 sub-models for predicting tags, span-end positions and replacemnt tokens.

Model is able to provide explanations for each edit operation.

By avoiding unnecessary copying of input spans, it is up to 5 times faster than a regular seq2seq model.

First tape: Spans

Second tape: how to replace the span

Third tape: Replace each token with an explanatory tag.

Eg:

 - He still dream to become a super hero
 - He still (copy)
 - He still dreams (s-v agreement)

# Converting target text to target edits
That depends on the model and what it supports

Token level vs span level edits

Tagged vs untagged edits

Most approaches based on edit distance and edit distance matrix.

The path induces an alignment which can be used to extract the edit operations that you want. You can also collapse edit operations if you have several inserts after several deletes, for example. This is "span-level" replacement.

You can also just support replacement operation, eg, a deletion replaces with emptystring and insertion is replacing an empty span with some text.

Reordering doesn't really fit into this. Better to have a specific reordering operation.


## Questions

 - Character level tokenization? You can end up with spurious alignments, you have to be careful not to break word boundaries. Sequence length is longer
 - Can you hallucinate by doing masked insertion? Possible, but in practice scores are higher.
 - How do you know what edit path to priortize if there are multiple? Some edits are more natural than others. We found that you probably want to push the inserts into the front of a delete sequence. Eg, delete one token, then insert a bunch, then delete some more.
 - How do humans do this? Humans probably don't go word by word, they probably identify rules and go rule-by-rule.


## Applications

 - Text-editing
	 - Task-specific (GECToR)
	 - General purpose
	 - General with task-specific modificationsa nd tricks (Seq2Edits)


 - Sentence-fusion
 - Sentence splitting
 - Text normalization
	 - Converting written text into its spoken verbalization, eg, changing 6 to six.
 - Text summarization / compression (abstractive/extractive)
 - Machine Translation automatic post editing
 - Grammatical Error Correction
	 - Text editing picked up in the last couple of years.
	 - Competitive or SOTA results on public benchmarks
	 - Custom edit operations, eg, PIE uses edit operations that are a bit more tailored towards GEC. Eg, AddSuffix(s) (play -> plays). Or ChangeTense (spend -> spent)
	 - GECToR uses some linguistic knowledge: Eg, lowercase sentence, add hyphen, verb form changes.
	 - Character level operations (Replace 3rd from end with v)
	 - Non-specific tricks
		 - Pre-traineind on synthetic data
		 - Iterative refinement
		 - Model ensembling
		 - Tweaking the probabilities of KEEP at token or sequence level
		 - Favor precision over recall. Eg, bias towards KEEP operations.
 - Predicitng error types:
	 - Predict the *type* of grammatical error, this is more explainable.

# Text Style Transfer with Unsupervised Text Editing

This is usually treated as an unsupervised problem. You just have a corpus in one style and a corpus in another style.

Levels of pre-training. Pre-training seems to help a lot. Can you pretrain the softmax layer?

## Style Transfer

 - only non-parallel source and target
 - goal transfer source sentence to target style
 - "The best place I've visited!" -> "The word place I've visited"

Subtask:
 - Determine which words to delete
 - Determine how to replace them.

### Masker
[[masker_unsupervised_text_style_transfer_with_padded_masked_language_models]]
1. Train MLM on target data
2. Mask out each input word to compute likelihood
3. Replace low-likelihood words with top prediction by MLM

"price isn't bad while food is the worst in zurich"

We mask out words by one.

1. Price and isn't look normal
2. "bad", but contextual says that there's a negation so this is fine
3. "worst" this is clearly negative, so an MLM trained on low-likelihood words should give it a low likelihood. Replace it with a mask and reconstruct it.
4. Zurich: When you mask this out, there is not really anything specific in the context that tells us that we're talking about Zurich, so the model gives us low-likelihood. Solution: train another MLM on the source domain and also measuer the likelihood there. If both models agree that this is low, then just leave it alone.

When the target and source models disagree, then delete a word and replace it with something else.

Question: What if there's a domain shift? Zurich always appears in negative reviews, Helsinki always appears in positive reviews.

### LEWIS (2021)
[[lewis_levensthein_editing_for_unsupervised_text_style_transfer]]
 Coarse-to-fine levensthein editor. Given the source text, the two-step editor first generates coarse edits via a tagger, then a fine model does the edits.

Unsupervised data generation: Style classifier: use that to generate the parallel examples. Then you can train a normal supervised text editing model. Look at the attention scores of individual words. Replace with a style agnostic template. Then you can synthesize based on the template.

This works as a way to regularize your output. Distilling masker to lasertagger improves generalization.

## Incomplete Utterance Rewriting
Used for dialogue applicaitons. "Voice dialogue interaction". Users ask questions -> next question refers to something in the context more generally.

Questions are incomplete so you cannot answer them standalone, they're kind of dialogue-like.

"Did Federer have any other injuries?" -> "Did Federer have any other injuries **beside his back**"

You need to look at the dialogue context to figure out the missing detail.

Approaches

 - Vanilla seq2seq
 - Text editing enhancements (copying text)
 - text editing: 

### Hierarchical Context Tagging for Utterance Rewriting (Jin 2022)

 - Flexible insertion before each source token from non-contiguous context spans
 - Out of context insertions possible from limited vocabulary (slotted rules)

### SCAI: Search-oriented conversational AI

Things you need to solve in order to make dialogue work.


## Text Simplificiation

The process of transforming/rewriting text into an equivalent form which is simpler to understand by the target audience.

"Last year, I read a book taht is authored by Jane", "Jane wrote a book, I read it last year".

 -> There is a very high overlap between text editing

Multiple operations 
 - Substitutions
 - Sentence splitting (break a complex sentence into a simpler one)
 - Deletion
 - Syntactic style transfer.

Edit-based models bound the number of edits: 
 - Controlled generation
 - Competitive or SOTA results on public benchmarkets
 - Advantageous in preserving facts

### Exeriments for text simplification

SARI

WikiLarge

Newsela

### Sequence Labelling (2017)

 - Word alignment from dynamic programming
 - Use external aligner for input and output sentences

SL data construction: Rewrite is a special case of REPLACE

MOVEdoes cross-alignment

Train model on "silver" labels.

During inference, predict DELETE, REPLACE, MOVE, ADD, REWRITE

Only consider two operations, DELETE and REPLACE. REPLACE looks at an external simplification dictionary.

### EditNTS

Create edit labels explicitly (ADD, DEL, KEEP)

New training objective function, learn $p(z|x)$

A neural programmer-interpreter (NPI)

Decoder visits each token autoregressively and decides what edit operations to do. Interpreter executes the label and produces a simplified token. Pointer moves to the next token if there is a DELETE or KEEP operation, but stays in the same place for INSERT.

### Iterative Editing (2020)

Four edit types (Removal, extraction, reodering, substitution)

At each iteration, predict a span, then predict an operation for that span.

Optimize a score:

LM: fluency while preserving rare words

Flesch Reading Ease simplicity

Lenght: Shorter is eter

Entity score: Entity preserving

Cosine Similarity: to original sentence

When to stop iterating? Do candidate generation, we want the change in score to be high enough based on previous sentence. If ratio isn't sufficiently high, then stop.

### Felix (Flexible Text Editing 2020)
[[felix_flexible_text_editing_through_tagging_and_insertion]]
 - Tagger (transformer with pointer network)
 - Insertion model: text infilling with BERT

Features:
 - Sample efficiency
 - Fast inference time
 - Flexible editing

## Controllable Generation and Edit-based models

Errors come from Hallucinations. There is a taxonomy of hallucination from Ji et al (2022).

Variatns of hallucinations:
 - Generated text contradicts source
 - Generated text is not grounded in source text
 - Factuality: Quality of statement being true or based in fact

Causes of hallucination:
 - Divergence of source texts and references in the training data
 - Memorized factual knowledge with high parameter count
 - In general, model quality issues

### Mitigation Strategies

Mitigating with text-editing and restricted vocabulary

 - Text editing provides some natural production
	 - Partial reuse of input tokens
		 - Its a good metric to monitor and set alerts on - if you have a natural query distribution shift and are doing lots of replaces, then you are having issues. If you are mostly keeping then things are fine.
		 - At least in 75% of cases, rewritten things don't have newer terms, they mostly just reorder the input or delete things.
	 - Insertion from restircted / hotfixable vocabularity
		 - If your mdoel learns a lot of spurious correlations to replace certain pronouns
		 - You can easily define some hot fix and just remove certain entities from the vocabulary set.
		 - Example:
			 - "How old is the president" "does he have a partner" -> Does Barack Obama have a partner
			 - "How old is the president of France" "does he have a partner" -> Does Barack Obama have a partner
			 - "Who is the richest person in the world" "how did he get rich"? -> "How did Barack Obama get rich"
			 - During prediction time just remove Barack Obama from the dictionary
			 - This was in either Felix or LaserTagger. Its easier to just use a rulebook. At inference time we can directly remove stuff that's not in our vocabulary.
	 - Supplemental edit operations for critical cases
		 - See Societal Biases in Language Generation: Progress and Challenges ACL 2021
		 - There are biases in pronominalization.


### Biasing the Likelihood of edit types

- Assigning bias/weights for each edit type results in differnt model behaviour
	- Confidence bias for KEEP (Omenlianchuk et al 2020)
		- Added to probability of KEEP tag for not changing the sourec token
	- Threshold values and relative weights (Kumar 2020)
	- Edit label ratio (Dong et al 2019)


\

### Controllable Dataset Generation

Synthetic data generation for GEC. Instaed of translating one sentence in one language we translate from an ungrammatical sentence to a grammatical one.

Backtranslation: Can we "backtranslate" into grammatical errors?

Unfortunately it does nto work very well.

 - Not enough diversity
 - Tedency to synthesize only trivial errors
 - Can we use error type tags (Bryant et al 2017) to generate more diverse and realistic grammatical errors (Stahlberg and Kumar 2021)
 - Corrupt the clean sentence consistent with the error tag.

Take a large collection of clean sentence, then take a dev set tag distribution, then use the tag corruption model to synthesize parallel data. You follow the tag distribution of the dev set. Generate more data with the same distribution over tags (so that the prior distribution doesn't shift).

Different ways of training this:
 - Option 1: Add the tag to the input sentence
	 - Eg, Noun inflection: There were a lot of sheep -> There were a lot of sheeps
	 - DET: Tehre were a lot of sheep -> There were lot of sheep
 - Option 2: Finite State Transducer: -> Force model to prdouce specific type of error.

Edit-based models are much more effective in this regard. The untagged version is better than the tagged one, it doesn't help to follow the tag distribution of the dev set.

it also helps to adapt your system to specific domains. Extract different tag distributions for different proficiency levels. It didn't really help to discriminate between different proficiency levels, but it helps to adapt to the tag distribution of native speakers.

200M syntehtic GEC trianing set (C4 200M): C4_200M dataset. [[synthetic_data_generation_for_grammatical_error_correction_with_tagged_corruption_models]]

How do you ensure that the generated data is diverse enough? How can you make the model robust against compositional errors.

 - We could hope that the corruption model could pick up some of the correlations. In general we are not asking the model to that though. We are not constraining the model to only produce that error type.
 - This would be a good follow-up work.

Why did synthetic data do better than native data? Is it an artifact of scale?

 - The tag distribution is different for native speakers
 - Native speakers tend to mostly make spelling errors and not so much grammatical errors
 - Just changing the prior probabilities seems to help.
 - If you're correcting language learner text then you need to be much more aggressive

What kinds of errors are easy to generate and what kind of errors are hard to generate?

 - Whenever you try to synthesize a error that has long range-dependencies and not really a thing that you can synthesize with one tag, then you have trouble
 - Its just a way of pretraining

In English we have errant, if we were to transfer to another language we can have something simialr.

Question : Is this sort of like a style transfer problem. I wonder if you can do data-driven generation of errors as opposed to introducing them with something like errant.

## Multilingual Text Editing

### Tokenization

This is a challenge that happens in multilingual settings.

 - Token: Smallest unit of text fed into your model
 - If you notice that tokenization is bad you might need to re-run both pretraining and fine-tuning.
 - Particularly important for text generation and internationalization.

Different levels:
 - Whitespace (LaserTagger)
 - Subwords (Felix, EdiT5)
 - Morphemes
 - Bytes

Challenges:
 - Non-lating alphabets and scripts
 - Cyrillic: 200 characters
 - CJK: 10,000s of characters

Subword algorithm is greedy: if "dog" more frequent than "sei", we'll prefer it in the vocab.

how do we encode "sensei" ? For english we have the individual letters. For korean the second character won't be in the vocabulary.

The solution to this is to fall back to bytes. Whenever you see a character that you don't know how to encode you fall back to bytes. This is basically what SentencePiece is doing.


### Morphology

Languages other than english have inflections which are quite complex.

Depending on tokenization this can be quite inefficient. drive -> drives. Don't have "drives" as another token when all you do is add an aspect.

Morphological operations: We can rwite a whole bunch of these tags and its going to take a lot of time.

Learned edit operations: Insrtead of learnign a vocabulary of word reprelacements, learn vocabulary of character replacements (learn subword edits from the data). We keep our tokenization the way it is but we append certain characters in the end. you don't have to hardcode them you can just learn from the data.

### Practical Aspects

Per language model or multilingual model? Both have pros and cons.

For multilingual models you can have cross-lingual training and lower maintenance costs.

However per-language models tend to work better for the target language and tend to be smaller and have independent release cycles. If you want to update Russian you don't have to worry that Arabic has degraded.

#### Latency

Case study:

 - EdiT5 to T5. Similar models but one has a one-layer decoder.

GEC: Need to emit 27 tokens from its autoregressive decoder.

The part at the very left is different from the part on the right. Its the encoder. The part on the right is the decoder. There's a lot of latency to decode step-by-step. Decoder takes 189ms and encoder takes 15ms.


if you want to reduce the latency of the seq2seq model, target the decoder. Either:
 - Reduce the number of stepsReduce the latency of each step.


Compare EditT5 [[edit5_semi_autoregressive_text_editing_with_t5_warm_start]]: 
 - 1-layer Decoder (this is not limited to just text editing, you can have a 1 layer decoder for GEC)
 - It moves work into the encoder, in particular because the encoder has these tagging and reordering mechanisms. It reduces the number of tokens that the decoder has to decode.
	 - Limits the use of the autoregressive mechanism.
 - Decoder only need to emit 10 tokens.
 - Decoder only takes 13ms as opposed to 189 ms.


To reduce latency: Each decoder step only takes 1.3ms instead of 7ms. There are 10 decoder steps instead of 27, this gives us another 2.7x reduction.


### Data Efficiency

Text editing models need a lot less data

The dashed curves represent seq2seq models and the non-dashed curves represent text-editing models. If we have very few training examples, the seq2seq models underperform compared to text editing models. When you have only 100, 1000 examples, the seq2seq model underperforms text editing models. If you only have a small amount of data you might want to use a text editing model.

### Distillation

Levensthein Transformer: Text editing model to replicate oracle edits. [[levenshtein_transformers]]

GECToR: Ensembles of GECToR mdoels (Tarnavyski et al ACL 2022) [[gector_grammatical_error_correction_tag_not_rewrite]]

# Recommendations and Future Directions

## Recommendations

Say you have a text-generation problem: Do your sources and targets overlap? If no, seq2seq model. If there is then consider how much training data you have. If you have lots of data and its latency critical, then text editing, otherwise seq2seq.

Tutorial Propsoal:

 - textedit.page.link/paper
 
## Future Work
1. Learned edit operations
	1. How to infer the latent operations that happen when you re-write the text and how can you apply them? Eg vector quantization
2. Tokenization optimized for editing
	1. No comprehensive comparison of tokenization and their effects on text editing methods
3. Text-editing for specific pre-training
	1. how can we design some text-editing specific pre-training methods that would benefit pre-training
4. Sampling
	1. Beam search - for text-editing these are not necessarily applicable. How can you sample from text-editing models
5. Scaling up text-editing models
	1. If you don't really care so much about the speed but more about the quality, what happens when you start scaling this up.


