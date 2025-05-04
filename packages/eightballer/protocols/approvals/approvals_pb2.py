"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fapprovals.proto\x12 aea.eightballer.approvals.v0_1_0"\x9f\x0b\n\x10ApprovalsMessage\x12n\n\x11approval_response\x18\x05 \x01(\x0b2Q.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Approval_Response_PerformativeH\x00\x12V\n\x05error\x18\x06 \x01(\x0b2E.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Error_PerformativeH\x00\x12d\n\x0cget_approval\x18\x07 \x01(\x0b2L.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Get_Approval_PerformativeH\x00\x12d\n\x0cset_approval\x18\x08 \x01(\x0b2L.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Set_Approval_PerformativeH\x00\x1a\x90\x01\n\x08Approval\x12\x10\n\x08asset_id\x18\x01 \x01(\t\x12\x11\n\tledger_id\x18\x02 \x01(\t\x12\x13\n\x0bexchange_id\x18\x03 \x01(\t\x12\x0e\n\x06is_eoa\x18\x04 \x01(\x08\x12\x13\n\x06amount\x18\x05 \x01(\x03H\x00\x88\x01\x01\x12\x11\n\x04data\x18\x06 \x01(\x0cH\x01\x88\x01\x01B\t\n\x07_amountB\x07\n\x05_data\x1a\xf2\x01\n\tErrorCode\x12^\n\nerror_code\x18\x01 \x01(\x0e2J.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.ErrorCode.ErrorCodeEnum"\x84\x01\n\rErrorCodeEnum\x12\x11\n\rUNKNOWN_ASSET\x10\x00\x12\x12\n\x0eUNKNOWN_LEDGER\x10\x01\x12\x14\n\x10UNKNOWN_EXCHANGE\x10\x02\x12\x1a\n\x16FAILED_TO_SET_APPROVAL\x10\x03\x12\x1a\n\x16FAILED_TO_GET_APPROVAL\x10\x04\x1aj\n\x19Set_Approval_Performative\x12M\n\x08approval\x18\x01 \x01(\x0b2;.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Approval\x1aj\n\x19Get_Approval_Performative\x12M\n\x08approval\x18\x01 \x01(\x0b2;.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Approval\x1ao\n\x1eApproval_Response_Performative\x12M\n\x08approval\x18\x01 \x01(\x0b2;.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Approval\x1a\x95\x02\n\x12Error_Performative\x12P\n\nerror_code\x18\x01 \x01(\x0b2<.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12h\n\nerror_data\x18\x03 \x03(\x0b2T.aea.eightballer.approvals.v0_1_0.ApprovalsMessage.Error_Performative.ErrorDataEntry\x1a0\n\x0eErrorDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x028\x01B\x0e\n\x0cperformativeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'approvals_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_APPROVALSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._loaded_options = None
    _globals['_APPROVALSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_options = b'8\x01'
    _globals['_APPROVALSMESSAGE']._serialized_start = 54
    _globals['_APPROVALSMESSAGE']._serialized_end = 1493
    _globals['_APPROVALSMESSAGE_APPROVAL']._serialized_start = 479
    _globals['_APPROVALSMESSAGE_APPROVAL']._serialized_end = 623
    _globals['_APPROVALSMESSAGE_ERRORCODE']._serialized_start = 626
    _globals['_APPROVALSMESSAGE_ERRORCODE']._serialized_end = 868
    _globals['_APPROVALSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_start = 736
    _globals['_APPROVALSMESSAGE_ERRORCODE_ERRORCODEENUM']._serialized_end = 868
    _globals['_APPROVALSMESSAGE_SET_APPROVAL_PERFORMATIVE']._serialized_start = 870
    _globals['_APPROVALSMESSAGE_SET_APPROVAL_PERFORMATIVE']._serialized_end = 976
    _globals['_APPROVALSMESSAGE_GET_APPROVAL_PERFORMATIVE']._serialized_start = 978
    _globals['_APPROVALSMESSAGE_GET_APPROVAL_PERFORMATIVE']._serialized_end = 1084
    _globals['_APPROVALSMESSAGE_APPROVAL_RESPONSE_PERFORMATIVE']._serialized_start = 1086
    _globals['_APPROVALSMESSAGE_APPROVAL_RESPONSE_PERFORMATIVE']._serialized_end = 1197
    _globals['_APPROVALSMESSAGE_ERROR_PERFORMATIVE']._serialized_start = 1200
    _globals['_APPROVALSMESSAGE_ERROR_PERFORMATIVE']._serialized_end = 1477
    _globals['_APPROVALSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_start = 1429
    _globals['_APPROVALSMESSAGE_ERROR_PERFORMATIVE_ERRORDATAENTRY']._serialized_end = 1477