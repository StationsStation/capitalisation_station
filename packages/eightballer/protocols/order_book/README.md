# Order Book Protocol

## Description

...

## Specification

```yaml
name: order_book
author: eightballer
version: 0.1.0
description: A protocol to enable agents to subscribe to order books and receive updates in real-time. This protocol facilitates monitoring changes in bid and ask prices along with their volumes for given trading pairs on specified exchanges.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/order_book:0.1.0
speech_acts:
  subscribe:
    exchange_id: pt:str
    symbol: pt:str
    precision: pt:optional[pt:str] # Precision or limit of order book depth to receive updates for.
    interval: pt:optional[pt:int] # Interval in milliseconds to receive updates.
  unsubscribe:
    exchange_id: pt:str
    symbol: pt:str
  order_book:
    order_book: ct:OrderBook
  get_depth:
    exchange_id: pt:str
    symbol: pt:str
  depth:
    exchange_id: pt:str
    bids: ct:PriceVol
    asks: ct:PriceVol
  error:
    error_msg: pt:str
...
---
ct:PriceVol: |
  repeated float price_vols = 1;

ct:OrderBook: |
  string exchange_id = 1;
  string symbol = 2;
  repeated PriceVol bids = 3;
  repeated PriceVol asks = 4;
  int32 timestamp = 5;
  string datetime = 6;
  int32 nonce = 7;
...
---
initiation: [subscribe,get_depth]
reply:
  subscribe: [order_book, error]
  order_book: [order_book, unsubscribe, error] # Allows continuous updates until unsubscribe.
  get_depth: [depth]
  depth: []
  unsubscribe: []
  error: []
termination: [unsubscribe, error, depth]
roles: {subscriber, publisher}
end_states: [unsubscribe, error]
keep_terminal_state_dialogues: false

```