---
title: "Guided-TTS: A Diffusion Model for Text-to-Speech via Classifier Guidance."
venue: "ICML"
pages: "11119-11133"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/KimKY22"
ee: "https://proceedings.mlr.press/v162/kim22d.html"
url: "https://dblp.org/rec/conf/icml/KimKY22"
authors: ["Heeseung Kim", "Sungwon Kim", "Sungroh Yoon"]
sync_version: 3
cite_key: "conf/icml/KimKY22"
---
The general idea behind this paper is to use classifier guided diffusion to generate speech.

In speech you have STT and TTS. Instead of making a complicated TTS pipeline, instead just learn to generate any old random speech and guide the diffusion process to generate speech which classifies to what you want out of your STT.

The nice thing about this is that you can train on untranscribed speech. Eg, your text is not tied to a particular speaker.

There are four modules to guided-TTS:

 - Unconditional DDPM
 - Phoneme classifier
 - Duration predictor
 - Speaker encoder

The unconditional DDPM generates a mel-spectrogram image with a U-net, starting from noise.

To do classifier guidence you use a frame-wise phoneme classifier. Basically "we want this spectrogram to classify to this phoneme".

Duration predictor: predicts how long in speech a given token will be. You need this because you need to know how much "speech" you want your DDPM to generate.

Speaker encoder: Takes a mel-spectromgram and gives you an encoding of which speaker it is. You need this to ensure that you have a consistent speaker (eg, during the backward process, guide diffusion such that it comes from the same speaker).


Norm-based guidance: Scale the norm of the classifier gradient in roportion to the norm of the score in order to prevent the gradient from being insignificant as the score goes up.