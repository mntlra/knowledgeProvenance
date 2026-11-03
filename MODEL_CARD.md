# Introducing Knowledge Provenance for Nanopublications (v1.0)

> **Research use only. Not a medical device.**
> This software was developed in the HEREDITARY project as a research prototype. It has not been assessed or certified under the EU Medical Device Regulation (EU) 2017/745. It must not be used to diagnose, treat, monitor or make any other decision about individual patients.

<!-- For demos and web applications, also show this line in the user interface:
"Research prototype of the HEREDITARY project. Not a medical device and not for clinical use. Do not enter personal or patient data." -->

## 1. Overview

| Field | Value |
|---|---|
| Name | Introducing Knowledge Provenance for Nanopublications |
| Version | 1.0 |
| Type | Software |
| Owner partner and contact | UNIPD, Laura Menotti, laura.menotti@unipd.it |
| License | MIT License (see LICENSE file) |
| Repository and DOI | https://github.com/mntlra/knowledgeProvenance |
| Release date | 08/12/2026 |
| Related task or deliverable | T4.1|
| How to cite | Menotti, L., Marchesin, S., Giachelle, F. et al. Provenance-driven nanopublications: representing source lineage and trust networks for multi-source assertions. Int J Digit Libr 26, 24 (2025). https://doi.org/10.1007/s00799-025-00431-x |

## 2. Intended use

**Primary intended use.** Research use

**Intended users.** Researchers, developers.

**Out-of-scope uses.** This release must not be used for
- clinical diagnosis, prognosis or treatment of individual patients;
- decisions about individuals, such as insurance, employment or access to care;
- re-identification of individuals or linkage with other data sources;
- populations, devices or data types not described in Section 3.

## 3. Data provenance

| Dataset | Source Publication | Type (public, synthetic, pseudonymized, anonymized) | Population (size, age, sex, country, condition) | Ethics approval or access conditions |
|---|---|---|---|---|
| CoreKB | Stefano Marchesin, Laura Menotti, Fabio Giachelle, Gianmaria Silvello, Omar Alonso, Building a large gene expression-cancer knowledge base with limited human annotations, Database, Volume 2023, 2023, baad061, https://doi.org/10.1093/database/baad061 | Public | Dataset constructed from PubMed articles | Publicly available |

This repository and the released files contain no personal data, pseudonymized records, identifiers or pseudonymization keys.

## 4. Method

- **Algorithm or architecture.** This repository contains the source code for creating nanopublications with Knowledge Provenance information and the code for serializing nanopublications representing CORE-KB's GCS facts.
- **Training setting.** N/A
- **Privacy techniques.** None (the used dataset is public)

## 5. Performance

- **Evaluation data.** N/A
- **Metrics and results.** N/A
- **Results by subgroup.** N/A

## 6. Known limitations and risks

- **Generalizability.** The library can be applied to any dataset.
- **Known biases and confounders.** N/A
- **Failure modes.** N/A
- **Privacy risks.** N/A

## 7. Responsible use and reporting

- **Terms of use.** Released under the MIT license. The software is intended for research use only and has not been validated for clinical applications.
- **Contact for misuse or vulnerability reports.** Laura Menotti, laura.menotti@unipd.it

## 8. Acknowledgement

Funded by the European Union under grant agreement No 101137074 (HEREDITARY). Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Health and Digital Executive Agency (HaDEA). Neither the European Union nor the granting authority can be held responsible for them.
