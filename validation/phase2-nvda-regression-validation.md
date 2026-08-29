# Phase 2 NVDA Regression Validation

## 1. Scope

This validation tests `stock-research-v0.2.2` against a second real-company dataset: NVIDIA Corporation (`NVDA`). It covers a mega-cap AI infrastructure company with high margins, elevated valuation, material stock-based compensation, a recent stock split, concentrated customers, and substantial Data Center exposure.

The validation uses manually prepared local CSV/JSON inputs. The four Python tools do not fetch data, access APIs, read credentials, connect to brokers, or execute trades.

Validation date: 2026-06-24

Python version: 3.9.6

## 2. Commands Run

| Command | Result | Notes |
|---|---:|---|
| `PYTHONPYCACHEPREFIX=/private/tmp/python-cache python3 -m compileall -q goodluck-stock-research/scripts` | Pass | The explicit cache prefix avoids the macOS sandbox restriction on the default bytecode cache directory. |
| Four example-data script commands | Pass | Ratio, DCF, peer comps, and implied expectations outputs were generated in `/private/tmp/stock-research-phase2/`. |
| Four MRVL script commands | Pass | Existing real-input regression remained compatible. |
| Four NVDA script commands | Pass | All NVDA outputs were generated from local inputs. |
| Broad repository keyword scan | Pass after review | Matches were limited to prohibitions, disclaimers, source guidance, validation text, and ordinary research terminology. |
| Narrow Python code scan | Pass | No network, credential, environment-secret, subprocess, broker, order-routing, or trade-execution code was found. |
| Output presence and non-empty check | Pass | All 12 regression outputs were present and non-empty. |

## 3. NVDA Regression Result

| Script | Result | Output | Notes |
|---|---:|---|---|
| `ratio_calculator.py` | Pass | `examples/real_tests/NVDA/outputs/nvda_ratio_output.md` | Preserved raw GAAP profitability, special-item warnings, SBC, share-count trend, margins, cash flow, and working-capital ratios without inventing normalized metrics. |
| `dcf_sensitivity.py` | Pass | `examples/real_tests/NVDA/outputs/nvda_dcf_sensitivity_output.md` | Used FCFE research approximation; enterprise value is not calculated and net debt is not subtracted. Output is framed as a pressure test, not a target-price promise. |
| `peer_comps_table.py` | Pass | `examples/real_tests/NVDA/outputs/nvda_peer_comps_output.md` | Derived forward growth is labeled by provenance. Human review remains necessary because the peer set is not uniformly comparable. |
| `implied_expectations.py` | Pass | `examples/real_tests/NVDA/outputs/nvda_implied_expectations_output.md` | Reverse-engineered revenue, earnings, and FCF scale-up requirements and explicitly stated that the output is not a forecast. |

The NVDA test correctly preserves the following distinction:

> AI-only revenue 未单独披露；data center revenue 可作为 AI-related exposure 的重要线索，但不能直接等同于 AI-only revenue。

## 4. Example Regression Result

All four example-data tools passed:

- Ratio calculator: Pass
- DCF sensitivity: Pass
- Peer comps table: Pass
- Implied expectations: Pass

The example DCF retained its FCFF bridge and net-debt subtraction. Unit labels, derived-growth provenance, disclaimers, and source metadata remained present.

## 5. MRVL Regression Result

All four MRVL real-input tools passed:

- Ratio calculator: Pass
- DCF sensitivity: Pass
- Peer comps table: Pass
- Implied expectations: Pass

The MRVL DCF retained its FCFE treatment and did not subtract net debt. Existing normalization warnings, amount units, per-share units, and derived forward-growth labels remained intact.

## 6. Safety Scan

| Check | Result | Notes |
|---|---:|---|
| Standard-library-only Python implementation | Pass | No third-party data, market, or networking package is imported. |
| No live API or web-fetch code | Pass | No `requests`, `urllib`, `http.client`, `socket`, `aiohttp`, `yfinance`, `openbb`, EDGAR client, or URL-opening implementation. |
| No credential handling | Pass | No API key, token, password, secret, keyring, or `os.environ` access. |
| No subprocess or external execution | Pass | No subprocess invocation or shell execution from the tools. |
| No broker or trading implementation | Pass | No broker connection, order routing, trade execution, buy, or sell logic. |
| Local file boundary | Pass | Tools read the user-specified local input and write the user-specified Markdown output. |

Broad-scan matches were manually reviewed. They were prohibitive documentation, source references, disclaimers, prior validation statements, or ordinary terms such as buybacks, customer orders, and buy/sell warnings.

## 7. Issues Found

| Issue | Severity | Category | Fix Applied | Needs v0.2.3? |
|---|---|---|---|---:|
| Net debt in the ratio tool uses cash and equivalents but cannot separately include marketable securities, which understates net cash for NVIDIA. | Medium | Schema / financial quality | No code change in Phase 2; documented as a method limitation in the NVDA report. | Yes |
| Peer output produces one blended summary without structured peer-group or comparability fields, so a mixed semiconductor set can create misleading medians. | Medium | Schema / peer methodology | No code change in Phase 2; report warns that medians require human comparability review. | Yes |
| Implied P/E expectations use reported GAAP net income even when material equity-security gains reduce earnings comparability. | Medium | Schema / valuation methodology | No code change in Phase 2; report identifies the need for a normalized earnings basis. | Yes |
| `OCF - capex` is an FCFE research approximation rather than a complete levered cash-flow model. | Method limitation | DCF methodology | Existing FCFE warning retained; no automatic adjustment attempted. | No |
| Forward revenue growth is mechanically derived from P/S ratios rather than sourced consensus. | Low | Market data | Existing `derived_from_ps_multiple` label retained. | No |

No High-severity issue was found. The three Medium issues are explicitly bounded method/schema limitations rather than silent calculation failures. They should be addressed in a focused v0.2.3 before adding another real-company regression.

## 8. Acceptance Criteria Review

| Criterion | Result | Evidence |
|---|---:|---|
| Four NVDA input files created | Pass | Financials, DCF assumptions, peer comps, and valuation inputs are present. |
| Four NVDA scripts run successfully | Pass | Each command exited successfully and produced Markdown. |
| Four NVDA outputs are non-empty | Pass | Ratio, DCF, peer, and implied-expectations reports contain results and limitations. |
| Inputs include source and source status | Pass | Official financial inputs are verified; secondary market inputs are indicative. |
| Market data includes timestamp, session, currency, and units | Pass | Regular-close timestamp, USD, `USD millions`, and `USD/share` are recorded. |
| Data Center revenue is not treated as AI-only revenue | Pass | The required distinction appears explicitly in the NVDA report. |
| DCF identifies FCFF/FCFE treatment | Pass | NVDA uses FCFE and does not subtract net debt. |
| Implied expectations are not presented as forecasts | Pass | Output describes a reverse-engineering framework and not a prediction model. |
| Peer comparability limitations are explicit | Pass | Weak comparability and blended-median limitations are documented. |
| No unsupported numeric input | Pass | Financial facts and market snapshots retain source and period/session metadata. |
| No direct buy/sell advice | Pass | Outputs remain research calculations and methodology review. |
| No API, scraping, broker, trade, or credential code | Pass | Static safety review and narrow Python scan passed. |
| Medium issues are handled or bounded | Pass with limitations | All Medium issues are documented with recommended v0.2.3 fixes; none silently invalidate arithmetic execution. |
| Example and MRVL regressions remain healthy | Pass | 8/8 prior-case script runs passed. |

## 9. Recommendation

- Phase 2 passed: Yes
- Ready for Phase 3 AVGO regression: No
- Need v0.2.3 before Phase 3: Yes
- Remaining limitations:
  - Net-cash analysis needs optional short-term investments or combined cash-and-investments support.
  - Peer comps need structured peer grouping and comparability metadata.
  - Implied P/E expectations need an optional normalized earnings basis.
  - Simplified FCFE DCF remains a pressure-test framework and requires analyst review of financing, taxes, working capital, and reinvestment.
  - Secondary market data and mechanically derived forward growth remain indicative and require cross-verification before formal investment use.

`stock-research-v0.2.2` remains suitable for research-grade local calculations when its source, methodology, and comparability limitations are carried into the final research report. Phase 3 should wait until the three Medium limitations are fixed in v0.2.3 or explicitly waived by the user.
