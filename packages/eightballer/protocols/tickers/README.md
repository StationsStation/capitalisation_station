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
    optional float bid_volume = 6;
    optional float ask_volume = 7;
    optional float high = 8;
    optional float low = 9;
    optional float vwap = 10;
    optional float open = 11;
    optional float close = 12;
    optional float last = 13;
    optional float previous_close = 14;
    optional float change = 15;
    optional float percentage = 16;
    optional float average = 17;
    optional float base_volume = 18;
    optional float quote_volume = 19;
    optional string info = 20;
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