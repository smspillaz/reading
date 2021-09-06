# Generarting Images with Sparse Representations

The high dimensionality of images presents architecture and sampling-efficiency challenges for likelihood-based generative models. Previous approaches such as VQ-VAE use deep autoencoders to obtain compact representations, which are more practical as inputs for likelihood-based models. We present an alternative approach, inspired by common image compression methods like JPEG, and convert images to quantized discrete cosine transform (DCT) blocks, which are represented sparsely as a sequence of DCT channel, spatial location, and DCT coefficient triples. We propose a Transformer-based autoregressive architecture, which is trained to sequentially predict the conditional distribution of the next element in such sequences, and which scales effectively to high resolution images. On a range of image datasets, we demonstrate that our approach can generate high quality, diverse images, with sample metric scores competitive with state of the art methods. We additionally show that simple modifications to our method yield effective image colorization and super-resolution models.

[[nash_generating_images_sparse_representations.pdf]]

https://icml.cc/virtual/2021/oral/8792

Autoregressive Generative Image Models

 - Image GPT: Generate images one pixel at a time. Proceed in raster scan order. Train using log-likelihood.


Problem: Generating images of higher resolutions, we can do images of low resolution easily, but high resolution its much harder. The existing approach is VQ-VAE.

Idea: Leverage work done in JPEG - DCT based sparse representation.

(1) Convert image to YUV, 2x chroma subsampling (HVS is not sensitive to chroma channel)
(2) Split image into 8x8 blocks and apply DCT
(3) Flatten the blocks using Z-flag ordering
(4) Quantize high-frequency components. Resulting vectors contain many zeros.
(5) Reassemble into dense DCT image and sparsify it by splitting it into a coordinate list.

![[dct_transform_image.png]]

By conditioning on the low frequency components you an reconstruct the higher frequency components (superresolution).


## DCTransformer

Autoregressive sequence model - takes elements from a sprase DCT sequence and predicts the next DCT value. Don't pass entire image into transformer, split image into intput and target chunks.

![[dc_transformer_chunk_based_training.png]]

Nice thing about DCTransformer is that it predicts where to place content and then predits what content to add.