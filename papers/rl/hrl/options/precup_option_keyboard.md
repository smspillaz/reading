---
title: The Option Keyboard: Combining Skills in Reinforcement Learning.
venue: NeurIPS
pages: 13031-13041
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/nips/BarretoBHCAHTHM19
ee: https://proceedings.neurips.cc/paper/2019/hash/251c5ffd6b62cc21c446c963c76cf214-Abstract.html
url: https://dblp.org/rec/conf/nips/BarretoBHCAHTHM19
authors: ["Andr\u00e9 Barreto", "Diana Borsa", "Shaobo Hou", "Gheorghe Comanici", "Eser Ayg\u00fcn", "Philippe Hamel", "Daniel Toyama", "Jonathan J. Hunt", "Shibl Mourad", "David Silver", "Doina Precup"]
sync_version: 3
cite_key: conf/nips/BarretoBHCAHTHM19
---
# The Option Keyboard: Combining Skills in Reinforcement Learning

Combining skills: Define and manipulate them in the space of "pseudo-rewards". Show that
every deterministic option can be unambiguously represented as a cumulant defined
in an extended domain.

Show how to approximate options whose cumulants are linear combinations of the cumulants of known
options. So once you have learned options associated with a set of cumulants, you can instantaeneously
synetheize options induced by any linear combiation of them without any learning (zero-shot).

Idea: Imagine you have a piano keyboard. In traditional RL, you play each note for one unit of time
and one key at a time.

Skills: You can play a note for an arbitrary number of timesteps and can play many notes at once.

Eg - an agent that can both walk and grasp an object should be able to do both simultaneously.

How to combine the skills?
 - Do so in the distribution space?
 - Do so in the goal space


Cumulant: $c: S \times A \times A \to R$. $Q^{\pi}_c$ is the expected discounted sum of cumulant $c$
under policy $\pi$.

Successor Features: Given cumulants $c_1$, $c_2$, ..., $c_d$: for any $c = \sum_i w_i c_i$, then:

$Q^{\pi}_c(s, a) = E^{\pi} [\sum^{\infty} \gamma^k \sum^d w_i C_{i, t + k}|S_t = s, A_t = a] = \sum^d w_i Q^{\pi}_{c_i} (s, a)$,
where $C_{i, t} = c_i(S_t, A_t, R_t)$ - so once we have computed $Q^{\pi}_c$ for a given cumulant under policy $\pi$,
then we can evaluate $\pi$ under any cumulant in the set $C = \{ c = \sum_i w_i c_i | w \in R^d \}$.

Generalized Policy Improvement: The Q value for the general policy for cumulant $c$ is at least as large as
than the maximum Q value for any of the sub-policies.

## How to combine options

Defining a relationships between options and cumulants.

A cumulant induces a policy if $]pi$ is optimal for the MDP $(S, a, p, c_{\pi}, \gamma)$. It
always possible to have a cumulant inducing ap olicy, eg
$c_{\pi}(s, a, \cdot) = \begin{cases} 0 \text{if} a = \pi(s) \\ z \text{otherwise} \end{cases}$. If
$z < 0$, then $\pi$ is the only policy that gives you the maximum possible value.

There can be more than one cumulant that induces the same policy.

We can use any cumulant to refer to a policy.

To extend this to options, define cumulants in the space of histories, $\pi_o : H \to A$.

(Something about extended cumulants and terminations, etc, didn't really understand this).


## Synthesizing Options using GPE and GPI


$e_i$ (the extended cumulant) can be linearly combined, so for any $w \in R^d, e = \sum_i w_i e_i$ defines a new deterministic
option $o_e = \omega_{e_i}$.

Any combined option inherits its termination funtion from its constituents.

## Learning with combined options

The new ptions are fully determined by the vector of weights $w \in R^d$. This is an
interface between the RL algorithm and the environment - the algorithm selects
$w$ and hands it over to GPE and GPI and waits until the action returned by GPI
is the termination action.

Given a set of value functionw $Q_E$ and a vector of weihgts, execute
the actions selected by GPE and GPI until termination or a terminal state.

General algorithm for Option Keyboard

 - Given:
   - Current state $s$
   - Vector of weights $w$
   - Value functions Q
   - Discount rate $\gamma$

 - Repeat:
   - Pick an action from the policy using the weighted combination of value functions
    - If $a$ is not terminal then execute the action and accumulate the reward.