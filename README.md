# David Nealon: AI product, governance and engineering

**I design, build and govern AI systems that act only within limits a human sets.**

I have an enterprise product and information-protection background across Microsoft 365, Purview and Copilot rollout, and I build hands-on in Rust, TypeScript and Python. My work sits where agentic AI meets security: capability with bounded authority, privacy at the model boundary, and evidence for every claim.

**Portfolio site:** https://bp2professional.github.io/ai-engineering-portfolio/ · **LinkedIn:** https://www.linkedin.com/in/davidmartinnealon/

> [!NOTE]
> This repository is a **curated public showcase**. The working repositories behind it are private and stay private. Everything here was written from scratch from an explicit allow-list. Where detail is withheld for security reasons, you will see a 🔒 marker instead of a silent gap. See [DISCLOSURE.md](DISCLOSURE.md).

---

## The five-minute version

| | |
| --- | --- |
| **Who I am** | An AI product and governance lead who builds. I have owned enterprise Microsoft 365, Copilot and information-protection products, and I write and ship my own AI systems. |
| **What I build** | AI systems where agents propose and people decide: governed self-improvement, reversible privacy for model calls, and AI-assisted sensitivity labelling. |
| **Why it matters** | Anyone adopting agentic AI has to answer who authorised what, within which limits, and how to prove it afterwards. My work makes those answers structural. |
| **How I handle security** | Structural controls first, detection last. This showcase also withholds exploitable detail on purpose, and says so. |
| **What I personally did** | Everything here is my own work. I set the architecture, the governance model and the acceptance criteria. AI coding agents write much of the code under a protocol I wrote, and every merge is my decision. |
| **What evidence exists** | Live, dated runs with numbers, including results that went against me. Every claim is labelled as demonstrated, prototype, proposal or hypothesis. |

---

## Selected work

### 1. [Jarvis: governed self-improving AI](case-studies/jarvis.md)

`✅ CORE PATH DEMONSTRATED`

A personal AI system that can find, propose and build improvements to its own code, but only inside a scope I approve and sign. The result is independently verified, and the merge is left to me.

```mermaid
flowchart LR
    A[Request] --> B[Discover] --> C[Propose] --> D{{Review and approve}} --> E{{High-trust confirmation}} --> F[Execute in sandbox] --> G[Validate independently] --> H[Report: draft PR]
    H --> I{{Owner merges}}
    classDef human fill:#17365d,color:#fff,stroke:#17365d
    class D,E,I human
```

*The designed lifecycle. Dark steps can only be taken by a human. Every step fails closed and writes a record saying why.*

- **Result:** on 23 September 2026 a candidate from Jarvis's own discovery run was approved, signed, built in a sandbox, independently re-tested and merged by me through a draft pull request. It took five signed attempts: the first four each stopped safely on at least one host defect, and none on the governance model. The contract for that run was hand-written; a single run from a typed request to a merged change is the acceptance test in progress.
- **Scale:** 310 commits and more than 290 merged pull requests in ten weeks, over 6,000 automated tests, and about 350,000 lines of Rust and TypeScript (including tests).

### 2. [Airlock: reversible, privacy-preserving inference](case-studies/airlock.md)

`🧪 PROTOTYPE · NOT YET EVALUATED`

Personal information is swapped for typed placeholders such as `[PERSON_001]` before a prompt reaches an external model, then restored in the answer inside the trusted boundary.

- **Result:** a working end-to-end prototype on Azure (Functions, Presidio, Azure AI Foundry, Bicep), built in two days. It is deliberately labelled *not yet evaluated*, and it makes no accuracy claims until it is measured.

### 3. [Governed AI sensitivity labelling](case-studies/information-protection.md)

`✅ DEMONSTRATED LIVE`

An on-device model proposes Microsoft Purview sensitivity labels, policy decides, a person approves each file, and every label is verified by reading it back through a separate read-only identity.

- **Result:** label coverage went from **56.59% to 99.22%** on a live developer tenant. **55 of 55** writes were verified by read-back, **zero bytes** of document content went to external AI, and the 55 metered writes cost about **US$0.10**.

### Research and experiments

[Twelve findings](RESEARCH.md), each labelled measured finding, experiment, proposal or hypothesis, and each with its limits. They include a prompt-injection detector that caught **1 of 27** held-out attacks (which is why nothing relies on it), a hybrid retriever that lost to plain vector search, and a small model that stopped abstaining once it was asked what something *is* rather than whether it is *allowed*.

---

## How I think about AI systems

- **Structural controls beat clever ones.** A capability that does not exist cannot be misused.
- **Authority is a record, not a mood.** Approving and doing are separate, attributable events.
- **Fail closed, and say why.** A refusal is an audited outcome, not an error to retry around.
- **Verify the result, not the report.** A 202 is not a label, and an agent's claim is not a test result.
- **Publish the number that did not flatter.** Honest maturity labels beat feature lists.
- **Check that the owner can still act.** A control that blocks everything passes every "is it blocked?" test.

---

## What is in this repository

| Path | What it is |
| --- | --- |
| [`case-studies/`](case-studies/) | Text editions of the three case studies |
| [`RESEARCH.md`](RESEARCH.md) | Research findings and experiments |
| [`DISCLOSURE.md`](DISCLOSURE.md) | The publication model and redaction policy this showcase follows |
| [`site/`](site/) | Source of the portfolio website: static HTML and CSS, no JavaScript, no third-party requests |
| [`scripts/check_publication.py`](scripts/check_publication.py) | The automated pre-publication check, run locally and in CI |

## Background

- Product ownership of Microsoft 365, Microsoft 365 Copilot and ChatGPT Enterprise in a large enterprise, including rollout, governance, adoption and value realisation.
- Microsoft Purview information protection: sensitivity labels, data loss prevention, sensitive information types and retention.
- MBA, Melbourne Business School. Microsoft certifications including SC-401, SC-900, AZ-900 and PL-900. ICAgile Certified Professional.

Employer work belongs to my employers and is not described here beyond these lines.

---

© 2026 David Nealon. All rights reserved. The content of this repository is published for reading and evaluation. Please contact me before reusing it.
