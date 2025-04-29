# Asset Bridging Protocol

## Description
A minimal, atomic request-response protocol for cross‑chain asset bridging.

## Specification

```yaml
name: asset_bridging
author: zarathustra
version: 0.0.1
description: A minimal, atomic request-response protocol for cross‑chain asset bridging.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: zarathustra/asset_bridging:0.0.1
speech_acts:
  request_bridge:
    source_chain: pt:str
    target_chain: pt:str
    source_token: pt:str
    target_token: pt:optional[pt:str]
    bridge: pt:str
    kwargs: pt:optional[pt:dict[pt:str, pt:str]]
  bridge_status:
    status: ct:BridgeStatus
    tx_hash: pt:bytes
  request_status:
    tx_hash: pt:bytes
  error:
    code: ct:ErrorCode
    message: pt:str
...
---
ct:BridgeStatus: |
  enum BridgeStatusEnum {
      IN_PROGRESS = 0;
      PENDING_CLAIM = 1;
      COMPLETED = 2;
      FAILED = 3;
    }
  BridgeStatusEnum status = 1;
ct:ErrorCode: |
  enum ErrorCodeEnum {
      UNKNOWN_ROUTE = 0;
      OTHER_EXCEPTION = 1;
    }
  ErrorCodeEnum error_code = 1;
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