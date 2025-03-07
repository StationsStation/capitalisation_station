"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rmarkets.proto\x12\x1eaea.eightballer.markets.v0_1_0"\x92\x13\n\x0eMarketsMessage\x12^\n\x0ball_markets\x18\x05 \x01(\x0b2G.aea.eightballer.markets.v0_1_0.MarketsMessage.All_Markets_PerformativeH\x00\x12R\n\x05error\x18\x06 \x01(\x0b2A.aea.eightballer.markets.v0_1_0.MarketsMessage.Error_PerformativeH\x00\x12f\n\x0fget_all_markets\x18\x07 \x01(\x0b2K.aea.eightballer.markets.v0_1_0.MarketsMessage.Get_All_Markets_PerformativeH\x00\x12\\\n\nget_market\x18\x08 \x01(\x0b2F.aea.eightballer.markets.v0_1_0.MarketsMessage.Get_Market_PerformativeH\x00\x12T\n\x06market\x18\t \x01(\x0b2B.aea.eightballer.markets.v0_1_0.MarketsMessage.Market_PerformativeH\x00\x1a\xe8\x01\n\tErrorCode\x12Z\n\nerror_code\x18\x01 \x01(\x0e2F.aea.eightballer.markets.v0_1_0.MarketsMessage.ErrorCode.ErrorCodeEnum"\x7f\n\rErrorCodeEnum\x12\x18\n\x14UNSUPPORTED_PROTOCOL\x10\x00\x12\x12\n\x0eDECODING_ERROR\x10\x01\x12\x13\n\x0fINVALID_MESSAGE\x10\x02\x12\x15\n\x11UNSUPPORTED_SKILL\x10\x03\x12\x14\n\x10INVALID_DIALOGUE\x10\x04\x1a\xf2\x07\n\x06Market\x12\n\n\x02id\x18\x01 \x01(\t\x12\x19\n\x0clowercase_id\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0bexchange_id\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x13\n\x06symbol\x18\x04 \x01(\tH\x02\x88\x01\x01\x12\x11\n\x04base\x18\x05 \x01(\tH\x03\x88\x01\x01\x12\x12\n\x05quote\x18\x06 \x01(\tH\x04\x88\x01\x01\x12\x13\n\x06settle\x18\x07 \x01(\tH\x05\x88\x01\x01\x12\x14\n\x07base_id\x18\x08 \x01(\tH\x06\x88\x01\x01\x12\x15\n\x08quote_id\x18\t \x01(\tH\x07\x88\x01\x01\x12\x16\n\tsettle_id\x18\n \x01(\tH\x08\x88\x01\x01\x12\x11\n\x04type\x18\x0b \x01(\tH\t\x88\x01\x01\x12\x11\n\x04spot\x18\x0c \x01(\x08H\n\x88\x01\x01\x12\x13\n\x06margin\x18\r \x01(\x08H\x0b\x88\x01\x01\x12\x11\n\x04swap\x18\x0e \x01(\x08H\x0c\x88\x01\x01\x12\x13\n\x06future\x18\x0f \x01(\x08H\r\x88\x01\x01\x12\x13\n\x06option\x18\x10 \x01(\x08H\x0e\x88\x01\x01\x12\x13\n\x06active\x18\x11 \x01(\x08H\x0f\x88\x01\x01\x12\x15\n\x08contract\x18\x12 \x01(\x08H\x10\x88\x01\x01\x12\x13\n\x06linear\x18\x13 \x01(\x08H\x11\x88\x01\x01\x12\x14\n\x07inverse\x18\x14 \x01(\x08H\x12\x88\x01\x01\x12\x12\n\x05taker\x18\x15 \x01(\x02H\x13\x88\x01\x01\x12\x12\n\x05maker\x18\x16 \x01(\x02H\x14\x88\x01\x01\x12\x1a\n\rcontract_size\x18\x17 \x01(\x02H\x15\x88\x01\x01\x12\x13\n\x06expiry\x18\x18 \x01(\x02H\x16\x88\x01\x01\x12\x1c\n\x0fexpiry_datetime\x18\x19 \x01(\tH\x17\x88\x01\x01\x12\x13\n\x06strike\x18\x1a \x01(\x02H\x18\x88\x01\x01\x12\x18\n\x0boption_type\x18\x1b \x01(\tH\x19\x88\x01\x01\x12\x16\n\tprecision\x18\x1c \x01(\x02H\x1a\x88\x01\x01\x12\x13\n\x06limits\x18\x1d \x01(\tH\x1b\x88\x01\x01\x12\x11\n\x04info\x18\x1e \x01(\tH\x1c\x88\x01\x01B\x0f\n\r_lowercase_idB\x0e\n\x0c_exchange_idB\t\n\x07_symbolB\x07\n\x05_baseB\x08\n\x06_quoteB\t\n\x07_settleB\n\n\x08_base_idB\x0b\n\t_quote_idB\x0c\n\n_settle_idB\x07\n\x05_typeB\x07\n\x05_spotB\t\n\x07_marginB\x07\n\x05_swapB\t\n\x07_futureB\t\n\x07_optionB\t\n\x07_activeB\x0b\n\t_contractB\t\n\x07_linearB\n\n\x08_inverseB\x08\n\x06_takerB\x08\n\x06_makerB\x10\n\x0e_contract_sizeB\t\n\x07_expiryB\x12\n\x10_expiry_datetimeB\t\n\x07_strikeB\x0e\n\x0c_option_typeB\x0c\n\n_precisionB\t\n\x07_limitsB\x07\n\x05_info\x1aQ\n\x07Markets\x12F\n\x07markets\x18\x01 \x03(\x0b25.aea.eightballer.markets.v0_1_0.MarketsMessage.Market\x1a^\n\x1cGet_All_Markets_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x10\n\x08currency\x18\x02 \x01(\t\x12\x17\n\x0fcurrency_is_set\x18\x03 \x01(\x08\x1a:\n\x17Get_Market_Performative\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x1ac\n\x18All_Markets_Performative\x12G\n\x07markets\x18\x01 \x01(\x0b26.aea.eightballer.markets.v0_1_0.MarketsMessage.Markets\x1a\\\n\x13Market_Performative\x12E\n\x06market\x18\x01 \x01(\x0b25.aea.eightballer.markets.v0_1_0.MarketsMessage.Market\x1a\x8d\x02\n\x12Error_Performative\x12L\n\nerror_code\x18\x01 \x01(\x0b28.aea.eightballer.markets.v0_1_0.MarketsMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12d\n\nerror_data\x18\x03 \x03(\x0b2P.aea.eightballer.markets.v0_1_0.MarketsMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01B\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'markets_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_MARKETSMESSAGE']._serialized_start = 50
    _globals['_MARKETSMESSAGE']._serialized_end = 2500
    _globals['_MARKETSMESSAGE_ERRORCODE']._serialized_start = 533
    _globals['_MARKETSMESSAGE_ERRORCODE']._serialized_end = 765
    _globals['_MARKETSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 638
    _globals['_MARKETSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 765
    _globals['_MARKETSMESSAGE_MARKET']._serialized_start = 768
    _globals['_MARKETSMESSAGE_MARKET']._serialized_end = 1778
    _globals['_MARKETSMESSAGE_MARKETS']._serialized_start = 1780
    _globals['_MARKETSMESSAGE_MARKETS']._serialized_end = 1861
    _globals['_MARKETSMESSAGE_GET_ALL_MARKETS_PERFORMATIVE']._serialized_start = 1863
    _globals['_MARKETSMESSAGE_GET_ALL_MARKETS_PERFORMATIVE']._serialized_end = 1957
    _globals['_MARKETSMESSAGE_GET_MARKET_PERFORMATIVE']._serialized_start = 1959
    _globals['_MARKETSMESSAGE_GET_MARKET_PERFORMATIVE']._serialized_end = 2017
    _globals['_MARKETSMESSAGE_ALL_MARKETS_PERFORMATIVE']._serialized_start = 2019
    _globals['_MARKETSMESSAGE_ALL_MARKETS_PERFORMATIVE']._serialized_end = 2118
    _globals['_MARKETSMESSAGE_MARKET_PERFORMATIVE']._serialized_start = 2120
    _globals['_MARKETSMESSAGE_MARKET_PERFORMATIVE']._serialized_end = 2212
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 2215
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 2484
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 2436
    _globals['_MARKETSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 2484