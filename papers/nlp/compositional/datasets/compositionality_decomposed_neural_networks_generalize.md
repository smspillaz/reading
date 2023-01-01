---
title: "Compositionality Decomposed - How do Neural Networks Generalise?"
venue: "J. Artif. Intell. Res."
volume: 67
pages: "757-795"
year: 2020
type: "Journal Articles"
access: "open"
key: "journals/jair/HupkesDMB20"
doi: "10.1613/JAIR.1.11674"
ee: "https://doi.org/10.1613/jair.1.11674"
url: "https://dblp.org/rec/journals/jair/HupkesDMB20"
authors: ["Dieuwke Hupkes", "Verna Dankers", "Mathijs Mul", "Elia Bruni"]
sync_version: 3
cite_key: "journals/jair/HupkesDMB20"
---

What does it mean for a neural model to be compositional?

In this work, they present a set of tests that connect linguistic notions of compositionality to what neural models do.

They investigate:
 1. If models sytematically recombine known parts and rules
 2. If models can extend their predictions beyond the length they have seen in training data
 3. If composition operations are local or global
 4. If model predictions are robust to synonym substitutionsIf models favour rules or exceptions during training

They come up with PCFG and apply the tests to an RNN, CNN and Transformer.

Tradeoff: Composition functions of symbolic models are easy to understand, but they can't seem to handle noise. Neural models can handle noise but they cannot do compositions required to process natural language.


Partee on compositionality: "The meaning of a whole is a function of the meanings of the parts and the way in which they are syntactically combined". What does this mean in practice?

## Related Work

### Artificial Data

1. Mathematics (Saxton et al)
2. SCAN (Lake and Baroni)
3. Logical inference: (logical entailment): Recurrent neural networks which recursively apply the same composition function seem to have a good inductive bias here

### Natural Data

Linzen: Number agreement, test to what extent can you process long distance subject-verb agreement (see also Goldberg 2019, Lin 2019)

Syntax in MT: Syntactic features can be extracted from the higher levels.


## Testing for Compositionality.

![[compositionality_decomposed_types.png]]

Three different kinds of compositionality to test for:

 1. Systematicity (recombining known parts and rules)
 2. Productivitiy (extending your productions past the length in the training data)
 3. Substitutivity (are you robust to synonym substitutions)
 4. Localism (are the compositional operations global or local)
 5. Overgeneralization (do you favour rules or exceptions?)

### Systematicity

Szabo (2012): If you understand "brown dog" and "black cat" then you understand "brown cat" and "black dog".

How to test this: Model only familiar with $a$ in contexts excluding $b$. Can it predict $a$ in the presence of $b$ where the combination is plausible?

### Productivity

Chomsky: Language is infinite

Testing this: Can you generate sequences longer than in the training data?

### Substitutivity

Pagin: Replacing a word with a synonym in the same sense does not change the meaning of the expression

Testing: Artificially introduce synonyms and consider how the prediction of the mdoel changes whne the expression is replaced by a synonym. Two cases:
 - One: where the synonym is always used in the same context and equally often
 - Two: where the synonym only happens in short sentences but not longer ones


### Localism

When operations are very local, then the meaning of a complex expression depends only on ;local structure and meaning of parts.

In global compositionality, meaning of expression follows from total structure.

Eg: under the lcoal view: "Peter thinks that X" and "Peter thinks that Y" are synonymous if X and Y are synonymous. Under the global view, these are not synonymous as they are not structurally identical.

Testing: Compare the meanings the model assigns to stand-alone sequences to those it assigns to the same sequences when they are part of a larger compound.

### Overgeneralization

Tetsing this: How do you behave on exceptions? When you see exceptions do you follow the exception or follow the rule?


## Dataset: PCFG SET

String-edit operations, eg:

    repeat A B C -> A B C A B C
    echo remove_first D K, E F -> E F F
    append swap F G H, repeat I J -> H G F I J I J

Think of them as functions applied to strings.

The dataset is *not* balanced. Instead it mirrors the length/depth distribution of WMT17.

Length: How long the sentences are (in words)

Depth: How deep the parse tree is (eg, how many nested functions do you have?)

## Models

LSTM sequence to sequence.

Conv sequence-to-sequence (two convolutions, hierarchically applied, multi-step attention)

Transformer: Big encoder-decoder

## Experiments and Results

Task Accurracy: Do you predict the entire sequence correctly on the in-distribution data?
 - Transformer does best here. Accurracy for LSTM and conv models below 80%.

Systematicy: Hold-out `swap repeat`, `append remove_seond`, `repeat remove_second` and `append swap` function compositions.

 - LSTM 53%, Conv 56%, Transformer 72%.

Productivity: Every depth in training is 3.9, average depth in test is 8.2. Average length in training is 16.3, average length in test is 32.9

 - As  depth or length increases, pretty much all models get worse, showing a linear drop between depth 4 to depth 14 and length 15 to length 50.

Substitutivity: Select two binary and two unary functions (`swap, repeat, append, remove_second`) and introduce synonyms (`swap_syn, repeat_syn, append_syn, remove_second_syn`). Two different conditions:
 1. Equally distributed
 2. Primitive synonyms: Eg, the synonym only appears in short contexts where the depth is 1.

 - Consistency across all: LSTM 60%, Conv 58%, Transformer 90%. Transformer is more consistently correct than consistently incorrect between synonyms.

![[compositionality_decomposed_localism_test.png]]

Localism: In this case, you check if the meaning of the whole is the same as the sum of the parts. Eg, you recursively apply the model to first `prepend B A`, then apply `append C` then apply `echo`. Check if the result is the same as `echo append C prepend B A`.  We don't care about correct answers, only consistent ones.

Consistency across the board is pretty bad. Transformer wasn't any better than the other two models.

What's the cause? Input string length - usually mistakes happen if string inputs have more than five characters.

Overgeneralization: Manually add exceptions to the dataset. Eg, `reverse echo`, `prepend remove_first` and `echo remove_first` and `prepend reverse` get a different interpretation from their usual meaning.  How much do you memorize the exception vs just overgeneralizing to the compositional meaning?  Transformer applies the rule to 88% of the exceptions, and LSTM/Conv to 68% to 79%.