"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bohlcv.proto\x12\x1caea.eightballer.ohlcv.v0_1_0"\xd4\n\n\x0cOhlcvMessage\x12Z\n\x0bcandlestick\x18\x05 \x01(\x0b2C.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.Candlestick_PerformativeH\x00\x12J\n\x03end\x18\x06 \x01(\x0b2;.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.End_PerformativeH\x00\x12N\n\x05error\x18\x07 \x01(\x0b2=.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.Error_PerformativeH\x00\x12R\n\x07history\x18\x08 \x01(\x0b2?.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.History_PerformativeH\x00\x12V\n\tsubscribe\x18\t \x01(\x0b2A.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.Subscribe_PerformativeH\x00\x1a\xe4\x01\n\tErrorCode\x12V\n\nerror_code\x18\x01 \x01(\x0e2B.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.ErrorCode.ErrorCodeEnum"\x7f\n\rErrorCodeEnum\x12\x18\n\x14UNSUPPORTED_PROTOCOL\x10\x00\x12\x12\n\x0eDECODING_ERROR\x10\x01\x12\x13\n\x0fINVALID_MESSAGE\x10\x02\x12\x15\n\x11UNSUPPORTED_SKILL\x10\x03\x12\x14\n\x10INVALID_DIALOGUE\x10\x04\x1aT\n\x16Subscribe_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x13\n\x0bmarket_name\x18\x02 \x01(\t\x12\x10\n\x08interval\x18\x03 \x01(\x05\x1a\xb1\x01\n\x18Candlestick_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x13\n\x0bmarket_name\x18\x02 \x01(\t\x12\x10\n\x08interval\x18\x03 \x01(\x05\x12\x0c\n\x04open\x18\x04 \x01(\x01\x12\x0c\n\x04high\x18\x05 \x01(\x01\x12\x0b\n\x03low\x18\x06 \x01(\x01\x12\r\n\x05close\x18\x07 \x01(\x01\x12\x0e\n\x06volume\x18\x08 \x01(\x01\x12\x11\n\ttimestamp\x18\t \x01(\x05\x1a\x82\x01\n\x14History_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x13\n\x0bmarket_name\x18\x02 \x01(\t\x12\x17\n\x0fstart_timestamp\x18\x03 \x01(\x05\x12\x15\n\rend_timestamp\x18\x04 \x01(\x05\x12\x10\n\x08interval\x18\x05 \x01(\x05\x1a\x85\x02\n\x12Error_Performative\x12H\n\nerror_code\x18\x01 \x01(\x0b24.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12`\n\nerror_data\x18\x03 \x03(\x0b2L.aea.eightballer.ohlcv.v0_1_0.OhlcvMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01\x1a\x12\n\x10End_PerformativeB\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ohlcv_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_OHLCVMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_OHLCVMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_OHLCVMESSAGE']._serialized_start = 46
    _globals['_OHLCVMESSAGE']._serialized_end = 1410
    _globals['_OHLCVMESSAGE_ERRORCODE']._serialized_start = 483
    _globals['_OHLCVMESSAGE_ERRORCODE']._serialized_end = 711
    _globals['_OHLCVMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 584
    _globals['_OHLCVMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 711
    _globals['_OHLCVMESSAGE_SUBSCRIBE_PERFORMATIVE']._serialized_start = 713
    _globals['_OHLCVMESSAGE_SUBSCRIBE_PERFORMATIVE']._serialized_end = 797
    _globals['_OHLCVMESSAGE_CANDLESTICK_PERFORMATIVE']._serialized_start = 800
    _globals['_OHLCVMESSAGE_CANDLESTICK_PERFORMATIVE']._serialized_end = 977
    _globals['_OHLCVMESSAGE_HISTORY_PERFORMATIVE']._serialized_start = 980
    _globals['_OHLCVMESSAGE_HISTORY_PERFORMATIVE']._serialized_end = 1110
    _globals['_OHLCVMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 1113
    _globals['_OHLCVMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 1374
    _globals['_OHLCVMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 1326
    _globals['_OHLCVMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 1374
    _globals['_OHLCVMESSAGE_END_PERFORMATIVE']._serialized_start = 1376
    _globals['_OHLCVMESSAGE_END_PERFORMATIVE']._serialized_end = 1394