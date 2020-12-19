# Option Critic Framework

## Motivation

How do you *discover* temporal abstractions?

Contributions:

 (1) Intra-option policy
 (2) Termination gradient
 (3) Train end-to-end

## Options Framework

Temporally extended actions:

$\omega \in \Omega: $(I_{\omega}, \pi_{\omega}, \beta_{\omega})$: Where $I_{\omega}$
is the "initiation set", $\pi$ is the option policy and $\beta_{\omega}$ is the termination condition

We assume that all options are available everywhere.

## Learning Options

Call-and-return: Pick an option $\omega$, follow the policy until termiantion,
as specified by $\beta_{\omega}$.

We have this function $U : \Omega \times S \to R$ function which
is the "option value function upon arrival"

$U(\omega, s') = (1 - \beta_{\omega}(s'))Q_{\Omega}(s', \omega) + \beta_{\omega(s')V_{\omega}(s')$

## Intra-option policy gradients

The gradient is proportional to the reward function for the entire problem.

The "goodness" of the termination function can only be evaluated by
which state we "terminate" into.

### Termination-gradient theorem

The gradient of the expected discounted return objective with respect to $\ve$
and the initial condition is ($s_1, \omega_0$):

$- \sum_{s', \omega} \mu_{\Omega} (s', \omega | s_1, \omega_0) \frac{\partial \beta_{\omega, \ve} (s')}{\partial \ve} A_{\Omega}(s', \omega)$

Where $\mu_{\Omega}$ is a discounted weighting of state option pairs, eg $\sum^\inf \gamma^tP(s_{t + 1}, \omega_t|s_1, \omega_0)$

)

## Option-Critic

Choose $\omega$ over an $\epsilon$-soft policy over options $\pi_{\Omega}(s)$

repeat:

 - Choose $a$ according to $\pi_{\omega, \theta}(a | s)$
 - Take action $a$

 Evaluate options:
  - Compute $\delta = r - Q_U(s, \omega, a)$ (advantage)
  - if $s'$ is non-terminal then add discounted termination-weighted reward to return
  - Set $Q_u(s, \omega, a)$ to current value plus the advantage

 Improve options:
  - Update parameters $\theta$ for the given option
  - Update parameters $\ve$ for the choice over options based on the
    advantage of choosing this option at this time.

 If $\beta_{\omega, \ve}$ terminates here, then choose a new $\omega$
