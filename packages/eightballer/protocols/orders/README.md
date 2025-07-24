# Orders Protocol

## Description
A protocol for representing orders.

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
    exchange_id: pt:optional[pt:str]
    ledger_id: pt:optional[pt:str]
  order_created:
    order: ct:Order
  cancel_order:
    order: ct:Order
    exchange_id: pt:optional[pt:str]
    ledger_id: pt:optional[pt:str]
  order_cancelled:
    order: ct:Order
  get_orders:
    symbol: pt:optional[pt:str]
    currency: pt:optional[pt:str]
    order_type: pt:optional[ct:OrderType]
    side: pt:optional[ct:OrderSide]
    status: pt:optional[ct:OrderStatus]
    exchange_id: pt:optional[pt:str]
    ledger_id: pt:optional[pt:str]
    account: pt:optional[pt:str]
  get_settlements:
    currency: pt:optional[pt:str]
    end_timestamp: pt:optional[pt:float]
    start_timestamp: pt:optional[pt:float]
    ledger_id: pt:optional[pt:str]
    exchange_id: pt:optional[pt:str]
  get_order:
    order: ct:Order
    exchange_id: pt:optional[pt:str]
    ledger_id: pt:optional[pt:str]
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
      NEW = 0;
      SUBMITTED = 1;
      OPEN = 2;
      PARTIALLY_FILLED = 3;
      CANCELLED = 4;
      FILLED = 5;
      CLOSED = 6;
      EXPIRED = 7;
      FAILED = 9;
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
    string symbol = 2;
    OrderStatus status = 3;
    OrderSide side = 4;
    OrderType type = 5;
    optional float price = 1;
    optional string exchange_id = 6;
    optional string id = 7;
    optional string client_order_id = 8;
    optional string info = 9;
    optional string ledger_id = 10;
    optional string asset_a = 11;
    optional string asset_b = 12;
    optional float timestamp = 13;
    optional string datetime = 14;
    optional string time_in_force = 15;
    optional bool post_only = 16;
    optional float last_trade_timestamp = 17;
    optional float stop_price = 18;
    optional float trigger_price = 19;
    optional float cost = 20;
    optional float amount = 21;
    optional float filled = 22;
    optional float remaining = 23;
    optional float fee = 24;
    optional float average = 25;
    optional string trades = 26;
    optional string fees = 27;
    optional float last_update_timestamp = 28;
    optional bool reduce_only = 29;
    optional float take_profit_price = 30;
    optional float stop_loss_price = 31;
    optional float immediate_or_cancel = 32;
ct:Orders: |
    repeated Order orders = 1;
...
---
initiation:
- create_order
- cancel_order
- get_order
- get_orders
- get_settlements
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