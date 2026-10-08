# V4 Knowledge Base - End-to-End Validation Report

**Generated:** 2026-10-08T11:46:03Z
**API tested:** http://127.0.0.1:8000

## Summary

| Metric | Value |
|--------|-------|
| Total tests | 32 |
| Passed | 32 |
| Failed | 0 |
| Pass rate | 100.0% |
| KB diseases covered | 116/116 |
| LLM used | NO |
| External API used | NO |

## Group Summary

| Group | Tests | Pass | Fail | Status |
|-------|-------|------|------|--------|
| T01_DirectKnowledge | 5 | 5 | 0 | ALL PASS |
| T02_TreatmentIntent | 3 | 3 | 0 | ALL PASS |
| T03_PreventionIntent | 3 | 3 | 0 | ALL PASS |
| T04_SessionDialogue | 2 | 2 | 0 | ALL PASS |
| T05_HighConfVisual | 2 | 2 | 0 | ALL PASS |
| T06_UncertaintyPreservation | 2 | 2 | 0 | ALL PASS |
| T07_SafetyBounds | 2 | 2 | 0 | ALL PASS |
| T08_HealthyPath | 2 | 2 | 0 | ALL PASS |
| T09_FullCoverage | 2 | 2 | 0 | ALL PASS |
| T10_SourceProvenance | 3 | 3 | 0 | ALL PASS |
| T11_APIEndpoint | 4 | 4 | 0 | ALL PASS |
| T12_SessionContinuity | 2 | 2 | 0 | ALL PASS |

## Detailed Results

| Test ID | Group | Description | Status | Duration (ms) | Notes |
|---------|-------|-------------|--------|---------------|-------|
| T01.01 | T01_DirectKnowledge | Apple scab direct text query | PASS | 12 |  |
| T01.02 | T01_DirectKnowledge | Corn NLB direct text query | PASS | 1 |  |
| T01.03 | T01_DirectKnowledge | Tomato late blight direct text query | PASS | 1 |  |
| T01.04 | T01_DirectKnowledge | Wheat stripe rust direct text query | PASS | 1 |  |
| T01.05 | T01_DirectKnowledge | Citrus greening direct text query | PASS | 1 |  |
| T02.01 | T02_TreatmentIntent | Treatment text-only query | PASS | 1 |  |
| T02.02 | T02_TreatmentIntent | Treatment with high-confidence visual (corn NLB) | PASS | 1 |  |
| T02.03 | T02_TreatmentIntent | Treatment with visual (tomato EB) | PASS | 1 |  |
| T03.01 | T03_PreventionIntent | Prevention text-only query | PASS | 1 |  |
| T03.02 | T03_PreventionIntent | Prevention with visual context (grape BR) | PASS | 1 |  |
| T03.03 | T03_PreventionIntent | Prevention for wheat leaf rust | PASS | 1 |  |
| T04.01 | T04_SessionDialogue | Session: disease -> treatment carry-over | PASS | 2 |  |
| T04.02 | T04_SessionDialogue | Session: disease -> prevention carry-over | PASS | 2 |  |
| T05.01 | T05_HighConfVisual | High-confidence spot-check (5 disease-crop pairs) | PASS | 6 |  |
| T05.02 | T05_HighConfVisual | High-confidence cross-commodity spot-check (10 slugs) | PASS | 11 |  |
| T06.01 | T06_UncertaintyPreservation | Low-confidence predictions hedged (3 cases) | PASS | 3 |  |
| T06.02 | T06_UncertaintyPreservation | is_uncertain flag respected | PASS | 1 |  |
| T07.01 | T07_SafetyBounds | Incompatible crop-disease slug handled safely | PASS | 1 |  |
| T07.02 | T07_SafetyBounds | Nonexistent disease slug does not crash | PASS | 1 |  |
| T08.01 | T08_HealthyPath | Healthy plant: no disease treatment emitted | PASS | 1 |  |
| T08.02 | T08_HealthyPath | Healthy crop text query: no invented diseases | PASS | 1 |  |
| T09.01 | T09_FullCoverage | All 116 disease slugs reachable in KB | PASS | 0 |  |
| T09.02 | T09_FullCoverage | All 116 slugs produce non-empty text response | PASS | 135 |  |
| T10.01 | T10_SourceProvenance | All 116 KB records have >=1 source | PASS | 0 |  |
| T10.02 | T10_SourceProvenance | Response cites sources for known diseases (5 slugs) | PASS | 6 |  |
| T10.03 | T10_SourceProvenance | Source dicts have required fields | PASS | 2 |  |
| T11.01 | T11_APIEndpoint | POST /api/chat text query returns 200 + message | PASS | 29 |  |
| T11.02 | T11_APIEndpoint | API response includes knowledge_sources | PASS | 22 |  |
| T11.03 | T11_APIEndpoint | API response includes router.intent | PASS | 9 |  |
| T11.04 | T11_APIEndpoint | Empty API request returns 400 | PASS | 4 |  |
| T12.01 | T12_SessionContinuity | Session persists disease context across 2 turns | PASS | 37 |  |
| T12.02 | T12_SessionContinuity | Different session IDs are independent | PASS | 16 |  |

## Validation Constraints

- **No LLM used** - all responses are deterministic knowledge-base driven
- **No external APIs** - zero paid API calls
- **Uncertainty safety** - low-confidence predictions never promoted to confident diagnoses
- **Source provenance** - every disease record cites >=1 authoritative source
- **116-disease coverage** - every V4 taxonomy record is retrievable and produces a response
- **Session isolation** - different session IDs maintain independent state
