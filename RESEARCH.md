# Research and experiments: what I measured, and what it does not prove

Selected findings from building governed AI systems. Each one is labelled for what it actually is and states its own limits. Several did not go the way I expected, and they are here because of that.

| Label | Meaning |
| --- | --- |
| `MEASURED FINDING` | A number from a real run, with the method and sample stated |
| `EXPERIMENT / PROTOTYPE` | Built and run, but not yet evaluated at a scale that supports a general claim |
| `ARCHITECTURAL PROPOSAL` | A design I have argued for and partly built, not yet proven |
| `HYPOTHESIS` | What I currently believe and am testing, and could be wrong about |

Unless stated otherwise, results come from my own systems on a single Apple M1 machine with 16 GB of memory, and much of it uses synthetic data. None of it is a benchmark of anyone else's product.

Designed web version: [bp2professional.github.io/ai-engineering-portfolio/research/](https://bp2professional.github.io/ai-engineering-portfolio/research/)

---

### 1. Detection is the weakest control, so do not build on it · `MEASURED FINDING`

A deny-list prompt-injection detector caught **54 of 54** attack phrasings it was tuned on and **1 of 27** held-out paraphrases of the same attacks. This changed the architecture: Jarvis rests on structural controls, and its strongest tests assert that untrusted content changes nothing even when the detector stays silent.

*Limits: one detector, one author's corpus. The finding is about heuristic detection in general, not any vendor's product.*

> 🔒 **PRIVATE SECURITY TEST: REDACTED.** The attack corpus and the detector's rules are not published.

### 2. A local memory engine against acceptance criteria set in advance · `MEASURED FINDING`

Acceptance criteria were written *before* the run, with a pre-agreed fallback plan. The pipeline was scored on a deterministic synthetic corpus (630 events, 450 seeded facts, 570 probes) beside a control run.

| Criterion | Threshold | Result |
| --- | --- | --- |
| Evidence recall in the context packet | ≥ 90% | 99.2% |
| Unanswerable questions answered anyway | ≤ 10% | 0 of 50 |
| Retrieval latency before the model (p95) | < 300 ms | 76 ms |
| Extraction batch peak memory | < 4 GB | 3.52 GB |
| Unsupported claims in extracted memories | reported | 0 of 517 |
| Relation recall | reported | 66.7%: the weakest number, reported as it came out |

**The history matters as much as the table.** This was the fourth measurement. The third failed three criteria and sent the architecture back for reconsideration; this one passed every criterion a machine can decide. The final go or no-go decision is mine, and it is still open.

*Limits: synthetic, templated data measures containment rather than semantic understanding. One corpus, one configuration; latency excludes the answering model.*

### 3. Hybrid retrieval did not beat plain vector search · `MEASURED FINDING`

I chose a hybrid design (keyword and vector search fused by reciprocal rank fusion) partly expecting it to win. On recall@20 over 541 memories and 18 seeded questions: keyword 12, vector 17, fused 16. I published it, and the write-up says it does not prove hybrid beats a strong semantic retriever on this corpus.

*Limits: 18 questions is a small sample. The point is the discipline of reporting it.*

### 4. Ask a small model what something is, not whether it is allowed · `MEASURED FINDING`

A small on-device model asked whether live memory records (mostly derived from my own media library) could be shared refused to decide on 254 of 300 in a pilot. In a pre-registered 2×2 prompt experiment with the same weights, asking what a record *is* rather than whether it *may leave* cut abstentions from 136 of 150 to 0 of 150. The model could categorise all along; it was declining to adjudicate, and that reluctance had been quietly acting as a safety guard. The replacement design removes all approval authority from the model: it describes, and a deterministic rule over a human-approved list decides. It is built and awaiting my sign-off before it is switched on.

*Limits: one model, one fairly uniform corpus; the held-out confirmatory run is still to come.*

### 5. Pre-registered adversarial tests that become permanent · `MEASURED FINDING`

For a data-sharing policy, 32 adversarial cases and their expected outcomes were committed *before* the first run, with benign controls so that a rule refusing everything could not pass. The harness collects every deviation before failing. Result: 0 deviations out of 32 and a byte-for-byte check that nothing was written. The suite now runs on every build.

*Limits: this proves the mechanism, not that the underlying list is complete.*

> 🔒 **PRIVATE SECURITY TEST: REDACTED.** The case list is not published.

### 6. Evidence tiers are kinds, not scores · `MEASURED FINDING`

Cross-modal search results are split into *verified* (a standing claim says so), *inferred* (a named chain of links implies it) and *similar* (vectors only). A similarity score can never promote a result to verified, and a test fails if a new route to "verified" appears. On a nine-case gold set, precision and recall were 1.0 in both configurations, with a median of 227 µs deterministic against 3.3 s semantic. Lessons: score-sorting a mixed list let the most numerous kind crowd out the rest (now interleaved by kind), and a gold set curated under one configuration and scored under another read 0.417 with nothing wrong (gold cases now declare their configuration).

*Limits: my own media library on one machine; some relationship types exist only in fixtures so far.*

### 7. Cost-aware model routing, measured rather than modelled · `MEASURED FINDING`

A deterministic router picks the least expensive model expected to clear each task's quality and risk bar, and escalates only with a named human's approval. Two separately authorised live runs produced same-token cost reductions of **39.6% and 40.4%** against a deliberately cheapest-possible frontier baseline, for about US$0.02 in total. A separate offline process re-prices the evidence without spending anything.

*Limits: no quality claim survives in this evidence, the baseline assumes the same token counts, and no invoice was reconciled. Two cents proves the apparatus, not a business case.*

### 8. A shadow decision plane: AI judges that advise but cannot decide · `ARCHITECTURAL PROPOSAL` · `MEASURED FINDING`

An external AI judge runs beside a deterministic policy, disagreements are recorded, and the judge's answer can never replace the policy's. If it is ever substituted, the mission fails. Along the way: a judge value of 0.54 turned out to be a probability of "yes" calibrated only in aggregate, meaning *no signal* rather than "54% sure". And a configured 300 ms timeout took over 6 seconds against a simulated rate limit, because it applied per attempt. Own your deadline.

*Limits: very few live comparisons so far, so no accuracy claim is made.*

### 9. Explanations checked against the evidence after they are written · `EXPERIMENT / PROTOTYPE`

A hosted model writes a plain-language explanation of a mission or memory, which is then checked against the recorded evidence before it is shown. A count guard is designed to withhold an explanation whose numbers contradict the evidence. One live acceptance run cost US$0.018 against a US$0.05 cap.

*Limits: owner acceptance testing only, not a user study.*

### 10. A Copilot Studio agent for portfolio prioritisation · `EXPERIMENT / PROTOTYPE`

Two published Copilot Studio agents with Entra ID sign-in capture a work request and its Weighted Shortest Job First (WSJF) inputs in conversation, then hand them to a Power Automate agent flow that records the item. Version one wrote to a SharePoint list; version two moved to a custom Dataverse table with typed columns.

*Limits: a three-day proof on a single-user developer tenant, with no solution-based lifecycle management.*

### 11. Two green test suites can hide two code paths that disagree · `MEASURED FINDING`

One rule had two write paths, each with its own passing suite, and one silently dropped a bad argument. The fix: a single shared decision table plus one test asserting that both paths agree across the whole input matrix, itself checked by deliberately breaking the code. Related: a frame-rate benchmark reading a flat 30.0 idle and 20.0 under load was measuring the test harness, not the renderer, as a same-minute A/B confirmed.

### 12. Self-improvement scales by widening evidence, not authority · `HYPOTHESIS`

I believe most of the value of a self-improving AI system can be captured at the *prepare* level (finding, ranking, specifying and drafting work) while execution authority stays narrow, scoped and human-signed. The Jarvis lifecycle is my test. Its core path has run once, on a deliberately small change, so this remains a hypothesis.
