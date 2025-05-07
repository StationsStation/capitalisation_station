# Spot Asset Protocol

## Description
A protocol for representing spot_assets.

## Specification

```yaml
name: spot_asset
author: eightballer
version: 0.1.0
description: A protocol for representing spot_assets.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/spot_asset:0.1.0
speech_acts:
  get_spot_asset:
    name: pt:str
    exchange_id: pt:str
  spot_asset:
    name: pt:str
    total: ct:Decimal
    free: ct:Decimal
    available_without_borrow: ct:Decimal
    usd_value: pt:optional[ct:Decimal]
    decimal: pt:optional[ct:Decimal]
  get_spot_assets:
    exchange_id: pt:str
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
  end: { }
...
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
      UNSUPPORTED_PROTOCOL = 0;
      DECODING_ERROR = 1;
      INVALID_MESSAGE = 2;
      UNSUPPORTED_SKILL = 3;
      INVALID_DIALOGUE = 4;
    }
  ErrorCodeEnum error_code = 1;
ct:Decimal: |
  int32 Base = 1;
  float Float = 2;
  string Display = 3;
...
---
initiation:
- get_spot_asset
- get_spot_assets
reply:
  get_spot_asset: [ spot_asset, error ]
  get_spot_assets: [ spot_asset, error, end]
  spot_asset: [ ]
  error: [ ]
  end: [ ]
termination: [ spot_asset, end, error ]
roles: { agent }
end_states: [ end, error, spot_asset]
keep_terminal_state_dialogues: true
...
```