"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10order_book.proto\x12.aea.eightballer.order_book_subscription.v0_1_0"\xee\x07\n\x10OrderBookMessage\x12d\n\x05error\x18\x05 \x01(\x0b2S.aea.eightballer.order_book_subscription.v0_1_0.OrderBookMessage.Error_PerformativeH\x00\x12|\n\x11order_book_update\x18\x06 \x01(\x0b2_.aea.eightballer.order_book_subscription.v0_1_0.OrderBookMessage.Order_Book_Update_PerformativeH\x00\x12l\n\tsubscribe\x18\x07 \x01(\x0b2W.aea.eightballer.order_book_subscription.v0_1_0.OrderBookMessage.Subscribe_PerformativeH\x00\x12p\n\x0bunsubscribe\x18\x08 \x01(\x0b2Y.aea.eightballer.order_book_subscription.v0_1_0.OrderBookMessage.Unsubscribe_PerformativeH\x00\x1a\x80\x01\n\tOrderBook\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04bids\x18\x03 \x03(\x05\x12\x0c\n\x04asks\x18\x04 \x03(\x05\x12\x11\n\ttimestamp\x18\x05 \x01(\x05\x12\x10\n\x08datetime\x18\x06 \x01(\t\x12\r\n\x05nonce\x18\x07 \x01(\x05\x1a\x95\x01\n\x16Subscribe_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x11\n\tprecision\x18\x03 \x01(\t\x12\x18\n\x10precision_is_set\x18\x04 \x01(\x08\x12\x10\n\x08interval\x18\x05 \x01(\x05\x12\x17\n\x0finterval_is_set\x18\x06 \x01(\x08\x1a?\n\x18Unsubscribe_Performative\x12\x13\n\x0bexchange_id\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x1a\x80\x01\n\x1eOrder_Book_Update_Performative\x12^\n\norder_book\x18\x01 \x01(\x0b2J.aea.eightballer.order_book_subscription.v0_1_0.OrderBookMessage.OrderBook\x1a\'\n\x12Error_Performative\x12\x11\n\terror_msg\x18\x01 \x01(\tB\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_book_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_ORDERBOOKMESSAGE']._serialized_start = 69
    _globals['_ORDERBOOKMESSAGE']._serialized_end = 1075
    _globals['_ORDERBOOKMESSAGE_ORDERBOOK']._serialized_start = 542
    _globals['_ORDERBOOKMESSAGE_ORDERBOOK']._serialized_end = 670
    _globals['_ORDERBOOKMESSAGE_SUBSCRIBE_PERFORMATIVE']._serialized_start = 673
    _globals['_ORDERBOOKMESSAGE_SUBSCRIBE_PERFORMATIVE']._serialized_end = 822
    _globals['_ORDERBOOKMESSAGE_UNSUBSCRIBE_PERFORMATIVE']._serialized_start = 824
    _globals['_ORDERBOOKMESSAGE_UNSUBSCRIBE_PERFORMATIVE']._serialized_end = 887
    _globals['_ORDERBOOKMESSAGE_ORDER_BOOK_UPDATE_PERFORMATIVE']._serialized_start = 890
    _globals['_ORDERBOOKMESSAGE_ORDER_BOOK_UPDATE_PERFORMATIVE']._serialized_end = 1018
    _globals['_ORDERBOOKMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 1020
    _globals['_ORDERBOOKMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 1059