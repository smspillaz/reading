---
title: "Unsupervised Neural Machine Translation with Generative Language Models Only."
venue: "CoRR"
volume: "abs/2110.05448"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2110-05448"
ee: "https://arxiv.org/abs/2110.05448"
url: "https://dblp.org/rec/journals/corr/abs-2110-05448"
authors: ["Jesse Michael Han", "Igor Babuschkin", "Harrison Edwards", "Arvind Neelakantan", "Tao Xu", "Stanislas Polu", "Alex Ray", "Pranav Shyam", "Aditya Ramesh", "Alec Radford", "Ilya Sutskever"]
sync_version: 3
cite_key: "journals/corr/abs-2110-05448/Han/2021"
---

Derive state-of-the-art unsupervised NMT from a pre-trained language model. Three steps:

1. Few-shot amplication: Generate a few translations and use them as few-shot demonstrations
2. Distillation: Discard the few-shot demonstrations and fine-tune
3. Backtranslation: Repeatedly translate and then fine-tine on both directions of translation at once, ensuring cycle consistency.


The main idea behind this paper is to *bootstrap* from a weak translation model  before amplifying the translation ability via backtranslation.

In this work they don't have any special tranining data. You just have a pretrained NLM and distill it on its own output.


## Related Work

1. Encoder-Decoder architectures trained jointly with DAE/reconstruction and backtranslation
2. Large-scale generative model pre-training
3. Few-shot prompting and distillation (self-training and noisy-student training)


## Backtranslation via Language Modelling

Backtranslation was introduced as a method for data augmentation using target-side monolingual data by sampling source-to-target data from another target-to-source translation model.

In this work, cast machine translation as a language modelling task - jointly train and sample generations from a single language model for both s-t-t and t-t-s translation.

```
[L1] <seq1> [[Translate]] [L2] <seq2>
```

At test time, prompt with the first four tokens, and parse the generated result. To do backtranslation, reverse the roles.

## Bootstrapping

The main idea here is to give a few source-target pairs as the prompt, then sample.

```
Given the following passage in [L1]: <sep> <src> <sep> a good [L2] translation is <sep> <tgt> <sep>
```

Samplify a pool of synthetic target-side translations and target side translations zero-shot from another language model $q$.

Discard the few-shot prompts and fine-tune $p_{\theta}$ (the LM) on this data, reversing and fine-tuning.

## Results

### Methodology

WMT14 EnFr Benchmark. Split the training set in half, use English text from one half and Frenfch text from the other.

To implement the bootstrap, set aside 2048 training examples and sample $N_s$  (1024) EnFr and 1024 FrEn  translations zero-shot from GPT-3.

During few-shot amplication, sample four million initial target and source translations using few-shot prompts

Fine tune for two epochs in the forwarde direction and another two in the backwards direction.

### Results using self-distillation

(eg, sampling from a single model and train it to imitate and backtranslate its own few-shot prompted generations).

### Results using self-amplified GPT-3 into smaller models

Use the big GPT-3 to self-amplify its own zero-shot translations.

## Discussion

1. Bias towards English Generation: After genernative pre-training on a corpus of English-dominated text, GPT-3 is much better at translating into English rather than translating out of it. But after two epochs of backtranslations, the gap is reversed
3. Data contamination from pre-training: For high-resource language pairs, naturally ocurrring demonstrations of translation are virtually guaranteed to happen.


### Ablations

#### Temperature

Enunov: Backtranslation more effective when translations are slightly noisy. Try using a temperature of 0 or 1 instead of 0.3; lower temperatures have marginally higher test set BLEU but higher temperatures have lower test loss

#### Self-amplification

Self-amplification improves translation quality as model scales.

#### Using real few-shot examples

Instead of using synthetic examples, use real ones. Bascially no difference.

#### Almost unsupervised, three examples only

# Concusion

**Data driven Architecture Engineering**: Task-specific inductive bias engineered into and learned from the training data rather than being hardcoded in the model architecture.