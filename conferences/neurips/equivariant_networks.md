# Equivariant Networks Track

Example:

 - Translation equivariance in CNNs
 - Translations are symmetries of many visual learning problems
 - Where the object is is not important
 - Convolutional layers exploit translation symmetry.

Equivariance and Symemtry:

 - Output featre map undergoes a translation when the input does
 - Equivariance means symetry is preserved.

Symmetry:

 - A transformation of some object that leaves some aspet of the object invariant.
 - Eg, rotate a triangle by 2pi/3, won't change the object.
 - We're referring to the description of the object, not the object itself.
   - Eg, we store the triangle as 3 co-ordinates
   - Rotate the triangle by this amount - the co-ordinates change
     but the object did not change
   - Alternative description of the same object.
 - Idea: Neural Networks should process equivalent representations equivalently.


Examples from machine learning:
 - Rotation of image, label should be the same
 - Graph: Permute the graph, same structure, should have the same encodings
 - Need to think about how you encode the graph so that it can be passed to
   the neural network. Encode the graph as an adjacency matrix.


Symmetries of a label function:
 - g (transformation): X to X
 - L (ground truth): X to Y

 - g is a symmetry if g(L(x)) = L(x)


Transformation Groups:
 - A transformation group is a set of transformations that:
   1. Contains the identity transformation (by definition, this is a symmetry)
   2. Closed under composition (composition is associative, two transformatiosn that are invariant, composing the two should be a symmetry)
   3. Closed under inverses (if it doens't change the object, it must be invertible because it does not lose information)

flavours of groups:

 - Discrete groups:
   - finite
   - Countably infinite - integer translations in 2D combined with rotations.

 - Countinuous groups:
   - Compact: group of rotations and reflections
   - Locally compact: There are fairly nice mathematical theora
   - Non-locally-compact.

 - commutative / non-commutative groups: The order doesn't matter or matters.
   - Commutative: 2D rotations
   - Non-comutative: 3D rotations, order matters - these are more difficult to understand.

How does knowledge about a symmetry group help with learning?

 - Consider rotations
 - Orbits: The orbit of a point x is the set of all points that you can get by
   applying transformations to x
 - Eg, for 90 degree rotations, generally 4 elements in this group, but
   for a circle, there is just one element.

 - If the network is equivariant, then all points in an orbit should map to one point
   in the data space and one point in the label space.

Equivalence relations:

 G-equivalence: x is G equivalent to y if and only if there exists some g in G such that g(x) = y

 - reflexivity: G contains the identity
 - transitivity: G is closed under composition
 - symmetry: if x is G equivalent to y, then y is G-equivalent to x

Invariance vs Equivariance:
 - Why is invariance not enough?
   - Picasso problem: we're trying to understand this image.
   - To recognize a face, it is useful to first detect parts of a face.
   - But a bag of face parts is not a face!
   - A network built on top of an invariant represetnation can't tell if things
     are in the right space relative to each other


Group representations:
 - Linear group actions
 - $\rho$: a representation
 - $\rho(gh)$ = $\rho(g)\rho(h)$: Eg, it should be the same as applying matrix multiplication


Graph features:
 - A representation of the symmetric group $s_n$:
   - trivial representation: Takes any permutation $P_{xy}$ and maps it to a single scalar
   - $\rho_1$: Equivariant features: you might want to associate one number with each number in the graph -
     node features transform by the permutation.
   - $\rho_2$: Tensor features

Example: Translation of 1D signals:
 - Group: Group of integers under addition
 - Consider the space of 1d signals with d = 5 samples

General setup:

 - Equivariant network:
   - Feature space $X_1$
   - maps betwene them (layers)
   - A symmetry group G
   - Group representation $rho_i$ of G for each $X_i$
   - Equivariant if for all layers and all group element, it is the case that applying $f_i$ after $\rho_i(g)$ is the
     same as $f_i$ then $\rho_{i - 1}(g)$.
   - Ladder-like diagram.

Equivariance as a Symmetry-consistent generalization

Lets say you have many letters of style A and they are all on orbits.

Lets say that the network maps the rotated X and Y to different points - this
cannot happen because the net must generalized consistently across the whole
output. This cannot happen anywhere in the input space including points that
you've never seen before.

Equivariance vs Data augmentation:
 - When you build an equivariant net, you're putting a constraint on every individual layer.
 - with data augmentation you're putting the constraint on the network as a whole, but
   the individual layers can be nonequivariant.
 - Data augmentation is easy to implement, equivariance is a bit trickier.
 - But data augmentation does not always work, you're definitely not guaranteed equivariance
   in the test data.
 - Convergence in equivariant models is much more efficient.


Canonicalization:
 - Invariant representation 
 - Estimate pose and use it to normalize the instance
 - the mapping that assingns a pose to an image is discontinuous. Makes learning harder.
 - Picasso problem: If you want to canonicalize a whole object, you first need to
   know where it is in the image.

Examples of where these have been applied:
 - Sets: Sets do not have an order (Deep sets)
   - Any permutation invariant function can be approximated by an architecture on the left
   - Independent processing of each element
   - Sum the feature vectors, then process the result (but this is not always the most efficient way)
   - The idea is that the sum loses the ordering

 - Graph Networks: Permutation of rows and cols of adjacency matrix does not change the graph!
 - Puminary Nodule Detection in CT scans: 3D group convolutional networks (G-CNNs)


Steerable CNN:
  - Work for continuous rotations
  - When you stabilize the feature map (backrotate it)
    - in the case of the CNN the feature maps fluctates, feature map that processes the input
      matches one feature in one orientation and a different feature in a different orietnation
    - In a G-CNN you match the same feature regardless of orientation
  - E2-CNN / E3-CNN

DNA CNN:
 - Reverse complement symemtry:
   - DNA can be read in two directions. Two strands with complementary letters.

Spherical CNNs:
 - Arises in a number of applications. You want a convoluitional net that is equivariant with respect
   to this group.

Computational physics and chemistry: 3D-embedded graph. You can rotate the whole molecule.


Equivariant Convolutions:
 - Whenever your data exists on signals.
 - Locality: Use small local filters, exploit the spatial structure in the data.
 - Space sharing: same parameters are used in different parts of the space
 - Generalize this concept from planar images to a much later class of signals.


Regular G-CNNs
 - Take each filter, rotate it 4 times, convolve translationally with the image. In total
   we get 8 feature maps.
 - Rotate the image and apply the rotated convolutions. So the feature maps detect the same
   feature but they're NOT in the same channel. Because they're rotated, they're in the second
   orientation channel.
 - We move them to a different position and apply a cyclic shift along the channel dimension.
 - We have a new kind of group representation in the network on the first layer.
 - On the next layer, we have to rotate spatially and then do a cyclic shift along the channels.


Spherical Convolution:
 - In spherical convolution, the output feature map R in SO(3) is computed as an
   inner product between the input feature map and a filter that is rotated by R.
 - The output feature map will be a function on the space of rotations.
 - Since SO3 is a 3-dimensional manifold, our output is a signal on the 3-dimensional manifold.

Feature fileds and induced represnetations:
 - Why is a vector field different from two scalar fields.
 - Alternative 1: Apply a rotation G, 90 degrees. Naive way to do this is to move vectors to a rotated position.
 - Alternative 2: Apply rotating the vectors themselves by applying $\rho(g) f(g^{-1} x)$

Steerable CNNs
 - Model convolution kernel as a map: $R^2 \to R^{C_{out} \times C_{in}}$
 - A steerable kernel satisfies K(rx) = $\rho_{out}(r)K(x) p_{in}(r)^{-1}$:
   - If we rotate the convolutional kernel
   - Its the same as taking the original convolution kernel and steering it using $\rho_{in}$ and $\rho_{out}$.
 - Convolution/cross correlation: $\int_{R^2} K(y -x) f_{in}(y) dy$
 - Input space: a 1-dimensional scalar fied, as output you want a vector field
 - The filters have to be steerable filters: to take a rotated version of that filter, you take a linear combination
   of the basis fitlers.
 - This creates an equivariant convolution filter.

Homogeneous spaces:
 - X is homogeneous for a group G if for any two points x and y, there exists $g \in G$ such that $gx = y$
   - For any two points you may be represent them by a transformation in $G$
   - plans are a homogenous space for the translation group, roto-translations, etc
   - spheres are a homogenous space for the 3D rotation group

 - Stabilizer subgroup:
   - Pick an arbitrary point. Ask what are all the rotations in the group $g$ that leave the point fixed
   - all the arotations through the north pole (if your point is the north group).


Cosets and coset spaces:
 - Left coset of subgroup H in G wtih respect to G is $gH = \{gh | h \in H\}$
 - Quotient space: Under mild conditions G/H inherits any topological structure from G
 - Eg, from SO3 G - you can pick a point, then find the stabilizer subgroup - this is SO2 H
   that describes G for a single point.


Feature fields: general theory

 - Group G and subgroup H
   - turns G into a principal-H bundle

 - Homogeneous space B = G/H - this gives us a coset space with a choice of origin
 - We can create an associated vector bundle - choose a feature space V
   - choose a representation $\rho$ for $H$, which tells you how this feature transforms
     under $H$ which doesn't move points around.
   - Attach each point in the base space, attach each point in the vector space with a representation.

Convolution is all you need:
 - Any equivariant linear map between two induced representations can be written as a convolution
   with a steerable kernel.

Steerable kernels:
 - Can be represented as
   - A space of kernels on $G$ subject to a linear constraint
   - A space of kenrels on $G/H$ subject to a weaker constraint
   - A space of kernels on $H_2 \\ G/H_1$ subject to an even weaker constraint.

Reference frame:
 - In order to represent a field numerically, you have to choose a reference frame
 - When you go to more general manifolds, thinngs become subtle
   - Unlike in the case of the plane wehere to an engineer it seems like there is
     an obvious chance of a reference frame, on a sphere it is non-obivious because
     there is no preferred choice of frame
   - On some manifolds there is no smoothly varying choice of reference frames.
 - In mathematics they insist on smoothness, so you cover your manifold with your
   neighbourhoods called charts.
 - In engineering you discretize the space anyway.

Gauge Symmetry and Gauge CNNS:
 - Symmetry between different frames
 - The same linear map should be applied to coefficients describing the field regardless of which frame was chosen.
 - If you change the frame, the coeffiecients will change, but the mapping will be similar.
