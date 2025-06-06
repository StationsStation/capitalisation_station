# Markets Protocol

## Description
A protocol for passing ohlcv data between compoents.

## Specification

```yaml
---

name: markets
author: eightballer
version: 0.1.0
description: A protocol for passing ohlcv data between compoents.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/markets:0.1.0
speech_acts:
  get_all_markets:
    exchange_id: pt:str
    currency: pt:optional[pt:str]
  get_market:
    id: pt:str
    exchange_id: pt:str
  all_markets:
    markets: ct:Markets
  market:
    market: ct:Market
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:dict[pt:str, pt:bytes]
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
ct:Market: |
    string id = 1;
    optional string lowercase_id = 2;
    optional string exchange_id = 3;
    optional string symbol = 4;
    optional string base = 5;
    optional string quote = 6;
    optional string settle = 7;
    optional string base_id = 8;
    optional string quote_id = 9;
    optional string settle_id = 10;
    optional string type = 11;
    optional bool spot = 12;
    optional bool margin = 13;
    optional bool swap = 14;
    optional bool future = 15;
    optional bool option = 16;
    optional bool active = 17;
    optional bool contract = 18;
    optional bool linear = 19;
    optional bool inverse = 20;
    optional float taker = 21;
    optional float maker = 22;
    optional float contract_size = 23;
    optional float expiry = 24;
    optional string expiry_datetime = 25;
    optional float strike = 26;
    optional string option_type = 27;
    optional float precision = 28;
    optional string limits = 29;
    optional string info = 30;
ct:Markets: |
    repeated Market markets = 1;
...
---
initiation: [get_all_markets]
reply:
  get_all_markets: [all_markets, error]
  get_market: [market, error]
  all_markets: []
  market: []
  error: [ ]
termination: [all_markets, market, error]
roles: { agent }
end_states: [ market, all_markets, error ]
keep_terminal_state_dialogues: false
```