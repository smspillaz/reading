# Hoefler et al, "Sparsity in Deep Learning: Pruning and growth for efficient inference and training in neural networks"

Today's network are overparameterized, 5% of parameters predict the remaining 95%. We know that sparser models generalize better.

BUT, over-parameterised models are easier to train. Why? Look at the loss functions:

![[additional_dimensions_sparsity.png]]

You can use the additional dimension to "go around" the local maxima in the first dimension, which might not have been possible if you were only using one dimension to start with.

## Sparsity vs Accuracy tradeoff

![[sparsity_accuracy_tradeoff.png]]

In deep learning its even worse.

## What do we mean by sparsity?

 - Model sparsity (remove weights from the model)
	 - Structured. Structured Sparsity: Has benefits to computational complexity - you have less overhead of remembering what you removed.
	 - Unstructured
	 - Activation sparsity (remove entire weight groups from the model)
	 - Channel sparsity
 - Ephemeral sparsity
	 - Dropout
	 - Gradient sparsification
	 - Error sparsification
	 - Optimizer state
	 - Activation sparsification (ReLU)
	 - Gated networks - conditional computation - routing it through a different subnetwork


How and when to sparsify:
 - Train, then sparsify (distillation, pruning)
 - Sparsify during training (including iterative sparsification)
 - Sparse training - remove neurons and re-grow them during training


All methods fit a generic schedule - initiate a structure, initialize weights, perform training, then prune/regrow.

 - "lottery ticket hypothesis": reset the weights to another point.


Sparsification during training has the advantage that you can turn weights on and off for a more efficient training schedule.
 - dense/sparse/dense training schedules.
 - benefits SGD trainings.
 - not just updating the weights, but also the structure of the network. Double optimization goal. Hard to differentiate in general.
 - "early structure adapation"
 - two phases of learning - the first is learning the structure and the learning of the weights in that structure.


## Fully sparse training schedules
 - Enables to train in extremely high dimensional sparse models.

(1) Dynamic sparsity:
 - Iteratively prune and grow during trianing
 - NeST (biologically inspired)
	 - Random initialization
	 - Growth phase adds neurons and weights
	 - Purning phase removes neurons and weights


(2) Static sparsity
 - Find a good static sparse network to train
	 - Designed (LCN, CNNs, sparse attention etc)
		 - Eg, "inductive bias", good sparsity scheme.
	 - Random (data independent)
	 - Pretrained (data-dependent)


Pretrained static fully sparse schedule
 - Takes advantage of early sparse adapation
 - Single Shot Network Pruning (SNIP)
	 - Find wieght importance measured by sensitivity for batch.
		 - $|\frac{\delta L}{\delta w} w|$
		 - Prune then train as usual
 - Snip fails at very high sparsity because it disconnects your network
	 - Fix: consider "gradient flow" - how do signals propagate.
	 - Random baseline performs quite well -> data free pruning.


## How to remove elements

 - Simplest scheme, we want to remove $k$ elements - means that we must train $\begin{pmatrix} n \\ k \end{pmatrix}$ models to convergence
	 - But this will take way too much time.
	 - In practice, use a selection scheme by some importance metric.
 - Data-free: neuron/weight similarity. Discard certain number of smaller weights.
 - Data-driven (inference only):
	 - Remember for each neuron and what the distribution is for that neuron.
		 - Remove trivial elements ("energy")
	 - Sensitivity
		 - If a neuron does not really change a whole lot - then it has no discriminative character and we can also remove it and replace it with a bias.
	 - Correlation of similarity
		 - If two different neurons are essentially always doing the same thing, then we can collapse it into one neuron.
 - Training-aware
	 - Use the loss function as a proxy to understand which elements are important.
	 - Regularization (`L_0, L_1, L_2`).
	 - Statistical variation, bayesian interpretation.



### [Data free] Magnitude based pruning

Remove weights with the smallest absolute magnitude.

Most popular and simplest methjod.


### Retraining - suprisingly effective but expensive

Prune, then retrain. Very simple method to fix mistakes caused by pruning. Update frequency is crucial.

### [Data driven] sparsification schemes

Run examples through the network and determine importance by sensitivity.

 - sensitivity of entwork with respect to weights, either layerwise or full.
 - generally, correct other neurons to maintain input/output mapping (linear system of equations)


Other methods based on activity/correlation
 - Remove neurons that rarely fire
	 - "average percentage of zeros"
 - Remove neurons with similar output
 - Remove weights between weakly connected neurons.


These will definitely not improve accuracy, they just remove things but do not re-train.


### [Training aware] Taylor expansion of the loss function.

$\delta L (w + \delta w) - L(w) \approx \triangledown_w L \delta w + \frac{1}{2} \delta w^TH d w$

Look at pruning as an optimization task.

 - First order: similar to simple methods (total weight change), useful for transfer learning.
 - Second Order: "LeCuin 1990: 'Optimal Brain Damage'" - consider diagonal approximation of the Hessian. Determine the sensitivity of each weight.
 - "Optimal Brain Surgeon": Use the full $H$.
 - The Hessian is a very large matrix - it is $N^2$ where $N$ is the number of parameters.
 - In theory this gives you a lot of power

![[pruning_schemes_and_loss_of_accuracy.png]]

OBS and OBD are "optimal brain surgeon" and "optimal brain damage"

Magnitude pruning as a special case: If $H$ is identity or a $cI$, then it is optimal.

### [Data and training aware] sparsifying regularization

Extend the loss function with a regularization term. Very easy to implement, hard to control.

Simplest form is weight decay.

Obvious sparsifier is $L_0$ norm, but this is np complete and nondifferentiable.

 - Other idea: polarization - pull some towards zero and some away from zero.


Most common: $L_1$ orm: 
 - Tighestest convex relaxation of $L_0$ - mostly differentiable
 - But reduces weight magnitude
 - Invariant to scaling (batch norm may mess it up)
 - Alternatives
	 - Hayer Square Reguarlizer ($\frac{L_1}{L_2}$ ratio)
	 - Shrinkage operator: $w' = (|w| - \delta) , \text{sgn}(w)$


### [Data and training aware] Learnable gating functions

Learnable sparsity parameters. We can soften the gating function.

 - softplus
 - sigmoid
 - learn the magnitude for magnitude pruning.


### [Data and training aware] Variational selection

 - Assume distribution over elements and prune based on variance
 - Elements with high variance have little contribution (low signal, much noise)
 - Train wegith weight was $w \sim N(w|\theta, a \theta^2)$
 - Large $a$ -> large multiplicative noise -> can be pruned
 - Very expenisve to train but impressive results for sparsity ratios
 - Bayesian dropout for structural pruning.



## Fully-sparse training

How do you re-grow the elements?

Weights are position sensitive, how do we add them?
 - Uniformly random
	 - Random walk in model sparse
	 - Creates power-law models
	 - If you enable random weighst and prune in a structured way, then you get a power-law model.
 - Based on the gradients
	 - Continue computing gradients for the runed weights - you have to store and compute the gradients and may need compute power and memory to do this.
	 - top$k$ plus $d$ method.
 - Locality
	 - Attach new neurons preferentially to neurons which are already well connected.



## Ephemeral Sparsification Schemes

Very few active neurons in biological brains active at any given point in time. Must stay within an energy budget.

Neural activations sparsity mimics biology. Eg, dropout - we drop between 20-50% of the weights. Variants of dropout.

This was originally developed as a regularizer, but in fact it is seen as an opportunity for performance. Drop small activations for speedups.

### [Ephemeral] Gradient sparsification

Gradient summation is the biggest bottleneck in data-parallel training.
- Huge interest in gradient sparsification
- Frameworks such as SparCML: 10x speedup in practice, theoretically founded.
- Sparsify gradients, accumulated error locally
- Proofs that this at least converges eventually.


For FC layers, we pruned gradients based on the absolute value and we had some error feedback.
 - Threshold method.

Adaptive: Top-k method (error feedback)

Gradient dropping: Absolute value, error feedback, layer norm

AdaComp: scale factor: Error feedback binning

Deep gradient compression: Error feedback, momentum correction, gradient clipping, momentum masking, warmup


### [Ephemeral] dynamic networks

Determine a different path through the network per example
 - No example touches all weights
 - Simple method: gating of subnetworks.

"Mixture of experts model"
 - Define n "experts"
 - Route each example to $k << n$ experts
 - Enables extremely large networks, switch transformer, etc.
 - Promising candidate: product-key networks. Give you a key-value store access.

## Sparse Transformers

Accuracy for head pruning - you cannot achieve a lot of sparsity by pruning whole heads.

If you do unstructured pruning, you can do relatively well with a moderate loss to accuracy.

## Systems aspects

Less than 30-40% sparsity is not really worth it to exploit.

Today's SoA is about 95%.

If you are willing to give up accuracy you can get to 99%.

In scientific computing you can get to extreme sparsity.

You can choose different representations for different ranges of sparsity (eg, RLE, CSR, COO)

Structure matters a lot for performance.

![[different_sparse_structure_schemes.png]]




