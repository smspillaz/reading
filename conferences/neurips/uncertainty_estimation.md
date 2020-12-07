# Practical Uncertainty Estimation and OOD Distribution Robustness in DL

## Why uncertainty and robustness

Uncertainty - two features, x_1 and x_2 and you try to predict y.

 - Output a distribution of predictions rather than just a point estimate
 - Classification problems: Output a label along with confidence.
 - Regression: Mean and variance which describes a distribution along a target

Good uncertainty estimates quantify when we can trust the model's predictions.

Scalar class label prediction - when can you trust the model's predictions

IID assumption

OOD - $p_{text}(y, x) \ne p_{train}(y, x)$

 - Good uncertainty estimates are important in this setting
 - We cannot expect the model to generalize to all OOD distributions
 - But there are some common things between train and test that we'd like the model to be robust to.


Covariate shift:
 - Distributional features change (eg, p(x) changes) but p(y|x) does not change.
 - Open-set recognition: new classes that appear at test time
   - Train a classifier on MNIST, then pass an image for a cat
   - Model should be able to say "this doesn't belong here"
   - Eg, I know what I don't know.


 - ImageNet-C: Varying intensity for dataset shift
  - Eg, take the clean data, add salt and pepper noise to it
  - Vary the intensity
  - Average model performance over all corruptions
  - Accuracy drops with increasing shift on ImageNet-C
  - Qualifty of uncertianty degrades with shift - overconfident mistakes.
  - NNs don't know when they don't know - model confidence from Softmax.
  - Models can become very confident on data that's far away from the model.

 - Models assign high confidence to OOD inputs - adversarial inputs.
   - You don't even need to generate adversarial examples
   - Eg, two moons: we're very confident at everywhere that's not the classification boundary
   - but if we introduce a new class of data, we classify it wrong and assign high confidence
   - ideally we want high certainty of the class near the training data, but low confidence
     once we move away from the training data.
   - Gaussian Processes exhibit this behaviour - uncertainty estimates work the way we expect them to.
   - There is some recent work that gets you GP like behaviour on the left.

 - Applications
  - Bandits and RL
  - Modelling uncertinaty crucial for exploration vs exploitation tradeoff
  - Inherent nonstationarity.

Model Uncertainty:
 - Many models can fit the training data well
 - Type 1 Uncertinaty: Epistemic uncertainty
   - As we get more and more data, this uncertainty should reduce as more classifiers can fit it
   - Models can be from the same hypothesis calsses, may be necessary to combine many models
     that have inductive biases
 - Type 2 Uncertainty: Data uncertainty
   - Labelling noise
   - Human disagreement
   - This is irreducible - persists even in the limit of infinite data.
   - The input is ambiguous


 - How do you measure the quality of uncertainty:
   - Calibration Error = |Confidence - Accuracy|
   - Confidence: predicted probabiltiy of correctness
   - Accuracy: Observed frequency of correctness


   - Eg, oif all days where model predicted rain with 80% probability, what fraction did we observe rain?
     - 80% implies perfect calibration
     - less than 80% implies overconfidence
     - greater than 80% implies underconfidence

     - regression: calibration corresponds to confidence interval

   - Expected Calibration Error:
     - ECE = \Sum \frac{n_b}{N} |acc(b) - conf(b)|
     - Bin the probabilities into B bmins
     - Compute the within-bin accuracy and within bin predicted confidence.
     - If you're below the diagonal, then the model is way more confident than it is accurate.


 Proper scoring rules:
  - Negative Log Likelihood: overemphasies tail probabilities

  - Brier Score: Quadratic penalty, bounded.

When to trust the model:
 - Evaluate model on OOD inputs which do not belong to any of the existing classes
 - Look at the model confidence - the confidence on the IID inputs should be higher than the
   confidence on the OOD inputs.


How to measure robustness?
 - Really important that we evaluate on dataset shifts which are not encounterd in the training
   data. Eg, covariate shift, difference of population etc.
 - Different renditions
 - Nearby video frames, multiple objects and poses

## Foundations on how to solve these tasks

Nearly all models are training probabilistic models - you want to maximize the probability
of the parameters conditioned on the data.

If you try to find the argmax of a distribution $\text{argmax} p(\theta|x, y)$ this only
gets you a setting, not uncertainty.

Approaches:
 - Try to estimate the full distribution, reason about predictions around the full distribution
 - Ensembling: Committee of models to obtain multiple good settings and predict over those
   multiple settings hoping that we get some interesting diversity over the prediction distribution
   that corresponds to uncertainty.


Probabilistic Machine Learning:

 - Training time: $p(\theta|x, y) = \frac{p(y, \theta|x)}{p(y|x)}$ - integrate over all possible models.
 - At prediction time we can reason about the entire distribution:
   - $p(y|x, D) = \int p(y|x, y, \theta)p(\theta|D)$ - marginalize over all possible models
   - take the average over predictions to get an expectation.

Bayesian Neural Networks:
 - Distribution over neural network predictions - distribution over the weights
 - Possible priors that you might put on your weights
 - All functions correspond to a differnet neural net, but they do different things away
   from the data - this allows us to reason about uncertainty away from the data.


Approximating the posterior:
 - $p(\theta|D)$
 - Local approximations
 - Sampling: MCMC, Montle Carlo, Markov Chains
   - Guided random walk through the posterior.


Variational Inference:
 - Recasting posterior inference as an optimization problem
 - Distribution over all weights is the product over gaussians
 - Minimize the KL divergence between a simple family and the true posterior distribution
   - Start with your simple distribution and optimize it to get as close as possible

 - You can optimize BNNs by optimizing the KL - optimizing the ELBO:
    - ELBO: the expected log likelihood of the posterior plus regularizing the posterior against a prior (KL)
    - Easy to do with SGD.
    - information theoretic view: minimize the number of bits to explain the data while trying not to pay many bits to devaite from the prior.


Infinite Width Baysian Deep Networks are GPs
 - A BNN defines a distribution over functions
 - Induced by a distribution over wieghts $p(\theta, x, y)$
 - In the limit of infinite width, this corresponds to a Gaussian Process.
 - This is nice because it allows us to reason about the behaviour of neural networks in new ways
   - We don't have to worry about the nuances of trianing, hidden units, etc.
   - Adlam & Pennington: Generalization properties of these models.
 - Truns out that being able to compute bayes rule in closed form gets us pretty well calibrated models.
   - Neural Tangents Library.

Gaussian Processes:

 - When we have a Gaussian Likelihood and a Gaussian prior - when you multiple a Gaussian by a Gaussian you get a Gaussian
 - Your predictions are another Gaussian Distribiution
 - Flexible distribuition over functions: Covariance over basis functions
   - Kernel trick K(X, X)
   - No longer reason about the parameters of the model, but rather how the examples covary
 - Get a posterior on  functions conditioned on data.
   - Corresponds to a Gaussian over functions.

Ensemble Learning:

 - A prior distribution often involves the complication of approximate inference
 - Ensemble learning: Aggregating the predictions over a collection of models.
   - This works quite well in practice.
 - Two main considerations:
   - Collection of mdoels
   - Aggregation of models:
     - Popular approach: Averaging over the predictions of $k$ independent models
     - other approaches: bagging, boosting, decision trees, stacking, etc


Bayes vs Ensembles: What's the difference:
 - Bayes posits a prior that weights different probabilities to different functions
 - Ensembles weight funcitons equally a-priori
   - Can apply any strategy, but there's no probabilistic interpretation.

Baysian Deep Ensembles via the Neural Tangent Kernel:
  - Deep ensembles are not actually any form of bayesian neural net
  - But you can tweak them a little bit to make them be samples from a BNN

Challenges with Bayes
 - Lots of recent methods tweak Bayes rule slightly to get the model to work well in pracitce
   - Tempering the posterior (temperature parameter) - turns out that it makes your accuracy go up
     but it is unclear what the model actually corresponds to
 - Deep learning tricks:
  - This bag of tricks needs to train BNNs (eg, intializiation, handling of exploding/vanishing gradients)
  - BatchNorm no longer correspond to any kind of Bayesian model.
 - Two objects of variational inference complicate the dynamics of training (competing objectives)
   - Need new heuristics to train these sorts of models
 - Bayes makes sense when the model is well specified
   - Sub-optimal when the model is mis-specified
   - Well-specified: There is a model in the model class that generated the data.

Simple Baselines:
 - How can I get uncertainty out of my models in a simple way?
   - Recalibation:
    - Modify softmax probabilities post-hoc
     - Recalibrate on a held-out validation set
     - Chop of the top and re-fit it on the validation set
     - if your model is overconfident, then you can smoothen the distribution to make it perform better on the validation dataset
     - divide by a scalar temperature value - higher value, flatter distribution
    - Caveat: When you have dataset shift - you don't get model uncertainty out of this.

   - Monte-Carlo Dropout: Dropout at test time, this effectively gives you an ensemble
   - Deep Ensembles:
     - Re-run SGD but with different random seeds and average the predictions
     - Every time you re-train you get to a different mode, different modes get you
       different models

   - Hyperparameter ensembles:
    - Add diversity in the hyperparameters as well as in the random seed
    - this gives you a little more diversity in your ensemble.

   - Bootstrap:
     - Resample the dataset with replacement and retrain
     - Each example gets a different weight under each model.
     - Can't really get this to work as well as ensembles
     - Nixon & Balaji: "I can't believe its not better".
       - Hypothesis: Bootstrap only gets to see a fraction of the data
         More data is better.

   - SWAG + Laplace:
     - Fit a simple distribution to the mode centered around the SGD solution
       - SWAG: Fit a Gaussian around average weight iterates near the modes
       - Laplace: Fit a quadratic at the mode using Hessian or Fisher information.
         - Optimize to the top of a single mode, fit a quadratic

## Recent Advances

Where do we go from here?

 - We wanted to leverage amount of transferrability by exploiting information from related tasks
 - Uncertainty/robustness frontier
 - X-axis: number of parameters: As the model scales. We don't just want to see gains test set performance
   but we want better calibration and better uncertainty.
 - But turns out that as we scale up the number of parameters, our uncertainty quality doesn't really scale.
 - Scale: As we use larger capacities we're constrained in many ways, we probably don't want to train multiple
   copies.

Ensembles as a giant model
 - We can trace the frontier by providing a perspective of ensembles as a single model
 - Paths between subenetworks are independent, SGD trained models have independent predictions
 - Brdge the gap from single model to ensembles by sharing parameters or by
   learning to decorrelate during training.
 - How to better share the information here?
   - We want to share parameters - instead of enforcing by construction that we have
     completely independent behaviour, we can have everything be glomped all together,
     then learn how to decorrelate.

 - BatchEnsemble:
   - Parameterize each weight matching as a new weight matrix multipled by the outer product of two vectors $r$ and $s$
     - $W_{i} = W \cdot F_i$, $F_i = s_i r_i^T$
     - $W$ is shared, $F_i$ is separate per model.
     - Shared parameters are taking the bulk of all parameter cost - the $s_i$ and $r_i$
       are much smaller.
   - Convenient vectorization
   - duplicate all exmaples in a mini-batch $k$ times, $Y = \phi(((X \cdot S)W) \cdot R)$
   - Can interpret rank-1 weight peturbations as feature-wise transformations.
   - Don't need to do that massive matrix multiplication by $F_i$. $S$ modulates the inputs
     and $R$ modulates the outputs.
   - Similar to FiLM.


 - Bayesian Neural Nets
   - Variational BNNs are effective at averaging uncertianty within a single mode
   - but they don't explore the full space.
   - Ensembles capture different modes.


 - Rank-1 Bayesian Neural Networks
   - Start from BatchEnsemble's parameterization
   - Add priors over rank-1 wieghts $p(r)$ and $p(s)$
     - $p(W) = \int \int N(W|(rs^T \sigma)^2p(r)p(s)$
   - Use mixture distribution as a variational posterior
     - Just the fact that you use multiple independent distributions, this is necesary
       to capture multi-modality captured by ensembles.

   - Rank-1 combine local and global behaviour.


Faster and Simpler Models:
 - You can get same results with an even simpler configuration MIMO (multi-input multi-output)
 - Instead of low-rank perturbations, rely on subnetwork paths learned implictly during training.
 - Basically: Pass multiple inputs and match to paths
   - You share all the activiations - one single forward pass. But by forcing $x_1$ to map
     to $y_1$, you get better results.
   - Over the course of training you learn to diversify.
   - Dustin: x_1, x_2, x_3 -> concat -> model architecture -> apply 3 separate output layers.
     Do average of softmax cross-entropies, each matching a corresponding input with its output.
   - Multiple output layers, do an average of softmax cross-entropies


How do you select the prior:
 - Standard normal prior N(O, 1) is the default, but its not great
   - Bad statistical properites:
     - Does not leverage information about the network structure
     - in the limit, all hidden units contribute infinitisemally to each input
     - Doesn't take into account parameter sharing and conditional dependence.
   - Bad optimization properties
     - Sensitive to parameterization
     - Too strong a regularizer

 - Increasingly popular idea is to think about the overall input-output relationship
   - function priors (Hafner, Sun)
   - priors can be non-probabilistic, coming in the form of structural biases
   - Think about inductive biases that assist OOD
     - Data augmentation: extend the distribution, encourage invariance to things that are irrelevant
     - Contrastive learning, equivariant architecture.	

 - Data Augmentation:
   - Two considerations:
     - set of base augmentations: color distortions, word substitution etc
       - translation/rotation/shear
       - composing base operations and mixing them can improve accuracy and calibration under shift.
       - AugMix improves accuracy and calibration by quite a bit.
       - Especially if we compare under this ImageNet-C test-set.
         - standard/standard ensemble calibration error scales with corruption
         - accuracy error scales with corruption
     - combination strategy

 - Distance awareness
   - As you are training on a certain manifold, you want your uncertainty to go up
     as you move away from the manifold.
   - Eg, half-moons
   - Spectral-normalized Neural GPs
    - Replace output layer with GP layer
    - Apply spectral normalization to preserve input distances within internal layers.
    - You take a given neural network architecture, you chop off the output layers, replace
      it with a Gaussian Process layer
      - As you look at the final activations, the GP allows you to capture similarity,
        eg two things that are similar have similar activations
      - Spectral normalization: Preserve the input distances, preserve input distances within
        the internal layers.


Open Challenges:
 - Scale
 - Datasets
 - Tasks
 - Model Parallelism: Mixture of experts


Uncertainty baselines
 - High-quality implementations of baselines on a variety of tasks

Robustness metrics:
 - 10 OOD datasets
 - Accuracy uncertainty and stability metrics
 - Many SOTA models.

Improving Marginalization:
 - Improve scaling

Priors and Inductive Biases:
 - Improves baseline
