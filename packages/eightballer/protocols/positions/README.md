# Positions Protocol

## Description
A protocol for passing position data between agent components.

## Specification

```yaml
---

name: positions
author: eightballer
version: 0.1.0
description: A protocol for passing position data between agent components.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/positions:0.1.0
speech_acts:
  get_all_positions:
    exchange_id: pt:str
    params: pt:optional[pt:dict[pt:str, pt:bytes]]
    side: pt:optional[ct:PositionSide]
  get_position:
    position_id: pt:str
    exchange_id: pt:str
  all_positions:
    positions: ct:Positions
    exchange_id: pt:str
  position:
    position: ct:Position
    exchange_id: pt:str
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:dict[pt:str, pt:bytes]
...
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
      UNKNOWN_EXCHANGE = 0;
      UNKNOWN_POSITION = 1;
      API_ERROR = 2;
    }
  ErrorCodeEnum error_code = 1;
ct:PositionSide: |
  enum PositionSideEnum {
      LONG = 0;
      SHORT = 1;
    }
  PositionSideEnum position_side = 1;
ct:Position: |
    string id = 1;
    string symbol = 2;
    optional int64 timestamp = 3;
    optional string datetime = 4;
    optional int64 last_update_timestamp = 5;
    optional float initial_margin = 6;
    optional float initial_margin_percentage = 7;
    optional float maintenance_margin = 8;
    optional float maintenance_margin_percentage = 9;
    optional float entry_price = 10;
    optional float notional = 11;
    optional float leverage = 12;
    optional float unrealized_pnl = 13;
    optional float contracts = 14;
    optional float contract_size = 15;
    optional float margin_ratio = 16;
    optional float liquidation_price = 17;
    optional float mark_price = 18;
    optional float last_price = 19;
    optional float collateral = 20;
    optional string margin_mode = 21;
    optional PositionSide side = 22;
    optional float percentage = 23;
    optional string info = 24;
    optional float size = 25;
    optional string exchange_id = 26;
    optional string hedged = 27;
    optional float stop_loss_price = 28;
    optional float take_profit_price = 29;
ct:Positions: |
    repeated Position positions = 1;
...
---
initiation: [get_all_positions, get_position]
reply:
  get_all_positions: [all_positions, error]
  get_position: [position, error]
  position: [ ]
  all_positions: [ ]
  error: [ ]
termination: [position, all_positions, error]
roles: { agent }
end_states: [ position, all_positions, error ]
keep_terminal_state_dialogues: false
```