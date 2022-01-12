---
title: BC-Z Zero-Shot Task Generalization with Robotic Imitation Learning
---


# BC-Z: Zero-Shot Task Generalization with Robotic Imitation Learning

The proposed system flexibly conditions the policy on different forms of task specificiation, including language instrucitons or videos of a person performing the task. This enables generalization at test time by providing something to condition on.

BC-Z is sort of like an "action decoder".

The policy architecture consists of an encoder $q(z|w)$ which processes a command $w$ into an embedding $z$ and a control layer $\pi$ which processes $(s, z)$ into some actions.

## Encoder Architecture and Learning Algorithm

If the command is a language command, use a pretrained multi-lingual sentence encoder. If a video command is used, use a CNN to encode the video frames.

**Language Regression Loss** By itself, this end-to-end approach overfits to initial objects scenes and learns poor embeddings. So to align the video embeddings, introduce a "language regression loss" - predict the mebedding of the task's language command with a cosine loss.

**Network architecture** The policy network processes the camera image with ResNet18. The whole policy is conditioned on $z$ through FiLM layers, which are in each of the 4 ResNet blocks.

## Experimental Results

### Zero-shot / few-shot generalization

Language conditioned policies are given a novel sentence.

First four held-out tasks do not require any cross-obejct set generlaization. Achieves an average success rate of 32\% and 44\% on the tasks that have a non-zero success rate.

Conditioning on videos of humans is more difficult, BC-Z is still able ot generalize to nine novel tasks.