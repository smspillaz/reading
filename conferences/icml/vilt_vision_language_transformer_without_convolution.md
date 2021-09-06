# ViLT: Vision-and-Language Transformer without Convolution or Region Supervision

[[kim_vilt_vision_language_transformer_without_convolution.pdf]]

Vision-and-Language Pre-training (VLP) has improved performance on various joint vision-and-language downstream tasks. Current approaches to VLP heavily rely on image feature extraction processes, most of which involve region supervision (e.g., object detection) and the convolutional architecture (e.g., ResNet). Although disregarded in the literature, we find it problematic in terms of both (1) efficiency/speed, that simply extracting input features requires much more computation than the multimodal interaction steps; and (2) expressive power, as it is upper bounded to the expressive power of the visual embedder and its predefined visual vocabulary. In this paper, we present a minimal VLP model, Vision-and-Language Transformer (ViLT), monolithic in the sense that the processing of visual inputs is drastically simplified to just the same convolution-free manner that we process textual inputs. We show that ViLT is up to tens of times faster than previous VLP models, yet with competitive or better downstream task performance. Our code and pre-trained weights are available at https://github.com/dandelin/vilt.

https://icml.cc/virtual/2021/oral/9492

Images and text often appear as aligned forms. They are usually processed separately.

We can also do modality interaction, eg, transformer.

Eg, VSE++, SCAN.

These types are made up of very shallow modality interaction layers and employ simple dot product for interaction.

CLIP - much heavier textual embedder, requires same amount of computation as visual embedders.

Then there's ViLBERT, LXMERT, UNITER, Pixel-BERT which have a big modality interaction layer.

In this model, the embedders are shallow and the modality interaction is large.

![[vilt_model_types.png]]

Models that belong to the upper figure rely on big CNNs to process the image, or grid-features.

In our model, we require only a linear embedding to process image inputs and results in drastically improved inference time.

## Architecture

You have:
 - Transformer for modality interaction
 - Word Embedding
 - Linear projection of flattened image patches.


The text-tokens are one-hot vectors, so we can embed them.

You add the token-type embeddings and concatenate them into a unified sequence. Iteractively update it through D-depth pre-norm transformer encoder. Resulting contextualized vector is multiplied by the pooling matrix and goes through $\text{tanh}
$

This vector $p$ serves as the pooled representation of the image-text pair.


Pre-train the model using COCO captions, SBU captions, conceptual captions and visual genome. Use 200K iterations.

## Pretraining tasks

### MLM

![[vilt_mlm_pretraining.png]]

Masked-language-modelling as the pre-training task, eg, you have a sequence of words, a sequence of image patches - predict the masked token

Whole-word-masking: bascially if you use wordpieces, you should not mask subwords because you can predict wordpieces from other subwords.


Also - masked patch prediction - predict RGB mean values, but this can hurt performance if applied. Does not provide useful cues to pretrain on.

### Contrastive Objective

![[vilt_contrastive_objective.png]]

Another idea for pre-training - predict whether image/text is aligned or misaligned.

To balance the ratio between aligned and misaligned pairs, sample from the minibatch.

#### Optimal Transport

Measures distance between sets - text set and feature set. Distance should be minimized when image/text pair is aligned and maximized when not.

Inexact proximal point method [[xie_proximal_point.pdf]].

## Fine-tuning

Attach head, fine-tune on VQAv2, NLVR2, COCO IR/TR, F30K/TR

## Ablation study - pretraining steps improve 
