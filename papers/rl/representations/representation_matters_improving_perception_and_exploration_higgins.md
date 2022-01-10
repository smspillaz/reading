# Representation Matters

[[representation_matters_disentanglement_exploration_robotics.pdf]]

Contributions:
 - Dimensionality strongly matters for task generalization, but is negligible for inputs
 - Observability of task-relevant aspects affects input-representation usecase
 - Disentanglement leads to better aux-tasks but only helps a little bit as inputs


Applies MONET and Transporter to transform input inputs which leads to performance on par with ground-truth simulator states.

Transporter: Unsupervised method for discovering keypoints of independently moving entities

MONet: Augment VAE with a recurrent attention network which partitions the image into N attention masks. Reconstruct the weighted sum.

## What happens when you transform from pixels to low-dimensional state

Two baselines:

 - Pixels
 - Ground truth states (fully observable features).


MONET can do about as well as the grouth truth, Transporter a litlte worse, entangled VAE much worse.

Pixels usually does badly and is about on-part with random projection.

If you discard task-relevant dimensions in the disentangled representation case it reduces task performance. Eg, need at least 4 features required to represent positions of two objects.


Authors claim that disentangelment has a "limited impact on policy inputs in our experiments", but when using smaller models, interpretability provided by disentanglement helps you to choose the right subset. Also helps with exploration because you can independently control features in the environment.