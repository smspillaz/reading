---
title: SynthBio - A Case Study in Human-AI Collaborative Curation of Text Datasets.
venue: CoRR
volume: abs/2111.06467
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2111-06467
ee: https://arxiv.org/abs/2111.06467
url: https://dblp.org/rec/journals/corr/abs-2111-06467
authors: ["Ann Yuan", "Daphne Ippolito", "Vitaly Nikolaev", "Chris Callison-Burch", "Andy Coenen", "Sebastian Gehrmann"]
sync_version: 3
cite_key: journals/corr/abs-2111-06467/Yuan/2021
---

Introduces a novel method for dataset curation. Use an LLM to provide seed generations to human raters, which means that you change dataset authoriing from a writing task to an editing task.

Curate SynthBio, a new evaluation set for WikiBio, composed of structured attribute lists describing fictional individuals mapped to NL biographies.

## Problem Scope

Progress in ML depends on availability of high quality benchmarks.

There is a shortage of such for NLG, because HQ labelled text is slow and expensive to generate. Some tasks are also really hard because the average crowd rater doesn't know enough about the task.

## WikiBio



Its a database of structured biographical information.

SynthBio is a task where you have to generate a description based on the biographical information.

![[synthbio_predictions.png]]

### Problems with the Dataset

1. Noise: Biograpchies contain information that cannot be found in the corresponding infobox and vice versa
2. Many infoboxes are short or indecipherable due to improper formatting
3. Validation and test sets fomed from real people and the language model has probably seen information about this person in its training set already.
4. Bias: Mathematicians are more often men, biographies in English Wikipedia are about Americans and Europeans.


## SynthBio

![[synthbio_overall_architecture.png]]

By constructing a synthetic dataset, we control for bias and reduce noise.

Curate an evaluation set that addreses some of the issues present in the original sets.

SynthBio: 2249 infoboxes of **fictional** individuals and 4692 biographices. You cannot achieve high performance by memorizing facts about real-world individuals.

Tried to get equal representation among male, female and nonbinary individuals. It has a much more uniformly distributed use of pronouns than WikiBio.

Also, each infobox maps to multiple biographies, there are multiple possible options. for how to decode the infobox into text (see Alva-Manchego).

### How to curate the dataset

Hybrid-workflow. Create a draft with the LLM and then the human edits it. Two LM,s GPT-3 and LLM.

Pipeline:
 1. LLM synthesizes infoboxes
 2. Humans revise and perform quality control
 3. LLM synthesizes biograpchies from revised infoboxes
 4. Humans revise and perform quality control over synthetic biographcies.

### How to get attribute lists

1. Generate some attribute lists and filter them (only filtered out 7).
2. Generate 350 attribute lists for each of hte eight notability types.
	1. Attributes: Gender, nationality,  birth date. All uniformly sampled.
3. To generate additional attributes, use LLM-Dialog:
	1. Birth/Death place, cause of death, partner, children, mother, father, name
	2. To generate these, use a "staged conversation" where you ask questions like a conversation.
4. Human Revision:
	1. Factual plausibility
	2. Appropriateness
	3. Formatting


### How to synthesize a biographcy

1. Generate biographies. Prompt LLM with infobox followed by "Biography of \[name\]: {"".
	1. Prepend three few-shot examples using the same format as the goal example.
2. Human revision of biographices
	1. Faithfulness: Delete text not attributable to the info box or revise text if there is minor inaccuracies.
	2. Fluency: Remove repetitive language and disfluency
	3. Formatting


## Evaluation of different models on this test set

### Methodology

Fine-tune each model on WikiBio.

Use T5 across three sizes ranging from 77M to 783M parameters. Use beam search to do inference.

Metrics:
 1. PARENT: Measure overlap between attribute values in the input and the generated output with respect to a reference (precision, recall, f-score)
 2. BLEURT: Measure semantic similarity between reference and generated output
 3. ROUGE: Measure lexical overlap between reference and generation
 4. ROUGE-L: Longest common subsequence.

Human evaluation:
 - Coverage
 - Faithfulness
 - Fluency

### Results

The models trained on WikiBio do worse on SynthBio than on WikiBio in terms of machine-metrics.

However in terms of human evaluation results - humans thought that beam search on T5 evaluated on SynthBio was much more faithful to the infobox than WikiBio.

Why the discrepancy?
 1. Focus on synthbio on tail examples with less representative and more highly specified attributes
 2. Model cannot rely on memorization
 3. Effect of model-produced  references combined with the rewriting by speakers of a different dialect.

Looking at subpopulations, what happened?

 1. No significant difference in performance as a function of the number of attributes in the input except for outlier cases where inputs are extremely long.
 2. Higher variance among results across nationalities, but no discernible pattern as to why certain nationalities do better.
 3. Notability type: "Sportsperson" does better than others.


This analysis rules out (2) and (3). One final exlanation: low-quality references lead to inflated automatic evaluation scores, so WikiBio is artificially higher than it should be. This is because you have the same distribution in the validation set, so poor performance on the infrequent stuff just doesn't matter so much.

## Discussion

*Curating Datasets*: Should we study the world as it is or hte world as we want it to be? Where you source your data from matters - WP editors are 90% men and North American.

*Advantages of Synthetic Data*: It is possibke to create a dataset that is grounded and faithful and more inclsuvie as well.

*Validity of using LMs to generate benchmark data*: Should we use generative LMs? Fully automated corpus creation is probably a bad idea. Human revision is probably still necessary for now. But it can't fix systematic biases, eg, overrepresentation of western institutions (Seung Ki Ahn is Korean but served in the US Military). Also imbalances that don't match prior knowledge - SynthBio has 5.1% PhDs whereas that's only 2% of the US population.