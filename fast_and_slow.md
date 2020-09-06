# Grounded Language Learning Fast and Slow

Contribution: Novel dual-coding external memory which can exhibit one-shot word learning.
 - after a single introduction to a novel object via continuoua visual perception and a language prompt,
   agent can re-identify the object and manipulate it as instructed ("put the dax on the bed").
 - integrates short-term within-episode knowledge and longer-term lexical and motor knowledge.
 - one-shot word-binding generalizes to novel exemplars within the same ShapeNet category

Agent observes the world via perception of the pixels and learns to respond to linguistic
stimuli by executing sequences of motor actions allowing it to move and manipulate objects.

Trained by combination of conventional RL and predictive (semi-supervised) learning.

Learning fast-map novel names to novel objects relies on explicit external memory.


## Environment

Room contains pre-specified number N of everyday 3D rendered objects from a global set G.

Episodes consist of a discovery phase and an instruction phase.
 - Discovery phase: Explore the room, environment returns a string with the name of the object.
 - Instruction phase: Randomize the room, emit some instruction
   - Learning signal: 1.0 if you pick up the correct object in time. 0.1 if you visit an object.

## Network Architecture

 - ResNet for processing the images
 - Self-Attention for processing the language input

## Memory Architecture

 - LSTM memory basically fails to learn anything.
 - Meta-Learning:
 - When you have to learn visual categories from pixel input, a slot based external
   memory mihgt be necessary to make meta-learning work successfully.
     - Basic idea: Allow the network to make explicit comparisons, rather than having to compress it
       into the weights or state of a recurrent network or LSTM.

Two approaches that you can do external memory with:

 (1) Differential Neural Computer: 
 - At each timestep, you have a latent vector $e_t = w(h_{t - 1}, r_{t - 1}, x_t)$,
   function of hidden state, previous memory read and current input
 - In this case, the input $x_t$ is just the concatenated pooled vision input + sentence embedding
 - Latent vector $e_t$ passed to the core memory LSTM to produce current state $h_t$.
 - Reading from memory produces $q(\bold{h}_t)$ (a query vector) and read strength. 
   - Compute the cosine similarity between the query and all embeddings in the memory - memory
     hard-thresholds this to return only the most simialr entries in the memory.
   - Aggregate everything into a single vector by normalizing with a softmax and taking the weighted average (by softmax).

 (2) Dual-coding Episodic Memory
 - Knowledge of the same situation is retained in modality-specific (visual / verbal) codes.
 - Instead of writing a single mebedding, write both the visaul and linguistic observations itno keyvalue external memory.
 - Either column can function as the key into the memory, or both simultaneously
 - Weight memories by softmax normalization $\hat m_j = s_j m_j$.
 - Apply self-attention to the memories $\hat m_j$ and sum the result elementwise into $r_t$.
 - Same process follows, concat $[r_t, h_{t - 1}, x_t]$ to produce the initial hidden state for the LSTM, which then produces
   the next hidden state $h_t$.
 
 (3) Gated Transformer
 - 4 Layer Transformer with principal embedding size of 256.


## Setting up the training
 - Train policy by V-trace off-policy actor-critic loss
 - Observation reconstruction: Latent vector passed to a ResNet, auxilary task to reconstruct the image. Then compute cross-entropy
   reconstruction loss. Also reconstruct the sentence.
      - Ablation study: *Seems to help quite a lot* (34\% accuracy -> 98\% accuracy for DCEM). Even for LSTM it takes you from 0.33 -> 0.55.

# Results
 - Dual-coding Episodic Memory: Still requires about 400 million steps in order to learn how to solve the task reliably (98%+ accuracy)
 - Baseline accuracy: 0.33
 - System seems to break down after about 8 objects. Observaton that we overfit to the "three-ness" of its experience. Fix
   this by increasing number of objects during meta-training.
 - Novel objects: Meta-training on 20 objects seems to genrealize well to novel objects. In fact, it is only when we drop down
   to three objects in the meta-training procedure that we lose this generalization capability.
 - Category extension: Can you handle different instances of the same type? Try ShapeNet:
    - Point to "this is a dax"
    - Ask the agent to "pick up a dax" which is of the same category but looks different.
      - Does OK during testing (55% accuracy)
      - To improve this, adjust categories *during training* (eg, "this is a dax" (1), then during the second phase in a
        training episode, "pick up a dax" has different attributes)
 - Temproal aspect: The $k$ parameter is important: remember that the memory returns the top $k$ memories. Robustness
   is enhanced if $k > 1$ (eg, if you have more than one view of the object, your robustness improves).

# Integrating Fast and Slow Learning
 - GPT3 is kind of able to do this through its context window:
    "To do a 'farduddle' means to jump up and down really fast. An example of a sentence that uses the word farduddle is:"
    
    response: "One day when I was playing tag with my little sister, she got really excited and she started doing these crazy farduddles"

 - Testing in this setting: combine a fast mapping task with a more conventional instruction following task
 - Discovery phase: Agent must explore to find the names of three unfamiliar objects, but room also contains familiar objects
 - Instruction phase: Put one of the unfamiliar objects on either the bed or into the box (familiar objects

