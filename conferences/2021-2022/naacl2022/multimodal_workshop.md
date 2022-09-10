# Yonatan Bisk - Body and Mind (Grounded Language Learning and VLN)

## Questions and Themes
- the amount of meaning that you can get from just perceiving the world is strictly less than interacting with it.  
- what is the "latent world" that exists in the minds of everyone else? We do things for a reason because we're social agents. We're modelling the internals of other people's minds.  

## Why is VLN complex? What causes the complexity?
- "the gap" between navigation in simulation. In simulated worlds we have been able to work with rich language, in the real world the representations and language are much more constrained.  
- In VLN we have visual complexity and language complexity, but still a static environment and simplified language space.  
- In VLN they simplified the action space in quite a logical way, which was to say, lets treat navigation as graph traversal.  

### Things that have helped in simulated environments
- Things that have helped:  
- Speaker-Follower model (take a trajecotry and describe it)  
- Tactical Rewind: backtracking in vision and language navigation  
- Better alignment between observations and actions (progress monitor)  
- Domain randomization like environmental dropout  
- Bayesian State Tracking  
- Querying and going to the web (VLN-BERT Majumdar)

### Moving beyond simulated environments into richer similators and robotics
- Question: If we move beyond simulators, what actually holds in terms of generalization? Do rich action spaces break algorithms (sequence length, pre-post conditions, output-space, nonreversibility)? Does rich language break things?  
- When humans see a task, they create a high level script with predictates and some sort of task tree and sub tasks. Eg you can build out an ungrounded plan.  
- This is hard. On ALFRED for example, a baseline gets 10% success on seen environments, 1-2% unseen. There's a couple of nice advances (Singh et al 2020 - Progress Monitor), LWIT (Look Wide and Interpret Twice), AMSLAM (learning to act with affordance award multi-modal neural slam), FILM 2020, LGS-FR  
- Why is it hard?  Everything? 

### What helps in richer environments
- What helps?  
- building a map, see FILM. This helps  
- Generate an abstract plan and project the plan on to the map. Have a list of compled subgoals and if you can't complete them keep exploring to build the map until you can put them on the map.  
- You have to model uncertainty over the map as well.  
- semantic search  
- if you have the map - value iteration  
- if you have the instruction attention over the map  
- first thing that happens when I go to someone's house - where is the bathroom  

## Asking for Help
- what if the agent needs help? This is hard  
- you have to know when to ask a question, you have to ask useful questions, you have to get useful answers and so on.  
- Few Shot Language Coordination via Theory of Mind  
- How rich should your model be of every person that you interact with?  
- Simulated Language LEarning from Communicative Goals and Linguistic Input.  
- Eg, how babies learn language. When and where do you supervise? How do you get useful feedback from humans? Language as a communicative game.  
- Should we imitate or act? Treating it as a game is a faster learning signal than just imitation. Communicative games are not fluency.  
- [[rmm_a_recursive_mental_model_for_dialogue_navigation|RMM]] recurisve mental model for dialog navigation. Extend POMDP with a stack. Start asking for subgoals - performance in unseen environments improves when you do this.  
- segmenting subtasks. Both in terms of the language and also the action trajectory. Eg options framework. No supervision later on  

## Future Work
- Questions inside Yonatan's brain right now  
- What semantics are only available via embodiment?  
- How rich should my model be of every person that I interact with?  
- What causes overextension?  
- What encourages models to build models of each other?



# Drew Hudson - Compositionality in Image Generation

05:40 on the workshop video.,

Foundation models fail in peculiar ways. They are highly inconsistent.

New benchmark: Winoground benchmark that evaluates compositionality. CLIP performs no better than chance. Foundation models capture a bag of concepts.

Can we encourage compositionality in generative models? What architectures can serve as an inductive bias? Pretty much all models rely on a stack of convolutions.

Convolutions have their own issues:
 - Fixed computation that doesn't adapt the input. The weight doesn't change dependent on the input that is given.
 - Convolutions have local receptive field. Hard to capture long-range dependencies. In GANs you have issues with consistency, eg, colors of eyes etc.
 - Dependencies across frames are even harder.

Is there a better architecture for image generation?
 - Transformers? Considers all pairwise relations and dynamically propagates information. Not used so much in vision because they're inefficient.
 - Vision Transformers solve this problem in a very hacky way eg by downsampling or taking patches.

Can we have the best of both worlds?
 - [[ganformer_generative_adversarial_transformers]].
 - Bipartite Transformer: Compute attention between latents and image features. Consider all the regions and apply attention between the latents.
 - We start by sampling $k$ latents. Then these capture the different objects in an image, then to generate the image we apply attention between the $k$ variables and the regions in the image in order to propagate information. This gives us some form of bottom-up and top-down processing.
 - The latent variables capture the high-level scene information and they inform how you parse the image itself.
 - From a computational perspective this is nice because you have a linear complexity - you never do self-attention on the image itself.

Results:
 - If we visualize the attention maps, we can see that different slots are generating different parts of te image. The latents attend to semantic entities and cooperatively generate a compositional scene.
 - For different layers (resolutions), the latents split up the work in different ways. Eg, at low resolutions you have segmentation and at high resolutions the latents correspond to different specular features.
- Excels on highly structured scenes, compared to GANs which tend to work well when there is one object in focus like faces.

Controllability:
 - We would like to be able to move one object without impacting the surrounding areas.
 - In DALL-E 2 you have to provide a mask, but ideally we want the model to just know that the object is there.
 - Humans address the task of drawing in an iterative way - first you start with the outline, then details, then colors etc.
 - We can see all the relations by looking at the initial sketches.
 - Can we do something similar in machine learning?
 - [[ganformer_2_compositional_transformers_for_scene_generation|GANFormer2]] model: Planning and Execution.
	 - Recurrently construct a compositional schematic layout (eg, a set of segments like category, shape, depth)
	 - Give images and segmentations that are predicted by a segmentation network.
	 - We have $k$ latents, but the latents are used to generate only the layout and the depth ordering.
	 - We can then compose the layouts by depth.
	 - At the execution stage we have a sort of differentiable painter - the latents model only the region that they are assigned to. Eg, you're masked by the predicted segmentation.
	 - With this we can dynamically add or remove objects.
	 - In this model, we explicitly incorporate a compositional structure into the model.
	 - Eg, if we remove an object in the latent space and render again, it removes it nicely from the rendered scene. You can also do style interpolation as well.
	 - Works well for real work images as well.
	 - Also really nicely interpretable as well.

# Victor Zhong: Reading to Learn

Its a good idea to read.

Instead of focussing on learning a specific environment or dataset, lets learn how to read so that we can learn how to learn on the fly.

If I give you a new board game, you don't have to re-learn the concepts, you instead use your skill of reading to fill in the blanks. Collecting lots of data on every single different problems is hard.

Is it possible to generalize via reading without supervised reading data?

  - Building symbolic variants of rich visual environments (TextWorld)
 - We tested whethaner we can read a manual to see if we can learn a policy that generalizes to new manuals.
 - Design a procedually set of games with a combinatorially large set of dynamics and accompanying text manuals.
 - Manual specifies the rules and then there is a goal. Manual is not specific to the instance, and only a subset is useful for the goal.
 - The key challenge is to read and cross-reference obserations from this particular game instance to words in the manual and generalize over new environments and new manuals.
 - The test manuals are rules are not seen during training. So you not only have environment shift but also dynamics shift.
 - At least on the baseline, you are able to generalize a little bit to new environments.

New benchmark task, SiLG. Incorporates GLL environments like RTFM, Messenger, Nethack.

TextWorld benchmark: Like alfred, but only with text.

Touchdown environment: navigating panoramas in Manhattan with long and complex natural language instructions. Still significant room for improvement vs human level performance.

When we do reinforcement learning on symbolic environments and abstract away the details of vision etc we observe faster convergenec and higher asymptotic performance. This is a promising approach - take a real environment, textify it, then solve it in the text world and transfer to the real world.

You can also take this approach and use it to label intermediate steps in demonstrations.

Turns out there is lots of data that fits this kind of "describe what the actors are doing" bill. Take for example tutorials or cooking demonstrations.

Once you have reading you can also combine this with search. So for example with NetHack, you're supposed to do certain things in throne rooms. Maybe you don't know that you're in a throne room, but you could do meta-learning, eg, look at the manual for text demonstrations of what to do and then transfer that into your policy.

Lots of other applications too. For example, reading a manual of medical diagnoses. Reading a manual of the UK tax code.

- SiLG: combined language grounding environments  
- using symbolic language as a surrogate for RL  
- take a real environment and textify it, then solve the problem in the text world. Eg solve rtfm in the text space if you can descrive the environment?  
- can we learn reading from unlabeled data? Eg, use unlabelled demonstrations to pretrain language grounding  
- dsitilling intermediate representations - inprovement over reward shaping and inverse rl  
- YOu can learn clip on a masive # of minecraft youtube and transcripts and learna reward function  
- can we read and design a curriculum?