Talk by Hinton et al at GTC21

Transformers
SimCLR => Maximize agreement between crops of similar images, minimize agreement between crops of different images

 => problem: not intuitively satisfying. What if a patch contains A and B and another patch contains A and C? Shouldn't get the same output vector.

 => We really want to disentangle the outputs so that enc(A & C) != enc(A & B) but shares some components, so its more different than enc(B & C).
 
 Representing part-whole hierarchies
 
  => Symbolic AI: Dynamically create a parse tree
  => Capsules: Allocate neurons to each possible node, activate a small subset and use dynamic routing
  =>Allocate embedding vectors to nodes in the parse tree, for each node use an island of identical vectors for all locations occupied by that node.
  
  
  For each location, we get different locations in the image. Allocate a column of hardware to each location. With each column we have multiple levels of representations.
  
  ![[glom_vectors.png]]
  
  These islands of identical vectors form a tree. Notice that you have replication at higher levels. Use the identity of vectors as a representational method.
  
  Question: How do you maintain consistency at the higher levels?
  
  ![[glom_levels_one_location.png]]
  
  Top-down neural net, bottom-up neural net. The columns interact in a simple way. They interact at timesteps.
  
  Averaging together things that are already similar.
  
  Reminds me of Locatello et al in ada-gvae.
  
  Contrastive learning - see how parts are related together to form the same whole.
  
   => problem: the very same face vector must produce the red vector for the nose and the green vector for the mouth. It has to produce two different kinds of vectors at different locations.
   
   
   Neural Fields: Top down neural net receives an extra input which represents the image location of the column (position embedding). Pose fo the face plus the position embedding .
   
   ![[neural_field_decoder_example_glom.png]]
   
   Attention weighted average. How much to weight the embedding at location y when updating x. This causes the islands to form. They are like echo chambers.
   
   Training: Deep end-to-end training, predict uncorrupted image from masked image. Similar to BERT.
   
   Consensus embedding at level L: Preditions coming from below and above. Predictions from attention weighted average of neighbouring columns. Consensus is the new embedding. Take the predictions made by the top-down neural net and make it more like the consensus.
   
   Is it wasteful to replicaete the object-level embedding vector for every location in an object?
   
   Replicating object embeddings is less expensive than you think because it allows you to have cheap long-range interactions - you only need a sparse set of connections.