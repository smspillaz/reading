# Pay attention to what you need: Do structural priors still matter in the age of billion parameter models?

https://neurips.cc/virtual/2021/tutorial/21891

Two types of scientists:
 - Birds: fly high, see connections, pool them together
 - Frogs: live on the ground, work out the details


## Why does we need structure and where does it come from

### What the original goals of AI research were

Compare statistical vs symbolic systems. Reasoning is what symbolic AI is good at.

### Why scale is not enough

"Universal function approxmation theorem". MLPs of arbitrary width or depth can approximate any continuous function.

For arbitrary width: There more hidden units you add ,the more steps you can get, you can use them to get a closer and closer approximation of the function. In practice you cannot get close enough to a step function - this is in the gaps where the bumps meet.

Our biggest trainable models are not too far from the brain in terms of the number of neurons and synapses. Why do we still have generalization problems?

Optimization is hard.

Architecture is hard.

The best architectures that currently work are not MLPs but they are convolution, recurrent or graph nets. They make particular assumptions within the data domain and the structure of the data.

### Where does structure come from?

One way to bring structure to deep learning is to think about what happens to the activations when we put thigns through the hierarchy. Should make the subsequent tasks more efficient and accurate.

Why symmetry matters:
 - "Those stubborn cores that remain unaltered even under transformations that could change them"
 - Transformatons can be applied in any order. One is a symmetry of the other. Results in the same thing.


ConvNet:
 - Reflects the translation symmetry.
 - T(C(robot)) = "robot" == C(T(robot)) = "robot"


RNN:
 - Reflects time-translation symmetry


Graph:
 - Permutation symmetry - whether you arrange yourself one way or another, the formation is still classified in that way. Permutation invariant.

What would be more powerful: learn the symmetries from data itself.

#### System 2

Knowledge base and inference engine.

What are grounded symbols?

 - Objects
 - Relations
 - Properties

Object/Relational/Properties. All symbols correspond to concrete objects, but they could be abstract.

Symbol grounding: How to learn to automatically populate a symbolic database from raw observational data.


Object discovery:
 - Waht and where
 - Key points
 - Attention

In some models such as MONET or IODINE, each representational slot can be decomposed into attributes. We want to automatically discover objects and represent them as symbolic knowledge.

Symmetries and disentanglement:
 - Grounded symbols naturally emerge in a representation that look like symmetry transformations.
 - There is nothing special about objects - things like like "red" or "large" are not dissimilar to "cube" or "cylinder". Properties/objects have no fundamental difference.


## Symmetries

 - Some transformations are only symmetrices at certain parameters, eg, rotations of triangles.
 - You can get groups of symmetries.
 - Group actions must transform something and preserve something.


Overfitting is much smaller for equivariant architectures.

### Disentanglement

"A vector representation is called a disentangled representation with respect to a particular decomposition of a symmetry group into subgroups. If it decomposed into independent subspaces, where each subspace is affected by the action of a single subgroup and the actions of all the other subgroups leave the subspace unaffected."

Independent factor of variation is disentangled representaiton cannot be one dimension. It is ok to use a single dimension for something like color, because that is a one dimensional space. However if one factor variation is directions in $R^3$, this cannot be represented as a product of two one dimensional objects.

The more symmetries you have the bigger the reduction of volume that you have.

If your representation is continuous, then respecting symmetries reduces the dimensionality of your problem. It reduces the number of degrees of freedom.

### How symmetries are used in practiced in NN architectures

For example, dog/not dog classifier.

We want the output to be invariant to rotation. What should we do in network?

All the hidden representations transform with symmetries - these are equivariant. The last layer is invariant.

Invariance is a form of equivariance. Proof is group averaging.

Group averaging:
 - Start from an arbitrary map
 - Consider all possible transformations of the input
 - Consider all maps of those transformations
 - Take the average of all the outputs

 => Note the output would be the same no matter which initial transformation you had. So the map is now invariant to that transformation.

Equivariance is a form of invariance. Proof 

### Equivariance from invariance

We have a function on $R^2$. Wave shape from the centre. Invariant with respect to rotation.

Take the gradient and obtain the gradients. Clear rotational symmetry - same amplitude, only the direction rotates.

### Normalizing flows

We want to learn a distribution.

1. Start with a simple distribution (eg, uniform, Gaussian, etc)
2. Smmoth family of invertible maps $F_{\phi}$
3. Define $q_{\phi}$ as the desnity of a random variable: $x = F_{\phi}(z), z \sim \pi$
	1. $q_{\phi}(x) = \i(z) (\det \frac{\partial F_{\phi} }{\partial z})^{-1}$


### Group equivariant convolutions

Features are maps on teh group itself $G \to R^{K}$. You can view an image as a map from $Z^2$ to $R$. Convolution is equivariant with respect to discrete translation.

What if you have a large group of symmetrires, eg, symmetry with flipping, rotation by 90 degrees.

Build feature maps on the group itslef

## NeuroSymbolic AI systems

How the amount of struture in an input representation affects properties of learned model.

AI Landscape from structured to unstructured:

 - Symbolic AI:
	 - Interpretabilty: You apply the rules and know how the rules work
	 - Data efficiency: Does not rely on data. So completely data efficient. 
	 - Transfer: Rules are defined for all $X$. However this depends on the quality of the handcrafted system.
	 - Universality: Algorithms are task-specific - we cannot use the dog classifier for cats.
 - Expert systems. Apply rules to a database of facts to infer relationships. The database of facts is the inputs.
 - NeuroSymbolic VQA
	 - Interpretability: 4/5
	 - Data efficiency: 4/5 - existing knowledge about useful types of reasoning steps have been encoded. Less left for the model to learn.
	 - Transfer: 3/5: - transfer to different combinations. After fine-tuning the scene encoder, you can still do well, but requires fine-tuning.
	 - Universality: 2/5: Some functions can be re-used, both others need to be written.
 - Deep Learning:
	 - Interpretability: Black box
	 - Data efficiency: Requires tons of data
	 - Transfer: No generalization to small changes
	 - Universality: A single model can be trained to solve many tasks

### NeuroSymbolic VQA

 - First segment objects
 - Predict size shape color material of each object
 - Turn the question into a program which finds objects by properties and composes things. Assmble functions which are already written.


### NeuroSymbolic Concept Learner: Interpreting scenes, words and sentences from natural supervision

 - you get a representation vector for each object
 - objects are mapped using learned neural operators
 - questions converted to a program from pre-defined functions
 - learn how to make the program via an RL algorithm

### Neural Modular Networks

Operates directly on raw data, does not require object representations extracted from images.

More general learnable modules that can be applied directly to images:
 - Attention module
 - Re-attention - moves attention from one part to the other
 - Combination: Combines two attention masks


Interpretability: requires interpreting attention maps - possible to have information leakage.

### Neural State Machine

Trained to answer visual reasoning questions. The observations are represented as a graph.

One of the key things facilitating transfer has been the modular structure of the neurosymbolic methods.

## Unsupervised scene representation learning

 - What/where models
 - Keypoint models
 - Object models with disentangled representations
 - Attention modules

### What/where representations

 - Define some crop of the original image
 - SPACE:
	 - Define background and foreground of images
	 - Where representation: Scaling and shift + depth


### Keypoints

Transporter:
 - Detect keypoints from videos. Leverage object motion to discover key points.
 - Detected keypoints refer to whole objects or parts of objects.
 - No assumptions about shape/size of objects
 - Assumptions that scene can be represented by points in 2D.


### Attention based

Slot Attention.

 - Attention mask to detect objects
 - No explicit representation for position of an object


MONET:
 - More structured - use an information bottleneck
 - Learn a disentangled representation
 - 