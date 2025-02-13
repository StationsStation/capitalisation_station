# Tickers Protocol

## Description

...

## Specification

```yaml
---
name: tickers
author: eightballer
version: 0.1.0
description: A protocol for passing ticker data between agent components.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/tickers:0.1.0
speech_acts:
  get_all_tickers:
    exchange_id: pt:str
    ledger_id: pt:str
    params: pt:optional[pt:dict[pt:str, pt:bytes]]
  get_ticker:
    asset_id: pt:str
    exchange_id: pt:str
    ledger_id: pt:str
  all_tickers:
    tickers: ct:Tickers
  ticker:
    ticker: ct:Ticker
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:dict[pt:str, pt:bytes]
...
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
      UNKNOWN_EXCHANGE = 0;
      UNKNOWN_TICKER = 1;
      API_ERROR = 2;
    }
  ErrorCodeEnum error_code = 1;
ct:Ticker: |
    string symbol = 1;
    int64 timestamp = 2;
    string datetime = 3;
    float ask = 4;
    float bid = 5;
    optional string asset_a = 6;
    optional string asset_b = 7;
    optional float bid_volume = 8;
    optional float ask_volume = 9;
    optional float high = 10;
    optional float low = 11;
    optional float vwap = 12;
    optional float open = 13;
    optional float close = 14;
    optional float last = 15;
    optional float previous_close = 16;
    optional float change = 17;
    optional float percentage = 18;
    optional float average = 19;
    optional float base_volume = 20;
    optional float quote_volume = 21;
    optional string info = 22;
ct:Tickers: |
    repeated Ticker tickers = 1;
...
---
initiation: [get_all_tickers, get_ticker]
reply:
  get_all_tickers: [all_tickers, error]
  get_ticker: [ticker, error]
  ticker: [ ]
  all_tickers: [ ]
  error: [ ]
termination: [ticker, all_tickers, error]
roles: { agent }
end_states: [ ticker, all_tickers, error ]
keep_terminal_state_dialogues: false



```