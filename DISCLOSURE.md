# Disclosure policy: what I publish, what I withhold, and how I decided

A portfolio about governed AI should be governed too. This page explains the rules this showcase was built under, so that what is missing reads as a decision rather than a gap.

## The publication model

1. **The working repositories stay private.** None of the source repositories behind this work has been made public, and their visibility has not been changed.
2. **Allow-list, never copy-then-redact.** Every file here was written from scratch from material deliberately selected for publication. Nothing was copied in wholesale and then trimmed, so there is no earlier, fuller version in this repository's history.
3. **Redaction happens before publication.** Sensitive detail never entered this repository: not in commits, branches, comments, page source, metadata or build output.
4. **Fail closed.** Where I was unsure whether something was safe to publish, I left it out.
5. **Every claim carries its status.** Demonstrated, measured, prototype, proposal or hypothesis, with limits stated. No metric was invented or rounded up.

## What is withheld, and why

| Category | Why |
| --- | --- |
| Secrets, keys, tokens and credential architecture | Knowing where credentials live and who may read them is most of an attack plan. |
| Trust-boundary implementation | How components exchange requests and how sandboxes are constrained is what an attacker needs to cross them. |
| Anti-bypass and anti-replay mechanisms | What they guarantee is published. How they work is not. |
| Host and infrastructure identifiers | Machine, tenant, subscription, app, certificate and label identifiers, endpoints and signing identities help an attacker and serve no reader. |
| Private security tests and open findings | Attack corpora, red-team case lists and unresolved findings stay private. |
| Employer and third-party intellectual property | Everything here is personal work. Employer work, data, configuration and internal metrics are not included. |
| Personal data | Including my own. Some experiments used my personal files and media as test data; their names and contents are never shown. |

## The redaction markers

| Marker | Used for |
| --- | --- |
| 🔒 **SECURITY REDACTION: IMPLEMENTATION DETAIL INTENTIONALLY WITHHELD** | The default, used whenever naming a more specific category would itself reveal something |
| 🔒 **TRUST BOUNDARY IMPLEMENTATION: REDACTED** | How separated components communicate or are contained |
| 🔒 **ANTI-BYPASS CONTROL: REDACTED** | How a guarantee such as single-use approval is enforced |
| 🔒 **SECRET AND CREDENTIAL HANDLING: REDACTED** | Where credentials live and which component may read them |
| 🔒 **HOST / INFRASTRUCTURE DETAIL: REDACTED** | Identifiers, names, locations and configuration of machines and cloud resources |
| 🔒 **PRIVATE SECURITY TEST: REDACTED** | Attack corpora and test cases |
| 🔒 **EMPLOYER / THIRD-PARTY IP: NOT INCLUDED** | Work that belongs to someone else |

Two rules govern them. **A marker must not leak by implication**: if naming the category would hint at an architecture or a weakness, the generic marker is used. And **markers are used sparingly**: they are there to show judgement, not to make the pages unreadable.

## How this showcase is checked

- A written allow-list of every file ([`ALLOWLIST.txt`](ALLOWLIST.txt)). The check fails if any file outside it appears.
- An automated pre-publication check ([`scripts/check_publication.py`](scripts/check_publication.py)), run on every push. It looks for credential-shaped strings, private keys, identifiers, private hostnames and file paths, personal contact details and internal ticket references, and it proves on every run that each pattern can fire, so a silent scan is never mistaken for a clean one.
- Before any publication, the same check is run locally against a private deny-list of specific names. That list cannot live in this repository, because the names themselves are private, so the check refuses to report a pass without it unless it is told explicitly that it is running in public CI, where it says so in its output.
- A review of the full Git history, not only the latest version, before the repository was made public.
- Screenshots of the working systems are not published.

## Found something that should not be here?

Please tell me via [LinkedIn](https://www.linkedin.com/in/davidmartinnealon/). I will treat it as a security report: fix first, then thank you.
