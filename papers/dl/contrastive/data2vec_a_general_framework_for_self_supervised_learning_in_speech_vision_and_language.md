---
title: "data2vec: A General Framework for Self-supervised Learning in Speech, Vision and Language."
venue: "ICML"
pages: "1298-1312"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/BaevskiHXBGA22"
ee: "https://proceedings.mlr.press/v162/baevski22a.html"
url: "https://dblp.org/rec/conf/icml/BaevskiHXBGA22"
authors: ["Alexei Baevski", "Wei-Ning Hsu", "Qiantong Xu", "Arun Babu", "Jiatao Gu", "Michael Auli"]
sync_version: 3
cite_key: "conf/icml/BaevskiHXBGA22"
---

The algorithms for self-supervised learning across modalities differ substantially, since they were each developed for different modalities.

data2vec is a framework that uses the same learning method for speech, NLP and CV.

The main idea is to predict latent representations of the full input data based on a masked view of the input in a self-distillation setup using a stnadard Transformer architecture. Instead of predicting modality specific targets, instead predict the contextualized latents.

#### How it works

Take a standard encoder-transformer and make a copy of it, one teacher and one student.

The teacher receives the entire input and the student receives the masked input. The student must predict the  latents of the teacher corresponding to the mask. The teacher is updated by EMA and the student is updated by gradient descent. Smooth L1 loss is used for the student targets.

Note that this is *not* the same as reconstructing your input. You are predicting a contextualized representation, since the latents predicted by the teacher have seen the input and its context through non-causal self-attention.

How are the training targets determined? In the paper it says that you construct the targets based on the normalized output of the top-K blocks of the teacher network for those timesteps masked in the student and averaging them together. Presumably by "blocks" the authors mean layers of the transformer.

How to do the masking? In each modality you should mask a contiguous region. In images that means that you mask a contiguous region in space, such as a contiguous region of superpixels. In audio data you mask a contiguous region of time. In text you mask a contiguous span.

#### Benchmarks

To evaluate data2vec, we use the same linear probing method.

In Computer Vision, data2vec is competitive with self-supervised leaners like [[emerging_properties_in_self_supervised_vision_transformers|dino]], BeIT, SimMIM, MaskFeat etc.

In speech, data2vec beats wav2vec, HuBERT and WavLM in WER as dataset size is scaled up.

In NLP data2vec is competitive with BERT and RoBERTA on most tasks in GLUE, though it is not quite ahead as much as in CV and speech.

#### Ablations

##### How much do the layer-averaged targets matter?

The plots in Figure 2 show WER on speech, GLUE score on NLP and top-1 valid accurracy on CV as the number of averaged layer targets from the top down increases. In general, performance increases monotonically as the number of layer averaged targets increases, but stop becoming monotonic at around 6 layers for speech, 8 layers for NLP and 3 layers for CV.

#### Target Feature Type

Should we use the output of the self-attention block, the layer normalization block or the feedforward network block? At least the experiments on speech show that using the output of the self-attention block is wrong, with a substantially higher WER. Instead the FFN has much better target representations.

#### Can representation collapse happen?

This is a situation when the teacher learns to predict the same representation for all targets and therefore the learning process degenerates.

This can happen if learning rates are too larget or learning rate warmup is too short, same with any other transformer. If EMA decay rate is too low this can also happen because student model collapse would be propagated too quickly to the teacher. So the method requires that you quite carefully tune the EMA hyperparameters. Collapse might also happen for modalities where adjacent targets are highly correlated. Promoting variance within the same batch is a good way to mitigate this problem (see [[vicreg_variance_invariance_covariance_regularization_for_self_supervised_learning]] and [[byol_self_supervised_no_contrastive]]).

They also say that representation collapse is avoided through the usage of normalization. Eg, if you apply instance or batch norm before or after averaging targets.