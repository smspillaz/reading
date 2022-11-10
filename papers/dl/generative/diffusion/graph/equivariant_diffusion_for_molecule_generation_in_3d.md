---
title: "Equivariant Diffusion for Molecule Generation in 3D."
venue: "ICML"
pages: "8867-8887"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/HoogeboomSVW22"
ee: "https://proceedings.mlr.press/v162/hoogeboom22a.html"
url: "https://dblp.org/rec/conf/icml/HoogeboomSVW22"
authors: ["Emiel Hoogeboom", "Victor Garcia Satorras", "Cl\u00e9ment Vignac", "Max Welling"]
sync_version: 3
cite_key: "conf/icml/HoogeboomSVW22"
---

Molecules live in 3D space, but have translational, rotational and reflectional symmetry. Eg, rotating the molecule doesn't change its structure.

A function is equivariant when the action of a transformation group applied to the input is the same as applying the transformation group to the output. Eg $T(f(x)) = f(T(x))$.

If we consider rotations and translations to be given by $R$, then for diffusion, you have:

$$
p(y|x) = p(Ry|Rx)
$$ for all orthogonal R.

How do you get there.

In [[equivariant_flows_exact_likelihood_generative_learning_for_symmetric_densities]] it was shown that invariant distributions with equivariant density functions results in an invariant distribution.

Then in [[geodiff_a_geometric_difffusion_model_for_molecular_conformation_generation]], it was shown that if $x \sim p(x)$ is invariant toa  group and the transition probabilities $y \sim p(y|x)$ of some markov chain are equivariant, then the marginal distirbution of $y$ at any timestep is also invariant to group transofrmations.

We want that: $Rz_x + t, z_h = f(Rx + t, h)$ for all $R$ and $t$.

Equivariant Graph Neural Networks: They are composed of "equivaraint graph convolutional layers". Each node gets coordinates $x_i$ and features $h_i$.

Equivariant Diffusion Model: EDM defines a noising process on both the node positions and features, but then learns denoising using the equivariant network.
