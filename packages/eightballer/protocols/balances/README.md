# Balances Protocol

## Description
A protocol for passing balance data between agent components.

## Specification

```yaml
name: balances
author: eightballer
version: 0.1.0
description: A protocol for passing balance data between agent components.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/balances:0.1.0
speech_acts:
  get_all_balances:
    params: pt:optional[pt:dict[pt:str, pt:bytes]]
    exchange_id: pt:optional[pt:str]
    ledger_id: pt:optional[pt:str]
    address: pt:optional[pt:str]
  get_balance:
    asset_id: pt:str
    exchange_id: pt:optional[pt:str]
    ledger_id: pt:optional[pt:str]
    address: pt:optional[pt:str]
  all_balances:
    balances: ct:Balances
    ledger_id: pt:optional[pt:str]
    exchange_id: pt:optional[pt:str]
  balance:
    balance: ct:Balance
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:dict[pt:str, pt:bytes]
...
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
      UNKNOWN_EXCHANGE = 0;
      UNKNOWN_ASSET = 1;
      API_ERROR = 2;
    }
  ErrorCodeEnum error_code = 1;
ct:Balance: |
      string asset_id = 1;
      float free = 2;
      float used = 3;
      float total = 4;
      bool is_native = 5;
      optional string contract_address = 6;
ct:Balances: |
      repeated Balance balances = 1;
...
---
initiation: [get_all_balances, get_balance]
reply:
  get_all_balances: [all_balances, error]
  get_balance: [balance, error]
  balance: [ ]
  all_balances: [ ]
  error: [ ]
termination: [balance, all_balances, error]
roles: { agent }
end_states: [ balance, all_balances, error ]
keep_terminal_state_dialogues: false
```