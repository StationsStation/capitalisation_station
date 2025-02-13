"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ebalances.proto\x12\x1faea.eightballer.balances.v0_1_0"\xf1\x0f\n\x0fBalancesMessage\x12b\n\x0call_balances\x18\x05 \x01(\x0b2J.aea.eightballer.balances.v0_1_0.BalancesMessage.All_Balances_PerformativeH\x00\x12X\n\x07balance\x18\x06 \x01(\x0b2E.aea.eightballer.balances.v0_1_0.BalancesMessage.Balance_PerformativeH\x00\x12T\n\x05error\x18\x07 \x01(\x0b2C.aea.eightballer.balances.v0_1_0.BalancesMessage.Error_PerformativeH\x00\x12j\n\x10get_all_balances\x18\x08 \x01(\x0b2N.aea.eightballer.balances.v0_1_0.BalancesMessage.Get_All_Balances_PerformativeH\x00\x12`\n\x0bget_balance\x18\t \x01(\x0b2I.aea.eightballer.balances.v0_1_0.BalancesMessage.Get_Balance_PerformativeH\x00\x1a\x8d\x01\n\x07Balance\x12\x10\n\x08asset_id\x18\x01 \x01(\t\x12\x0c\n\x04free\x18\x02 \x01(\x02\x12\x0c\n\x04used\x18\x03 \x01(\x02\x12\r\n\x05total\x18\x04 \x01(\x02\x12\x11\n\tis_native\x18\x05 \x01(\x08\x12\x1d\n\x10contract_address\x18\x06 \x01(\tH\x00\x88\x01\x01B\x13\n\x11_contract_address\x1aV\n\x08Balances\x12J\n\x08balances\x18\x01 \x03(\x0b28.aea.eightballer.balances.v0_1_0.BalancesMessage.Balance\x1a\xb2\x01\n\tErrorCode\x12\\\n\nerror_code\x18\x01 \x01(\x0e2H.aea.eightballer.balances.v0_1_0.BalancesMessage.ErrorCode.ErrorCodeEnum"G\n\rErrorCodeEnum\x12\x14\n\x10UNKNOWN_EXCHANGE\x10\x00\x12\x11\n\rUNKNOWN_ASSET\x10\x01\x12\r\n\tAPI_ERROR\x10\x02\x1a\xd8\x02\n\x1dGet_All_Balances_Performative\x12j\n\x06params\x18\x01 \x03(\x0b2Z.aea.eightballer.balances.v0_1_0.BalancesMessage.Get_All_Balances_Performative.ParamsEntry\x12\x15\n\rparams_is_set\x18\x02 \x01(\x08\x12\x13\n\x0bexchange_id\x18\x03 \x01(\t\x12\x1a\n\x12exchange_id_is_set\x18\x04 \x01(\x08\x12\x11\n\tledger_id\x18\x05 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x06 \x01(\x08\x12\x0f\n\x07address\x18\x07 \x01(\t\x12\x16\n\x0eaddress_is_set\x18\x08 \x01(\x08\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01\x1a\xb3\x01\n\x18Get_Balance_Performative\x12\x10\n\x08asset_id\x18\x01 \x01(\t\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x12\x1a\n\x12exchange_id_is_set\x18\x03 \x01(\x08\x12\x11\n\tledger_id\x18\x04 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x05 \x01(\x08\x12\x0f\n\x07address\x18\x06 \x01(\t\x12\x16\n\x0eaddress_is_set\x18\x07 \x01(\x08\x1a\xc6\x01\n\x19All_Balances_Performative\x12K\n\x08balances\x18\x01 \x01(\x0b29.aea.eightballer.balances.v0_1_0.BalancesMessage.Balances\x12\x11\n\tledger_id\x18\x02 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x03 \x01(\x08\x12\x13\n\x0bexchange_id\x18\x04 \x01(\t\x12\x1a\n\x12exchange_id_is_set\x18\x05 \x01(\x08\x1aa\n\x14Balance_Performative\x12I\n\x07balance\x18\x01 \x01(\x0b28.aea.eightballer.balances.v0_1_0.BalancesMessage.Balance\x1a\x91\x02\n\x12Error_Performative\x12N\n\nerror_code\x18\x01 \x01(\x0b2:.aea.eightballer.balances.v0_1_0.BalancesMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12f\n\nerror_data\x18\x03 \x03(\x0b2R.aea.eightballer.balances.v0_1_0.BalancesMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01B\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'balances_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_BALANCESMESSAGE_GET_ALL_BALANCES_PERFORMATIVE_PARAMSENTRY']._loaded_options = None
    _globals['_BALANCESMESSAGE_GET_ALL_BALANCES_PERFORMATIVE_PARAMSENTRY']._serialized_options = b'8\x01'
    _globals['_BALANCESMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_BALANCESMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_BALANCESMESSAGE']._serialized_start = 52
    _globals['_BALANCESMESSAGE']._serialized_end = 2085
    _globals['_BALANCESMESSAGE_BALANCE']._serialized_start = 554
    _globals['_BALANCESMESSAGE_BALANCE']._serialized_end = 695
    _globals['_BALANCESMESSAGE_BALANCES']._serialized_start = 697
    _globals['_BALANCESMESSAGE_BALANCES']._serialized_end = 783
    _globals['_BALANCESMESSAGE_ERRORCODE']._serialized_start = 786
    _globals['_BALANCESMESSAGE_ERRORCODE']._serialized_end = 964
    _globals['_BALANCESMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 893
    _globals['_BALANCESMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 964
    _globals['_BALANCESMESSAGE_GET_ALL_BALANCES_PERFORMATIVE']._serialized_start = 967
    _globals['_BALANCESMESSAGE_GET_ALL_BALANCES_PERFORMATIVE']._serialized_end = 1311
    _globals['_BALANCESMESSAGE_GET_ALL_BALANCES_PERFORMATIVE_PARAMSENTRY']._serialized_start = 1266
    _globals['_BALANCESMESSAGE_GET_ALL_BALANCES_PERFORMATIVE_PARAMSENTRY']._serialized_end = 1311
    _globals['_BALANCESMESSAGE_GET_BALANCE_PERFORMATIVE']._serialized_start = 1314
    _globals['_BALANCESMESSAGE_GET_BALANCE_PERFORMATIVE']._serialized_end = 1493
    _globals['_BALANCESMESSAGE_ALL_BALANCES_PERFORMATIVE']._serialized_start = 1496
    _globals['_BALANCESMESSAGE_ALL_BALANCES_PERFORMATIVE']._serialized_end = 1694
    _globals['_BALANCESMESSAGE_BALANCE_PERFORMATIVE']._serialized_start = 1696
    _globals['_BALANCESMESSAGE_BALANCE_PERFORMATIVE']._serialized_end = 1793
    _globals['_BALANCESMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 1796
    _globals['_BALANCESMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 2069
    _globals['_BALANCESMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 2021
    _globals['_BALANCESMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 2069