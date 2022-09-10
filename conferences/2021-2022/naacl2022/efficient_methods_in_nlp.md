# Efficient Methods in NLP Track

## KroneckerBERT: Significant Compression of Pre-Trained Language Models Through Kronecker Decomposition and Knowledge Distillation
Over-parameterization is a key to success but moores law has a limit. In many cases there are strict constraints with respect to memory and energy consumption.

Current methods: Pruning, quantization, knowledge distillation.

Decomposition methods like SVD can offer high compression factor at the expense of a significant drop in performance.

But unlike SVD, Kronecker decomposition exploits redundancies in predefined patches and hence allows for more flexibility.

Kronecker Product:

$$
\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} \otimes \begin{bmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{bmatrix}  = \begin{bmatrix} a_{11} b_{11} & a_{11} b_{12} & a_{12} b_{11} & a_{12} b_{12} \\ a_{11} b_{21} & a_{11} b_{22} & a_{12} b_{21} & a_{12} b_{22} \\ a_{21} b_{11} & a_{21} b_{12} & a_{22} b_{11} & a_{22} b_{12} \\ a_{21} b_{21} & a_{21} b_{21} & a_{22} b_{22} & a_{22} b_{22} \end{bmatrix}
$$

Any matrix can be approximated using a sum of Kronecker Products.

Represented in this way, memory goes down from $O(m^4)$ to $O(m^2)$

Nearest Kronecker Problem: $\mathcal{W} = \mathcal{A}_i \otimes \mathcal{B}_i$, find $\min_{A, B} ||W - A \otimes B||_F$

This can be computed by reshaping and computing rank-1 SVD. If we have a pretrained model, we can use those matrices to obtain a pretrained kronecker model.

We can use this to compress the query, key and value matrices on each attention head.

For training you use knowledge distillation. Use a consistency loss between embedding outputs, attention matrices and FFN output.

In comparison to other baselines, for a compression factor of 8, we can outperform TinyBERT and MobileBERT while losing only 2 percentage points on accurracy.

## On Transferrability of Prompt Tuning for NLP

Pre-trained models are pretty good, but fine-tuning is difficult.

Parameter-Efficient Tuning Methods (only optimize a small part of parameters for downstream tasks while freezing the rest of the arameters of the PLM). Eg, Adapter, Prefix, LoRA, etc.

Prompt Tuning just tunes the prompt prefix. Prompt-tuning can acheive near fine-tuning performance. Requires more training time than fine-tuning.

We attempt to improve prompt-tuning by prompt transfer across different tasks and models. In cross-task transfer, we assume that similar tasks may require similar skills. So try to directly use the prompt on the target task. For tasks within the same type, transferring prompts between them can generally perform well.

We propose to transfer prompts with initialization. Choose the prompt of the most similar task. This can speed up training and achieve better performance. Train prompts on a smaller PLM and use them on a larger PLM.

However when doing cross-model transfer, directly using prompts is impossible because the semantic spaces of different models are inconsistent. Learn instead of projection function

## Sparse Distillation: Speeding up text classification by using bigger student models

Motivation: If you want a faster model for your NLP task, a very common option is to use knowledge distillation. Distill it into a smaller model that is faster during inference.

But sometimes we want an even-faster model. We want something that is big, sparse, shallow and fast.

Inspiration from Deep Averaging Networks (2015). Has only three layers - an embedding table, two linear layers concatenated to make a prediction. Break it down into n-grams, take the embeddings, average them and make the prediction.

We want to find literature to support the design decision.

Some expensive operations in transformers may not be necessary.  Eg, localized attention performs just as well as everything-to-everythign attention. In some cases n-gram models may actually be good enough.

Three stages in total, train a teacher model, then do knowledge distillation and minimize
consistency loss between teacher and student output logits.

Usually a good idea to further fine-tune the student model on the training data again.

Findings: 
- 600x speedup for a 3% performance drop. Student DAN can match fine-tuning baselines within a 3% gap compared to other methods. Gap is bigger on sentence-pair tasks.
- Better to use a smaller vocab and large embedding dimension than large vocab and small embedding dimension under a parameter budget.
- Pruning the least frequent n-grams can help to cut down model size by a lot and you only lose about 10% accurracy when doing this. Be careful about how the frequency is computed - if it is computed in a less relevant domain corpus you will get worse downstream performance.

## FNet: Mixing Tokens with Fourier Transformers (James Lee-Thorp)

[[fnet_mixing_tokens_fourier_transforms]]

Replace attention with other modules that mix tokens. So replace self-attention with a discrete fourier transform.

Main take-aways:
 1. Simple lienar token mixing transformations along with standard MLPs in feed-forward layers can model diverse relationships in text
 2. 92% BERT-Base accurracy on GLUE but trians 80% faster on a GPU
 3. Scales well - 50-80% lighter on memory than a Transformer.

The FNet architecture is similar to a transformer but instead of an attention layer you have a "mixing" layer.

Mixing layer uses a 2D fourier transform, then after that we extract the real component. There's no learnable weights, its just the same mixing transformation every time.
 - Its a 1D fourier transform along the sequence dimension and
 - a 1D fourier transform along the embedding dimension.

Fourier transform puts you into a space where multiplication is sort of like convolution, except that its with a soft window size. This is sort of then like attention but with a softening attention window.

That said, we're breaking things by extracting the real component. FFT scales very well to long sequences.

For GLUE BERT-Base we underperform by about 8%. The gap between BERT and FNet closes for the large configuration

The real wins are in latentcy. FNet is 80% faster on GPUs. FNet has quite nice scaling properties as well, but in larger configurations BERT dominates, but for smaller models, FNet is good in terms of accurracy/latency tradeoff.

## Learning to Win Lottery Tickets in BERT Transfer via Task-agnostic Mask Training

 - Large scale pretrained language models are hard to deploy in resource constrained scenarios, so lots of studies on compression
 - Lottery Ticket Hypothesis says that randomly initialized dense networsk contain a sparse subnetwork with similar accuracy to the full model.

Universally Transferrable BERT Subnetworks:  You can transfer to multiple downstream tasks as a repalcement of the original BERT and still do just as well. Magnitude based pruning.

Oneshot magnitude pruning vs random pruning: Average downstream performance of BERT subnetwork correlates with pretraining performance. OMP subnetworks outperform random subnetworks. 

## Method: Pruning Setup

Apply a binary mask to the model weights to obtain some subnetwork, which are the weights of the self-attention, FFN and word embeddings.

Task-agnostic mask training (TAMT): Directly optimize subnetwork structure on pretraining tasks, eg, you train the binary mask variables to do better on the pretraining task and finetuning tasks.

In mask training, each weight matrix associated with a binary mask and real-valued mask. In the forward pass we use hard-masking according to the binary mask, then in the backwards pass we do gradient estimation by using the straight-through estimator. Basically like gumbel softmax.

Oneshot magnitude pruning is used to initialize the real-valued mask.

The masked trainng objective can be any loss function.

Experiments:
 - Does the effectiveness of TAMT come from improvement on the pretraining tasks? Yes, better pre-training performance results in better downstream performance.
 - How efficient in TAMT? TAMP is more efficient and can achieve good compression in a short amount of time.
 - Is OMP initialization necessary? Yes, good initialization is necessary.
 - How do subnetworks found by different methods differ in the mask structure? Its not all in the same region, the subnetwork structure space might contain multiple regions of winning tickets that are disjoint with each other.
 - Is TAMT still a good choice when reducing fine-tuning data? Advantage of TAMT reduces with reduced training data, if you have less than 10,000 data points, performance drops drastically.

## Towards Efficient NLP: A Standard Evaluation and Strong Baseline

We are going from SOTA to "Pareto-SOTA". Eg, what's whats the performance-per-inference time. Eg, no other model is better at that compute time.

Current comparison is usually point-to-point. But you actually want to compare as a factor of scaling. Data points in a line-to-line comparison are not publicly accessible.

Different works use different efficiency metris, eg FLOPs, time, number of layers, parameters.

So there is a need for a standard evaluation.

They propose the ELUE benchmark. https://eluebenchmark.fastnlp.top

ELUE benchmark does multi-dimensional evaluation, is publicly accessible, has standardd evaluation with a unified metric (FLOPs and number of params) and is easy to use.

In the ELUE benchmark we have the following tasks:
 - Sentiment analysis (SST-2, IMDb)
 - NLI (SNLI, SciTail)
 - Similarity and Paraphrase (MRPC, STS-B)

How does the submission work? We could make it so that you have to submit models, that way you can't cheat, but this increases load on the benchmark side and its costly to do submissions.

The other option is to just submit test predictions but you cannot capture efficiency in this way. In this case we submit test files and python file with a model. Then combining the two kinds of files we can calculate the FLOPs for each sample.

You have to score the performance, FLOP pairs.

ElasticBERT pre-trained model baseline. This is a multi-exit transformer encoder, where you can make predictions from any layer. We can easily make a plot here of efficiency vs prediction accurracy.

## Adaptable Adapters

Models get bigger and bigger. We don't have to fine-tune all the parameters for each tiny downstream data.

Adapters is one of the solutions. Adapters are just some layers that we insert inside the pretrained model which are fine-tuned on the finetuning dataset.

Do we have to use this same architecture?

Adaptable Adapters introduce flexibility in designing adapter architectures.

Activation function: This is one of the hyperparameters. This is used in training and inference, typically ReLU.

Rational activation function: We learn a "suitable" activation. We can learn different activation functions at different layers of the model.

Layer Selection: Gumbel Softmax: End-to-end differentiable switch with hard-attention. Attends to element of a set.

