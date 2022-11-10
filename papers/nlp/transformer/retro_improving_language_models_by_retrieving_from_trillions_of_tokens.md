---
title: "Improving language models by retrieving from trillions of tokens."
tags: ["DeepMind"]
cite_key: "journals/corr/abs-2112-04426/Borgeaud/2021"
venue: "CoRR"
volume: "abs/2112.04426"
year: "2021"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2112-04426"
ee: "https://arxiv.org/abs/2112.04426"
url: "https://dblp.org/rec/journals/corr/abs-2112-04426"
authors: ["Sebastian Borgeaud", "Arthur Mensch", "Jordan Hoffmann", "Trevor Cai", "Eliza Rutherford", "Katie Millican", "George van den Driessche", "Jean-Baptiste Lespiau", "Bogdan Damoc", "Aidan Clark", "Diego de Las Casas", "Aurelia Guy", "Jacob Menick", "Roman Ring", "Tom Hennigan", "Saffron Huang", "Loren Maggiore", "Chris Jones", "Albin Cassirer", "Andy Brock", "Michela Paganini", "Geoffrey Irving", "Oriol Vinyals", "Simon Osindero", "Karen Simonyan", "Jack W. Rae", "Erich Elsen", "Laurent Sifre"]
sync_version: 3
---

[[retro_improving_language_models_by_retrieving_from_trillions_of_tokens.pdf]]

Enhance autoregressive language models by conditioning on document chunks retrieved from a large corpus, based on local similarity with preceding tokens.

Assume a 2 trillion token database. With this, you can get comparable performance to GPT-3 and Jurrassic-1 despite using 25x fewer parameters.

RETRO combines a frozen BERT retriever, a differentiable encoder and chunked cross-attention mechanism to predict tokens based on an order of magnitude more data than what is typically consumed during training. You can also "retrofit" pre-trained transformers with retrieval and still get good performance.

Instead of increasing the size of the model, increase the size of the database. This makes the model semi-parametric. There is some existing work on using language models with databases of a limited size (billions of tokens). This work shows the benefits of scaling to trillions of tokens for large parametric language models.

## Contributions

1. RETRO: A chunked cross-attention module to incorporate the retrieved tett with linear time complexity. Retrieving based on a pre-trained frozen BERT works at scale.
2. Method and model scales well with database size. RETRO can be improved at evaluation time by increasing the database size and number of retrieved neighbours.
3. Evaluation aware proximity of test documents with the training set addressing the problem of test-set leakage.


# Architecture
![[retro_architecture.png]]

Retrieve at the level of contiguous token *chunks* instead of individual tokens.

First construct a key-value database where values store the raw chunks and the keys are the frozen BERT embeddings.

Why frozen? Otherwise you'd have to recompute the embeddings during training.

### Retrieval enhanced autoregressive token models

With some pre-computation, augment each chunk with a set $\text{RET}_{\mathcal{D}}(C_u)$ of $k$ neighbours from $\mathcal{D}$, the database. You hvae the following retrieval-enhanced log-likelihood

$$
L(X|\theta, \mathcal{D}) = \sum^l_u \sum^m_i \mathcal{l}_{\theta}(x_{(u - 1)m + i}|(x_j)_{j < (u - 1)m + i}, (\text{RET}_{\mathcal{D}}(C_{u'}))_{u' < u})
$$

Set $\text{RET}(C_1) = \emptyset$, eg, the likleihood of tokens from the first chunk does not depend on any retrieval data. So the probability of the $i$th token of the $u$th chunk only depends on previously seen tokens and on the data retrieved from previous chunks.

### How does the retrieval work?

You have a key-value memory. Each value consists of two contiguous chunks of tokens $[N, F]$, where $N$ is the neighbour chunk used to compute the key and $F$ is its continuation in the original document.

For each $C$, retrieve the approximate $k$-nearest-negibhours from the key-value database using the L2 norm on the BERt mebeddings. This gives you the corresponding values of $\text{RET}(C)$ up to $k$ neighbours. Filter out neighbours that originate from the same document - otherwise you'd end up retrieving tokens that you can use to autocomplete the document and that wouldn't be helpful.

### Model Architecture

The retrieved tokens get fed into an encoder, which computes the encoded neighbours set $E$.

For each chunk $C_u$ the $k$ retrieval neighbours are fed into the encoder yielding the outputs $E_u^j = \text{ENC}(\text{RET}(C_u)^j, H_u)$

#### Retrieval Encoder

It is conditioned on the hidden vector and you encode the neighbours given in the database. Output an embedding.

The retrieval encoder is non-causal.

The encoding of the $j$th neighbour of the $u$th chunk, depends on the attended activation $H_u$ of chunk $C_u$ at layer $\min (P)$

#### Cross-chunk Attention

To perform chunked cross-attention (denoted as CCA, not to be confused with canonical correlation analysis), split a given intermediate activation into $l - 1$ attending chunks. $H^+_u$ holds the intermediate embeddings of the last token in a chunk and of the first $m + 1$ tokens in the next chunk. Then compute the cross-attention between those chunks and the encoded.

If you want to represent the second chunk you can only use the first chunk.

### Causal Masking

Even thouhg each CCA attends only to the neighbours and the preceding chunk, the depenencies over neighbours are propagated via self-attention. So the activations of the $i$th token in the $u$th chunk therefore potentially depend on the set of all previous neighbours.

## Quantifying Dataset Leakage

Split the evaluation sequences into chunks and split the training data into chunks.

Then for each eevaluation sentence, find the 10 closest neighbours and compute the LCS.

You can then obtain the log likelihood for each chunk $C$ and the number of bytes encoded.

# Related Work

GPT-2/3 and Jurassic show that scaling up LLMs lead to massive improvements on many downstream tasks.

Carlini demonstrate that LLMs memorize their training set indicating that retrieval might help. but significant leakage between training and test set s might make comparing and evaluating models trained on these datasets difficult.

**TF-IDF**: Historically, retrieval depends on TF-IDF and BM25. There's also LDA. Some papers by Zhang and Gu retrieve translation pairs based on edit distance between source sentences.

With deep learning, some retrieval ssytesm have switched to learned representations based on NN activations, for example Continuous Cache and kNN-LM. SPALM integrates the database into the NN processing process.

RETRO shares components with kNN-LM and DPR in that it uses frozen retrieval representations. Using chunks allows for repeated retrieval while generating a sentence as opposed to retrieving only once based on the prompt alone.

Retrieval is also part of the pre-training process and not plugged in at the end.

# Privacy, Safety and Fairness

LLMs prefer to perfectly memorize parts of their training data. Retrieval models do this inherently, but unlike LLMs, you can easily delete things in the retrieval model's database. You can also make the retrieval DB differentially private.

Keeping retrieval models up to date with new knowledge requires only updating the database. You don't need to have an expensive retraining of the whole thing.

LLMs are also prone to generating toxic outputs. Retrieval based models can be filtered.

Samples from large models can be difficult to interpret, but retrieval based models provide a little more insight as one can inspect the neighbours at inference time.


# Scaling
![[retro_scaling_parameters.png]]
We scale from 150 million to 7 billion non-embedding parameters. Things improve as you scale the number of parameters.

![[retro_scaling_database.png]]

In the above figure the scaling performance of the retrieval dataset is shown. There are dramatic gains as retrieval data is increased from wikipedia to all of massive text.

Also there are consistent improvements as you scale the number of neighbours from 1 to 10. Larger models do better with more neighbours.

# RetroFitting

Freeze the pretrained weights and train only cross-attention and neighbour encoder parameters. This offers an efficient alternative path to enhance transformers with retrieval, requiring only 6 million sequences.

Fine-tuning is done using the natural questions dataset. Left-pad the data such taht the answer coincides with the end of the first chunk of 64 tokens and thus aligns with the first retrieving chunk. You can get good performance "retrofitting" the model on only 3% of the number of tokens seen during pretraining.

# Relating Relative retrieval performance to dataset leakage

RETRO exploits leakage more strongly than the baseline models as indicated by the negative slope. This is due to the explicit ability to copypaste existing training chunks to predict leaked evaluation chunks.






# Applications

 - Online learning (update the database with text that you've seen and avoid the huge encoder context?)
	 - Chatbots
	 - RPG games
 - Don't learn speaker characteristics
 - Cheaper fine-tuning if your model is retrofitted (but that depends on the distribution of tokens, if that shifts then you might need to shift the prior)