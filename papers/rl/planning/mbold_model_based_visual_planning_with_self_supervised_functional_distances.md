# Model-based visual planning with self-supervised functional distances

Learning goal-reaching policies with RL is hard when hand-engineered reward functions are not available. Planning to reach goals requires a notion of functional similarity between observations and goal states.

Learn entirely offline using unlabelled data.

Reach arbitrary goals that can reach specific goal images. Learn from other robots just from images.

They all follow the laws of physics.

Visual Foresight Algorithm: MPC using MSE planning costs. Prior model-based and model-free methods struggle to learn in the absence of reward labels.

Q-learning also leads to poor results.

## MBOLD algorithm (described in this paper)

Terminal distance functions learned through Q-learning.

Make predictiosn directly in image space.

Learned distance functions approximate the shortest path between pairs of images. Define as Q-learning. Use hindsight relabelling to attach goals to transitions. Use offline data.

After learning a dynamics function, use them to plan by sampling. Predict several possible outputs from different actions. Replanning performed from newly observed space.

Also works in real-world.

![[mbold_learned_distance_functions.png]]

Distances are qualitatively well-shaped.

MBOLD outperforms VAE and pixel distances.

MBOLD combines predictive models and functional distances in a self-supervised approach.