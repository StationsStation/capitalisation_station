## Audit of PR-158 and PR-162

**Scope:** only the changes from `audit/pr-158.patch` and `audit/pr-162.patch`, as well as their descriptions `pr-158-desc.txt` and `pr-162-desc.txt`.  
**Goals:** assess factual correctness, security (under a trusted environment), and performance impact.

---

### 1. PR-158 — Portfolio value persistence

- **Implemented functionality**
  - Adds a `db_models.py` module with a `PortfolioValue` model and a `PortfolioDatabase` wrapper for storing snapshots.
  - In `ArbitrageStrategy.__init__` and `CollectDataRound.act`, initializes the DB and computes/persists the total portfolio value in the quote asset (USDC).

- **Factual correctness**
  - **Datetime and timezone.** Uses `datetime.datetime.now(tz=datetime.timezone.utc)` when no explicit timestamp is provided — this is compatible with Python 3.9+ and does not cause issues.
  - **`PortfolioDatabase.get_timeseries` interface.** Signature: `get_timeseries(column: str, limit: int = 300) -> list[tuple]`. The column is selected via `getattr(PortfolioValue, column)`, which is fragile (an invalid name will raise), but the failure is localized and easy to diagnose. It is recommended to either validate column names against an explicit allowlist or encapsulate column selection.
  - **Hard assumption of two venues.** `CollectDataRound` explicitly assumes there are exactly two trading venues:
    - checks like `len(base_asset_holdings) == 2`, `len(quote_asset_holdings) == 2`, `len(base_asset_tickers) == 2`, `len(quote_asset_denominated_value) == 2`;
    - when this invariant is violated, no data is persisted and only a diagnostic log is written.
    - This works as a “data completeness” signal but hardcodes the “2 venues” invariant and will silently stop persisting data if the configuration changes.
  - **Ticker case sensitivity.** The code contains a `TODO: case incensitive matching`, but actual matching requires exact equality `base_asset == strategy_base_asset` and `quote_asset == strategy_quote_asset`. The “case-insensitive matching (weETH/WEETH)” promised in the PR description is not implemented — a discrepancy between description and implementation.

- **Security**
  - Uses SQLAlchemy ORM without raw SQL; injection risk in a trusted configuration is minimal.
  - The SQLite path (`sqlite:///../data/agent_data.db`) is created via `Path(...).parent.mkdir(parents=True, exist_ok=True)`, which is safe given a trusted filesystem.
  - The PR does not bake SQLite-specific options into the generic engine configuration (no `connect_args` etc.), which keeps DB backend portability reasonable.

- **Performance**
  - Portfolio value is computed by iterating through `self.strategy.state.portfolio` and `self.strategy.state.prices` with several nested loops. For a typical arbitrage bot, the data volume is small and CPU impact is expected to be low.
  - Writing a single snapshot to SQLite at the end of `CollectDataRound` is inexpensive. At very high round frequencies it might be worth:
    - batching writes, or
    - offloading persistence to a separate worker/queue.

- **Code quality notes**
  - `ArbitrageStrategy.__init__` contains a comment with profanity (**"fucking _context"**). It has no runtime effect but is undesirable in audited or externally reviewed code.

---

### 2. PR-162 — HTTP `/metrics` and runtime strategy parameter updates

- **Implemented functionality**
  - In `trading_state.handlers.HttpHandler`:
    - `GET /metrics` returns current state/parameters;
    - `POST /metrics` accepts JSON with partial parameter updates.
  - In `simple_fsm.strategy`:
    - defines a `TypedDict ArbitrageStrategyParams`;
    - coerces initial strategy parameters to this type;
    - in `AgentState.to_json`, current `trading_strategy` parameters are serialized via `asdict(...)` filtered by `ArbitrageStrategyParams`.
  - In `CoolDownRound`, updates are applied in a deferred manner: the POST handler stores updated parameters in `agent_state.arbitrage_strategy_params_update_request`, and `CoolDownRound.act` pulls them, clears the slot, and calls `replace(current_params, **typed_params)` (atomic dataclass instance swap).

- **Factual issues**
  - **Critical HTTP routing bug.**  
    `_handle_request` uses:
    ```python
    if http_msg.method == "get" and http_msg.url.find("/metrics"):
        ...
    elif http_msg.method == "post" and http_msg.url.find("/metrics"):
        ...
    ```
    - `str.find` returns `0` when the substring is at the start (which is `False` in a boolean context) and `-1` when not found (which is `True`).
    - As a result, requests to `"/metrics"`/`"/metrics?...“` never reach the GET/POST branches, while some unrelated URLs may erroneously be treated as matches.
    - **Recommendation:** replace with `if "/metrics" in http_msg.url:` or, preferably, `if http_msg.url.startswith("/metrics"):`.
  - **API mismatch with `PortfolioDatabase.get_timeseries`.**  
    In `AgentState.to_json`:
    ```python
    datetime_timeseries = portfolio_db.get_timeseries(column="total_usd_val", days=7)
    ```
    But in `PortfolioDatabase` (PR-158):
    ```python
    def get_timeseries(self, column: str, limit: int = 300) -> list[tuple]:
    ```
    - The `days` parameter does not exist, so with both PRs merged this will raise a `TypeError` on the first `to_json` call.
    - **Recommendations (one of):**
      - extend `get_timeseries` to `(column: str, days: int | None = None, limit: int | None = None)` and implement time-window filtering; or
      - keep only `limit` and implement “7 days” logic at a higher layer, where time semantics are known.
  - **Assumption that `trading_strategy` is always set.**  
    `AgentState.to_json` assumes `self.arbitrage_strategy.trading_strategy` is always a dataclass instance (via `asdict(trading_strategy)`), but in `ArbitrageStrategy` the default is `None` and it is initialized in `SetupRound` only once. If `to_json` is called before the first successful `SetupRound`, this will raise a `TypeError`. This lifecycle invariant should at least be guarded by an explicit check and log.

- **Security**
  - **No authentication for `/metrics`.**
    - Anyone who can reach the agent’s HTTP port can issue `POST /metrics` and change trading parameters (base_asset, order_size, min_profit, etc.).
    - Within a fully trusted environment this may be acceptable, but if the port is exposed externally this is a real operational risk.
    - **Minimal measures:**
      - bind the endpoint to `localhost` only; and/or
      - introduce a simple shared secret (e.g. `X-Auth-Token` header).
  - **Input validation.**
    - `HttpHandler._handle_post` calls:
      ```python
      received_params = json.loads(http_msg.body)
      ```
      without `try/except`. Invalid JSON will raise and can crash the handler.
    - Afterwards, values are cast to types via `expected_type(value)` with error handling and logging; this reduces the risk of invalid types entering the strategy.
    - **Recommendation:** wrap JSON parsing and return HTTP 400/422 on error.

- **Performance**
  - All `/metrics`-related work and parameter updates happen per HTTP request and once per `CoolDownRound`, i.e. not on the hot path.
  - Calls to `get_type_hints(ArbitrageStrategyParams)` and `dataclasses.replace(...)` are relatively expensive but negligible at low request rates.
  - `self.context.logger.info(...)` on each update is useful for audit; at very high update frequencies the log level could be reduced.

---

### 3. Integration of the two PRs

- **Critical integration bug**
  - `AgentState.to_json` (PR-162) calls `get_timeseries(..., days=7)`, while `PortfolioDatabase.get_timeseries` (PR-158) expects `(column, limit)`.  
  - With both PRs enabled, this will immediately raise an exception during state serialization.

- **Important assumptions**
  - PR-158 hard-codes a two-venue model with “complete” data for both venues. This is fine if the architecture guarantees “exactly two”, but under configuration changes the logic will quietly stop persisting data.
  - PR-162 assumes `trading_strategy` is initialized by the time `to_json` is called, which depends on round ordering and successful execution.

---

### 4. Summary and recommendations

- **Merge-blocking issues**
  - Fix `GET/POST /metrics` routing (replace `.find` with `in` or `startswith`).
  - Align `get_timeseries` interfaces in PR‑158 and PR‑162 (add `days` support or change the call site).

- **Strongly recommended improvements**
  - Add error handling around `json.loads(http_msg.body)` and return appropriate HTTP error codes for invalid JSON.
  - Explicitly document and/or make configurable the “two venues” assumption in the snapshot logic (PR-158).
  - Remove or soften the profane comment in `ArbitrageStrategy.__init__`.
  - Add basic authentication or network restrictions for `/metrics` if the agent can be reached from untrusted networks.

- **Overall assessment**
  - **Correctness:** overall sound architecture, but with one critical and several medium-severity defects.
  - **Security (trusted environment):** acceptable, with no obvious “hard” vulnerabilities, but `/metrics` should be considered a sensitive surface.
  - **Performance:** no substantial regressions identified; localized optimizations may be useful as data volume grows.

