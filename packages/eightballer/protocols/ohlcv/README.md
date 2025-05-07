# Ohlcv Protocol

## Description
A protocol for passing ohlcv data between compoents.

## Specification

```yaml
---
name: ohlcv
author: eightballer
version: 0.1.0
description: A protocol for passing ohlcv data between compoents.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/ohlcv:0.1.0
speech_acts:
  subscribe:
    exchange_id: pt:str
    market_name: pt:str
    interval: pt:int
  candlestick:
    exchange_id: pt:str
    market_name: pt:str
    interval: pt:int
    open: pt:float
    high: pt:float
    low: pt:float
    close: pt:float
    volume: pt:float
    timestamp: pt:int
  history:
    exchange_id: pt:str
    market_name: pt:str
    start_timestamp: pt:int
    end_timestamp: pt:int
    interval: pt:int
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:dict[pt:str, pt:bytes]
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
...
---
initiation: [subscribe]
reply:
  subscribe: [candlestick, error, end]
  candlestick: [end]
  history: [candlestick, error]
  error: [ ]
  end: [ ]
termination: [error, end]
roles: { agent }
end_states: [ end, error ]
keep_terminal_state_dialogues: true
```