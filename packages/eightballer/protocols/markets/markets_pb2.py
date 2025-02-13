"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rmarkets.proto\x12\x1eaea.eightballer.markets.v0_1_0"\x8e\x0f\n\x0eMarketsMessage\x12^\n\x0ball_markets\x18\x05 \x01(\x0b2G.aea.eightballer.markets.v0_1_0.MarketsMessage.All_Markets_PerformativeH\x00\x12R\n\x05error\x18\x06 \x01(\x0b2A.aea.eightballer.markets.v0_1_0.MarketsMessage.Error_PerformativeH\x00\x12f\n\x0fget_all_markets\x18\x07 \x01(\x0b2K.aea.eightballer.markets.v0_1_0.MarketsMessage.Get_All_Markets_PerformativeH\x00\x12\\\n\nget_market\x18\x08 \x01(\x0b2F.aea.eightballer.markets.v0_1_0.MarketsMessage.Get_Market_PerformativeH\x00\x12T\n\x06market\x18\t \x01(\x0b2B.aea.eightballer.markets.v0_1_0.MarketsMessage.Market_PerformativeH\x00\x1a\xe8\x01\n\tErrorCode\x12Z\n\nerror_code\x18\x01 \x01(\x0e2F.aea.eightballer.markets.v0_1_0.MarketsMessage.ErrorCode.ErrorCodeEnum"\x7f\n\rErrorCodeEnum\x12\x18\n\x14UNSUPPORTED_PROTOCOL\x10\x00\x12\x12\n\x0eDECODING_ERROR\x10\x01\x12\x13\n\x0fINVALID_MESSAGE\x10\x02\x12\x15\n\x11UNSUPPORTED_SKILL\x10\x03\x12\x14\n\x10INVALID_DIALOGUE\x10\x04\x1a\xee\x03\n\x06Market\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0clowercase_id\x18\x02 \x01(\t\x12\x0e\n\x06symbol\x18\x03 \x01(\t\x12\x0c\n\x04base\x18\x04 \x01(\t\x12\r\n\x05quote\x18\x05 \x01(\t\x12\x0e\n\x06settle\x18\x06 \x01(\t\x12\x0f\n\x07base_id\x18\x07 \x01(\t\x12\x10\n\x08quote_id\x18\x08 \x01(\t\x12\x11\n\tsettle_id\x18\t \x01(\t\x12\x0c\n\x04type\x18\n \x01(\t\x12\x0c\n\x04spot\x18\x0b \x01(\x08\x12\x0e\n\x06margin\x18\x0c \x01(\x08\x12\x0c\n\x04swap\x18\r \x01(\x08\x12\x0e\n\x06future\x18\x0e \x01(\x08\x12\x0e\n\x06option\x18\x0f \x01(\x08\x12\x0e\n\x06active\x18\x10 \x01(\x08\x12\x10\n\x08contract\x18\x11 \x01(\x08\x12\x0e\n\x06linear\x18\x12 \x01(\x08\x12\x0f\n\x07inverse\x18\x13 \x01(\x08\x12\r\n\x05taker\x18\x14 \x01(\x02\x12\r\n\x05maker\x18\x15 \x01(\x02\x12\x15\n\rcontract_size\x18\x16 \x01(\x02\x12\x0e\n\x06expiry\x18\x17 \x01(\x02\x12\x17\n\x0fexpiry_datetime\x18\x18 \x01(\t\x12\x0e\n\x06strike\x18\x19 \x01(\x02\x12\x13\n\x0boption_type\x18\x1a \x01(\t\x12\x11\n\tprecision\x18\x1b \x01(\x02\x12\x0e\n\x06limits\x18\x1c \x01(\t\x12\x0c\n\x04info\x18\x1d \x01(\t\x1aQ\n\x07Markets\x12F\n\x07markets\x18\x01 \x03(\x0b25.aea.eightballer.markets.v0_1_0.MarketsMessage.Market\x1a^\n\x1cGet_All_Markets_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x10\n\x08currency\x18\x02 \x01(\t\x12\x17\n\x0fcurrency_is_set\x18\x03 \x01(\x08\x1a:\n\x17Get_Market_Performative\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x1ac\n\x18All_Markets_Performative\x12G\n\x07markets\x18\x01 \x01(\x0b26.aea.eightballer.markets.v0_1_0.MarketsMessage.Markets\x1a\\\n\x13Market_Performative\x12E\n\x06market\x18\x01 \x01(\x0b25.aea.eightballer.markets.v0_1_0.MarketsMessage.Market\x1a\x8d\x02\n\x12Error_Performative\x12L\n\nerror_code\x18\x01 \x01(\x0b28.aea.eightballer.markets.v0_1_0.MarketsMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12d\n\nerror_data\x18\x03 \x03(\x0b2P.aea.eightballer.markets.v0_1_0.MarketsMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01B\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'markets_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_MARKETSMESSAGE']._serialized_start = 50
    _globals['_MARKETSMESSAGE']._serialized_end = 1984
    _globals['_MARKETSMESSAGE_ERRORCODE']._serialized_start = 533
    _globals['_MARKETSMESSAGE_ERRORCODE']._serialized_end = 765
    _globals['_MARKETSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 638
    _globals['_MARKETSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 765
    _globals['_MARKETSMESSAGE_MARKET']._serialized_start = 768
    _globals['_MARKETSMESSAGE_MARKET']._serialized_end = 1262
    _globals['_MARKETSMESSAGE_MARKETS']._serialized_start = 1264
    _globals['_MARKETSMESSAGE_MARKETS']._serialized_end = 1345
    _globals['_MARKETSMESSAGE_GET_ALL_MARKETS_PERFORMATIVE']._serialized_start = 1347
    _globals['_MARKETSMESSAGE_GET_ALL_MARKETS_PERFORMATIVE']._serialized_end = 1441
    _globals['_MARKETSMESSAGE_GET_MARKET_PERFORMATIVE']._serialized_start = 1443
    _globals['_MARKETSMESSAGE_GET_MARKET_PERFORMATIVE']._serialized_end = 1501
    _globals['_MARKETSMESSAGE_ALL_MARKETS_PERFORMATIVE']._serialized_start = 1503
    _globals['_MARKETSMESSAGE_ALL_MARKETS_PERFORMATIVE']._serialized_end = 1602
    _globals['_MARKETSMESSAGE_MARKET_PERFORMATIVE']._serialized_start = 1604
    _globals['_MARKETSMESSAGE_MARKET_PERFORMATIVE']._serialized_end = 1696
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 1699
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 1968
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 1920
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 1968