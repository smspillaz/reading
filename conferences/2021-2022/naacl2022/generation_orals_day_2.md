# Low Resource Style Transfer via Domain Adaptive Meta Learning

Method 1: Improvements on MAML

Method 2: Adversarial Transfer Model

 - Use adversarial Style Training to do unsupervised text style transfer
 - Pre-trained generation language model as base sequence model

Combining methods 1 and 2, DAML-ATM (Domain adaptive Meta-Learning with Adversarial Transfer Model

# Don't take it Literally an Edit invariant Loss

Problems in training text-genreation mdoels - optimize the cross entropy loss.

CE loss assumes exact matches of the source sentence with the target.

Problematic situations are like:
 - Paraphrases
 - Noisty Targets
 - Weak Sueprvision

Other related work :
 - Policy gradient (unstable)
 - Student Forcing (subsitutte teacher forcing, alleviate influence of noise)
 - Loss Truncation (adaptively remove high-loss examples, assume that they are invalid)

EISL: Edit-invariant sequence loss

 - Inspired by translation invariation property in image.
- Compute convolution over nosiy target.


Denote $C$ as the number of times the n-gram of $y*$ happens in $y$. We want to maximize the number of times that the reference sequence $yU$ appears in the candidate.

Minimize the expected vlaue of $C$. Derive an upper bound of the loss. The upper bound only involves a conditional distribution.

Minimizing the n-gram matching loss over all positions can cause the model to assign equal probability to all positions and therefore cause training to collapse. The solution is to adopt gumbel softmax to reweight the n-gram positions

Connections with common techniques:
 - CE is a special case of ESL
	 - Eg, when the n-gram is the same length as the generated sequence
 - BLEU and CSL: BLEU considers n-gram precisions and EISL maximizes the log probability.

Resutls:
 - Learning frm noisy text
 - Shuffle noisy: Translation frm german to english. Lets say your targets are shuffled, can you still learn to generate good translations?
 - EISL can learn good information in rather noisy data.

Unsupervised Text Style Transfer:
 - Transfer a positive sentiment to an egative one and there doesn't exist parallel data.
 - The sentence is like weak supervision to keep the candidate preserved.

Learning non-autoregressive generation:
 - Predict tokens simultaneously with a single decoding step. Harder to keep the order of words in the sentences.

This mainly works on messy targets. If the target is clean, the loss doesn't help that much.

# Towards Robust and Semantically Organised Latent Representations for Unsupervised Text Style Transfer

Task: Text style transfer.

Assumption: Every sentence consists of independent style and content components.

Style is defined by class label (sentiment, formality, toxicity, etc)
Content is the style independent information.

Zero-shot approaches for TST. Most real life datasets are non-parallel. The style-transfer output is not there. We consider the zero-shot setting. Feed raw sentences during training and use class labels during inference.

Prior works:
 - Adversarial Autoencoder: Latent Prior Z is enforecd to be gaussian using discriminator and adversarial loss
 - Identity covariance matrix, disentangled latent units in Z, clustering towards the mean.

The denoising AAE - add discrete noise to the input (eg, token dropout). This denoising promotes clustering of similar sentences together.

Why does this happen
 - sentences with high word overlap have a higher probability of being mapped to the same intermediate representation
 - Stylistically dissimilar sentences with high word overlap might be mapped close by
 - Levensthein distance being small does not imply similarity. Eg "service was friendly" -> "service was rude".

Instead of doing word dropout, just do continuous noise on the embedding space Maybe controllable noise in the mebedding space can avoid mapping dissimilar sentences together. Similar words get noised into a common represnetation, but dissimilar words are unlikely to be noised into a common representation. Eg "good" and "great" are closeby, but "good" and "bad" are far apart.

Methodology: Hyperspheres in E: The perturbation embeds $E$ such that the resultant $E'$ live in a HS whose density and raidus we can control. Controlling the radius of the hypersphere helps to control for meaning.

Inductive TST using Vector Arithmetic. TST is possible using simple vector arithmetic.

The difference between the means of all vectors ins tyle Y and X is computed, then you add the difference to all words and hopefully this transfers the style.

Quantitative analysis of the latent space: TSNE plot of encoded latent vectors. EPAAE shoes tighter and mor organized clustering than DAAE.

By controllign the parameter $k$ we can control the amount of transfer to the new style.

Question: Does the batch size matter? For contrastive losses you need large batch sizes to make this work. Its not that our objective is to push them away from each toher. Its a zero shot approach, we just feed it raw input sentences and $y$ pushes itself away because if we add noise, it will automatically push together

# MOVER

Hyperbole - a figure of speech that deliberately exxagerates a meaning of a sentence to show emotions.

 - I won't wait for you, it took you centuries to get dressed

Hyperbole generation
 - I won't wait for you, it took you a long time to get dressed -> I won't wait for you it took centuries for you to get dressed.


To generate hyperbolic sentence, we introduce MOVER
 - Mask: mask potential hyperbolic spans
 - Over-generate: fine-tuning BART to predict masked spans, generating multiple candidates
 - Rank: Re-rank based on hyperbolicity.

Extract hyperbolic spans based on PSO-n-gram (eg, they tend to have a simlar structure) and unexpectedness (eg, how much does this fit)