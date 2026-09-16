# T3.7 four-arm grant verification

Date: 2026-09-15

Verification is read from execution traces and served endpoint receipts, never
from configuration. A grant check is run before scoring each cell and its trace
receipt is attached to that cell.

| Arm | Required observed check |
|---|---|
| 1 — LLM alone | From the model session, attempt one classical-tool call and one foundation-model call. Both must produce recorded unavailable-capability refusals. No tool result may enter the context. |
| 2 — mechanical floors | The runner trace must contain zero model calls and only the pinned Floor C, Floor M and Floor M+ invocations declared for the cell. Any model-session event fails the grant check. |
| 3 — LLM plus classical | From the model session, make a classical call that returns a parseable result, then attempt a foundation-model call. The latter must return a recorded firewall refusal in the trace. A configuration claim or missing endpoint is not a refusal. |
| 4 — LLM plus classical plus foundation models | From the model session, make both a classical call and a foundation-model call. The foundation-model call must succeed with a parseable score, and its receipt must identify a served checkpoint whose SHA-256 and parameter count exactly match the tool card. A successful response from an unverified or undersized checkpoint fails. |

The arm 3 negative and arm 4 positive checks are a coupled control: the same
foundation-model capability denied to arm 3 must be demonstrably live and
identity-verified for arm 4. If either half fails, the contrast is not measured.

Persistent-memory disablement is checked from a fresh model session using a
prior-session marker. Arms 1, 3 and 4 must answer without the marker; arm 2 has
no model session and is checked by the zero-model-call trace predicate.

If arm 4's positive check fails for a cell, that cell is recorded as a coverage
failure. It is never assigned zero and never enters the arm 4 minus arm 3 paired
comparison as a scored null.
