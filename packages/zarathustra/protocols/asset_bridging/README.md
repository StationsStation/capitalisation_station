# Asset Bridging Protocol

## Description
A minimal, atomic request-response protocol for cross-chain asset bridging.

## Specification

```yaml
name: asset_bridging
author: zarathustra
version: 0.1.0
description: A minimal, atomic request-response protocol for cross-chain asset bridging.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: zarathustra/asset_bridging:0.1.0
speech_acts:
  request_bridge:
    request: ct:BridgeRequest
  bridge_status:
    result: ct:BridgeResult
  request_status:
    result: ct:BridgeResult
  error:
    info: ct:ErrorInfo
...
---
ct:BridgeRequest: |
  string source_ledger_id = 1;
  string target_ledger_id = 2;
  string source_token = 3;
  optional string target_token = 4;
  float amount = 5;
  string bridge = 6;
  optional string receiver = 7;
ct:BridgeResult: |
  enum Status {
      FAILED = 0;
      SUCCESS = 1;
      PENDING = 2;
      ERROR = 3;
      CLAIMABLE = 4;
    }
  string source_chain = 1;
  string target_chain = 2;
  optional string source_tx_hash = 3;
  optional string target_tx_hash = 4;
  optional uint64 target_from_block = 5;
  Status status = 6;
  map<string,string> extra_info = 7;
ct:ErrorInfo: |
  enum Code {
      INVALID_PERFORMATIVE = 0;
      CONNECTION_ERROR = 1;
      INVALID_ROUTE = 2;
      INVALID_PARAMETERS = 3;
      ALREADY_FINALIZED = 4;
      OTHER_EXCEPTION = 5;
    }
  Code code = 1;
  string message = 2;
...
---
initiation:
  - request_bridge
  - request_status
reply:
  request_bridge: [bridge_status, error]
  request_status: [bridge_status, error]
  bridge_status: []
  error: []
termination: [bridge_status, error]
roles: {agent, ledger}
end_states: [successful, failed]
keep_terminal_state_dialogues: false
```