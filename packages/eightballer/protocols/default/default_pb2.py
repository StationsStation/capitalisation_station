"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rdefault.proto\x12\x1eaea.eightballer.default.v0_1_0"\xce\x06\n\x0eDefaultMessage\x12R\n\x05bytes\x18\x05 \x01(\x0b2A.aea.eightballer.default.v0_1_0.DefaultMessage.Bytes_PerformativeH\x00\x12N\n\x03end\x18\x06 \x01(\x0b2?.aea.eightballer.default.v0_1_0.DefaultMessage.End_PerformativeH\x00\x12R\n\x05error\x18\x07 \x01(\x0b2A.aea.eightballer.default.v0_1_0.DefaultMessage.Error_PerformativeH\x00\x1a\xe8\x01\n\tErrorCode\x12Z\n\nerror_code\x18\x01 \x01(\x0e2F.aea.eightballer.default.v0_1_0.DefaultMessage.ErrorCode.ErrorCodeEnum"\x7f\n\rErrorCodeEnum\x12\x18\n\x14UNSUPPORTED_PROTOCOL\x10\x00\x12\x12\n\x0eDECODING_ERROR\x10\x01\x12\x13\n\x0fINVALID_MESSAGE\x10\x02\x12\x15\n\x11UNSUPPORTED_SKILL\x10\x03\x12\x14\n\x10INVALID_DIALOGUE\x10\x04\x1a%\n\x12Bytes_Performative\x12\x0f\n\x07content\x18\x01 \x01(\x0c\x1a\x8d\x02\n\x12Error_Performative\x12L\n\nerror_code\x18\x01 \x01(\x0b28.aea.eightballer.default.v0_1_0.DefaultMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12d\n\nerror_data\x18\x03 \x03(\x0b2P.aea.eightballer.default.v0_1_0.DefaultMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01\x1a\x12\n\x10End_PerformativeB\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'default_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_DEFAULTMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_DEFAULTMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_DEFAULTMESSAGE']._serialized_start = 50
    _globals['_DEFAULTMESSAGE']._serialized_end = 896
    _globals['_DEFAULTMESSAGE_ERRORCODE']._serialized_start = 317
    _globals['_DEFAULTMESSAGE_ERRORCODE']._serialized_end = 549
    _globals['_DEFAULTMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 422
    _globals['_DEFAULTMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 549
    _globals['_DEFAULTMESSAGE_BYTES_PERFORMATIVE']._serialized_start = 551
    _globals['_DEFAULTMESSAGE_BYTES_PERFORMATIVE']._serialized_end = 588
    _globals['_DEFAULTMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 591
    _globals['_DEFAULTMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 860
    _globals['_DEFAULTMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 812
    _globals['_DEFAULTMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 860
    _globals['_DEFAULTMESSAGE_END_PERFORMATIVE']._serialized_start = 862
    _globals['_DEFAULTMESSAGE_END_PERFORMATIVE']._serialized_end = 880