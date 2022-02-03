# Understanding and extending Neural Radiance Fields

## "NeRF": Representing Scences as Neural Radiance Fields for view synthesis.

Radiance: How much light is being emitted by a point in space

Field: Its a field in the calculus sense.

NeRF: view synthesis: view interpolation

Prior work:
 - Soft 3D work, turn volume into an alpha field
 - Multiplane image methods (stereo magnification, local light fields)
 - Neural volumes: Map from an image to a 3D volumetric interpretation of the world that can be collapsed down from different view angles

Its a great rendering model, but has horrible storage requirements. Bad idea to discretize the world and put it into bins.

Parallel work:
 - NNs as continuous shape representaitons (occupancy networks, CVPR)
 - Another way of looking at a neural network: the neural network *is* the output. It maps from a point in space to a property of that point in space, eg, from x, y, z to a colour.
	 - DeepSDF
	 - Scene Representaiton Networks
	 - Differentaible Volumetric Rendering
 - Difficult to optimize, but very compressible.


NeRF exists at the intersection of these two lines of work

 - input: $(x, y, z, \theta, \phi)$
 - a boring MLP
 - output $(r, g, b, \sigma)$ (how dense is this pixel in space)

Similar to a ray tracer. For every pixel you shoot a ray out from your eye into a pixel, then you trace where that ray goes.

Volume rendering is trivially differentaible:

$$
C \approx \sum T_i a_i, c_i
$$

How much light is blocked earlier along ray:

$$
T_i = \prod^{i - 1}_{j = 1} (a - \alpha_j)
$$

$$\alpha_i = 1 - e ^{-\sigma \delta t_i}$$

Iterate through pixels in an image, shoot out a ray according to our NN, then we do gradient descent to minimize the squared error between the rendered value and the pixel value.

Training network to reproduce all input views of the image.

NeRF is not magic. it only ever sees one scene. it really just tries to memorize the world in a way that happens to do smooth interpolation. Require slots of images.

### Sample efficiency?

Coarse/fine model.

Treat weights as probabilities for new samples.

View directions as input. The model can reason about reflecting and such. At every point in space you learn a 2D function that maps from a viewing direction to a colour.

## Positional Encoding

"one weird trick"

 - Toy problem: Memorizing a 2D image. Can you memorize the image? It will be oversmooth.
 - Take coordinates and sinusoidal positional encoding.
 - If you do this, it now works, you can now memorize the image.
 - We didn't expect that to be so successful....

## "Fourier Frequences Let Networks Learn High Frequency Functions in Low-Dimensional Domains"

Why do 2D positional encodings work well?

You have $L$ frequencies in your positional encoding. This is the highest frequency you can model.

Turns out that you don't even need positional encodings. You can just use random fourier feature. Eg, random matrix pushed through sine and cosine.

### Neural Tangent Kernel

Under certain conditions, neural networks are equivalent to kernel regression.

$$
f(x; \theta) = \sum_i (K^{-1}y)_i k(x_i, x)
$$
ReLU MLPs correspond to a "dot product" kenrel.


Dot product under fourer features is actually a stationary kernel. Its shift invariant and only depends on distances.

`x = torch.cat([torch.sin(x @ B), np.cos(x @ B)], dim=-1)`

## "NeRF in the Wild"

-  Colours don't match up
- Exposure times
- Photos not taken in isolation
- Have to remove all the extra stuff. We want the static stuff.

Input to the systme is a viewpoint + appearance embedding.

Static/transition reconstructions. This captures the transient structure of the scene. Composite the two.

Parameterize the uncertainty as well.

