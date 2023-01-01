---
title: "Compositional Attention Networks for Machine Reasoning."
venue: "ICLR"
year: 2018
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/HudsonM18"
ee: "https://openreview.net/forum?id=S1Euwz-Rb"
url: "https://dblp.org/rec/conf/iclr/HudsonM18"
authors: ["Drew A. Hudson", "Christopher D. Manning"]
sync_version: 3
cite_key: "conf/iclr/HudsonM18"
---

Presents the "MAC" framework, a novel differentiable NN "designed to facilitate explicit and expressive reasoning".

Moves away from a "monolithic black box" towards a design that encourages "both transparency and versatility".

Decompose problems into a series of attention-based reasoning steps.

MAC: Memory, attention, composition.

Applied to CLEVR and get 98.9% accuracy. Requires 5x less data to learn.

CLEVR contains unbiased "compositional" questions that require an array of reasoning skills, such as transitive and logical relations, counting, comparisons, etc.

# Architecture
![[mac_architecture.png]]

There are three operation units that work in tandem.

The *control unit* updates the control state to attend to each iteration to some aspect of a given question.

The *read unit* extracts information out of a knowledge-base, guided by control and memory states.

The *write unit* integrates the retrieved information into the mmroy state.

This enocurages a sequence of attention-based reasoning operations that are directly inferred from the data.



## Input unit

Take a question string $S$ and convert into word embeddings which gives "contextual words" (a sequence) and a "question representation" (a vector).

At each step, convert the question vector into a "position aware question" (eg, the aspects of the question relevant at the $i$th reasoning step).

The image is processed by a ResNet pretrained on ImageNet outputting convolutional features. This results in a 14x14xd tensor.

The image then **becomes the initial state of the knowledge base**. So when you see "knowledge base" think "image being processed".

## MAC Cell

![[mac_cell.png]]

For each step, you have hidden states $c_i$ and $m_i$ , which are the control and memory states at that step.

### Control Unit

![[mac_control_unit.png]]

This takes the previous control and the $q_i$ (eg, the question at timestep $i$) and performs an attention operation over the contextual words, then computes the attention-weighted average to get the next control.

## Memory Unit

![[mac_read_unit.png]]

![[mac_write_unit.png]]

This holds the intermediate result obtained from the reasoning process up to the $i$th step, by integrating the preceding hidden state with new information from the image performed by $c_i$.

The point of the control unit is that it guides which information in the image to ingest into the mmeory state through indirect means.

The read unit takes the previous memory state and uses it to perform attention over the knowledge base to get some retrieved information out. It then creates a "retrieval state" from the attention-weighted knowledge-base. The steps are:

1. Compute direct interaction between knowledge-base elements and the memory, resulting in an attention map over the knowledge-base
2. Concatenate elements of hte knowledge-base to the attention-weighted knowledge-base and do a linear transformation. "this allows us to consider new information that is not directly related to the prior intermediate result".
3. Measure dot product between control operation and interaction vectors (for each pixel) and compute the retrieval state.

The write unit takes the memory state and control in order to figure out a new memory state.

1. First combine $r_i$ (the retrieval state) with the prior intermediate result $m_{i - 1}$ by a linear transform.
2. Do self-attention between the current memory state and all previous memory states.
3. Memory gate: Sigmoid gate over memory states to interpolate between previous mmeory and candidate memory conditioned on reasoning operation. Skip a reasoning step if necessary.

### Output Unit

Take the question and the final memorys tate and pass through an MLP. Softmax gives the answer.

# Experiments

![[mac_curves_data_efficiency.png]]

Halves the error rates that you get with FiLM (so FiLM got accuracy of 97.88).

one nice thing is that this approach seems to be much more data efficient.

## CLEVR-Humans (human natural language annotations)

Only 18k samples.

Gets 81.5% accuracy.

## Generalization

Looked at performance when you have 10% of the data (70k samples). In this case you have a performance of 85.5% on average, which is better than other models. Baseline of predicting the most frequent answer for each question type is already 42.1%

# Demonstration

![[mac_demonstration.png]]