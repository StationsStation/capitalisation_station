# Orders Protocol

## Description

...

## Specification

```yaml
name: orders
author: eightballer
version: 0.1.0
description: A protocol for representing orders.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/orders:0.1.0
speech_acts:
  create_order:
    order: ct:Order
  order_created:
    order: ct:Order
  cancel_order:
    order: ct:Order
  order_cancelled:
    order: ct:Order
  get_orders:
    exchange_id: pt:str
    symbol: pt:optional[pt:str]
    currency: pt:optional[pt:str]
    order_type: pt:optional[ct:OrderType]
    side: pt:optional[ct:OrderSide]
    status: pt:optional[ct:OrderStatus]
  get_settlements:
    exchange_id: pt:str
    currency: pt:optional[pt:str]
    end_timestamp: pt:optional[pt:float]
    start_timestamp: pt:optional[pt:float]
  get_order:
    order: ct:Order
  order:
    order: ct:Order
  orders:
    orders: ct:Orders
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:dict[pt:str, pt:bytes]
...
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
      UNKNOWN_MARKET = 0;
      INSUFFICIENT_FUNDS = 1;
      UNKNOWN_ORDER = 2;
      API_ERROR = 3;
    }
  ErrorCodeEnum error_code = 1;
ct:OrderStatus: |
  enum OrderStatusEnum{
      SUBMITTED = 0;
      OPEN = 1;
      PARTIALLY_FILLED = 2;
      CANCELLED = 3;
      FILLED = 4;
      CLOSED = 5;
      EXPIRED = 6;
      FAILED = 8;
    }
  OrderStatusEnum order_status = 1;
ct:OrderType: |
  enum OrderTypeEnum{
      LIMIT = 0;
      MARKET = 1;
    }
  OrderTypeEnum order_type = 1;
ct:OrderSide: |
  enum OrderSideEnum{
      BUY = 0;
      SELL = 1;
    }
  OrderSideEnum order_side = 1;
ct:Order: | 
    string id = 1;
    string client_order_id = 2;
    string info = 3;
    float timestamp = 4;
    string datetime = 5;
    float last_trade_timestamp = 6;
    OrderStatus status = 7;
    string symbol = 8;
    OrderType type = 9;
    string time_in_force = 10;
    bool post_only = 11;
    OrderSide side = 12;
    float price = 13;
    float stop_price = 14;
    float trigger_price = 15;
    float cost = 16;
    float amount = 17;
    float filled = 18;
    float remaining = 19;
    float fee = 20;
    float average = 21;
    string trades = 22;
    string fees = 23;
    float last_update_timestamp = 24;
    bool reduce_only = 25;
    float take_profit_price = 26;
    float stop_loss_price = 27;
    string exchange_id = 28;
ct:Orders: |
    repeated Order orders = 1;
...
---
initiation:
- create_order
- cancel_order
- get_order
- get_orders
reply:
  create_order: [ order_created, error ]
  cancel_order: [ order_cancelled, error ]
  get_order: [ order, error ]
  get_orders: [ orders, error]
  get_settlements: [ orders, error]
  order_created: []
  order_cancelled: []
  order: []
  orders: []
  error: []
termination: [ error, order, orders, order_created, order_cancelled]
roles: { agent }
end_states: [ error]
keep_terminal_state_dialogues: false
...

```