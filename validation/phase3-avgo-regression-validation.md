# Phase 3 AVGO Regression Validation

## 1. Scope

Phase 3 tests the v0.2.x local tool layer against Broadcom's acquisition-driven semiconductor plus infrastructure-software profile. The run uses manually prepared local inputs and includes the v0.2.4 acquisition-accounting fix required by the first AVGO pass.

## 2. Commands Run

| Command | Result | Notes |
|---|---|---|
| Python compileall | Pass | Standard-library scripts compile. |
| AVGO ratio / DCF / peer comps / implied expectations | Pass | Four non-empty outputs generated. |
| Example, MRVL and NVDA four-tool regressions | Pass | No regression after the optional-field schema change. |
| Old-schema compatibility and invalid numeric checks | Pass | Optional fields remain backward compatible; malformed values fail. |
| Broad and narrow safety scans | Pass | No implementation-level safety issue. |

## 3. AVGO Regression Result

| Script | Result | Output | Notes |
|---|---:|---|---|
| Ratio calculator | Pass | `examples/real_tests/AVGO/outputs/avgo_ratio_output.md` | Includes GAAP, normalized, net-debt and acquisition-accounting evidence. |
| DCF sensitivity | Pass | `examples/real_tests/AVGO/outputs/avgo_dcf_sensitivity_output.md` | FCFE research approximation; no net-debt double subtraction. |
| Peer comps | Pass | `examples/real_tests/AVGO/outputs/avgo_peer_comps_output.md` | Preserves blended/core statistics and comparability metadata. |
| Implied expectations | Pass | `examples/real_tests/AVGO/outputs/avgo_implied_expectations_output.md` | Uses sourced normalized earnings and labels market data indicative. |

## 4. Example Regression Result

All four example scripts passed. The financial example now demonstrates acquisition-accounting fields using clearly fictional values.

## 5. MRVL Regression Result

All four MRVL scripts passed. New acquisition fields remain optional and unpopulated; the output does not invent values.

## 6. NVDA Regression Result

All four NVDA scripts passed. Existing cash-plus-short-term-investments and GAAP earnings cautions remain intact.

## 7. Safety Scan

Broad-scan hits were classified as:

1. Prohibitions, disclaimers and validation statements.
2. Official EDGAR source references or ordinary terms such as buybacks and customer orders.
3. Actual code risk: none.

The narrow Python scan found no network import, credential read, `os.environ`, subprocess, browser, broker, order-routing or trading-execution implementation.

## 8. Issues Found

| Issue | Severity | Category | Fix Applied | Needs v0.2.4? |
|---|---|---|---|---:|
| Acquisition-accounting fields absent from ratio schema | Medium | Implementation / schema | Added six optional fields and a dedicated ratio table | Yes; completed |
| Consolidated tools do not calculate segment profitability | Method limitation | Report-layer analysis | Explicitly documented; no unsupported model added | No |
| AVGO peer set is inherently heterogeneous | Method limitation | Valuation judgment | Blended/core separation and notes retained | No |
| One secondary market-data snapshot | Low | Evidence coverage | Marked indicative / pending cross-check | No |

## 9. Acceptance Criteria Review

| Criterion | Result | Evidence |
|---|---:|---|
| AVGO input and output set complete | Pass | Four inputs, four outputs and case report exist. |
| Source metadata and units retained | Pass | Inputs contain source, period, currency, basis and units. |
| Market timestamp/session retained | Pass | 2026-06-24 regular-close snapshot. |
| VMware and acquisition accounting explicit | Pass after fix | Dedicated AVGO report and ratio section. |
| GAAP / Non-GAAP not mixed | Pass | Both bases shown separately with caution. |
| Segment / AI narrative not mixed | Pass | AI semiconductor disclosure is distinguished from consolidated AI-only revenue. |
| Peer metadata used | Pass | Group, status, notes and inclusion flags are visible. |
| DCF and implied expectations correctly framed | Pass | FCFE bridge and reverse-engineering warnings are explicit. |
| No unsupported advice or unsafe code | Pass | Research-only outputs; safety scan passed. |
| No unresolved High/Medium implementation issue | Pass | Medium acquisition gap fixed; remaining items are Method limitations. |

## 10. Recommendation

- Phase 3 passed: Yes
- Ready for Phase 4 real-case review: Yes
- Need v0.2.4 before Phase 4: Yes; implemented and validated
- Remaining limitations: segment/SOTP analysis, peer comparability, normalized reconciliation quality and DCF assumptions remain analyst judgments.

