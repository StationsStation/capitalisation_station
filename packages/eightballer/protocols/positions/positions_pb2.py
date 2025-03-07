"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fpositions.proto\x12 aea.eightballer.positions.v0_1_0"\x98\x19\n\x10PositionsMessage\x12f\n\rall_positions\x18\x05 \x01(\x0b2M.aea.eightballer.positions.v0_1_0.PositionsMessage.All_Positions_PerformativeH\x00\x12V\n\x05error\x18\x06 \x01(\x0b2E.aea.eightballer.positions.v0_1_0.PositionsMessage.Error_PerformativeH\x00\x12n\n\x11get_all_positions\x18\x07 \x01(\x0b2Q.aea.eightballer.positions.v0_1_0.PositionsMessage.Get_All_Positions_PerformativeH\x00\x12d\n\x0cget_position\x18\x08 \x01(\x0b2L.aea.eightballer.positions.v0_1_0.PositionsMessage.Get_Position_PerformativeH\x00\x12\\\n\x08position\x18\t \x01(\x0b2H.aea.eightballer.positions.v0_1_0.PositionsMessage.Position_PerformativeH\x00\x1a\xb7\x01\n\tErrorCode\x12^\n\nerror_code\x18\x01 \x01(\x0e2J.aea.eightballer.positions.v0_1_0.PositionsMessage.ErrorCode.ErrorCodeEnum"J\n\rErrorCodeEnum\x12\x14\n\x10UNKNOWN_EXCHANGE\x10\x00\x12\x14\n\x10UNKNOWN_POSITION\x10\x01\x12\r\n\tAPI_ERROR\x10\x02\x1a\x93\n\n\x08Position\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x16\n\ttimestamp\x18\x03 \x01(\x03H\x00\x88\x01\x01\x12\x15\n\x08datetime\x18\x04 \x01(\tH\x01\x88\x01\x01\x12"\n\x15last_update_timestamp\x18\x05 \x01(\x03H\x02\x88\x01\x01\x12\x1b\n\x0einitial_margin\x18\x06 \x01(\x02H\x03\x88\x01\x01\x12&\n\x19initial_margin_percentage\x18\x07 \x01(\x02H\x04\x88\x01\x01\x12\x1f\n\x12maintenance_margin\x18\x08 \x01(\x02H\x05\x88\x01\x01\x12*\n\x1dmaintenance_margin_percentage\x18\t \x01(\x02H\x06\x88\x01\x01\x12\x18\n\x0bentry_price\x18\n \x01(\x02H\x07\x88\x01\x01\x12\x15\n\x08notional\x18\x0b \x01(\x02H\x08\x88\x01\x01\x12\x15\n\x08leverage\x18\x0c \x01(\x02H\t\x88\x01\x01\x12\x1b\n\x0eunrealized_pnl\x18\r \x01(\x02H\n\x88\x01\x01\x12\x16\n\tcontracts\x18\x0e \x01(\x02H\x0b\x88\x01\x01\x12\x1a\n\rcontract_size\x18\x0f \x01(\x02H\x0c\x88\x01\x01\x12\x19\n\x0cmargin_ratio\x18\x10 \x01(\x02H\r\x88\x01\x01\x12\x1e\n\x11liquidation_price\x18\x11 \x01(\x02H\x0e\x88\x01\x01\x12\x17\n\nmark_price\x18\x12 \x01(\x02H\x0f\x88\x01\x01\x12\x17\n\nlast_price\x18\x13 \x01(\x02H\x10\x88\x01\x01\x12\x17\n\ncollateral\x18\x14 \x01(\x02H\x11\x88\x01\x01\x12\x18\n\x0bmargin_mode\x18\x15 \x01(\tH\x12\x88\x01\x01\x12R\n\x04side\x18\x16 \x01(\x0b2?.aea.eightballer.positions.v0_1_0.PositionsMessage.PositionSideH\x13\x88\x01\x01\x12\x17\n\npercentage\x18\x17 \x01(\x02H\x14\x88\x01\x01\x12\x11\n\x04info\x18\x18 \x01(\tH\x15\x88\x01\x01\x12\x11\n\x04size\x18\x19 \x01(\x02H\x16\x88\x01\x01\x12\x18\n\x0bexchange_id\x18\x1a \x01(\tH\x17\x88\x01\x01\x12\x13\n\x06hedged\x18\x1b \x01(\tH\x18\x88\x01\x01\x12\x1c\n\x0fstop_loss_price\x18\x1c \x01(\x02H\x19\x88\x01\x01\x12\x1e\n\x11take_profit_price\x18\x1d \x01(\x02H\x1a\x88\x01\x01B\x0c\n\n_timestampB\x0b\n\t_datetimeB\x18\n\x16_last_update_timestampB\x11\n\x0f_initial_marginB\x1c\n\x1a_initial_margin_percentageB\x15\n\x13_maintenance_marginB \n\x1e_maintenance_margin_percentageB\x0e\n\x0c_entry_priceB\x0b\n\t_notionalB\x0b\n\t_leverageB\x11\n\x0f_unrealized_pnlB\x0c\n\n_contractsB\x10\n\x0e_contract_sizeB\x0f\n\r_margin_ratioB\x14\n\x12_liquidation_priceB\r\n\x0b_mark_priceB\r\n\x0b_last_priceB\r\n\x0b_collateralB\x0e\n\x0c_margin_modeB\x07\n\x05_sideB\r\n\x0b_percentageB\x07\n\x05_infoB\x07\n\x05_sizeB\x0e\n\x0c_exchange_idB\t\n\x07_hedgedB\x12\n\x10_stop_loss_priceB\x14\n\x12_take_profit_price\x1a\xa0\x01\n\x0cPositionSide\x12g\n\rposition_side\x18\x01 \x01(\x0e2P.aea.eightballer.positions.v0_1_0.PositionsMessage.PositionSide.PositionSideEnum"\'\n\x10PositionSideEnum\x12\x08\n\x04LONG\x10\x00\x12\t\n\x05SHORT\x10\x01\x1a[\n\tPositions\x12N\n\tpositions\x18\x01 \x03(\x0b2;.aea.eightballer.positions.v0_1_0.PositionsMessage.Position\x1a\xce\x02\n\x1eGet_All_Positions_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12m\n\x06params\x18\x02 \x03(\x0b2].aea.eightballer.positions.v0_1_0.PositionsMessage.Get_All_Positions_Performative.ParamsEntry\x12\x15\n\rparams_is_set\x18\x03 \x01(\x08\x12M\n\x04side\x18\x04 \x01(\x0b2?.aea.eightballer.positions.v0_1_0.PositionsMessage.PositionSide\x12\x13\n\x0bside_is_set\x18\x05 \x01(\x08\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01\x1aE\n\x19Get_Position_Performative\x12\x13\n\x0bposition_id\x18\x01 \x01(\t\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x1a\x82\x01\n\x1aAll_Positions_Performative\x12O\n\tpositions\x18\x01 \x01(\x0b2<.aea.eightballer.positions.v0_1_0.PositionsMessage.Positions\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x1a{\n\x15Position_Performative\x12M\n\x08position\x18\x01 \x01(\x0b2;.aea.eightballer.positions.v0_1_0.PositionsMessage.Position\x12\x13\n\x0bexchange_id\x18\x02 \x01(\t\x1a\x95\x02\n\x12Error_Performative\x12P\n\nerror_code\x18\x01 \x01(\x0b2<.aea.eightballer.positions.v0_1_0.PositionsMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12h\n\nerror_data\x18\x03 \x03(\x0b2T.aea.eightballer.positions.v0_1_0.PositionsMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01B\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'positions_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_POSITIONSMESSAGE_GET_ALL_POSITIONS_PERFORMATIVE_PARAMSENTRY']._loaded_options = None
    _globals['_POSITIONSMESSAGE_GET_ALL_POSITIONS_PERFORMATIVE_PARAMSENTRY']._serialized_options = b'8\x01'
    _globals['_POSITIONSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_POSITIONSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_POSITIONSMESSAGE']._serialized_start = 54
    _globals['_POSITIONSMESSAGE']._serialized_end = 3278
    _globals['_POSITIONSMESSAGE_ERRORCODE']._serialized_start = 575
    _globals['_POSITIONSMESSAGE_ERRORCODE']._serialized_end = 758
    _globals['_POSITIONSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 684
    _globals['_POSITIONSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 758
    _globals['_POSITIONSMESSAGE_POSITION']._serialized_start = 761
    _globals['_POSITIONSMESSAGE_POSITION']._serialized_end = 2060
    _globals['_POSITIONSMESSAGE_POSITIONSIDE']._serialized_start = 2063
    _globals['_POSITIONSMESSAGE_POSITIONSIDE']._serialized_end = 2223
    _globals['_POSITIONSMESSAGE_POSITIONSIDE_POSITIONSIDEENUM']._serialized_start = 2184
    _globals['_POSITIONSMESSAGE_POSITIONSIDE_POSITIONSIDEENUM']._serialized_end = 2223
    _globals['_POSITIONSMESSAGE_POSITIONS']._serialized_start = 2225
    _globals['_POSITIONSMESSAGE_POSITIONS']._serialized_end = 2316
    _globals['_POSITIONSMESSAGE_GET_ALL_POSITIONS_PERFORMATIVE']._serialized_start = 2319
    _globals['_POSITIONSMESSAGE_GET_ALL_POSITIONS_PERFORMATIVE']._serialized_end = 2653
    _globals['_POSITIONSMESSAGE_GET_ALL_POSITIONS_PERFORMATIVE_PARAMSENTRY']._serialized_start = 2608
    _globals['_POSITIONSMESSAGE_GET_ALL_POSITIONS_PERFORMATIVE_PARAMSENTRY']._serialized_end = 2653
    _globals['_POSITIONSMESSAGE_GET_POSITION_PERFORMATIVE']._serialized_start = 2655
    _globals['_POSITIONSMESSAGE_GET_POSITION_PERFORMATIVE']._serialized_end = 2724
    _globals['_POSITIONSMESSAGE_ALL_POSITIONS_PERFORMATIVE']._serialized_start = 2727
    _globals['_POSITIONSMESSAGE_ALL_POSITIONS_PERFORMATIVE']._serialized_end = 2857
    _globals['_POSITIONSMESSAGE_POSITION_PERFORMATIVE']._serialized_start = 2859
    _globals['_POSITIONSMESSAGE_POSITION_PERFORMATIVE']._serialized_end = 2982
    _globals['_POSITIONSMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 2985
    _globals['_POSITIONSMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 3262
    _globals['_POSITIONSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 3214
    _globals['_POSITIONSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 3262