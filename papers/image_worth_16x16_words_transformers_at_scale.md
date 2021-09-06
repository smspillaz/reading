# An image is worth 16x16 Words: Transformers for Image Recognition at Scale

https://iclr.cc/virtual/2021/poster/3013

 => In vision, attention is either applied in conjunction with convolutional networks, or used to replace certain components of convolutional networks while keeping their overall structure in place.
 => We show that this reliance on CNNs is not necessary and a pure transformer applied directly to sequences of image patches can perform very well on image classification tasks
 
 Can we make use of the pure transformer network for images?
 
 Transfer learning benefits from scale. When you increase the size of the pre-training data, performance improves a little it. Increasing the model size also helps.
 
 In this paper, explore the use of a pure transformer for vision, ViT, focussing on transfer learning usecase. Study as well the scaling properties, what does the model learn.
 
 ## Vision transformer
 
 Split image into patches.
 
 Linear projection of flattened patches. The order is lost, so we add some positional embeddings.
 
 Then feed it into an encoder with a dummy token that can attend to everything else. Attach the classification head to the representation for the dummy.
 
 Base model: 12 layers, hidden size 768, MLP size 3072, 12 heads, 86M params.
 
 Also experiment with a hybrid CNN, instead of passing patches, pass the linearized feature maps.
 
 Scaling the transformer architecture is enough to make the CNN features unnecessary.
 
 ViT-Huge beats SOTA while being 4x cheaper to pre-train.
 
 ViT-Large/16 is 14x cheaper to train and matches CNN SOTA.
 
 ViT speed scales mostly linearly in number of patches =.
 
 ### Position Embeddings
 
 Visualize the cosine similarity of learned position embeddings. Different small images use different query patches. Deviates from locality in interesting ways.
 
 
 ### Receptive Field Size
 
 For each attention head, plot the average distance between query patch and the patch it attends to.
 
 Finding: Early layers, some attention heads are local, some are globals, then later on attention becomes much more global. Idea of "building up local features".