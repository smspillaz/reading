# Towards Nonlinear Disentanglement with Temporal Sparse Coding

 - Most experiments are limited to carefully constructed scenarios
 - Natural data: Sparse prior on temporally adjacent observations and recover teh true latent variables up to permutation and sign flips
 - More datasets: Natural sprites and KITTI masks, integrate measured dynamics.


=> Disentanglement:
	We want to learn representations such that we can recover the generator factors. To compare, we need to know the state of the world.
	
	Nonlinear ICA: If observations are sampled IID, it is impossible to guarantee that the model recovers the underlying state of the world. Similar result in Locatello.
=> What do we know from existing work -  we need an inductive bias
=> can this be found in natural video?


We, we have a video of a car driving. We could extract the instance segmentation mask, extract scale, x and y position. These are all relevant for downstream tasks.

Use a large scale YouTube-VOS dataset. If we analyse the transition distributions, they all have the same shape. The amount of factor changes in small in magnitude but occassionaly they can change a lot. These are sparse. By imposing a prior that expects these transitions, we can achieve identifiability.

Dataset: Natural sprite: Render sprites in accordance of objects, isolate transitions from data complexities.

Dataset: KITTI masks: pedestrian masks extracted by autonomous recorded videos.

The world is not IID: It changes slowly over time.

We have the state of the world, but this state is a function of time z = g(t), it has dynamics. The observations are temporal sequences. Assuming sparse natural transition statistics, this becomes identifiable.

![[sparse_disentanglement.png]]

Intuition: Start with sparse natural transitions. This gives us a prior that objects in nature change sparsely. 

Notice that the prior on the distribution has principal components that are orthogonal.

Generator will learn something that is rotated. The model latents mix up horizontal and vertical transitions. If we pass each latent through the generator, then the typical observations will have diagonal transitions, but this is a problem, because the real data has sparse transitions, so these transitions can only be matched up to a permutation or sign flip.

Standard VAE. Optimize a standard normal prior and produce good reconstructions. Optimize the posterior to match the prior but also provide good reconstructions.

For the second timestep, there is a different prior - transition prior. Centered around the posterior mean from the last timestep. So we expect the latent to move in certain directions around the previous posterior. Then compute the posterior with respect to THIS prior.

Results. Inputs: Pairs of inputs that differ sparsely. Aggregate across metrics.

If you use a uniform prior, slow-VAE still performs OK, but we have an overall drop in performance. Latent walk - xy position and scale have been mapped into single dimension. However rotation hasn't been

![[nonlinear_disentanglement_failure_cases.png]]

Still some failure cases. For the optimal case you expect to see diagonals. Note that for rotation, correlations are sinusoidal.


Training with natural data: (KITTI masks):
 - For concepts that can be quantified, these are represented clearly in certain dimensions, but mapping is not perfectly one to one..
