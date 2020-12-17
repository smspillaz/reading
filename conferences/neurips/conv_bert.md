# ConvBERT: Improving BERT with Span Based Dyanmic Convolution

Pretrain, then finetune.

Some studies use compression and knowledge distillation (tinyBERT, ELECTRA)

Transfer: Self-attention and feed-forward model. BERT needs much more training
than Resnet.

Observation: large proportion of global attention head actually learns local
dependencies (computational redundancy).

 - Answer: convolution - replace some of the global attention heads
 - span based dynamic convolution
   - generate kernel from span of input tokens - generate different kernel
     for same token in different context

![[img/conv_bert.png]]
 
   - use convolution on the input to generate the key vector
   - use linear layer to generate query vector
   - Take QK and put through linear layer, then softmax
	   - Then the result is a "lightweight convolution"
	   - Modulate with value and pass through linear feed-forward

Mixed-attention block:

![[img/conv_bert_mixed_attention.png.png]]

 - Combines self-attention and span-based attention
 - self-attention has lower rank. span attention works on spans

Does a little better on GLUE compared to other convolutional methods. Also does a little better than bert-base.

Disentangles the attention types - self attention maps concentrate more on the global attention parts, rather than the local span

Which kernel size to use? A kernel size of 9 seems good, otherwise receptive field will be too large

