# Structure, Symmetry and Equivariance in Deep RL

Structure

 - How something is made up of its parts:
	 - Traffic lights network: made up of individual lights, but the lights must co-operate to achieve some goal
	 - Robot: several joints
	 - Video games
	 - MDPs
 - Symmetry:
	 - Similarity of things in different orientations - left and right sides are mirrored versions. Actions good to take on one side, good to take on the others as well.
	 - Pong: up when the paddle is down or down when the paddle is up, similar.
	 - Can we re-use the solution from one orientation for all the other orientations.


Groups:
 - A group is a set together with a binary operation obeying the group axioms
	 - Identity
	 - Invertibility
	 - Closure
	 - Associativity
	 - Eg, translations, rotations
 - Equivariance
	 - f(g x) = g' f(x) (applying operator g on x, then mapping to feature space f is equivalent to mapping to feature space then applying the feature-space version of g, g')
	 - Eg, g changes the color. There exists some g' that changes the color in the "feature space". g' on f(x) is the same as f on g x
 - Invariance
	 - f(g x) = f(x): Feature representation doesn't care about the transformation.
	 - Eg, g changes the color. Representation doesn't care about the color. It is *invariant*.



Much work around equivariance is in computer vision. If we rotate a dog 90 degrees, its still a dog! In the real world, this is a bit useless though, as the dog will fall over.

Reinforcement learning has plenty such problems.
 - Multi-agent systems.
 - Moving left leg forward. Same as moving right leg forward.
 - Semi-group equivariance.


MDP Homomorphisms:
 - Map ground MDP -> abstract MDP, preserves dynamics
 - Basically, the dynamics are preserved. Transitions and rewards are preserved. A policy that is optimal in the abstract MDP is optimal in the larger MDP by definition.
 - The reduction in joint state-action space allows us to exploit symmetrices in the action space.


Structure in DRL:
 - Problems are quite sample hungry to solve in a naive way.
 - Co-operative multi-agent systems, co-ordination graphs.
 - Composable planning with attributes (Zhang et al)


Structure and Equivariance:
 - Plannable Approximations to MDP Homomorphisms (AAMAS 2020):
 -  - Equivariance under actions
 -  Enforce action-equivariance constraints.
 -  Network becomes structure preserving map, MDP homomorphism.

## Plannable Approximations to MDP Equivariance under Actions

![[plannable_approximations_to_mdp_equivariance_under_actions.png]]

 -  If we take an action in the original MDP and map to an abstract MDP, it should be the same as mapping to the abstract MDP and taking the equivalent action there.
 -  Same with the latent space


Combine this view on learning state representations with a contrastive loss that prevents latent space collapse.

Perform exact value iteration in latent space. Map the policy back to the original space using Q value of the original. Trains in much fewer epochs than reconstruction baselines. CartPole-v0 in only 100 trajectories.

![[plannable_mdp_homomorphisms.png]]

States that transition together end up close ot each other. Learnt representations given in figure above. This work's approach is on the right.

## Contrastive Learning of Structured World Models
![[contrastive_learning_structured_world_models_architecture.png]]

Learning representations of states structured as objects and relatiosn. Use GNN based model that predicts relationships.

Object-factorized contrastive loss. This enables the model to do better at multi-step predictions than autoencoders. Object-based factorization and relational model contribute to being good at the next states.

## Symmetry in Deep RL

Equivariance: Kaleidoscope experience reply: equivariant encoding (Laskin et al).

*MDP Homomorphic Networks: Group Symmetries in Reinforcement Learning*

Often symmetries to be found in reinforcement learning problems.

If we flip the image for pong, we expect a policy with flipped actions to perform the same. Same with cartpole.

![[mdp_homomorphic_networks.png]]

Symmetric state-action pairs have the same policy. Computing the policy then permuting it is the same as permuting and then computing the policy. You can exploit the symmetries to reduce the number of samples required.

You can create a deep network constrained by MDP homomorphisms. 

How to create equivariant neural networks? Symmetrizer, see the paper.

GridWorld - rotational symmetry of four elements.

## Future Work

 - Group structure as a prior for self-supervised learning
 - Equivariance without group structure (driving in the snow)
 - Symmetries in factored MDPs, partial observability, multiple agents
 - **Learning** symmetries
 - **Approximate** symmetries

