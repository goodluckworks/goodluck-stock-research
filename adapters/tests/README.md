# Local Adapter Tests

测试仅使用 Python 标准库和三个短小、人工构造的本地 HTML fixture。

```bash
python3 goodluck-stock-research/adapters/tests/run_local_adapter_tests.py
```

覆盖：

- MRVL、NVDA、AVGO evidence package。
- 必填输出文件与非空检查。
- SHA-256 与 raw snapshot 一致性。
- `source_status` / `data_status` 分离。
- unresolved financial fields。
- normalized draft 不包含财务数字。
- 默认 no-overwrite 与显式 overwrite 记录。
- `https://` source URL 仅保存为字符串。
- adapter 源码没有网络、环境密钥、subprocess、browser、broker 或交易 import/调用。

Expected JSON 文件保存每个 fixture 的稳定 metadata 和 checksum，用于防止 fixture 或契约无意漂移。

## SEC Adapter Tests

SEC adapter tests 默认也不联网：

```bash
python3 goodluck-stock-research/adapters/tests/run_sec_adapter_tests.py
```

覆盖 MRVL/NVDA/AVGO fixture、mocked live success、HTTP/timeout failure、SEC-only
URL 与 redirect、User-Agent、bounded retry、no-overwrite、raw snapshot 和
`draft_unpopulated` contract。真实 live smoke 不在默认测试中执行。
