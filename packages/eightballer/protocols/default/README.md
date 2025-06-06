# Default Protocol

## Description
A protocol for exchanging any bytes message.

## Specification

```yaml
name: default
author: eightballer
version: 0.1.0
description: A protocol for exchanging any bytes message.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/default:0.1.0
speech_acts:
  bytes:
    content: pt:bytes
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:dict[pt:str, pt:bytes]
  end: {}
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
initiation: [bytes, error]
reply:
  bytes: [bytes, error, end]
  error: []
  end: []
termination: [end, error]
roles: {agent}
end_states: [successful, failed]
keep_terminal_state_dialogues: true
```