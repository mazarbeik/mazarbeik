<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="Mohammad Mahdi Azarbeik. PhD candidate, TU Wien; researcher, Medical University of Vienna. Machine learning for decisions under uncertainty. Research interests: offline reinforcement learning, off-policy evaluation, clinical decision support, large language models, state estimation.">
</picture>

<p>
<a href="https://mazarbeik.github.io/azarbeik/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-website-dark.svg"><img src="assets/btn-website-light.svg" height="38" alt="Website"></picture></a>
<a href="https://scholar.google.com/citations?user=tVbfK3AAAAAJ"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-scholar-dark.svg"><img src="assets/btn-scholar-light.svg" height="38" alt="Google Scholar"></picture></a>
<a href="https://orcid.org/0000-0003-0780-4928"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-orcid-dark.svg"><img src="assets/btn-orcid-light.svg" height="38" alt="ORCID"></picture></a>
<a href="https://www.linkedin.com/in/mohammad-mahdi-azarbeik-757597201/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-linkedin-dark.svg"><img src="assets/btn-linkedin-light.svg" height="38" alt="LinkedIn"></picture></a>
<a href="mailto:mm.azarbeik@gmail.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-email-dark.svg"><img src="assets/btn-email-light.svg" height="38" alt="Email mm.azarbeik@gmail.com"></picture></a>
<a href="https://mazarbeik.github.io/azarbeik/cv/Azarbeik_CV.pdf"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-cv-dark.svg"><img src="assets/btn-cv-light.svg" height="38" alt="CV (PDF)"></picture></a>
</p>

I'm Mahdi, a machine-learning researcher in Vienna. I'm a researcher at the [Medical University of Vienna](https://www.meduniwien.ac.at/) and a PhD candidate in Computer Science at [TU Wien](https://www.tuwien.at/en/). My background is in mechanical engineering, where I worked on state estimation and sensor fusion; the common thread through my work since is quantifying how reliable an estimate is.

## Research

My work spans three fields, shown here in the order I came to them. Across all three, the aim is to learn from imperfect data and to quantify how far the results can be trusted.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/fields-dark.svg">
  <img src="assets/fields-light.svg" width="100%" alt="One signal line through three fields. 01, Sensing and estimation (M.Sc., Sharif University of Technology): many noisy measurements, one estimate. 02, Learning systems (PhD, TU Wien): one state, many possible decisions. 03, Clinical decision support (Medical University of Vienna): vital signs, decided step by step.">
</picture>

### 01 · Sensing & estimation

Kalman filtering and sensor fusion that turn low-cost, noisy sensor signals into reliable estimates of motion, together with their remaining uncertainty.

<table>
<tr>
<td width="300"><a href="https://mazarbeik.github.io/azarbeik/#motion"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-motion-dark.svg"><img src="assets/project-motion-light.svg" width="300" alt="Schematic: an arm with two inertial sensors, and the estimated wrist path with its uncertainty ellipses."></picture></a></td>
<td>

**Inertial motion capture with SLAM**<br>
<sub>2023 · First author</sub>

Fusing drifting inertial sensors with camera-based SLAM in extended and square-root unscented Kalman filters to track a human arm, validated against an optical motion-capture system.

Journal article in *Measurement* (2023), with an open dataset and a graphical-abstract video.<br>
[DOI](https://doi.org/10.1016/j.measurement.2023.113690) · [arXiv](https://arxiv.org/abs/2302.08294) · [Dataset](https://doi.org/10.21227/yaxm-6273) · [Video (MP4)](https://mazarbeik.github.io/azarbeik/assets/media/measurement-graphical-abstract.mp4)

</td>
</tr>
<tr>
<td width="300"><a href="https://mazarbeik.github.io/azarbeik/#eu-trains"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-wear-dark.svg"><img src="assets/project-wear-light.svg" width="300" alt="Schematic: a wrist-worn sensor streams a pulse waveform into a network."></picture></a></td>
<td>

**AI-enabled wearables: EU-TRAINS**<br>
<sub>2025–2026 · Horizon Europe</sub>

Lead researcher for the Ludwig Boltzmann Institute for Digital Health and Patient Safety on a Horizon Europe project developing AI-enabled wearables for multisport training and remote healthcare.

Funded by Horizon Europe, grant agreement 101130495.<br>
[CORDIS](https://cordis.europa.eu/project/id/101130495) · [Project site](https://eu-trains.eu/)

</td>
</tr>
</table>

### 02 · Learning systems

Offline reinforcement learning, which learns decision policies from logged data rather than by trial and error, and off-policy evaluation of those policies; these are the methods behind the clinical work in 03. Also hallucination detection in large language models.

<table>
<tr>
<td width="300"><a href="https://mazarbeik.github.io/azarbeik/#hallucination"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-halluc-dark.svg"><img src="assets/project-halluc-light.svg" width="300" alt="Schematic: lines of generated text are scanned and two spans are flagged as hallucinations."></picture></a></td>
<td>

**Hallucination detection in language models**<br>
<sub>2024 · TU Wien team</sub>

Detecting hallucinations in language-model outputs (SemEval-2024 Task 6) with an ensemble that combines black-box detectors and detectors reading the model's internal activations.

Ranked 3rd in the model-aware track and 8th in the model-agnostic track; paper in the SemEval-2024 proceedings (ACL).<br>
[Paper (PDF)](https://mazarbeik.github.io/azarbeik/papers/arzt-azarbeik-2024-semeval-hallucination.pdf) · [DOI](https://doi.org/10.18653/v1/2024.semeval-1.173) · [Team code](https://github.com/kleines-gespenst/shroom-hackathon)

</td>
</tr>
</table>

### 03 · Clinical decision support

Treatment strategies for sepsis and renal replacement therapy, learned from intensive-care records, evaluated with several off-policy methods and reviewed with physicians for clinical plausibility.

<table>
<tr>
<td width="300"><a href="https://mazarbeik.github.io/azarbeik/#rrt"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-rrt-dark.svg"><img src="assets/project-rrt-light.svg" width="300" alt="Schematic: a marker of kidney function rising over 24 hours in 4-hour steps, and the question of when to start renal replacement therapy."></picture></a></td>
<td>

**Timing renal replacement therapy**<br>
<sub>2024–2025 · Co-author</sub>

Learning when to start renal replacement therapy in critically ill patients with acute kidney injury, using reinforcement learning with high-confidence off-policy evaluation.

Conference abstract in *Journal of Critical Care* (ICCAI 2024); preprint on Research Square (2025).<br>
[Abstract](https://doi.org/10.1016/j.jcrc.2024.154964) · [Preprint](https://doi.org/10.21203/rs.3.rs-6243566/v1)

</td>
</tr>
<tr>
<td width="300"><a href="https://mazarbeik.github.io/azarbeik/#sepsis"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-sepsis-dark.svg"><img src="assets/project-sepsis-light.svg" width="300" alt="Schematic: the path clinicians took through a grid of patient states, and the one a learned policy would take."></picture></a></td>
<td>

**Treatment strategies for sepsis**<br>
<sub>2025 · First author</sub>

Learning fluid and vasopressor dosing policies for sepsis from intensive-care records (MIMIC-IV), and comparing off-policy evaluation methods, whose choice can change which policy appears best.

Conference abstract in *Journal of Critical Care* (ICCAI 2025, Vienna); full paper in preparation.<br>
[Abstract](https://doi.org/10.1016/j.jcrc.2025.155385)

</td>
</tr>
</table>

## Publications

- `2026` **Learning and evaluating improved reinforcement learning-based policies for sepsis treatment on MIMIC-IV**<br>
  **M. M. Azarbeik**, L. Kapral, R. Weiss, C. Heitzinger, O. Kimberger. *Journal of Critical Care* 92, 155385. Conference abstract, ICCAI 2025. [DOI](https://doi.org/10.1016/j.jcrc.2025.155385)
- `2025` **Optimized renal replacement therapy decisions in intensive care: A reinforcement learning approach**<br>
  L. Kapral, R. Bologheanu, **M. M. Azarbeik**, A. Bilir, R. Weiss, S. Bartos, S. Schaller, C. Heitzinger, E. Schaden, O. Kimberger. *Research Square*. Preprint. [DOI](https://doi.org/10.21203/rs.3.rs-6243566/v1)
- `2025` **Optimal timing for renal replacement therapy in critically ill patients using reinforcement learning algorithms**<br>
  L. Kapral, **M. M. Azarbeik**, R. Weiss, R. Bologheanu, C. Heitzinger, O. Kimberger. *Journal of Critical Care* 86, 154964. Conference abstract, ICCAI 2024. [DOI](https://doi.org/10.1016/j.jcrc.2024.154964)
- `2024` **TU Wien at SemEval-2024 Task 6: Unifying model-agnostic and model-aware techniques for hallucination detection**<br>
  V. Arzt, **M. M. Azarbeik**, I. Lasy, T. Kerl, G. Recski. *Proceedings of the 18th International Workshop on Semantic Evaluation (SemEval-2024)*, ACL, pp. 1183–1196. Workshop paper. [PDF](https://mazarbeik.github.io/azarbeik/papers/arzt-azarbeik-2024-semeval-hallucination.pdf) · [DOI](https://doi.org/10.18653/v1/2024.semeval-1.173) · [Code](https://github.com/kleines-gespenst/shroom-hackathon)
- `2023` **Augmenting inertial motion capture with SLAM using EKF and SRUKF data fusion algorithms**<br>
  **M. M. Azarbeik**, H. Razavi, K. Merat, H. Salarieh. *Measurement* 222, 113690. Journal article. [DOI](https://doi.org/10.1016/j.measurement.2023.113690) · [arXiv](https://arxiv.org/abs/2302.08294) · [Data](https://doi.org/10.21227/yaxm-6273)
- `2022` **An overview of the design experience and group analysis of a spinning ride from the perspective of engineering education**<br>
  A. Meghdari, S. M. J. Zolanvari, H. Izanlo, M. S. Tohidi Nafe, **M. M. Azarbeik**, et al. *Iranian Journal of Engineering Education* 24(94), pp. 39–60. Journal article, in Persian. [DOI](https://doi.org/10.22047/ijee.2022.321010.1874)

Also listed on [Google Scholar](https://scholar.google.com/citations?user=tVbfK3AAAAAJ) and [ORCID](https://orcid.org/0000-0003-0780-4928).

## Experience

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/path-dark.svg">
  <img src="assets/path-light.svg" width="100%" alt="Path from Tehran to Vienna. 2016 to 2020: B.Sc., Mechanical Engineering, K. N. Toosi University of Technology. 2020 to 2023: M.Sc., Mechanical Engineering, Sharif University of Technology, state estimation and sensor fusion. Since 2023: PhD candidate in Computer Science (Informatics), TU Wien, and University Assistant from 2023 to 2025, on offline reinforcement learning, off-policy evaluation and language models. February 2025 to April 2026: Researcher, EU-TRAINS, Ludwig Boltzmann Institute for Digital Health and Patient Safety. Since July 2025: Researcher, Medical University of Vienna, anaesthesia and intensive care medicine.">
</picture>

**Teaching assistant.** Reinforcement Learning, Generative AI and Data-oriented Programming Paradigms at TU Wien; Numerical Analysis at K. N. Toosi University of Technology.

**Peer review.** *PLOS Digital Health*, *Measurement*, *Journal of Intelligent & Robotic Systems* and *IEEE Sensors Journal*.

**Toolkit.** `Python` `PyTorch` `TensorFlow` `scikit-learn` `SQL` `BigQuery` `PostgreSQL` `Google Cloud` `Git` `MIMIC-IV` `ViennaAIdb` `MATLAB` `ROS` `Arduino`

## Next

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/next-dark.svg">
  <img src="assets/next-light.svg" width="100%" alt="Next research directions: 01, multi-agent reinforcement learning for collaborative clinical decisions; 02, what it takes to bring clinical AI to the bedside; 03, federated learning on sensitive clinical data.">
</picture>

I'm glad to discuss research on reinforcement learning in healthcare, clinical decision support and the evaluation of clinical AI. Email is the best way to reach me: [mm.azarbeik@gmail.com](mailto:mm.azarbeik@gmail.com).
