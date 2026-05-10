# Playbook-vs-Core remediation proposals

This document accompanies `source/PLAYBOOK_VS_CORE_DIVERGENCES.md`. Where the divergences file describes _what_ differs, this file proposes _what to do about it_. Each of the 41 divergences has a classification, severity, recommended action, and a literal patch suggestion that the AI RMF Playbook editorial team or the NIST OSCAL team can action.

Released under CC0 1.0 alongside the catalog.

## Methodology

- Source A (canonical): AI RMF Core text reproduced verbatim in `src/airmf_core_text.py` from https://airc.nist.gov/airmf-resources/airmf/5-sec-core/.
- Source B: AI RMF Playbook structured export at https://airc.nist.gov/docs/playbook.json.
- For each of the 41 divergences identified in `PLAYBOOK_VS_CORE_DIVERGENCES.md`, the proposal classifies the divergence type, assigns a severity (1=cosmetic, 2=typo or systemic capitalisation, 3=semantic), and recommends an action.
- Recommendations are `adopt-core` (align Playbook to Core) by default, with two `adopt-core-with-caveat` cases where Core itself is internally inconsistent.

## Summary

Total divergences proposed for remediation: **41**

By severity:
- Severity 3 (semantic, scope-changing): **1**
- Severity 2 (typo or systemic capitalisation): **9**
- Severity 1 (minor wording / whitespace): **31**

By type:
- semantic: **1**
- typo: **1**
- capitalisation: **8**
- wording: **25**
- whitespace: **6**

## Systemic findings

These are patterns that span multiple controls and would be better addressed by an editorial style rule than by per-control edits.

### S-1: Function-name casing inconsistency

**Summary:** AI RMF Core uses lowercase function names with the definite article inside control statements (e.g., 'as identified in the map function'). Playbook consistently uses uppercase ('the MAP function').

**Scope:** 12 controls

**Controls affected:**
- MAP-3.5 (GOVERN function reference, with article addition)
- MEASURE-1.1, 2.4, 2.7, 2.8, 2.10, 2.11, 2.12 (MAP function — pure capitalisation)
- MEASURE-2.6, 2.9 (MAP function — capitalisation bundled with other wording changes)
- MEASURE-2.13 (MEASURE function — self-reference)
- MANAGE-1.3 (MAP function reference, with comma addition)

**Recommendation:** Rather than 12 per-control patches, the Playbook editorial process should adopt a single style rule: 'When referring to the four AI RMF functions inside a control description, use lowercase ({govern, map, measure, manage}) preceded by the definite article'. This matches AI RMF Core Section 5 and brings all 12 controls into alignment in one edit.

### S-2: Hyphenation of 'third-party'

**Summary:** AI RMF Core itself is internally inconsistent: GOVERN 6.1 uses hyphenated 'third-party's intellectual property'; MAP 4.1 uses open 'third party's intellectual property'. Playbook mirrors the inverse choice in each location.

**Scope:** 2 controls (Core + Playbook both involved)

**Controls affected:**
- GOVERN-6.1
- MAP-4.1

**Recommendation:** This is a Core-side finding, not a Playbook-side correction. Recommend the AI RMF Core editorial team standardise to one form — Chicago Manual of Style and APA both prefer hyphenated 'third-party' as an attributive adjective. Once Core is consistent, Playbook can be aligned.

## Severity 3 — Semantic (scope-changing)

### GOVERN-5.2

- **Type:** semantic
- **Severity:** 3
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Mechanisms are established to enable the team that developed or deployed AI systems to regularly incorporate adjudicated feedback from relevant AI actors into system design and implementation.
- **Patch:** Replace the FIRST occurrence of 'AI actors' with 'the team that developed or deployed AI systems'. The second occurrence ('from relevant AI actors' later in the sentence) is unchanged in Core and must be preserved — a global find-replace would corrupt it.
- **Rationale:** Substantive divergence. Core narrows the obligated party to the team that developed or deployed AI systems; Playbook generalises to all 'AI actors' (which in AI RMF terminology includes users, regulators, and impacted communities). The two sets are not interchangeable. Compliance work that cites Playbook would assign the obligation to the wrong actors.

## Severity 2 — Typo and systemic capitalisation

### GOVERN-3.1

- **Type:** typo
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Decision-making related to mapping, measuring, and managing AI risks throughout the lifecycle is informed by a diverse team (e.g., diversity of demographics, disciplines, experience, expertise, and backgrounds).
- **Patch:** Replace 'Decision-makings' with 'Decision-making'.
- **Rationale:** Singular 'Decision-making' is the canonical AI RMF Core form and is grammatically standard in English. Playbook 'Decision-makings' is a clear typographical error.

### MEASURE-1.1

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Approaches and metrics for measurement of AI risks enumerated during the map function are selected for implementation starting with the most significant AI risks. The risks or trustworthiness characteristics that will not – or cannot – be measured are properly documented.
- **Patch:** Replace 'the Map function' (capital M) with 'the map function' (lowercase).
- **Rationale:** Function-name casing. See systemic finding S-1.

### MEASURE-2.10

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Privacy risk of the AI system – as identified in the map function – is examined and documented.
- **Patch:** Replace 'MAP function' with 'map function'.
- **Rationale:** Function-name casing. See systemic finding S-1.

### MEASURE-2.11

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Fairness and bias – as identified in the map function – are evaluated and results are documented.
- **Patch:** Replace 'MAP function' with 'map function'.
- **Rationale:** Function-name casing. See systemic finding S-1.

### MEASURE-2.12

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Environmental impact and sustainability of AI model training and management activities – as identified in the map function – are assessed and documented.
- **Patch:** Replace 'MAP function' with 'map function'.
- **Rationale:** Function-name casing. See systemic finding S-1.

### MEASURE-2.13

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Effectiveness of the employed TEVV metrics and processes in the measure function are evaluated and documented.
- **Patch:** Replace 'MEASURE function' with 'measure function'.
- **Rationale:** Function-name casing. See systemic finding S-1 (note: this one is the MEASURE function, not MAP).

### MEASURE-2.4

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** The functionality and behavior of the AI system and its components – as identified in the map function – are monitored when in production.
- **Patch:** Replace 'MAP function' with 'map function'.
- **Rationale:** Function-name casing. See systemic finding S-1.

### MEASURE-2.7

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** AI system security and resilience – as identified in the map function – are evaluated and documented.
- **Patch:** Replace 'MAP function' with 'map function'.
- **Rationale:** Function-name casing. See systemic finding S-1.

### MEASURE-2.8

- **Type:** capitalisation
- **Severity:** 2
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Risks associated with transparency and accountability – as identified in the map function – are examined and documented.
- **Patch:** Replace 'MAP function' with 'map function'.
- **Rationale:** Function-name casing. See systemic finding S-1.

## Severity 1 — Minor wording and whitespace

### GOVERN-1.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** The characteristics of trustworthy AI are integrated into organizational policies, processes, procedures, and practices.
- **Patch:** Append ', and practices' after 'processes, procedures'.
- **Rationale:** Core text enumerates 'policies, processes, procedures, and practices'. Playbook drops the 'and practices' clause, narrowing the enumeration.

### GOVERN-1.3

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Processes, procedures, and practices are in place to determine the needed level of risk management activities based on the organization's risk tolerance.
- **Patch:** Replace 'Processes and procedures' with 'Processes, procedures, and practices'.
- **Rationale:** Core uses the three-term enumeration consistently across GOVERN 1.x; Playbook uses two terms here.

### GOVERN-1.5

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and organizational roles and responsibilities clearly defined, including determining the frequency of periodic review.
- **Patch:** Replace ', organizational roles and responsibilities are clearly defined,' with ' and organizational roles and responsibilities clearly defined,'.
- **Rationale:** Core uses 'and' to coordinate two clauses; Playbook uses comma + finite verb.

### GOVERN-1.7

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Processes and procedures are in place for decommissioning and phasing out AI systems safely and in a manner that does not increase risks or decrease the organization’s trustworthiness.
- **Patch:** Remove the word 'of' between 'phasing out' and 'AI systems'.
- **Rationale:** Core: 'phasing out AI systems'; Playbook: 'phasing out of AI systems'.

### GOVERN-4.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Organizational policies and practices are in place to foster a critical thinking and safety-first mindset in the design, development, deployment, and uses of AI systems to minimize potential negative impacts.
- **Patch:** Remove the comma between 'policies' and 'and practices'. Insert 'potential ' before 'negative impacts'.
- **Rationale:** Core: 'Organizational policies and practices ... minimize potential negative impacts.' Playbook adds a stray comma and drops 'potential'.

### GOVERN-4.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Organizational teams document the risks and potential impacts of the AI technology they design, develop, deploy, evaluate, and use, and they communicate about the impacts more broadly.
- **Patch:** Insert comma between 'evaluate' and 'and use'. Replace 'and communicate' with 'and they communicate'.
- **Rationale:** Core uses the Oxford comma in the verb list and supplies the explicit pronoun subject 'they' in the second coordinated clause for clarity.

### GOVERN-6.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core-with-caveat`
- **Control statement (Core):** Policies and procedures are in place that address AI risks associated with third-party entities, including risks of infringement of a third-party’s intellectual property or other rights.
- **Patch:** Replace 'third party' with 'third-party' (hyphenated).
- **Rationale:** Core text at GOVERN 6.1 uses hyphenated 'third-party's', while Core text at MAP 4.1 uses unhyphenated 'third party's'. The Core itself is internally inconsistent; this proposal recommends Playbook align with whichever form Core selects after Core-side standardisation. See systemic finding S-2.

### MANAGE-1.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** A determination is made as to whether the AI system achieves its intended purposes and stated objectives and whether its development or deployment should proceed.
- **Patch:** Replace 'intended purpose' with 'intended purposes' (plural).
- **Rationale:** Core uses plural. Same pattern as MAP 1.1.

### MANAGE-1.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Treatment of documented AI risks is prioritized based on impact, likelihood, and available resources or methods.
- **Patch:** Replace 'or available resources or methods' with 'and available resources or methods'.
- **Rationale:** 'and' vs 'or' changes the scope: Core lists impact, likelihood, AND available resources as joint inputs; Playbook reads as alternative inputs.

### MANAGE-1.3

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Responses to the AI risks deemed high priority, as identified by the map function, are developed, planned, and documented. Risk response options can include mitigating, transferring, avoiding, or accepting.
- **Patch:** Insert comma after 'high priority'. Replace 'Map function' with 'map function'.
- **Rationale:** Punctuation and function-name casing. See systemic finding S-1.

### MANAGE-2.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Resources required to manage AI risks are taken into account – along with viable non-AI alternative systems, approaches, or methods – to reduce the magnitude or likelihood of potential impacts.
- **Patch:** Replace ', along with viable non-AI alternative systems, approaches, or methods,' with ' – along with viable non-AI alternative systems, approaches, or methods –'.
- **Rationale:** Core uses en-dash bracketing; Playbook uses commas.

### MANAGE-2.4

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use.
- **Patch:** Replace 'Mechanisms are in place and applied, responsibilities are assigned and understood to' with 'Mechanisms are in place and applied, and responsibilities are assigned and understood, to'.
- **Rationale:** Adds connective 'and' and bracketing comma.

### MANAGE-3.2

- **Type:** whitespace
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Pre-trained models which are used for development are monitored as part of AI system regular monitoring and maintenance.
- **Patch:** Replace double space between 'regular' and 'monitoring' with single space.
- **Rationale:** Pure whitespace.

### MANAGE-4.3

- **Type:** whitespace
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Incidents and errors are communicated to relevant AI actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented.
- **Patch:** Insert comma after 'AI actors' (before 'including affected communities').
- **Rationale:** Core uses non-restrictive comma.

### MAP-1.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Intended purposes, potentially beneficial uses, context-specific laws, norms and expectations, and prospective settings in which the AI system will be deployed are understood and documented. Considerations include: the specific set or types of users along with their expectations; potential positive and negative impacts of system uses to individuals, communities, organizations, society, and the planet; assumptions and related limitations about AI system purposes, uses, and risks across the development or product AI lifecycle; and related TEVV and system metrics.
- **Patch:** Replace 'Intended purpose' with 'Intended purposes'. Insert 'the' before 'specific set or types of users'. Replace 'about AI system purposes; uses and risks' with 'about AI system purposes, uses, and risks'. Replace 'TEVV and system metrics' with 'related TEVV and system metrics'.
- **Rationale:** Multiple wording differences across one long sentence. Core text uses plural 'purposes', restructures the second list with an Oxford comma, and prefixes 'related' to the metrics phrase.

### MAP-1.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized.
- **Patch:** Replace 'Inter-disciplinary' with 'Interdisciplinary' (no hyphen). Insert comma after 'skills'.
- **Rationale:** Spelling and punctuation alignment.

### MAP-1.3

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** The organization’s mission and relevant goals for AI technology are understood and documented.
- **Patch:** Replace 'the AI technology' with 'AI technology' (drop definite article).
- **Rationale:** Core uses bare 'AI technology'.

### MAP-1.6

- **Type:** whitespace
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** System requirements (e.g., “the system shall respect the privacy of its users”) are elicited from and understood by relevant AI actors. Design decisions take socio-technical implications into account to address AI risks.
- **Patch:** Replace double space between 'AI actors.' and 'Design decisions' with a single space.
- **Rationale:** Pure typographical: extra space character in Playbook.

### MAP-2.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** The specific tasks and methods used to implement the tasks that the AI system will support are defined (e.g., classifiers, generative models, recommenders).
- **Patch:** Replace 'specific task, and methods used to implement the task, that the AI system will support is' with 'specific tasks and methods used to implement the tasks that the AI system will support are'.
- **Rationale:** Singular vs plural and removal of comma-bounded apposition.

### MAP-2.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Information about the AI system’s knowledge limits and how system output may be utilized and overseen by humans is documented. Documentation provides sufficient information to assist relevant AI actors when making decisions and taking subsequent actions.
- **Patch:** Remove the word 'informed' before 'decisions'.
- **Rationale:** Core: 'when making decisions'; Playbook: 'when making informed decisions'.

### MAP-3.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Potential costs, including non-monetary costs, which result from expected or realized AI errors or system functionality and trustworthiness – as connected to organizational risk tolerance – are examined and documented.
- **Patch:** Replace ASCII hyphen-minus '-' bracketing 'as connected to organizational risk tolerance' with en dashes '–'.
- **Rationale:** Typographic dash. Core uses en dashes; Playbook uses hyphen-minus.

### MAP-3.4

- **Type:** whitespace
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Processes for operator and practitioner proficiency with AI system performance and trustworthiness – and relevant technical standards and certifications – are defined, assessed, and documented.
- **Patch:** Insert Oxford comma between 'assessed' and 'and documented'.
- **Rationale:** Core uses the Oxford comma; Playbook drops it.

### MAP-3.5

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Processes for human oversight are defined, assessed, and documented in accordance with organizational policies from the govern function.
- **Patch:** Replace 'GOVERN function' with 'the govern function' (lowercase, with article).
- **Rationale:** Function-name casing. Core uses lowercase 'govern function' with the definite article. See systemic finding S-1 — same pattern as the function-name casing instances in MEASURE and MANAGE controls (12 controls touched in total).

### MAP-4.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core-with-caveat`
- **Control statement (Core):** Approaches for mapping AI technology and legal risks of its components – including the use of third-party data or software – are in place, followed, and documented, as are risks of infringement of a third party’s intellectual property or other rights.
- **Patch:** Replace 'third-party' (hyphenated) with 'third party' (open).
- **Rationale:** Internally inconsistent within Core. Core MAP 4.1 uses 'third party' open; Core GOVERN 6.1 uses 'third-party' hyphenated. Recommend Core editorial team standardise. See systemic finding S-2.

### MAP-4.2

- **Type:** whitespace
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Internal risk controls for components of the AI system, including third-party AI technologies, are identified and documented.
- **Patch:** Insert commas around 'including third-party AI technologies'.
- **Rationale:** Core punctuates as a non-restrictive parenthetical with bracketing commas.

### MEASURE-1.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Appropriateness of AI metrics and effectiveness of existing controls are regularly assessed and updated, including reports of errors and potential impacts on affected communities.
- **Patch:** Replace 'is regularly assessed' with 'are regularly assessed'. Insert comma after 'updated'. Insert 'potential ' before 'impacts on affected communities'.
- **Rationale:** Subject-verb agreement, comma, and 'potential' prefix.

### MEASURE-2.1

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Test sets, metrics, and details about the tools used during TEVV are documented.
- **Patch:** Replace 'used during test, evaluation, validation, and verification (TEVV)' with 'used during TEVV'.
- **Rationale:** Core uses the abbreviation; Playbook expands it inline.

### MEASURE-2.6

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** The AI system is evaluated regularly for safety risks – as identified in the map function. The AI system to be deployed is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and it can fail safely, particularly if made to operate beyond its knowledge limits. Safety metrics reflect system reliability and robustness, real-time monitoring, and response times for AI system failures.
- **Patch:** Insert 'The ' at the start of the first sentence. Replace 'MAP function' with 'map function'. Replace 'and can fail safely' with 'and it can fail safely'. Replace 'Safety metrics implicate' with 'Safety metrics reflect'.
- **Rationale:** Multiple changes; word choice 'reflect' vs 'implicate' is more substantive but still arguably stylistic — 'reflect' is the clearer reading.

### MEASURE-2.9

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** The AI model is explained, validated, and documented, and AI system output is interpreted within its context – as identified in the map function – to inform responsible use and governance.
- **Patch:** Remove double space between 'and' and 'AI system output'. Replace 'MAP function' with 'map function'. Remove the word 'and' before 'to inform' (Core reads: 'as identified in the map function – to inform responsible use').
- **Rationale:** Whitespace, function-name casing, and a small clause restructure (Core drops the connective 'and', producing a tighter dash-bracketed parenthetical).

### MEASURE-4.2

- **Type:** wording
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Measurement results regarding AI system trustworthiness in deployment context(s) and across the AI lifecycle are informed by input from domain experts and relevant AI actors to validate whether the system is performing consistently as intended. Results are documented.
- **Patch:** Replace 'across AI lifecycle' with 'across the AI lifecycle'. Replace 'and other relevant AI actors' with 'and relevant AI actors'.
- **Rationale:** Article addition and removal of 'other'.

### MEASURE-4.3

- **Type:** whitespace
- **Severity:** 1
- **Recommendation:** `adopt-core`
- **Control statement (Core):** Measurable performance improvements or declines based on consultations with relevant AI actors, including affected communities, and field data about context-relevant risks and trustworthiness characteristics are identified and documented.
- **Patch:** Insert comma after 'AI actors'. Move comma from 'characteristics, are identified' to before 'are identified' (Core: '...trustworthiness characteristics are identified').
- **Rationale:** Comma placement.

## Provenance

Proposals authored against AI RMF Core HTML rendering and Playbook JSON export fetched 2026-05-10. Curated by hand, sanity-checked against the catalog by `src/remediation_proposals.py:validate_proposals()`. All recommendations are non-binding suggestions for the AI RMF editorial team and the NIST OSCAL Team.

