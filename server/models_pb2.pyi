from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Publication(_message.Message):
    __slots__ = ("name", "title", "url", "description", "content", "hierarchy", "pub_date", "art_type", "prob", "content_fetched", "created_at", "mark", "status", "due_date", "due_reason", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    HIERARCHY_FIELD_NUMBER: _ClassVar[int]
    PUB_DATE_FIELD_NUMBER: _ClassVar[int]
    ART_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROB_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FETCHED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MARK_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    DUE_REASON_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    title: str
    url: str
    description: str
    content: str
    hierarchy: str
    pub_date: _timestamp_pb2.Timestamp
    art_type: str
    prob: float
    content_fetched: bool
    created_at: _timestamp_pb2.Timestamp
    mark: int
    status: int
    due_date: _timestamp_pb2.Timestamp
    due_reason: int
    id: int
    def __init__(self, name: _Optional[str] = ..., title: _Optional[str] = ..., url: _Optional[str] = ..., description: _Optional[str] = ..., content: _Optional[str] = ..., hierarchy: _Optional[str] = ..., pub_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., art_type: _Optional[str] = ..., prob: _Optional[float] = ..., content_fetched: bool = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mark: _Optional[int] = ..., status: _Optional[int] = ..., due_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., due_reason: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("id", "type", "page", "amount")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: str
    page: int
    amount: int
    def __init__(self, id: _Optional[int] = ..., type: _Optional[str] = ..., page: _Optional[int] = ..., amount: _Optional[int] = ...) -> None: ...
