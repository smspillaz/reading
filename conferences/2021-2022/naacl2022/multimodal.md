# Challenges in Multimodality
## Challenge 1: Representation

What's the right representation. Also think about:
 - Fusion
 - Coordination
 - Fission

### Fusion

Learn a joint representation that models cross-modal interactions between individual elements of different modalities.

Spectrum of fusion:
 - Simple fusion: Modalities are homogenous, fusion just means adding or concatenation
 - Heterogenous fusion

What is a very popular approach to fusion?
 - Unimodal encoder approach. As a first step, encode each separately and get a vector for each, then do fusion. This is "basic fusion"
 - How do you do the cross-modal interaction? We can study the univariate case first. Eg, linear regression: $z = w_0 + w_1 x_A + ... + w_n x_Z + (w_{n + 1}) (x_A \times x_B)$
 - **Additive fusion**: Late fusion
 - **Multiplicative fusion**: Bilinear fusion is usually a better approach: $w (x^T_A \cdot x_B)$. This is basically just attention right?
 - **Tensor fusion**: You add a $1$ to your vector is that you get both the unimodal and the bimodal interaction $Z = w([x_A,  1]^T \cdot [x_B, 1])$ . The weight matrix may end up quite large. But you can take the big weight matrix and decompose into two. This is **Low rank fusion**.
	 - See Efficient Low Rank Multimodal Fusion with Modality-specific Factors (ACL 2018) [[efficient_low_rank_multimodal_fusion_with_modality_specific_factors]]

What about higher-order interaction terms?

 * **Gated fusion**: Basically just $\sigma(x_A) + (1 - \sigma)(x_B)$ or attention.
 * **Nonlinear fusion**: Fusion and prediction are linked. What is happening in that model?
	 * Lets look at those nonlinear models - is there any way to project it into an additive representation? Can you take the nonlinear function as if it is two unimodal encoders and you simply added them at the end.
	 * You can project by integrating: $E_{x_B}[f_A(x_a, x_b)$ + $E_{x_A}[f_A(x_a, x_b)$ - $E_{x_A, x_B}[f_A(x_a, x_b)$
	 * If the additive projection is equal to nonlinear fusion, then the non-additive intertactions are not properly modelled. More on this in the quantification challenge.
 * There is an open-challenge of "complex fusion". Hetereogenous modalities - how do you bring them together?
	 * Very early fusion: Convolutional LSTM unit
	 * See "on the benefits of early fusion in multimodal representation learning" 2022

### Coordinated Representations

 - Learn multimodally contextualized representations that are coordinated through their cross-modal intetractions
 - You don't want to force everything to live in one space.
 - Learn a coordination function - the loss gives you the amount of coordination between modalities.
 - Eg, simply use cosine similarities.
 - Canonical Correlation Analysis - data could be correlated in different axes.
 - Deep Canonically Correlated Autoencoders (DCCAE)
	 - See "Wang et al On Deep Multi-view representation learning PMLR 2015" [[on_deep_multi_view_representation_learning_objectives_and_optimization]]
	 - Multi-view latent "intact space" - Multiview intact space learning.
		 - there is an "intact representation that is unchanged"
		 - You have an "original meaning"
 - Gated Coordination: $z_A = g_A(x_a, x_b) x_A$ $z_B = g_B(x_a, x_b) x_b$
 - Contrastive learning perspective: Paired data: Samples that are close should be close in latent space etc.
	 - Visual Semantical Embeddings
	 - CLIP [[clip_transferable_visual_models_from_natural_language_supervision]]


### Representation Fission

Modality-level fission: You have language and vision. We want to learn three representations
 - Language (information only in the language modality, eg, syntactic structure, vocab, morphology)
 - Vision (information only in the visual modality)
 - Language-vision (information in both modalities)

Some approaches: 
- Disentangle the representations into something that's only in language, only in vision or only in both.
	- Learn three three encoders - loss that says that you don't want overlap in between - you can add a generative loss - you add a decoder such that you can still reconstruct each modality individually.
- Information theory perspective
	- Conditional entropy vs mutual information loss.
	- See Tsai et al Self-Supervised Learning from a Multi-View perspective.


### Fine-grained fission

Fine-grained fission - a clustering approach.

See Hu et al Deep Multimodal Clustering for Unsupervised Audiovisual Learning (CVPR 2019) [[deep_multimodal_clustering_for_unsupervised_audiovisual_learning]]

Unimodal encoders: Localized activations for different objects.

Explore all possible ways that these local patches relate to each other.

Then you can cluster them and discover multiple audiovisual correspondences.

## Challenge 2: Alignment

 - Multiple objects
 - Tokenization

### Connections

Idnetifying connections between elements of multiple modalities.

 - Statistical (Association / Dependency)
 - Semantic (Corrrespondence by grounding, Relationship from a knowledgebase)

Connections can be conditional or unconditional.

Connections don't necessarily mean interaction.

Most language and vision studies primarily correspondence. Its very correspondence oriented. You have two modalities and you wanna learn a representation for both modalities such that you can study the common information.

Language grounding. You wanna learn words or phrases and you want to learn the link and identify those connections. This is very similar to information retrieval and learning coordinated representations.


## Aligned Representations

Modle all cross-modal connections and interactions to learn better representations

Each modality has connections. There can be cross-modal interactions.

Assumptions:
 - Each modality has segmented elements (eg, an image is a list of objects)
 - List of elements: These elements can be formulated as a list (with positional encoding)
 - Early fusion: Concatenated modalities ([[lxmert]] [[uniter]]).
 - All elements are connected
 - Same modelling method for all interactions (similarity kernels)

Pairwise cross-models - cross-modal attention block x n layers.

What does it mean to have a "directional transformer". You want to learn a representation of language that is visually contextualized. Eg, is there anything in the video which can help to better contextualize the word. What are the most correlated visual elements - then you can get visually correlated information.

Also many architectures use a residual connection - keep the representation of the word and just add to it.

See [[vilbert_pretraining_task_agnostic_visiolinguistic_representations_for_vision_and_language_tasks]], [[lxmert]]

### Graph networks

Aligned represnetaitons with graph networks: You have knowledge that there are a subset of connections and you can use that knowledge or discover a subset of connections - eg, not every word should be connected to every image. Define edge functions for different types of interactions (eg, correspondence, dependency, relationships). if you know already know the connections, you can transform it in a feedforward neural network.

Key technical challenge: Neighbourhood aggregation:

 - Averaging
 - Convolution
 - Attention

Learning the graph - make it with the least amount of connections - they have both the multimodal aspect and the structural aspect.

### Segmentation

How do you handle the ambiguity in segmentation?

Eg, signals, medical imaging.

One approach is to do "many-to-many" mapping. Look at all elements and do the mapping at the smallest granularity.

See eg Dynamic Time Warping. Exploring all the ways of doing that mapping.

Connectionist Temporal Classification:
 - Try to predict which phoneme is currently spoken.
 - You can add some prior knowledge about the way that phonemes are spoken to reconstruct the phonemes.

	Clustering approach:  (HUBERT). [[hubert_self_supervised_speech_representation_learning_by_masked_prediction_of_hidden_units]]

 - Look at all speech samples and do a cluster
 - Use the clusteres as a prediction task. Try to train a transformer in such a way that if I mask something, I can still predict which cluster it came from. You're almost learning a mini-dictionary.

## Challenge 3: Reasoning

 - Combining knowledge, usually throuhg multiple inferential steps, exploiting the multimodal alignment and problem structure
 - Usually just involves stacking more layers
 - But you could have "socratic models" which use words as an intermediate representation
 - External knowledge? How to integrate this?


Sub-challenges:
 - Structure modelling
 - Intermediate concepts
 - Inference paradigm
 - External Knowledge


Recall rerepsentation fusion - in a single step of inference.

Reasoning goes beyond the simple case of fusion. It should be more explicitly interpretable and robust so that you get better guarantees.

### Structure modelling

Defining or learning relationships over which composition occurrs

 - Single-step
 - Temporal reasoning (assume that multimodal data comes in the form of sequences.)
	 - Apply a memory mechanism - keep track of it throughout multiple timesteps throughout multiple sequences.
	 - Use the multimodal memory to discover interactions across the data.
	 - Many choices - RNN, LSTM, Tranfromer, key-value memory, episodic memory.
	- Rajagoapaln et al, Extending LSTM for Multi-view Structured Learning.
- Temporal structure in multi-view sequences
	- **Writing into memory** - use a coordination function - measure representation that you currently see and similarity between that and what is in the memory. More similar representations should be stored, more dissimilar functions should not be stored.
	- **Composing:** How can I derive the process of composing - do some weighted function / gating to determine what to keep from the previous timestep and what to add from current timestep.
	- **Reading**: Learn a summary function over the memory.
- Hierarchical structure modelling
	- Leverage syntatic structure of language (See Learning to Compose and Reason with Language Tree Strucutres for Visual Grounding 2019) [[learning_to_compose_and_reason_language_tree_structures_for_visual_grounding]]
	- Basically, parse statement into parse tree, then do object detection and match images to nodes in the tree. Then you can learn what is related. You can compose nodes in the image according to the edges in the tree.
- Interactive Structure
	- Structure defined through reinforcement
	- Integrates multimodality into RL framework
	- "A survey of reinforcment learnign informed by natural language, IJCAI 2019" [[survey_rl_informed_by_natural_language]].
	- Eg,
		- Language conditioned RL (the goal is given as the language)
		- Language assisted RL (you are given a wiki, it is part of the state)
	- There's a full multimodal RL lecture series from CMU
	- key ideas are still the same - action taken at previous timesteps affect future states. You learn aligned representations that take into account time and action trajectory.
	- RL policy seeks to maximize cumulative reward
- Structure Discovery
	- Structure is fully learned from optimization and data. We don't assume that we have domain knowledge about the structure. We just try to learn it through optimization and data.
		- Define basic representation building blocks (layer norm, conv, self-attention)
		- Define basic fusion blocks (concat fuse, attention fuse, add fuse)
		- Automatically search for composition using NAS
	- See MUFASA: Multimodal fusion architecture search for electronic health records AAAI 2021
	- Nice, but slow.
- Neuro-symbolic concepts
	- Hand-crafted concepts based on domain knowledge
	- Attention maps (attend to red shapes in the image)
	- Attend to circles
	- Then do logical composition with interpretable output concepts. Combine intersection.
	- Neural Module Networks [[deep_compositional_question_answering_with_neural_module_networks]]

## Inference Paradigm

How increasingly abstract concepts are inferred from multimodal evidences.

Recall representation fusion.

Potential issues: 
- Spurious correlations
- Not robust to targetd manipulations
- Lack of interpretability/control

Towards explicit inference paradigms:
	- Logical inference. Given premises inferred from multimodal evidence, how can one derive logical conclusions? See VQA-LOL (Visual Question Answering under the Lens of Logic 2020) [[vqa_lol_visual_question_answering_through_the_lens_of_logic]]
		- Basic premises
		- "Is the man NOT wearing shoes AND is there beer?" (logical connectives)
		- "Is there beer AND is there a WINE GLASS" (models are not robust to adversarial antonyms)
		- How to integrate logical inference
		- We know that the models are resonably successful at modelling the basic premises. We could parameterize the model by explicitly modelling these connections, such as AND. We can use a "soft-and" operator so that we can do backprop.
		- You can extend this to other OR, NOT
	- Causal Inference: How can one determine the actual causal effect of a variable in a larger system?
		- This is a big challenge, there is no free lunch unless you know something about the underlying causal process in your data.
		- See towards Causal VQA: revealing and Reducing Spurious Correlations by Invariant and Covariant Semantic Editing (CVPR 2020 Agarwal) [[towards_causal_vqa_revealing_and_reducing_spurious_correlation_by_invariant_and_covariant_semantic_editing]]
		- "How many zebras are there in the picture"
		- Treatment varaible: zebras
		- Causal inference by making targeted changes on datapoint. Eg, if you remove one zebra from the image and ask again, the model says that there are still two.
		- Intereventional conditional: $p(y|\text{do}(\text{zebras} = 1))$
		- Causal VQA: Does my multimodal model capture causation or correlation
		- Eg, what color is the balloon?
			- If the image has pink umbrellas the model might say "pink"
			- You could remove the umbrellas and see if the result changes.
			- You can intervene on the confounding variable.
		- How can you make them more robust to spruous correlations.
		- Simple approach: Collect datasets where you have interventions. Can I explicitly model the fact that my model should be covariant to the changes I make to the image (by changing relavant details)
		- You want the model to be invariant to changes in irrelevant details.

### Domain knowledge

Are there knowledge in other forms that we can use, eg, knowledge graphs taht we can use to model the reasoning paradigm.

- Eg, "What kind of board is this" - requires knowledge of water sportsa and sports equipment.
- How can we add this knowledge into the reasoning process?
	- Wikidata.
	- Knowledge graphs can tell you affordances, attributes.
	- Concepts etc are interpretable, mulit-step inference, and composable in the sense that they are graph-based.


### Open Challenges

 - Multi-step structure and causal inference?
 - Concepts - interpretable and differentiable representations
 - Composition
 - Knowledge
 - Probing pretrained models for reasoning capabilities

## Challenge 4: Generation
- Generating modalities

Paradigm 1: Summarization: Learning a generative process to produce raw modalities that refelcts cross modal interactions, structure and coherence
Paradigm 2: Translation: Translating to some other modality
Paradigm 3: Creation: creating more content than you started with

### Translation

Decoding high-dimensional multimodal data

Exemplar and Generative processes. With a new set of data coming in I can use the generative process I learned before.

Sub-challenge: Translation: DALL-E

 - An armchair in the shape of an avocado: Still generate realsitic images 
 [[dall_e]] [[dall_e_2_hierarhical_text_conditioned_image_generation_with_clip_latents]].
 - Discrete VAE
 - Autoregressive trnasformer. Learn a model that captures the correpondences between images and text. Take language, encode it and use that to predict a set of discrete tokens that you had through image encoders.
 - Take the predicted image tokens to generate the actual images.
 - You're trying to coordinate your content.

### Summarization

 - Summarize high-dimensional data
 - Eg, How2 dataset - long transcript but short summary.
 - Complementary cross-modal interactions. Fusion via joint representation and capture complementary cross-modal interactions.

### Creation

Simultaneously generating multiple modalities to increase information concent while maintaining coherence within and across modalities.

Generate in each modality more information content.

Two constraints:
 - Still respect cross-modal interactions - whatever you generate in the video should correspond to the images and correspond to what you here in the audio
 - Still respect temporal / causal / logical structure.

Some initial attempts: factorized generation
 - Learning Factorized Multimodal Representations ICLR 2019 [[learning_factorized_multimodal_representations]]
- **This enables us to generate more content than we started with.**
- Create more multimodal data that is realistic.
- Example, SVHN / MNIST style transfer.

### Summary

 - Summarization
 - Translation
 - Creation


### Open challenges

 - Beyond text / images / video: audio, sets / graphs etc.
 - Translation beyond descriptive text and images
 - Creation: fully multimodal generation with cross-modal coherence  + within modality consistency
 - Ethical concerns
 - 

See -
 - PULSE
 - Extracting Training data from Large Language Models (USENIX 2021)
 - The woamn Worked as a Babysitter: on Biases in Language Generation (EMNLP 2019)

## Challenge 5: Transferrence

 - Transfer knowledge between modalitieis, usually to help the target modality

Sub-challenges:
 - Transferring directly (FiLM)
 - Co-learning via representation. A modality is used during training to help and not at test time.

### Transfer via Pretrained Models

 - 0-shot VQA
 - Adapter and pretrained model -> answer the visual query
 - 1-shot VQA: Transfer via prefix tuning. Who invented this thing? Try to use external knowledge that is sorted. Eg, prompting to amplify stored knowledge.
 - We don't know what the knowledge is.
 - Multimodal Few-Shot learning with Frozen Language Models NeurIPS 2021.
 - Transfer across partially observable modalities: HighMMT (High MMT: Towards Modality and Task Generalization for High Modality Representation Learning 2022). [[highmmt_towards_modality_and_task_generation_for_high_modality_representation_learning]]
 - Use task-specific classifiers using multi-task learning.
 - We assume that everything can be shored across modalitiesd and tasks.
 - Assumptions
	 - All modalities can be represented as sequences
	 - Dimensions can be perfectly captures by modality specific embeddings
	 - Cross-modal connections and interactions are shared ac ross modalities and tasks

### Co-learning via Representation

Representation co-ordination for zero-shot visual classification

Use the word-embedding space.

New test image from unknown image class. Only images are used at test-time 

Multi-modal co-learning > language only training.

Foundations of multimodal co-learning Information Fusion 2020. Zadeh et al.

### Co-learning via Generation

Bimodal translations

Both modalities required at test time.

See Found in Translation: Learning Robust Joint Representatiosn vai Cyclic Translations between Modailities (AAAI 2019). [[found_in_translation_learning_robust_joint_representations_by_cyclic_translations_between_modalities]]

Only language modality used at test time.

One big issue: How do you ensure that both modalities are being used? Predict the secondary modality from the first one, then predict the first modality from the predictions of the second one.

Use cross-modal translation during training, then at test time you just use the language.

Masked language mdoelling: Vokenization: Improving Language Understanding with Contextualized Visual-Grounded Supervision (Tan and Bansal 2020).

Only text used at test time. This works much better than just predicting language tokens during training.

Many more dimensions of transfer. See:
 - Perceiver [[perceiver_io]]
 - MultiModal ViT-BERT [[mm_vit_multi_modal_video_transformer_for_compressed_video_action_recognition]]
 - PolyViT [[polyvit_co_training_vision_transformers_on_images_videos_and_audio]]
 - UniT, VLBERT,
 - ViLBERT
 - VL-T5
 - VATT [[vatt_transformers_for_multimodal_self_supervised_learning_from_raw_video_audio_and_text]]
 - FLAVA [[flava_a_foundational_language_and_vision_alignment_model]]
 - HighMMT, Gato ([[gato_a_generalist_agent]])

Open-challenges:
 - Low resource
 - Beyond language and vision
 - Settings where SOTA unimodal encoders are not deep learning (tabular)
 - Complexity in data, modelling and training
 - Interpretability (next step)

## Challenge 6: Quantification

 - Empirical and theoretical study to better understand hetereogeneity

Two key areas:

1. Modalities are hetereogeneous. This is what makes it difficult.
2. Modalities are connected with each other and interact.
3. Learning: We're introducing more data and bigger models - can we understand the challenges in the learning process.

## Heterogeneity

Modality biases: Unimodal bias and modality collapse:
	Characterizing and overcoming the greedy nature of learning in multi-modal deep nerual networks Wu et al 2022 [[characterizing_and_overcoming_the_greedy_nature_of_learning_in_multi_modal_deep_neural_networks]]
	Javaloy et al Mitigating Modality Collapse in Multimodal VAEs via Impartial Optimization ICML 2022 [[mitigating_modality_collapse_in_multimodal_vaes_via_impartial_optimization]]
	Goyal et al: Making the V in VQA matter: Elevating the role of image understanding in visual question answering: CVPR 2017 [[making_the_v_in_vqa_matter_elevating_the_role_of_image_understanding_in_visual_question_answering]]


VQA modals often answer the question without looking at the image. Eg "what color is the banana". Bananas are almost always yellow, so you can just ignore the image.

How to deal with this?
 - Balancing modalities in the data
 - Balancing training: Re-train biased models to balance their prediction logits.

## Fairness and Social Biases

 - Image captioning models capture spurious correlations between gender and genertaed actions.
- Eg, image of a woman sitting at a computer -> "a man sitting at a computer". If you look at the heatmap of activations it is mostly looking at the computer.
- Cross-modal interactions worsen socail bases (Srinivasan and Bisk: Biases compound in pre-trained vision and language models NAACL 2022)
- Biases tend to be amplified by looking at the image. Visual modalities make the model more confident in reinforcing stereotypes.


## Noise topologies and robustness

Modalities are different because there are different ways that they see noise.

There are modality specific robustness issues.

Then there is multimodal robustness issues.

Strong tradeoff between performance and robustness. Models that perform well tend to lose more accuracy as more imperfections are introduced.

Liant et al: Multibench: Multiscale benchmarks for multimodal representation learning (NeurIPS 2021).

Noise topologies and robustness
 - Multimodal Deep Learning (Ngiam ICML 2011)
 - Srivastava and Salakhutdinov: Multimodal learning with deep boltzmann machines JMLR 2014
 - Tran et al Missing modalities imputation via cascaded residual autoencoder CVPR 2017
 - Found in translation: Learning robust joint representaitons via cyclic...


## Cross-modal interactions

Modalities are connected, which elements are connected and why?

 - Association
 - Dependency
 - Correspondence
 - Relationships

"Does my multimodal model learn cross-modal interactions? Its harder to tell than you might think!" (EMNLP 2020)

Can we quantify individual cross-modal interactions? Any non-additive interaction must contribute a second order gradient.

"MultiViz: An Analysis Benchmark for Visualizing and Understanding multimodal models" 2022 [[multiviz_an_analysis_benchmark_for_visualizing_and_understanding_multimodal_models]]

$f$ exhibits interactions between 2 features $x_A$ and $x_B$ iff ....

Eg, with CLEVER: The other small shiny thing that is the same shape as the tiny yellow shiny object is what color: You take the gradient of the thing that you're interested in vs the gradient of everything else.

You can analyze these models to see how much they pick up the corresponding cross-modal interactions.

You can also examine unimodal importance.
 - M2Lens: Visualizing and Explaining Multimodal Models for Sentiment Analysis (Wang et al 2021). [[m2lens_visualizing_and_explaining_multimodal_models_for_sentiment_analysis]]
 - If the norm for one vector is greater tahn the other, you have dominande
 - If the norms dot product is > 0 then you have complementary encodings
 - If the norms dot product < 0 then you have conflicting encodings.

Also some recent work in visualizing multi-modal transformers
 - VL-InterpreT: An interactive visualization tool for interpreting vision-language transformers (CVPR 2022). [[vl_interpret_an_interactive_visualization_tool_for_interpreting_vision_language_transformers]]

#### Open Challenges

 - How can we evaluate the success of interpreting cross-modal interactions?
 - Real-word datasets and models do not have cross modal interactions?
 - Model-simuoation - can humans reproduce model predictions with high accuracy and agreement? If the model is fully transparent, you can give it to a human and let the human simulate the model's predictions, in terms of both the correct and incorrect predictions
 - Model debugging - can humans look at a cross-modal interaction and see where the model went wrong? Can you find the bugs and fix the bugs?
 - Faithfulness - do explanations accuracyly reflect the model's internal mechanics
 - Usefulness - too much information
 - Disagreement: different interpretation methods give different explanations
 - Evaluations: how to best evaluate interpretation methods

## Multimodal Learning Process

How can we understand the actual learning process and optimization challenges that come with multimodal learning.

Adding more modalities should always help? Sometimes adding more modalities actually *hurts* performance.
 - See Wang et al : What makes training multi-modal classification networks hard? (CVPR 2022)

Two explanations:
 - more prone to overfitting due to increased complexities
 - different rates of convergence. One modalitiy might overfit while the other one is generalizing

Can you compute the ratio of generalization to overfitting for each modality and then re-balance?

We have to train the multimodal model and also unimodal models.

Reweight loss according to unimodal OGR values.

See an new survey paper: Fundamental of Multimodal ML: A taxonomy

See also Full Multimodal ML Course at CMU. Also an advanced topics course on multi-modal.