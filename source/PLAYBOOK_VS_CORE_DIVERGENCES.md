# Playbook JSON vs AI RMF Core: divergence inventory

Cross-checked 2026-05-10 against AI RMF Core HTML rendering at
https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ and the
Playbook structured export at https://airc.nist.gov/docs/playbook.json.

## Summary

- 41 of 72 subcategories drift (56.9%)
- GOVERN: 9 of 19 subcategories drift
- MAP: 11 of 18 subcategories drift
- MEASURE: 14 of 22 subcategories drift
- MANAGE: 7 of 13 subcategories drift

Of these:
- 1 typo
- 1 semantic divergence
- 7 capitalisation-only (function name MAP vs map etc.)
- 32 minor wording / punctuation

## Methodology

- Source A: AI RMF Playbook structured export, https://airc.nist.gov/docs/playbook.json (fetched 2026-05-10).
- Source B: AI RMF Core HTML rendering at https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ (fetched 2026-05-10), Tables 1-4.
- For each of the 72 subcategories, the Playbook `description` field was compared byte-for-byte against the corresponding Core text in the HTML table cell.
- Tests/test_core_text_drift.py automates the Core re-fetch and embedded-constants comparison.

## Per-function inventory

### GOVERN function (9 divergences)

**GOVERN 1.2** (minor wording)

- Playbook: `The characteristics of trustworthy AI are integrated into organizational policies, processes, and procedures.`
- Core:     `The characteristics of trustworthy AI are integrated into organizational policies, processes, procedures, and practices.`

**GOVERN 1.3** (minor wording)

- Playbook: `Processes and procedures are in place to determine the needed level of risk management activities based on the organization's risk tolerance.`
- Core:     `Processes, procedures, and practices are in place to determine the needed level of risk management activities based on the organization's risk tolerance.`

**GOVERN 1.5** (minor wording)

- Playbook: `Ongoing monitoring and periodic review of the risk management process and its outcomes are planned, organizational roles and responsibilities are clearly defined, including determining the frequency of periodic review.`
- Core:     `Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and organizational roles and responsibilities clearly defined, including determining the frequency of periodic review.`

**GOVERN 1.7** (minor wording)

- Playbook: `Processes and procedures are in place for decommissioning and phasing out of AI systems safely and in a manner that does not increase risks or decrease the organization’s trustworthiness.`
- Core:     `Processes and procedures are in place for decommissioning and phasing out AI systems safely and in a manner that does not increase risks or decrease the organization’s trustworthiness.`

**GOVERN 3.1** (typo)

- Playbook: `Decision-makings related to mapping, measuring, and managing AI risks throughout the lifecycle is informed by a diverse team (e.g., diversity of demographics, disciplines, experience, expertise, and backgrounds).`
- Core:     `Decision-making related to mapping, measuring, and managing AI risks throughout the lifecycle is informed by a diverse team (e.g., diversity of demographics, disciplines, experience, expertise, and backgrounds).`

**GOVERN 4.1** (minor wording)

- Playbook: `Organizational policies, and practices are in place to foster a critical thinking and safety-first mindset in the design, development, deployment, and uses of AI systems to minimize negative impacts.`
- Core:     `Organizational policies and practices are in place to foster a critical thinking and safety-first mindset in the design, development, deployment, and uses of AI systems to minimize potential negative impacts.`

**GOVERN 4.2** (minor wording)

- Playbook: `Organizational teams document the risks and potential impacts of the AI technology they design, develop, deploy, evaluate and use, and communicate about the impacts more broadly.`
- Core:     `Organizational teams document the risks and potential impacts of the AI technology they design, develop, deploy, evaluate, and use, and they communicate about the impacts more broadly.`

**GOVERN 5.2** (SEMANTIC DIVERGENCE)

- Playbook: `Mechanisms are established to enable AI actors to regularly incorporate adjudicated feedback from relevant AI actors into system design and implementation.`
- Core:     `Mechanisms are established to enable the team that developed or deployed AI systems to regularly incorporate adjudicated feedback from relevant AI actors into system design and implementation.`

**GOVERN 6.1** (minor wording)

- Playbook: `Policies and procedures are in place that address AI risks associated with third-party entities, including risks of infringement of a third party’s intellectual property or other rights.`
- Core:     `Policies and procedures are in place that address AI risks associated with third-party entities, including risks of infringement of a third-party’s intellectual property or other rights.`

### MAP function (11 divergences)

**MAP 1.1** (minor wording)

- Playbook: `Intended purpose, potentially beneficial uses, context-specific laws, norms and expectations, and prospective settings in which the AI system will be deployed are understood and documented. Considerations include: specific set or types of users along with their expectations; potential positive and negative impacts of system uses to individuals, communities, organizations, society, and the planet; assumptions and related limitations about AI system purposes; uses and risks across the development or product AI lifecycle; TEVV and system metrics.`
- Core:     `Intended purposes, potentially beneficial uses, context-specific laws, norms and expectations, and prospective settings in which the AI system will be deployed are understood and documented. Considerations include: the specific set or types of users along with their expectations; potential positive and negative impacts of system uses to individuals, communities, organizations, society, and the planet; assumptions and related limitations about AI system purposes, uses, and risks across the development or product AI lifecycle; and related TEVV and system metrics.`

**MAP 1.2** (minor wording)

- Playbook: `Inter-disciplinary AI actors, competencies, skills and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized.`
- Core:     `Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized.`

**MAP 1.3** (minor wording)

- Playbook: `The organization’s mission and relevant goals for the AI technology are understood and documented.`
- Core:     `The organization’s mission and relevant goals for AI technology are understood and documented.`

**MAP 1.6** (whitespace/punctuation only)

- Playbook: `System requirements (e.g., “the system shall respect the privacy of its users”) are elicited from and understood by relevant AI actors.  Design decisions take socio-technical implications into account to address AI risks.`
- Core:     `System requirements (e.g., “the system shall respect the privacy of its users”) are elicited from and understood by relevant AI actors. Design decisions take socio-technical implications into account to address AI risks.`

**MAP 2.1** (minor wording)

- Playbook: `The specific task, and methods used to implement the task, that the AI system will support is defined (e.g., classifiers, generative models, recommenders).`
- Core:     `The specific tasks and methods used to implement the tasks that the AI system will support are defined (e.g., classifiers, generative models, recommenders).`

**MAP 2.2** (minor wording)

- Playbook: `Information about the AI system’s knowledge limits and how system output may be utilized and overseen by humans is documented. Documentation provides sufficient information to assist relevant AI actors when making informed decisions and taking subsequent actions.`
- Core:     `Information about the AI system’s knowledge limits and how system output may be utilized and overseen by humans is documented. Documentation provides sufficient information to assist relevant AI actors when making decisions and taking subsequent actions.`

**MAP 3.2** (minor wording)

- Playbook: `Potential costs, including non-monetary costs, which result from expected or realized AI errors or system functionality and trustworthiness - as connected to organizational risk tolerance - are examined and documented.`
- Core:     `Potential costs, including non-monetary costs, which result from expected or realized AI errors or system functionality and trustworthiness – as connected to organizational risk tolerance – are examined and documented.`

**MAP 3.4** (whitespace/punctuation only)

- Playbook: `Processes for operator and practitioner proficiency with AI system performance and trustworthiness – and relevant technical standards and certifications – are defined, assessed and documented.`
- Core:     `Processes for operator and practitioner proficiency with AI system performance and trustworthiness – and relevant technical standards and certifications – are defined, assessed, and documented.`

**MAP 3.5** (minor wording)

- Playbook: `Processes for human oversight are defined, assessed, and documented in accordance with organizational policies from GOVERN function.`
- Core:     `Processes for human oversight are defined, assessed, and documented in accordance with organizational policies from the govern function.`

**MAP 4.1** (minor wording)

- Playbook: `Approaches for mapping AI technology and legal risks of its components – including the use of third-party data or software – are in place, followed, and documented, as are risks of infringement of a third-party’s intellectual property or other rights.`
- Core:     `Approaches for mapping AI technology and legal risks of its components – including the use of third-party data or software – are in place, followed, and documented, as are risks of infringement of a third party’s intellectual property or other rights.`

**MAP 4.2** (whitespace/punctuation only)

- Playbook: `Internal risk controls for components of the AI system including third-party AI technologies are identified and documented.`
- Core:     `Internal risk controls for components of the AI system, including third-party AI technologies, are identified and documented.`

### MEASURE function (14 divergences)

**MEASURE 1.1** (minor wording)

- Playbook: `Approaches and metrics for measurement of AI risks enumerated during the Map function are selected for implementation starting with the most significant AI risks. The risks or trustworthiness characteristics that will not – or cannot – be measured are properly documented.`
- Core:     `Approaches and metrics for measurement of AI risks enumerated during the map function are selected for implementation starting with the most significant AI risks. The risks or trustworthiness characteristics that will not – or cannot – be measured are properly documented.`

**MEASURE 1.2** (minor wording)

- Playbook: `Appropriateness of AI metrics and effectiveness of existing controls is regularly assessed and updated including reports of errors and impacts on affected communities.`
- Core:     `Appropriateness of AI metrics and effectiveness of existing controls are regularly assessed and updated, including reports of errors and potential impacts on affected communities.`

**MEASURE 2.1** (minor wording)

- Playbook: `Test sets, metrics, and details about the tools used during test, evaluation, validation, and verification (TEVV) are documented.`
- Core:     `Test sets, metrics, and details about the tools used during TEVV are documented.`

**MEASURE 2.4** (capitalisation only (function name))

- Playbook: `The functionality and behavior of the AI system and its components – as identified in the MAP function – are monitored when in production.`
- Core:     `The functionality and behavior of the AI system and its components – as identified in the map function – are monitored when in production.`

**MEASURE 2.6** (minor wording)

- Playbook: `AI system is evaluated regularly for safety risks – as identified in the MAP function. The AI system to be deployed is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and can fail safely, particularly if made to operate beyond its knowledge limits. Safety metrics implicate system reliability and robustness, real-time monitoring, and response times for AI system failures.`
- Core:     `The AI system is evaluated regularly for safety risks – as identified in the map function. The AI system to be deployed is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and it can fail safely, particularly if made to operate beyond its knowledge limits. Safety metrics reflect system reliability and robustness, real-time monitoring, and response times for AI system failures.`

**MEASURE 2.7** (capitalisation only (function name))

- Playbook: `AI system security and resilience – as identified in the MAP function – are evaluated and documented.`
- Core:     `AI system security and resilience – as identified in the map function – are evaluated and documented.`

**MEASURE 2.8** (capitalisation only (function name))

- Playbook: `Risks associated with transparency and accountability – as identified in the MAP function – are examined and documented.`
- Core:     `Risks associated with transparency and accountability – as identified in the map function – are examined and documented.`

**MEASURE 2.9** (minor wording)

- Playbook: `The AI model is explained, validated, and documented, and  AI system output is interpreted within its context – as identified in the MAP function – and to inform responsible use and governance.`
- Core:     `The AI model is explained, validated, and documented, and AI system output is interpreted within its context – as identified in the map function – to inform responsible use and governance.`

**MEASURE 2.10** (capitalisation only (function name))

- Playbook: `Privacy risk of the AI system – as identified in the MAP function – is examined and documented.`
- Core:     `Privacy risk of the AI system – as identified in the map function – is examined and documented.`

**MEASURE 2.11** (capitalisation only (function name))

- Playbook: `Fairness and bias – as identified in the MAP function – are evaluated and results are documented.`
- Core:     `Fairness and bias – as identified in the map function – are evaluated and results are documented.`

**MEASURE 2.12** (capitalisation only (function name))

- Playbook: `Environmental impact and sustainability of AI model training and management activities – as identified in the MAP function – are assessed and documented.`
- Core:     `Environmental impact and sustainability of AI model training and management activities – as identified in the map function – are assessed and documented.`

**MEASURE 2.13** (capitalisation only (function name))

- Playbook: `Effectiveness of the employed TEVV metrics and processes in the MEASURE function are evaluated and documented.`
- Core:     `Effectiveness of the employed TEVV metrics and processes in the measure function are evaluated and documented.`

**MEASURE 4.2** (minor wording)

- Playbook: `Measurement results regarding AI system trustworthiness in deployment context(s) and across AI lifecycle are informed by input from domain experts and other relevant AI actors to validate whether the system is performing consistently as intended. Results are documented.`
- Core:     `Measurement results regarding AI system trustworthiness in deployment context(s) and across the AI lifecycle are informed by input from domain experts and relevant AI actors to validate whether the system is performing consistently as intended. Results are documented.`

**MEASURE 4.3** (whitespace/punctuation only)

- Playbook: `Measurable performance improvements or declines based on consultations with relevant AI actors including affected communities, and field data about context-relevant risks and trustworthiness characteristics, are identified and documented.`
- Core:     `Measurable performance improvements or declines based on consultations with relevant AI actors, including affected communities, and field data about context-relevant risks and trustworthiness characteristics are identified and documented.`

### MANAGE function (7 divergences)

**MANAGE 1.1** (minor wording)

- Playbook: `A determination is made as to whether the AI system achieves its intended purpose and stated objectives and whether its development or deployment should proceed.`
- Core:     `A determination is made as to whether the AI system achieves its intended purposes and stated objectives and whether its development or deployment should proceed.`

**MANAGE 1.2** (minor wording)

- Playbook: `Treatment of documented AI risks is prioritized based on impact, likelihood, or available resources or methods.`
- Core:     `Treatment of documented AI risks is prioritized based on impact, likelihood, and available resources or methods.`

**MANAGE 1.3** (minor wording)

- Playbook: `Responses to the AI risks deemed high priority as identified by the Map function, are developed, planned, and documented. Risk response options can include mitigating, transferring, avoiding, or accepting.`
- Core:     `Responses to the AI risks deemed high priority, as identified by the map function, are developed, planned, and documented. Risk response options can include mitigating, transferring, avoiding, or accepting.`

**MANAGE 2.1** (minor wording)

- Playbook: `Resources required to manage AI risks are taken into account, along with viable non-AI alternative systems, approaches, or methods – to reduce the magnitude or likelihood of potential impacts.`
- Core:     `Resources required to manage AI risks are taken into account – along with viable non-AI alternative systems, approaches, or methods – to reduce the magnitude or likelihood of potential impacts.`

**MANAGE 2.4** (minor wording)

- Playbook: `Mechanisms are in place and applied, responsibilities are assigned and understood to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use.`
- Core:     `Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use.`

**MANAGE 3.2** (whitespace/punctuation only)

- Playbook: `Pre-trained models which are used for development are monitored as part of AI system regular  monitoring and maintenance.`
- Core:     `Pre-trained models which are used for development are monitored as part of AI system regular monitoring and maintenance.`

**MANAGE 4.3** (whitespace/punctuation only)

- Playbook: `Incidents and errors are communicated to relevant AI actors including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented.`
- Core:     `Incidents and errors are communicated to relevant AI actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented.`

## Notes

The catalog uses Core wording for control statements because compliance work cites the Core. Playbook content is reproduced unchanged in implementation guidance parts (`guidance`, `ai-rmf-suggested-actions`, `ai-rmf-documentation-questions`, `ai-rmf-references`), where it is Playbook-native.

Many of the divergences look incidental (commas, conjunctions, pluralisation) but a small number meaningfully change meaning, most notably GOVERN 5.2 where the Playbook substitutes "AI actors" for the Core's "the team that developed or deployed AI systems" — these refer to overlapping but not identical sets of stakeholders in AI RMF terminology.
