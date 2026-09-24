<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="Mohammad Mahdi Azarbeik. Offline reinforcement learning for critical care.">
</picture>

[Google Scholar](https://scholar.google.com/citations?user=tVbfK3AAAAAJ) &emsp; [LinkedIn](https://www.linkedin.com/in/mohammad-mahdi-azarbeik-757597201/) &emsp; [mm.azarbeik@gmail.com](mailto:mm.azarbeik@gmail.com)

I'm a PhD candidate in Computer Science at [TU Wien](https://www.tuwien.at/) (Institute of Logic and Computation) and a researcher at the [Medical University of Vienna](https://www.meduniwien.ac.at/), where I work with the Clinical Division of General Anaesthesia and Intensive Care Medicine.

I apply offline reinforcement learning to treatment decisions in the intensive care unit: learning policies from retrospective electronic health records, then evaluating them off-policy with the statistical care that clinical claims require.

## Dissertation

One offline RL pipeline, built on the [AI Clinician](https://doi.org/10.1038/s41591-018-0213-5) framework and extended across three clinical problems. The projects are ordered so that the reward signal becomes progressively more direct, from long-horizon patient outcomes in sepsis to measured drug concentrations in tacrolimus dosing.

| Domain | Decision | Status |
|---|---|---|
| Sepsis | IV fluid and vasopressor dosing | Published, 2026; second manuscript in preparation |
| Renal replacement therapy | When to initiate RRT | Published, 2025 |
| Tacrolimus | Dose selection | In progress |

## Publications

- **Learning and evaluating improved reinforcement learning-based policies for sepsis treatment on MIMIC-IV.** *Journal of Critical Care*, 2026.
- **Optimal timing for renal replacement therapy using reinforcement learning.** *Journal of Critical Care*, 2025.
- **TU Wien at SemEval-2024: Hallucination detection in LLMs.** *SemEval-2024*.
- **Augmenting inertial motion capture with SLAM using EKF and SRUKF.** *Measurement*, 2023.

The full list is on [Google Scholar](https://scholar.google.com/citations?user=tVbfK3AAAAAJ).

## Positions

- **Medical University of Vienna**, Researcher, Jul 2025 – present
- **Ludwig Boltzmann Institute for Digital Health and Patient Safety**, Researcher, Feb 2025 – Apr 2026
- **TU Wien**, University Assistant, Oct 2023 – Jan 2025. Taught Reinforcement Learning, Generative AI and LLMs, and Data-oriented Programming.

## Other work

Alongside clinical RL, I have worked on state estimation for robotics, fusing inertial motion capture with SLAM, and on hallucination detection in large language models. I also contribute to [EU-TRAINS](https://cordis.europa.eu/project/id/101130495), a Horizon Europe project, on AI-driven wearables for exercise performance monitoring.

## Tools

`Python` `PyTorch` `TensorFlow` `scikit-learn` `SQL` `PostgreSQL` `BigQuery` `GCP` `Docker` `Git` `MATLAB` `ROS`

## Get in touch

I'm interested in multi-agent RL for collaborative clinical decisions, what it takes to deploy clinical AI at the bedside, and federated learning on sensitive clinical data. If you work on any of these, or on offline RL in healthcare generally, write to me at [mm.azarbeik@gmail.com](mailto:mm.azarbeik@gmail.com).
