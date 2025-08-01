# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: liquidity_provision.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x19liquidity_provision.proto\x12*aea.eightballer.liquidity_provision.v0_1_0\"\xe4\x10\n\x19LiquidityProvisionMessage\x12y\n\radd_liquidity\x18\x05 \x01(\x0b\x32`.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.Add_Liquidity_PerformativeH\x00\x12i\n\x05\x65rror\x18\x06 \x01(\x0b\x32X.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.Error_PerformativeH\x00\x12}\n\x0fliquidity_added\x18\x07 \x01(\x0b\x32\x62.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.Liquidity_Added_PerformativeH\x00\x12\x81\x01\n\x11liquidity_removed\x18\x08 \x01(\x0b\x32\x64.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.Liquidity_Removed_PerformativeH\x00\x12\x7f\n\x10liquidity_status\x18\t \x01(\x0b\x32\x63.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.Liquidity_Status_PerformativeH\x00\x12}\n\x0fquery_liquidity\x18\n \x01(\x0b\x32\x62.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.Query_Liquidity_PerformativeH\x00\x12\x7f\n\x10remove_liquidity\x18\x0b \x01(\x0b\x32\x63.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.Remove_Liquidity_PerformativeH\x00\x1a\xed\x01\n\tErrorCode\x12q\n\nerror_code\x18\x01 \x01(\x0e\x32].aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.ErrorCode.ErrorCodeEnum\"m\n\rErrorCodeEnum\x12\x10\n\x0cINVALID_POOL\x10\x00\x12\x11\n\rINVALID_TOKEN\x10\x01\x12\x17\n\x13INSUFFICIENT_AMOUNT\x10\x02\x12\x0b\n\x07TIMEOUT\x10\x03\x12\x11\n\rUNKNOWN_ERROR\x10\x04\x1a\xeb\x01\n\x1a\x41\x64\x64_Liquidity_Performative\x12\x0f\n\x07pool_id\x18\x01 \x01(\t\x12\x11\n\ttoken_ids\x18\x02 \x03(\t\x12\x0f\n\x07\x61mounts\x18\x03 \x03(\x05\x12\x17\n\x0fmin_mint_amount\x18\x04 \x01(\x05\x12\x10\n\x08\x64\x65\x61\x64line\x18\x05 \x01(\x05\x12\x11\n\tuser_data\x18\x06 \x01(\x0c\x12\x18\n\x10user_data_is_set\x18\x07 \x01(\x08\x12\x13\n\x0b\x65xchange_id\x18\x08 \x01(\t\x12\x11\n\tledger_id\x18\t \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\n \x01(\x08\x1a\xee\x01\n\x1dRemove_Liquidity_Performative\x12\x0f\n\x07pool_id\x18\x01 \x01(\t\x12\x11\n\ttoken_ids\x18\x02 \x03(\t\x12\x13\n\x0b\x62urn_amount\x18\x03 \x01(\x05\x12\x13\n\x0bmin_amounts\x18\x04 \x03(\x05\x12\x10\n\x08\x64\x65\x61\x64line\x18\x05 \x01(\x05\x12\x11\n\tuser_data\x18\x06 \x01(\x0c\x12\x18\n\x10user_data_is_set\x18\x07 \x01(\x08\x12\x13\n\x0b\x65xchange_id\x18\x08 \x01(\t\x12\x11\n\tledger_id\x18\t \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\n \x01(\x08\x1aq\n\x1cQuery_Liquidity_Performative\x12\x0f\n\x07pool_id\x18\x01 \x01(\t\x12\x13\n\x0b\x65xchange_id\x18\x02 \x01(\t\x12\x11\n\tledger_id\x18\x03 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x04 \x01(\x08\x1a\x46\n\x1cLiquidity_Added_Performative\x12\x0f\n\x07pool_id\x18\x01 \x01(\t\x12\x15\n\rminted_tokens\x18\x02 \x01(\x05\x1aK\n\x1eLiquidity_Removed_Performative\x12\x0f\n\x07pool_id\x18\x01 \x01(\t\x12\x18\n\x10received_amounts\x18\x02 \x03(\x05\x1a\x65\n\x1dLiquidity_Status_Performative\x12\x0f\n\x07pool_id\x18\x01 \x01(\t\x12\x19\n\x11\x63urrent_liquidity\x18\x02 \x01(\x05\x12\x18\n\x10\x61vailable_tokens\x18\x03 \x03(\x05\x1a\x8e\x01\n\x12\x45rror_Performative\x12\x63\n\nerror_code\x18\x01 \x01(\x0b\x32O.aea.eightballer.liquidity_provision.v0_1_0.LiquidityProvisionMessage.ErrorCode\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\tB\x0e\n\x0cperformativeb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'liquidity_provision_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_LIQUIDITYPROVISIONMESSAGE']._serialized_start = 74
    _globals['_LIQUIDITYPROVISIONMESSAGE']._serialized_end = 2222
    _globals['_LIQUIDITYPROVISIONMESSAGE_ERRORCODE']._serialized_start = 978
    _globals['_LIQUIDITYPROVISIONMESSAGE_ERRORCODE']._serialized_end = 1215
    _globals['_LIQUIDITYPROVISIONMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 1106
    _globals['_LIQUIDITYPROVISIONMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 1215
    _globals['_LIQUIDITYPROVISIONMESSAGE_ADD_LIQUIDITY_PERFORMATIVE']._serialized_start = 1218
    _globals['_LIQUIDITYPROVISIONMESSAGE_ADD_LIQUIDITY_PERFORMATIVE']._serialized_end = 1453
    _globals['_LIQUIDITYPROVISIONMESSAGE_REMOVE_LIQUIDITY_PERFORMATIVE']._serialized_start = 1456
    _globals['_LIQUIDITYPROVISIONMESSAGE_REMOVE_LIQUIDITY_PERFORMATIVE']._serialized_end = 1694
    _globals['_LIQUIDITYPROVISIONMESSAGE_QUERY_LIQUIDITY_PERFORMATIVE']._serialized_start = 1696
    _globals['_LIQUIDITYPROVISIONMESSAGE_QUERY_LIQUIDITY_PERFORMATIVE']._serialized_end = 1809
    _globals['_LIQUIDITYPROVISIONMESSAGE_LIQUIDITY_ADDED_PERFORMATIVE']._serialized_start = 1811
    _globals['_LIQUIDITYPROVISIONMESSAGE_LIQUIDITY_ADDED_PERFORMATIVE']._serialized_end = 1881
    _globals['_LIQUIDITYPROVISIONMESSAGE_LIQUIDITY_REMOVED_PERFORMATIVE']._serialized_start = 1883
    _globals['_LIQUIDITYPROVISIONMESSAGE_LIQUIDITY_REMOVED_PERFORMATIVE']._serialized_end = 1958
    _globals['_LIQUIDITYPROVISIONMESSAGE_LIQUIDITY_STATUS_PERFORMATIVE']._serialized_start = 1960
    _globals['_LIQUIDITYPROVISIONMESSAGE_LIQUIDITY_STATUS_PERFORMATIVE']._serialized_end = 2061
    _globals['_LIQUIDITYPROVISIONMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 2064
    _globals['_LIQUIDITYPROVISIONMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 2206
# @@protoc_insertion_point(module_scope)
