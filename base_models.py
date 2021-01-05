from typing import Optional, List, Union
from enum import Enum

from pydantic import BaseModel, HttpUrl


class ChatEventEnum(str, Enum):
    new_chat = 'new_chat'
    new_message = 'new_message'


class MessageKindEnum(str, Enum):
    file_visitor = 'file_visitor'
    visitor = 'visitor'
    keyboard_response = 'keyboard_response'


class Fields(BaseModel):
    Id: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    orderId: Optional[str] = None


class Visitor(BaseModel):
    field_value: Fields
    id: str

    class Config:
        fields = {'field_value': 'fields'}


class Button(BaseModel):
    text: Optional[str] = None
    id: Optional[str] = None


class Request(BaseModel):
    messageId: Optional[str] = None


class Data(BaseModel):
    url: Optional[HttpUrl] = None
    media_type: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    button: Optional[Button] = None
    request: Optional[Request] = None


class Message(BaseModel):
    text: Optional[str] = None
    kind: Optional[MessageKindEnum] = None
    visitor: Optional[str] = None
    id: Optional[str] = None
    data: Union[Optional[List[Data]], Optional[Data]] = None


class Chat(BaseModel):
    id: Optional[int] = None
    language: Optional[str] = None


class ChatEventBody(BaseModel):
    visitor: Optional[Visitor] = None
    messages: Optional[List[Message]] = None
    message: Optional[Message] = None
    event: ChatEventEnum
    chat: Optional[Chat] = None
    chat_id: Optional[str] = None
