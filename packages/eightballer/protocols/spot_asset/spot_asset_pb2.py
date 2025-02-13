"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10spot_asset.proto\x12!aea.eightballer.spot_asset.v0_1_0"\xab\x0c\n\x10SpotAssetMessage\x12S\n\x03end\x18\x05 \x01(\x0b2D.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.End_PerformativeH\x00\x12W\n\x05error\x18\x06 \x01(\x0b2F.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Error_PerformativeH\x00\x12i\n\x0eget_spot_asset\x18\x07 \x01(\x0b2O.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Get_Spot_Asset_PerformativeH\x00\x12k\n\x0fget_spot_assets\x18\x08 \x01(\x0b2P.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Get_Spot_Assets_PerformativeH\x00\x12a\n\nspot_asset\x18\t \x01(\x0b2K.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Spot_Asset_PerformativeH\x00\x1a7\n\x07Decimal\x12\x0c\n\x04Base\x18\x01 \x01(\x05\x12\r\n\x05Float\x18\x02 \x01(\x02\x12\x0f\n\x07Display\x18\x03 \x01(\t\x1a\xed\x01\n\tErrorCode\x12_\n\nerror_code\x18\x01 \x01(\x0e2K.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.ErrorCode.ErrorCodeEnum"\x7f\n\rErrorCodeEnum\x12\x18\n\x14UNSUPPORTED_PROTOCOL\x10\x00\x12\x12\n\x0eDECODING_ERROR\x10\x01\x12\x13\n\x0fINVALID_MESSAGE\x10\x02\x12\x15\n\x11UNSUPPORTED_SKILL\x10\x03\x12\x14\n\x10INVALID_DIALOGUE\x10\x04\x1a@\n\x1bGet_Spot_Asset_Performative\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x1a\xed\x03\n\x17Spot_Asset_Performative\x12\x0c\n\x04name\x18\x01 \x01(\t\x12J\n\x05total\x18\x02 \x01(\x0b2;.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Decimal\x12I\n\x04free\x18\x03 \x01(\x0b2;.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Decimal\x12]\n\x18available_without_borrow\x18\x04 \x01(\x0b2;.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Decimal\x12N\n\tusd_value\x18\x05 \x01(\x0b2;.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Decimal\x12\x18\n\x10usd_value_is_set\x18\x06 \x01(\x08\x12L\n\x07decimal\x18\x07 \x01(\x0b2;.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.Decimal\x12\x16\n\x0edecimal_is_set\x18\x08 \x01(\x08\x1a3\n\x1cGet_Spot_Assets_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x1az\n\x12Error_Performative\x12Q\n\nerror_code\x18\x01 \x01(\x0b2=.aea.eightballer.spot_asset.v0_1_0.SpotAssetMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x1a\x12\n\x10End_PerformativeB\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spot_asset_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_SPOTASSETMESSAGE']._serialized_start = 56
    _globals['_SPOTASSETMESSAGE']._serialized_end = 1635
    _globals['_SPOTASSETMESSAGE_DECIMAL']._serialized_start = 565
    _globals['_SPOTASSETMESSAGE_DECIMAL']._serialized_end = 620
    _globals['_SPOTASSETMESSAGE_ERRORCODE']._serialized_start = 623
    _globals['_SPOTASSETMESSAGE_ERRORCODE']._serialized_end = 860
    _globals['_SPOTASSETMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 733
    _globals['_SPOTASSETMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 860
    _globals['_SPOTASSETMESSAGE_GET_SPOT_ASSET_PERFORMATIVE']._serialized_start = 862
    _globals['_SPOTASSETMESSAGE_GET_SPOT_ASSET_PERFORMATIVE']._serialized_end = 926
    _globals['_SPOTASSETMESSAGE_SPOT_ASSET_PERFORMATIVE']._serialized_start = 929
    _globals['_SPOTASSETMESSAGE_SPOT_ASSET_PERFORMATIVE']._serialized_end = 1422
    _globals['_SPOTASSETMESSAGE_GET_SPOT_ASSETS_PERFORMATIVE']._serialized_start = 1424
    _globals['_SPOTASSETMESSAGE_GET_SPOT_ASSETS_PERFORMATIVE']._serialized_end = 1475
    _globals['_SPOTASSETMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 1477
    _globals['_SPOTASSETMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 1599
    _globals['_SPOTASSETMESSAGE_END_PERFORMATIVE']._serialized_start = 1601
    _globals['_SPOTASSETMESSAGE_END_PERFORMATIVE']._serialized_end = 1619