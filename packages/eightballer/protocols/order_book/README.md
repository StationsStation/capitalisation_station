# Order Book Protocol

## Description
A protocol to enable agents to subscribe to order books and receive updates in real-time. This protocol facilitates monitoring changes in bid and ask prices along with their volumes for given trading pairs on specified exchanges.

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
  order_book_update:
    order_book: ct:OrderBook
  error:
    error_msg: pt:str
...
---
ct:OrderBook: |
  string exchange_id = 1;
  string symbol = 2;
  repeated int32 bids = 3;
  repeated int32 asks = 4;
  int32 timestamp = 5;
  string datetime = 6;
  int32 nonce = 7;
...
---
initiation: [subscribe,]
reply:
  subscribe: [order_book_update, error]
  order_book_update: [order_book_update, unsubscribe, error] # Allows continuous updates until unsubscribe.
  unsubscribe: []
  error: []
termination: [unsubscribe, error]
roles: {subscriber, publisher}
end_states: [unsubscribe, error]
keep_terminal_state_dialogues: false
```