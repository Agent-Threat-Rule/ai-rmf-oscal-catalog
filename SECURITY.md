# Security policy

This is an OSCAL data project. The artifacts published here are JSON
documents (catalog and profiles) and Python source code that generates them.
There is no running service, no user authentication, no cryptographic
material handled by this project.

## Supported versions

Active version: **v0.4.0**.

Older versions remain in the git history but receive no security updates.
Downstream consumers should pin to a specific version (or the `main`
branch with explicit awareness that `main` may move forward).

## Reporting a vulnerability

### What counts as a security issue here

This is a relatively narrow surface. Genuine security issues in this
project would typically be one of:

- A generator that emits invalid OSCAL JSON in a way that causes downstream
  parsers to crash or behave unsafely.
- A regex in `cross_references.py` that exhibits catastrophic backtracking
  on adversarial input from the Playbook source (the source is currently
  trusted, but defence-in-depth is welcome).
- A tier profile that mistakenly includes a control ID that does not exist
  in the catalog (causes downstream tooling to fail loudly, but this would
  be detected by `completeness_check.py`).
- A schema validation gap that lets the generator emit non-OSCAL-conformant
  output without `validate.py` flagging it.

### What does **not** count as a security issue here

- AI RMF Core text content concerns (those are NIST's authoritative source;
  report to NIST — see below).
- AI RMF Playbook content concerns (those are NIST's; report to NIST).
- Disagreement with the tier selections (open a normal feature/discussion
  issue).
- "This catalog isn't endorsed by NIST" — this is intentional and clearly
  documented (see README, `parties` and `remarks` in catalog metadata).

### How to report

If you've identified what you believe to be a genuine security issue:

1. **Preferred:** email [adam@agentthreatrule.org](mailto:adam@agentthreatrule.org)
   with subject prefix `[ai-rmf-oscal-catalog security]`. Include:
   - A concise description of the issue
   - Steps to reproduce
   - Suggested fix if you have one
   - Whether you'd like public credit for the report

2. **Acceptable:** open a private GitHub security advisory via the
   "Report a vulnerability" button under the
   [Security tab](https://github.com/Agent-Threat-Rule/ai-rmf-oscal-catalog/security)
   of this repository.

3. **For low-severity / non-sensitive issues:** opening a normal public
   issue is fine. The bar for "must be reported privately" is low here
   because there is no running service.

### Response time

The project has a single active maintainer (see
[MAINTAINERS.md](./MAINTAINERS.md)). Best-effort response time is 7 days
for acknowledgment and 30 days for resolution. If you have not heard back
in 14 days, please nudge — single-maintainer projects sometimes drop
threads.

### Coordinated disclosure

For genuine security issues, the project follows coordinated disclosure:

- Acknowledgement within 7 days
- Triage within 14 days
- Fix or mitigation within 30 days where feasible (longer for upstream
  schema or third-party-dependency issues)
- Public disclosure after fix is available, with credit to the reporter
  (unless the reporter prefers anonymity)

## Upstream contact

For issues that should be reported to NIST rather than (or in addition to)
this project:

- **AI RMF Core text content**: contact the AI RMF team at
  [aiframework@nist.gov](mailto:aiframework@nist.gov) or via the
  [AI Resource Center](https://airc.nist.gov/).
- **NIST OSCAL Team**: file an issue in
  [usnistgov/OSCAL](https://github.com/usnistgov/OSCAL) following their
  contribution guidelines.
- **NIST CAISI**: see the [CAISI website](https://www.nist.gov/caisi).

## Threat model

This project does not run as a service. The threat model is therefore
limited to:

1. **Tampered source data** — if `source/ai-rmf-playbook.json` were
   replaced with adversarial content, the generator would produce a
   tampered catalog. Mitigation: source is committed to git; PRs that
   modify source files are subject to maintainer review.
2. **Compromised release pipeline** — if a malicious actor pushed a tag
   without going through review, downstream consumers might receive
   adulterated artifacts. Mitigation: only maintainers can push to `main`
   and tag releases. Branch protection is enabled. Tags are signed when
   feasible.
3. **Adversarial input to validators** — `tests/test_core_text_drift.py`
   fetches the AIRC website. If that website were compromised, the test
   could produce false positives or false negatives. Mitigation: the test
   has a deterministic baseline and reports drift, not blind acceptance.

This is not a comprehensive threat model and the project welcomes
contributions to expand it.
