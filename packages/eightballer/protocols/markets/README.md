# Markets Protocol

## Description

...

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
    string lowercase_id = 2;
    string symbol = 3;
    string base = 4;
    string quote = 5;
    string settle = 6;
    string base_id = 7;
    string quote_id = 8;
    string settle_id = 9;
    string type = 10;
    bool spot = 11;
    bool margin = 12;
    bool swap = 13;
    bool future = 14;
    bool option = 15;
    bool active = 16;
    bool contract = 17;
    bool linear = 18;
    bool inverse = 19;
    float taker = 20;
    float maker = 21;
    float contract_size = 22;
    float expiry = 23;
    string expiry_datetime = 24;
    float strike = 25;
    string option_type = 26;
    float precision = 27;
    string limits = 28;
    string info = 29;
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