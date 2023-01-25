---
title: "Diffusion models as plug-and-play priors."
venue: "CoRR"
volume: "abs/2206.09012"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2206-09012"
doi: "10.48550/ARXIV.2206.09012"
ee: "https://doi.org/10.48550/arXiv.2206.09012"
url: "https://dblp.org/rec/journals/corr/abs-2206-09012"
authors: ["Alexandros Graikos", "Nikolay Malkin", "Nebojsa Jojic", "Dimitris Samaras"]
sync_version: 3
cite_key: "journals/corr/abs-2206-09012/Graikos/2022"
---

Pose a variational inference problem where the diffusion model is the prior. It is inference and not inference. Optimize the image wrt the diffusion model.


You can do also continuous relaxation if combinatorial problems. You can use whatever schedule you want. Eg you don't need to go from t = T to t = 0.


How well the diffusion model can denoise the image is an indicator of how good your energy function is.