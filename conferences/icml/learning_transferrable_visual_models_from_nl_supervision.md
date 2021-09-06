# Learning Transferrable Visual Models from Natural Language Supervision

State-of-the-art computer vision systems are trained to predict a fixed set of predetermined object categories. This restricted form of supervision limits their generality and usability since additional labeled data is needed to specify any other visual concept. Learning directly from raw text about images is a promising alternative which leverages a much broader source of supervision. *We demonstrate that the simple pre-training task of predicting which caption goes with which image is an efficient and scalable way to learn SOTA image representations from scratch on a dataset of 400 million (image, text) pairs collected from the internet*. After pre-training, natural language is used to reference learned visual concepts (or describe new ones) enabling zero-shot transfer of the model to downstream tasks. We study the performance of this approach by benchmarking on over 30 different existing computer vision datasets, *spanning tasks such as OCR, action recognition in videos, geo-localization, and many types of fine-grained object classification*. *The model transfers non-trivially to most tasks and is often competitive with a fully supervised baseline without the need for any dataset specific training*. For instance, we match the accuracy of the original ResNet-50 on ImageNet zero-shot without needing to use any of the 1.28 million training examples it was trained on.

https://icml.cc/virtual/2021/oral/9194

[[transferrable_visual_models_from_nl_supervision.pdf]]

## CLIP approach

Contrastive Learning. Match the pairs. CLIP is learning to do this job but matching image/text pairs using a dataset.

Contrastive Language-Image pre-training.

1. Sample a random batch size of pairs.
2. Text encoder encodes text into feature vectors
3. Image encoder encodes images into feature vectors
4. We want the minimize the average cross-entropy loss.

We want a set of encoders that can encode you into a shared multi-model embedding scheme.

## Applications

This way you can do zero-shot image classification.

Now that you have the feature vectors for all the text and the image. Eg, "A photo of a [object]". Select the text corresponding to the object that has the highest log probabiliyt.

This is why we chose a contrastive approach over the predictive method. Predictive only needs to determine if two things are related or not, whereas contrastrive needs to maximize distance to negative samples.

## Representation Learning

Use linear probes - train a logistic regression classifier on features and get the accuracy.

## Zero shot transfer

Things that seem more in-distribution for clip, it does well zero-shot. But on the other side, for domain specific tasks like medical-imaging you don't do so well.

## Robustness to natural distribution shift

Zero-shot clip is much more robust. An ideal robust model should have the asme performance on both. Zero-shot CLIP models are much closer to ideal robust models.

## Related Work

- Natural Language Supervision
	- VFCC100M WSL
	- VirTex
	- ICMLM
	- ConVIRT
