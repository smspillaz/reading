---
title: "Neural Arithmetic Units."
venue: "ICLR"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/MadsenJ20"
ee: "https://openreview.net/forum?id=H1gNOeHKPS"
url: "https://dblp.org/rec/conf/iclr/MadsenJ20"
authors: ["Andreas Madsen", "Alexander Rosenberg Johansen"]
sync_version: 3
cite_key: "conf/iclr/MadsenJ20"
---
# Neural Arithmetic Units

Differentiable binary arithmetic operations:
 - Eg, for a vector x learn the function $(x_5 + x_1) \cdot x_7$. Let each unit decide which inputs to use.

NALU:
 - Addition and multiplication unit
 - Pick which one to use based on sigmoid.

$W_{h_t, h_{t - 1}} = \tanh(W_{h_t, h_{t - 1}} \sigma (\hat M_{h_t, h_{t - 1}})$

NAC_+ : z_{h_t} = \sum^{H_{t - 1} W_{h_t, h_{t - 1}} z_{h_t - 1}

NAC_* : z_{h_t} = \exp (\sum^{H_{t - 1} W_{h_t, h_{t - 1}} \log(|z_{h_t - 1}|))

Basic idea, $W$ and $M$ are weights and $z_{h_{t - 1}}$ is the input. NAC_* uses exponential-log
for the multiplication ops for positive inputs.

NALU combines the two using linear interpolation + gating.

## Initialization

Xavier initialization causes the expected value and gradient to be zero and doesn't give you
the desired bias for {-1, 0, 1}.

Solution: Sparsifying regularizer, penalize non |1| values.

## Neural Multiplication Unit

Problem with original NAC_* - it does not handle division very well due to optimization issues.
Main problem is a small |z_t| + \eps and a negative weight value. In this case we will be dividing.

(Why? \exp (\sum^{H_{t - 1} W_{h_t, h_{t - 1}} \log(|z_{h_t - 1}|)) \to \exp (\sum^{H_{t - 1} \log((|z_{h_t - 1}| + \epsilon)^{W_{h_t, h_{t - 1}}}))
\to \exp (\log(\product^{H_{t - 1} (|z_{h_t - 1}| + \epsilon)^{W_{h_t, h_{t - 1}}})) \to \product^{H_{t - 1} (|z_{h_t - 1}| + \epsilon)^{W_{h_t, h_{t - 1}}}
by log-laws).

New unit:

$z_{h_t} = \product^{H_{t - 1}}_{h_{t - 1} = 1} (W_{h_t - 1, h_t} z_{h_{t - 1}} + 1 - W_{h_t - 1, h_t}$

The idea here is that you don't support division.

Initialize weights with expected value of 0.5. Expected value of output is then 0.5^{H_{t - 1}}$

## Gating mechanism

Both units converge, picking between the two becomes much harder.

# Experiments

Uniformly distributed ranodm numbers. Measures "success". success rate
and training time seem to go down and up respectively as you increase the number
of hidden units.

Another experiment: Multiply MNIST.