"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rtickers.proto\x12\x1eaea.eightballer.tickers.v0_1_0"\xe4\x13\n\x0eTickersMessage\x12^\n\x0ball_tickers\x18\x05 \x01(\x0b2G.aea.eightballer.tickers.v0_1_0.TickersMessage.All_Tickers_PerformativeH\x00\x12R\n\x05error\x18\x06 \x01(\x0b2A.aea.eightballer.tickers.v0_1_0.TickersMessage.Error_PerformativeH\x00\x12f\n\x0fget_all_tickers\x18\x07 \x01(\x0b2K.aea.eightballer.tickers.v0_1_0.TickersMessage.Get_All_Tickers_PerformativeH\x00\x12\\\n\nget_ticker\x18\x08 \x01(\x0b2F.aea.eightballer.tickers.v0_1_0.TickersMessage.Get_Ticker_PerformativeH\x00\x12T\n\x06ticker\x18\t \x01(\x0b2B.aea.eightballer.tickers.v0_1_0.TickersMessage.Ticker_PerformativeH\x00\x1a\xb1\x01\n\tErrorCode\x12Z\n\nerror_code\x18\x01 \x01(\x0e2F.aea.eightballer.tickers.v0_1_0.TickersMessage.ErrorCode.ErrorCodeEnum"H\n\rErrorCodeEnum\x12\x14\n\x10UNKNOWN_EXCHANGE\x10\x00\x12\x12\n\x0eUNKNOWN_TICKER\x10\x01\x12\r\n\tAPI_ERROR\x10\x02\x1a\x9f\x05\n\x06Ticker\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x10\n\x08datetime\x18\x03 \x01(\t\x12\x0b\n\x03ask\x18\x04 \x01(\x02\x12\x0b\n\x03bid\x18\x05 \x01(\x02\x12\x14\n\x07asset_a\x18\x06 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07asset_b\x18\x07 \x01(\tH\x01\x88\x01\x01\x12\x17\n\nbid_volume\x18\x08 \x01(\x02H\x02\x88\x01\x01\x12\x17\n\nask_volume\x18\t \x01(\x02H\x03\x88\x01\x01\x12\x11\n\x04high\x18\n \x01(\x02H\x04\x88\x01\x01\x12\x10\n\x03low\x18\x0b \x01(\x02H\x05\x88\x01\x01\x12\x11\n\x04vwap\x18\x0c \x01(\x02H\x06\x88\x01\x01\x12\x11\n\x04open\x18\r \x01(\x02H\x07\x88\x01\x01\x12\x12\n\x05close\x18\x0e \x01(\x02H\x08\x88\x01\x01\x12\x11\n\x04last\x18\x0f \x01(\x02H\t\x88\x01\x01\x12\x1b\n\x0eprevious_close\x18\x10 \x01(\x02H\n\x88\x01\x01\x12\x13\n\x06change\x18\x11 \x01(\x02H\x0b\x88\x01\x01\x12\x17\n\npercentage\x18\x12 \x01(\x02H\x0c\x88\x01\x01\x12\x14\n\x07average\x18\x13 \x01(\x02H\r\x88\x01\x01\x12\x18\n\x0bbase_volume\x18\x14 \x01(\x02H\x0e\x88\x01\x01\x12\x19\n\x0cquote_volume\x18\x15 \x01(\x02H\x0f\x88\x01\x01\x12\x11\n\x04info\x18\x16 \x01(\tH\x10\x88\x01\x01B\n\n\x08_asset_aB\n\n\x08_asset_bB\r\n\x0b_bid_volumeB\r\n\x0b_ask_volumeB\x07\n\x05_highB\x06\n\x04_lowB\x07\n\x05_vwapB\x07\n\x05_openB\x08\n\x06_closeB\x07\n\x05_lastB\x11\n\x0f_previous_closeB\t\n\x07_changeB\r\n\x0b_percentageB\n\n\x08_averageB\x0e\n\x0c_base_volumeB\x0f\n\r_quote_volumeB\x07\n\x05_info\x1aQ\n\x07Tickers\x12F\n\x07tickers\x18\x01 \x03(\x0b25.aea.eightballer.tickers.v0_1_0.TickersMessage.Ticker\x1a\xab\x02\n\x1cGet_All_Tickers_Performative\x12\x11\n\tledger_id\x18\x01 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x02 \x01(\x08\x12\x13\n\x0bexchange_id\x18\x03 \x01(\t\x12\x1a\n\x12exchange_id_is_set\x18\x04 \x01(\x08\x12g\n\x06params\x18\x05 \x03(\x0b2W.aea.eightballer.tickers.v0_1_0.TickersMessage.Get_All_Tickers_Performative.ParamsEntry\x12\x15\n\rparams_is_set\x18\x06 \x01(\x08\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01\x1a\x89\x01\n\x17Get_Ticker_Performative\x12\x10\n\x08asset_id\x18\x01 \x01(\t\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x12\x1a\n\x12exchange_id_is_set\x18\x03 \x01(\x08\x12\x11\n\tledger_id\x18\x04 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x05 \x01(\x08\x1a\xc1\x01\n\x18All_Tickers_Performative\x12G\n\x07tickers\x18\x01 \x01(\x0b26.aea.eightballer.tickers.v0_1_0.TickersMessage.Tickers\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x12\x1a\n\x12exchange_id_is_set\x18\x03 \x01(\x08\x12\x11\n\tledger_id\x18\x04 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x05 \x01(\x08\x1a\xba\x01\n\x13Ticker_Performative\x12E\n\x06ticker\x18\x01 \x01(\x0b25.aea.eightballer.tickers.v0_1_0.TickersMessage.Ticker\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x12\x1a\n\x12exchange_id_is_set\x18\x03 \x01(\x08\x12\x11\n\tledger_id\x18\x04 \x01(\t\x12\x18\n\x10ledger_id_is_set\x18\x05 \x01(\x08\x1a\x8d\x02\n\x12Error_Performative\x12L\n\nerror_code\x18\x01 \x01(\x0b28.aea.eightballer.tickers.v0_1_0.TickersMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12d\n\nerror_data\x18\x03 \x03(\x0b2P.aea.eightballer.tickers.v0_1_0.TickersMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01B\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tickers_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_TICKERSMESSAGE_GET_ALL_TICKERS_PERFORMATIVE_PARAMSENTRY']._loaded_options = None
    _globals['_TICKERSMESSAGE_GET_ALL_TICKERS_PERFORMATIVE_PARAMSENTRY']._serialized_options = b'8\x01'
    _globals['_TICKERSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_TICKERSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_TICKERSMESSAGE']._serialized_start = 50
    _globals['_TICKERSMESSAGE']._serialized_end = 2582
    _globals['_TICKERSMESSAGE_ERRORCODE']._serialized_start = 533
    _globals['_TICKERSMESSAGE_ERRORCODE']._serialized_end = 710
    _globals['_TICKERSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 638
    _globals['_TICKERSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 710
    _globals['_TICKERSMESSAGE_TICKER']._serialized_start = 713
    _globals['_TICKERSMESSAGE_TICKER']._serialized_end = 1384
    _globals['_TICKERSMESSAGE_TICKERS']._serialized_start = 1386
    _globals['_TICKERSMESSAGE_TICKERS']._serialized_end = 1467
    _globals['_TICKERSMESSAGE_GET_ALL_TICKERS_PERFORMATIVE']._serialized_start = 1470
    _globals['_TICKERSMESSAGE_GET_ALL_TICKERS_PERFORMATIVE']._serialized_end = 1769
    _globals['_TICKERSMESSAGE_GET_ALL_TICKERS_PERFORMATIVE_PARAMSENTRY']._serialized_start = 1724
    _globals['_TICKERSMESSAGE_GET_ALL_TICKERS_PERFORMATIVE_PARAMSENTRY']._serialized_end = 1769
    _globals['_TICKERSMESSAGE_GET_TICKER_PERFORMATIVE']._serialized_start = 1772
    _globals['_TICKERSMESSAGE_GET_TICKER_PERFORMATIVE']._serialized_end = 1909
    _globals['_TICKERSMESSAGE_ALL_TICKERS_PERFORMATIVE']._serialized_start = 1912
    _globals['_TICKERSMESSAGE_ALL_TICKERS_PERFORMATIVE']._serialized_end = 2105
    _globals['_TICKERSMESSAGE_TICKER_PERFORMATIVE']._serialized_start = 2108
    _globals['_TICKERSMESSAGE_TICKER_PERFORMATIVE']._serialized_end = 2294
    _globals['_TICKERSMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 2297
    _globals['_TICKERSMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 2566
    _globals['_TICKERSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 2518
    _globals['_TICKERSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 2566