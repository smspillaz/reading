# On the Transfer of Disentangled Representations in Realistic Settings

https://iclr.cc/virtual/2021/poster/2681

Motivation: Path towards disentangled representation learning in more challenging realistic settings

New realistic dataset where the factors have:
 - Correlations
 - Occlusions
 - Sim-to-real
 - More-complex and realistic


This allows us to evaluate sim2real transfer.

Disentanglement methods based on VAE. Using a form of weak supervision we can realiably learn disentangled representations.

![[realistic_settings_disentanglement_vae_training_colors.png]]

OOD Generalization on Downstream Tasks:
 - Fix one factor of variation
 - Pick the cube color, pick a set of colors to be held out
 - Train representation on a representation that does not contain cubes of the held out colors
 - Train downstream tasks on some of the VAE colors, but not all.
 - OOD1: VAE has seen them, downstream task has not
 - OOD2: VAE has not seen them.
 
 Task: Given representation x, predict true value of non-OOD factors.
 
 OOD1 Generalization: Very high disentanglement, lower generalization error.
 
 OOD2: Generalization: Disentanglement plays a minor role when representation function goes OOD.
 
 Input noise vs OOD2: Adding noise at training time significantly improves the OOD2 case.