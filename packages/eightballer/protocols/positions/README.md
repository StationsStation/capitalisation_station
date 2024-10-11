# Positions Protocol

## Description

...

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
ct:Positions: |
    repeated Position positions = 1;
ct:Position: |
    string id = 1;
    string symbol = 2;
    int64 timestamp = 3;
    string datetime = 4;
    int64 lastUpdateTimestamp = 5;
    float initialMargin = 6;
    float initialMarginPercentage = 7;
    float maintenanceMargin = 8;
    float maintenanceMarginPercentage = 9;
    float entryPrice = 10;
    float notional = 11;
    float leverage = 12;
    float unrealizedPnl = 13;
    float contracts = 14;
    float contractSize = 15;
    float marginRatio = 16;
    float liquidationPrice = 17;
    float markPrice = 18;
    float lastPrice = 19;
    float collateral = 20;
    string marginMode = 21;
    PositionSide side = 22;
    float percentage = 23;
    string info = 24;
    float size = 25;
    string exchange_id = 26;
    string hedged = 27;
    float stop_loss_price = 28;
    float take_profit_price = 29;
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