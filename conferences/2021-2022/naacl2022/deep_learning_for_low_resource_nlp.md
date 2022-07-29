# Deep Learning for Low-Reosurce NLP workshop

## Invited Talk: Seb Ruder

Most languages have limited amounts of unalbelled data, for example languages that have no text data.

Other challenges:
 - Compute cost
 - Data transfer cost
 - Space cost

### Sample Efficiency - Data Efficiency - Subword Segmentation

 - Language specific inductive biases (word presentations and segmentation)
 - Bilingual Lexicons

Subword segmetnation is suboptimal for low-resource languages. Words in languages with a lot of data are under-segmented, words in languages with less data are over segmented. Many are not aligning with linguistically useful morephemes.

Solutions;
 - Deterministic word segmentation
 - Probabilistic segmentation (BPE dropout)
 - Subword regularization (probabilistic segmentations during training)

We can combine segmentations during training

 - Cross-entropy over determinsitic input, pross-snetropy over probabilsitic input (exposes model to different segmentations) and a consistency loss - eg predictons should be robust to different kinds of segmentation.

#### Other word-level inductive biases
 - Integrate bias directly into the subword segmentation algorithm.
 - Prefer tokens that are sharped across
 - Explicit modelling of tones

### Alternative Data sources

Usually bilingual lexicons have the largest language coverage - this usually comes from the bible.

Adapting the mdoel to a target language: Fine-tune the model on monolingual data in the taret language using MLM.

### Word-to-Word Translation

Pseudo-monolingual dataset

 - Replace words in english monolingual data with their corresponding translations
- Pseudo-task: replace words in english with their corresponding translations in target language
- Refine the data by:
	- Inducing additional lexicons
	- Label distillation - train initial model for the task, then generate more pseudo-labels


### Takeaways
 - Indcutive biases particualrly usesful in low-resource settings
 - How models segment and represent words an be improved, particularly in morphologically rich languages


### Adapter Layers  - Space Efficiency

Allocate additional capacity for each language - small bottleneck layers inserted between existing pre-trained model weights.

To insert the adapter, you add a new FF module with a residual layer within each transformer layer.

 - Adapter parameters are encapsulated between transformer layers with parameters which are frozen
 - This means that we can only store the adapter layers and hotswap them between the same pretrained checkpoint.


Adapters learn transfromers making the model more suited to a task or language.

See MAD-X: Multiuple adapters for cross-lingual transfer

  - Step 1: Train language adapters for source and target languages
  - Step 2: Train a task adapter, stacked on top of source language adapter.
  - Language adapter and transformer weights are frozen and the task adapter is trained on the task.

Adapters can lead to increase robustness. They can outperform continuous prompt methods

Fine-tuning means that you only have to adapt a small number of parameters.

Adapaters enable extensions ato incorporate hierarchical structure, conditioning via parametr generation. You can condition the adapter on the input as well.

Lots of different shapes of adapters
 - Adapter
 - Prefix tuning
 - LoRA
 - Parallel Adapter
 - Scaled PA


### Time Efficiency

Instead of relying on subword segmentation we could just consume bytes directly. However applying transformers to bytes results in increase computation. Attention is expensive.

#### Gradient based subword tokenization
 - Learn a score $p_{b, i}$ for each block via linear transformation.
 - Learn a score for 1-blocks, 2-blocks, 3-blocks. Learn how important or how relevant each particular block is for the overall performance of the model
 - Find a softmax transformation for each position.
 - To compute latent subwords ....
 - Downsample latent subwords with stride-based mean pooling

#### Re-scaling the transformer stack

 - In multilingual models much of the capacity is allocated to subword embeddings
 - Eg, the embedding layers are the biggest.
 - For cahracter models, we have much less space in the embedding space, but to make up for that you have a really huge encoder.
 - Byte-based mdoels are competitive compared to their subword based counterparts.