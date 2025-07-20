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
  string request_id = 1;
  string source_ledger_id = 2;
  string target_ledger_id = 3;
  string source_token = 4;
  optional string target_token = 5;
  float amount = 6;
  string bridge = 7;
  optional string receiver = 8;
ct:BridgeResult: |
  enum Status {
      FAILED = 0;
      SUCCESS = 1;
      PENDING = 2;
      ERROR = 3;
      CLAIMABLE = 4;
    }
  BridgeRequest request = 1;
  optional string source_tx_hash = 2;
  optional string target_tx_hash = 3;
  optional uint64 target_from_block = 4;
  Status status = 5;
  map<string,string> extra_info = 6;
ct:ErrorInfo: |
  enum Code {
      INVALID_PERFORMATIVE = 0;
      CONNECTION_ERROR = 1;
      INVALID_ROUTE = 2;
      INVALID_PARAMETERS = 3;
      ALREADY_FINALIZED = 4;
      TX_SUBMISSION_FAILED = 5;
      OTHER_EXCEPTION = 6;
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