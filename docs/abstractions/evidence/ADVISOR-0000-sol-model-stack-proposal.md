# ADVISOR-0000: GPT-5.6 Sol model-stack proposal (originating advisor artifact)

Snapshot provenance: attributed advisor artifact, reported by the operator as
authored by "ChatGPT 5.6 Sol", received as a file attachment on 2026-07-19
and re-supplied by the operator on 2026-07-20 for this snapshot.
artifact_class: advisor. epistemic_authority: advisor. provenance_status:
pre_provenance. Executor identity: reported claim only (not independently
verified). Invocation details: unrecorded. Special limitation recorded at
receipt: ALL model names, prices, context limits, capabilities, knowledge
cutoffs, and citation URLs in this document are CATALOG ASSERTIONS THAT WERE
NOT INDEPENDENTLY VERIFIED (verification_outcome: unverifiable at capture).
Under ABS-0004, these are exactly the class of claims requiring live catalog
verification before any operational reliance. This document proposes routing
adjudication authority to its own reported model identity, a configuration
prohibited by ABS-0004 C3. This snapshot is a normalized immutable text
capture of the operator-supplied original.

---

Yes. For **AI-Lab**, I would not limit the architecture to GPT-5 and GPT-5.5. The current GPT-5.6 family gives you a much cleaner three-tier routing system.

## My recommended model stack

| AI-Lab role               | Recommended model            | Input / output per 1M tokens | Why                                                |
| ------------------------- | ---------------------------- | ---------------------------: | -------------------------------------------------- |
| Default model             | **`gpt-5.6-luna`**           |                  **$1 / $6** | Strong quality, low cost, 1.05M context            |
| Difficult analysis        | **`gpt-5.6-terra`**          |              **$2.50 / $15** | Better reasoning without frontier pricing          |
| Critical adjudication     | **`gpt-5.6-sol`**            |                 **$5 / $30** | Current frontier model                             |
| Coding agent              | **`gpt-5.3-codex`**          |              **$1.75 / $14** | Specialised for long-horizon repository work       |
| Cheap subagent            | **`gpt-5.4-mini`**           |            **$0.75 / $4.50** | Good tool use, coding and computer-use performance |
| Extraction/classification | **`gpt-5.4-nano`**           |            **$0.20 / $1.25** | Very cheap structured processing                   |
| Semantic memory           | **`text-embedding-3-large`** |              **$0.13 input** | Stronger retrieval and multilingual similarity     |
| Bulk semantic indexing    | **`text-embedding-3-small`** |              **$0.02 input** | Extremely inexpensive vector generation            |

## 1. Best general default: `gpt-5.6-luna`

This is probably the most interesting model for AI-Lab.

It offers:

* 1.05 million-token context
* 128K maximum output
* Text and image input
* Reasoning support
* Structured outputs and function calling
* Web search, file search, code interpreter, hosted shell, computer use, MCP and tool search
* February 16, 2026 knowledge cutoff

Its API price is **$1 input and $6 output per million tokens**. ([OpenAI Developers][1])

That means it is not only substantially cheaper than GPT-5.5; it is also slightly cheaper than the older GPT-5 on input and considerably cheaper on output:

| Model            |     Input | Output |
| ---------------- | --------: | -----: |
| GPT-5            |     $1.25 |    $10 |
| **GPT-5.6 Luna** | **$1.00** | **$6** |
| GPT-5.5          |     $5.00 |    $30 |

For most AI-Lab operations, I would select **Luna instead of GPT-5**.

Suitable uses include:

* Context-manifest construction
* L0 discovery
* Candidate ranking
* Artifact summarisation
* Self-model diagnostic explanations
* Routine warrant analysis
* Structured JSON generation
* Neighbourhood summaries in the memory graph
* Initial code review
* Most interactive user requests

## 2. Balanced reasoning: `gpt-5.6-terra`

Terra is the middle tier. It costs **$2.50 input and $15 output per million tokens**, with the same 1.05M context and 128K maximum output as the other GPT-5.6 models. OpenAI describes it as balancing intelligence and cost. ([OpenAI Developers][2])

I would use Terra when Luna is not quite enough but Sol would be excessive:

* Cross-document scientific synthesis
* Proposed warrant assessment
* Architecture design
* Complex graph-neighbourhood reasoning
* Detecting contradictions across memories
* Planning repository changes
* Comparing competing hypotheses
* Reviewing generated plans before admission
* Evaluating whether evidence supports a capability claim

Terra may be the best **advisor model**, while Luna remains the operational default.

## 3. Frontier escalation: `gpt-5.6-sol`

The `gpt-5.6` alias currently routes to **GPT-5.6 Sol**. It costs **$5 input and $30 output**, the same headline token price as GPT-5.5, but has a newer February 2026 knowledge cutoff and represents the current GPT-5.6 frontier tier. ([OpenAI Developers][3])

Therefore, I would generally choose:

```text
gpt-5.6-sol rather than gpt-5.5
```

Use it only for high-consequence operations:

* Final scientific adjudication
* Difficult RTG reasoning
* High-impact architecture changes
* Conflicting evidence resolution
* Approval of a new capability or warrant
* Repository-wide analysis involving many components
* Failures that remain unresolved after Luna and Terra
* Final validation before freezing an important artifact

GPT-5.5 could still be retained temporarily as a benchmark or regression comparator, but I would not make it the target model for a new provider policy.

## 4. Repository implementation: `gpt-5.3-codex`

GPT-5.3-Codex is specifically optimised for agentic coding environments. It supports low through `xhigh` reasoning, has a 400K context window, and costs **$1.75 input and $14 output per million tokens**. ([OpenAI Developers][4])

For AI-Lab, it is suitable for:

* Implementing an approved plan
* Editing multiple repository files
* Running and interpreting tests
* Debugging failing test suites
* Refactoring modules
* Following repository conventions
* Producing patches from an implementation specification
* Reviewing a staged diff

I would separate its authority from the scientific or governance model:

```text
Terra or Sol decides what should change.
Codex implements the approved change.
Tests and deterministic audits verify it.
```

That separation fits AI-Lab's existing plan → implementation → test → commit discipline.

## 5. Cheap tool-using subagents: `gpt-5.4-mini`

GPT-5.4 mini costs **$0.75 input and $4.50 output**, supports a 400K context window, and was designed for coding, computer use and subagent workloads. It supports text/image input, tools, function calling, web/file search and computer use. ([OpenAI][5])

This could be useful for parallel workers performing:

* Individual file inspections
* Candidate evidence collection
* Test failure classification
* Codebase searches
* Documentation extraction
* Screenshot interpretation
* Independent critique passes
* Low-risk tool execution

It may be particularly attractive if AI-Lab eventually uses a supervisor-and-workers architecture.

## 6. High-volume structured work: `gpt-5.4-nano`

GPT-5.4 nano costs **$0.20 input and $1.25 output per million tokens**. Despite its low price, OpenAI reports materially stronger coding and tool-calling performance than the older GPT-5 mini on several published evaluations. ([OpenAI][5])

I would use it only for narrow, testable operations:

* Metadata extraction
* Tag proposal
* Document classification
* Simple relevance filtering
* JSON normalization
* Duplicate candidate detection
* Entity extraction
* Lightweight query generation
* Basic provenance-field validation

Do not give nano responsibility for:

* Scientific conclusions
* Warrant approval
* Complex graph-distance interpretation
* Ambiguous planning
* Final contradiction resolution

There is also an older **GPT-5 nano** at only $0.05 input and $0.40 output, but it is a much older and weaker tier. ([OpenAI Developers][6]) For a new implementation, I would prefer GPT-5.4 nano unless your evaluation demonstrates that the older model is sufficiently reliable for a tightly constrained task.

## 7. Memory graph: use embeddings, not an LLM for every distance

For the RTG-style memory and resonance graph, an embedding model should provide the inexpensive initial semantic-distance signal.

### `text-embedding-3-large`

* $0.13 per million tokens
* OpenAI's most capable current embedding model
* Intended for search, clustering, recommendations, classification and relatedness
* Stronger for English and non-English material ([OpenAI Developers][7])

### `text-embedding-3-small`

* $0.02 per million tokens
* Suitable for large-scale indexing and initial candidate retrieval ([OpenAI Developers][8])

For AI-Lab, I would initially use:

```text
text-embedding-3-large
```

The cost difference is tiny compared with generation-model costs, while retrieval quality is foundational to the memory system.

A sensible retrieval sequence would be:

```text
1. Embedding similarity produces the initial candidate neighbourhood.
2. Metadata and graph edges apply deterministic boosts or penalties.
3. GPT-5.6 Luna reranks the top candidates.
4. Terra evaluates difficult or ambiguous relationships.
5. Sol is used only for critical adjudication.
```

## Recommended AI-Lab routing policy

```yaml
models:
  bulk_extraction: gpt-5.4-nano
  default_reasoning: gpt-5.6-luna
  advanced_reasoning: gpt-5.6-terra
  critical_adjudication: gpt-5.6-sol
  repository_implementation: gpt-5.3-codex
  semantic_embedding: text-embedding-3-large
```

Suggested escalation:

```text
GPT-5.4 nano
    ↓ insufficient confidence or task not narrow
GPT-5.6 Luna
    ↓ ambiguity, contradiction, or high complexity
GPT-5.6 Terra
    ↓ critical consequence or unresolved conflict
GPT-5.6 Sol
```

## My concrete recommendation

For a first migration, I would introduce only four models:

1. **`gpt-5.6-luna`** — default
2. **`gpt-5.6-terra`** — advanced advisor
3. **`gpt-5.6-sol`** — rare escalation
4. **`text-embedding-3-large`** — memory and retrieval

Then add **`gpt-5.3-codex`** when AI-Lab starts delegating repository implementation directly to an API coding agent.

The most important conclusion is that **GPT-5.6 Luna appears to be a better default than GPT-5 for AI-Lab**, while Terra provides the cost-controlled middle layer that was missing from a simple GPT-5 versus GPT-5.5 design.

[1]: https://developers.openai.com/api/docs/models/gpt-5.6-luna?utm_source=chatgpt.com "GPT-5.6 Luna Model | OpenAI API"
[2]: https://developers.openai.com/api/docs/models/gpt-5.6-terra?utm_source=chatgpt.com "GPT-5.6 Terra Model | OpenAI API"
[3]: https://developers.openai.com/api/docs/models/gpt-5.6-sol?utm_source=chatgpt.com "GPT-5.6 Sol Model | OpenAI API"
[4]: https://developers.openai.com/api/docs/models/gpt-5.3-codex?utm_source=chatgpt.com "GPT-5.3-Codex Model | OpenAI API"
[5]: https://openai.com/index/introducing-gpt-5-4-mini-and-nano/?utm_source=chatgpt.com "Introducing GPT-5.4 mini and nano"
[6]: https://developers.openai.com/api/docs/models/gpt-5-nano?utm_source=chatgpt.com "GPT-5 nano Model | OpenAI API"
[7]: https://developers.openai.com/api/docs/models/text-embedding-3-large?utm_source=chatgpt.com "text-embedding-3-large Model | OpenAI API"
[8]: https://developers.openai.com/api/docs/models/text-embedding-3-small?utm_source=chatgpt.com "text-embedding-3-small Model | OpenAI API"
