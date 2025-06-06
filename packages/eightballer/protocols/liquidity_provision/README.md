# Liquidity Provision Protocol

## Description
This protocol specifies interactions for managing liquidity in DeFi platforms, including adding and removing liquidity, and querying liquidity conditions.

## Specification

```yaml
name: liquidity_provision
author: eightballer
version: 0.1.0
description: This protocol specifies interactions for managing liquidity in DeFi platforms, including adding and removing liquidity, and querying liquidity conditions.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/liquidity_provision:0.1.0
speech_acts:
  add_liquidity:
    pool_id: pt:str
    token_ids: pt:list[pt:str]
    amounts: pt:list[pt:int]
    min_mint_amount: pt:int
    deadline: pt:int
    user_data: pt:optional[pt:bytes]
    exchange_id: pt:str
    ledger_id: pt:optional[pt:str]
  remove_liquidity:
    pool_id: pt:str
    token_ids: pt:list[pt:str]
    burn_amount: pt:int
    min_amounts: pt:list[pt:int]
    deadline: pt:int
    user_data: pt:optional[pt:bytes]
    exchange_id: pt:str
    ledger_id: pt:optional[pt:str]
  query_liquidity:
    pool_id: pt:str
    exchange_id: pt:str
    ledger_id: pt:optional[pt:str]
  liquidity_added:
    pool_id: pt:str
    minted_tokens: pt:int
  liquidity_removed:
    pool_id: pt:str
    received_amounts: pt:list[pt:int]
  liquidity_status:
    pool_id: pt:str
    current_liquidity: pt:int
    available_tokens: pt:list[pt:int]
  error:
    error_code: ct:ErrorCode
    description: pt:str
---
ct:ErrorCode:
  enum ErrorCodeEnum {
    INVALID_POOL = 0;
    INVALID_TOKEN = 1;
    INSUFFICIENT_AMOUNT = 2;
    TIMEOUT = 3;
    UNKNOWN_ERROR = 4;
  }
  ErrorCodeEnum error_code = 1;
---
initiation: [add_liquidity, remove_liquidity, query_liquidity]
reply:
  add_liquidity: [liquidity_added, error]
  remove_liquidity: [liquidity_removed, error]
  query_liquidity: [liquidity_status, error]
  liquidity_added: []
  liquidity_removed: []
  liquidity_status: []
  error: []
termination: [liquidity_added, liquidity_removed, liquidity_status, error]
roles: { liquidity_provider, liquidity_seeker }
end_states: [liquidity_added, liquidity_removed, liquidity_status, error]
keep_terminal_state_dialogues: false
```