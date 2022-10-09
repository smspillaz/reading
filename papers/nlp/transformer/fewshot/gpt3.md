---
title: "Language Models are Few-Shot Learners."
venue: "NeurIPS"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/nips/BrownMRSKDNSSAA20"
ee: "https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html"
url: "https://dblp.org/rec/conf/nips/BrownMRSKDNSSAA20"
authors: ["Tom B. Brown", "Benjamin Mann", "Nick Ryder", "Melanie Subbiah", "Jared Kaplan", "Prafulla Dhariwal", "Arvind Neelakantan", "Pranav Shyam", "Girish Sastry", "Amanda Askell", "Sandhini Agarwal", "Ariel Herbert-Voss", "Gretchen Krueger", "Tom Henighan", "Rewon Child", "Aditya Ramesh", "Daniel M. Ziegler", "Jeffrey Wu", "Clemens Winter", "Christopher Hesse", "Mark Chen", "Eric Sigler", "Mateusz Litwin", "Scott Gray", "Benjamin Chess", "Jack Clark", "Christopher Berner", "Sam McCandlish", "Alec Radford", "Ilya Sutskever", "Dario Amodei"]
sync_version: 3
cite_key: "conf/nips/BrownMRSKDNSSAA20"
---

# Model and Architecture

Same architecture as GPT-2 with the same tweaks:
 - Modified initialization
 - Pre-normalization
 - Reversible tokenization

"Except, we use alternating dense and locally banded sparse attention patterns in the layers of the transforemr, similar to [[sparse_transformer]]".

Train 8 different model sizes, from 125 million parameters to 175 billion parameters.

# Dataset

Common Crawl Dataset, nearly 1 trillion words.

1. Downloaded and filtered a version based on similarity to a range of high-quality reference corpora
2. Fuzzy deduplication
3. High-quality reference corpora added to the training mix.


# Training Process

Big batch size, relatively small learning rates.

To tune the learning rate, use " An empirical model of large-batch training" (gradient scale method).

# Evaluation

Evaluate each example in the evaluation set by randomly drawing K examples from that task's training set as a conditioning.

On takss that involve choosing one correct completion from several options, provide K examples of context plus correct completion.

On free-form completion, use beam-search with beam width 4 and length penalty of 0.6.

# Discussion

What realistic usecases can you come up with for one-shot learning

-   Style transfer
-   code refactoring
-   code translation

The model ws able to do close to perfect two-digit summarization with few-shot learning => only 10,000 combinations. Could possibly memorize it, but would need to see the training data and how the data is tokenised.

 => to learn the rules you need 10x10x10