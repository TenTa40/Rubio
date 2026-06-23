"""
Rubio - Rubika Bot API Library
Models: dataclass-based models for all API objects
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from .enums import (
    ChatType, FileType, ForwardedFrom as ForwardedFromEnum, PollStatus as PollStatusEnum,
    ButtonSelectionType, ButtonSelectionSearch, ButtonSelectionGet, ButtonCalendarType,
    ButtonTextboxTypeKeypad, ButtonTextboxTypeLine, ButtonLocationType,
    MessageSender, UpdateType, ChatKeypadType, MetadataType, ButtonType
)


@dataclass
class File:
    file_id: str
    file_name: Optional[str] = None
    size: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "File":
        if not data:
            return None
        return cls(
            file_id=data.get("file_id", ""),
            file_name=data.get("file_name"),
            size=data.get("size"),
        )


@dataclass
class Location:
    latitude: str
    longitude: str

    @classmethod
    def from_dict(cls, data: dict) -> "Location":
        if not data:
            return None
        return cls(
            latitude=data.get("latitude", ""),
            longitude=data.get("longitude", ""),
        )

    def to_dict(self) -> dict:
        return {"latitude": self.latitude, "longitude": self.longitude}


@dataclass
class Chat:
    chat_id: str
    chat_type: Optional[ChatType] = None
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Chat":
        if not data:
            return None
        return cls(
            chat_id=data.get("chat_id", ""),
            chat_type=ChatType(data["chat_type"]) if data.get("chat_type") else None,
            user_id=data.get("user_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            title=data.get("title"),
            username=data.get("username"),
        )


@dataclass
class Bot:
    bot_id: str
    bot_title: Optional[str] = None
    avatar: Optional[File] = None
    description: Optional[str] = None
    username: Optional[str] = None
    start_message: Optional[str] = None
    share_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Bot":
        if not data:
            return None
        return cls(
            bot_id=data.get("bot_id", ""),
            bot_title=data.get("bot_title"),
            avatar=File.from_dict(data["avatar"]) if data.get("avatar") else None,
            description=data.get("description"),
            username=data.get("username"),
            start_message=data.get("start_message"),
            share_url=data.get("share_url"),
        )


@dataclass
class BotCommand:
    command: str
    description: str

    def to_dict(self) -> dict:
        return {"command": self.command, "description": self.description}


@dataclass
class ForwardedFrom:
    type_from: Optional[ForwardedFromEnum] = None
    message_id: Optional[str] = None
    from_chat_id: Optional[str] = None
    from_sender_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ForwardedFrom":
        if not data:
            return None
        return cls(
            type_from=ForwardedFromEnum(data["type_from"]) if data.get("type_from") else None,
            message_id=data.get("message_id"),
            from_chat_id=data.get("from_chat_id"),
            from_sender_id=data.get("from_sender_id"),
        )


@dataclass
class Sticker:
    sticker_id: str
    file: Optional[File] = None
    emoji_character: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Sticker":
        if not data:
            return None
        return cls(
            sticker_id=data.get("sticker_id", ""),
            file=File.from_dict(data["file"]) if data.get("file") else None,
            emoji_character=data.get("emoji_character"),
        )


@dataclass
class ContactMessage:
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ContactMessage":
        if not data:
            return None
        return cls(
            phone_number=data.get("phone_number", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )


@dataclass
class PollStatusModel:
    state: Optional[PollStatusEnum] = None
    selection_index: int = -1
    percent_vote_options: List[int] = field(default_factory=list)
    total_vote: int = 0
    show_total_votes: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "PollStatusModel":
        if not data:
            return None
        return cls(
            state=PollStatusEnum(data["state"]) if data.get("state") else None,
            selection_index=data.get("selection_index", -1),
            percent_vote_options=data.get("percent_vote_options", []),
            total_vote=data.get("total_vote", 0),
            show_total_votes=data.get("show_total_votes", False),
        )


@dataclass
class Poll:
    question: str
    options: List[str] = field(default_factory=list)
    poll_status: Optional[PollStatusModel] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Poll":
        if not data:
            return None
        return cls(
            question=data.get("question", ""),
            options=data.get("options", []),
            poll_status=PollStatusModel.from_dict(data["poll_status"]) if data.get("poll_status") else None,
        )


@dataclass
class AuxData:
    start_id: Optional[str] = None
    button_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "AuxData":
        if not data:
            return None
        return cls(
            start_id=data.get("start_id"),
            button_id=data.get("button_id"),
        )


@dataclass
class ButtonSelectionItem:
    text: str
    image_url: Optional[str] = None
    type: Optional[ButtonSelectionType] = None

    def to_dict(self) -> dict:
        d = {"text": self.text}
        if self.image_url:
            d["image_url"] = self.image_url
        if self.type:
            d["type"] = self.type.value
        return d


@dataclass
class ButtonSelection:
    selection_id: str
    search_type: Optional[ButtonSelectionSearch] = None
    get_type: Optional[ButtonSelectionGet] = None
    items: List[ButtonSelectionItem] = field(default_factory=list)
    is_multi_selection: bool = False
    columns_count: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"selection_id": self.selection_id}
        if self.search_type:
            d["search_type"] = self.search_type.value
        if self.get_type:
            d["get_type"] = self.get_type.value
        if self.items:
            d["items"] = [i.to_dict() for i in self.items]
        d["is_multi_selection"] = self.is_multi_selection
        if self.columns_count:
            d["columns_count"] = self.columns_count
        if self.title:
            d["title"] = self.title
        return d


@dataclass
class ButtonCalendar:
    type: ButtonCalendarType = ButtonCalendarType.DATE_PERSIAN
    default_value: Optional[str] = None
    min_year: Optional[str] = None
    max_year: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"type": self.type.value}
        if self.default_value:
            d["default_value"] = self.default_value
        if self.min_year:
            d["min_year"] = self.min_year
        if self.max_year:
            d["max_year"] = self.max_year
        if self.title:
            d["title"] = self.title
        return d


@dataclass
class ButtonNumberPicker:
    min_value: str
    max_value: str
    default_value: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"min_value": self.min_value, "max_value": self.max_value}
        if self.default_value:
            d["default_value"] = self.default_value
        if self.title:
            d["title"] = self.title
        return d


@dataclass
class ButtonStringPicker:
    items: List[str] = field(default_factory=list)
    default_value: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"items": self.items}
        if self.default_value:
            d["default_value"] = self.default_value
        if self.title:
            d["title"] = self.title
        return d


@dataclass
class ButtonTextbox:
    type_line: ButtonTextboxTypeLine = ButtonTextboxTypeLine.SINGLE_LINE
    type_keypad: ButtonTextboxTypeKeypad = ButtonTextboxTypeKeypad.STRING
    place_holder: Optional[str] = None
    title: Optional[str] = None
    default_value: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "type_line": self.type_line.value,
            "type_keypad": self.type_keypad.value,
        }
        if self.place_holder:
            d["place_holder"] = self.place_holder
        if self.title:
            d["title"] = self.title
        if self.default_value:
            d["default_value"] = self.default_value
        return d


@dataclass
class ButtonLocation:
    type: ButtonLocationType = ButtonLocationType.PICKER
    default_pointer_location: Optional[Location] = None
    default_map_location: Optional[Location] = None
    title: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"type": self.type.value}
        if self.default_pointer_location:
            d["default_pointer_location"] = self.default_pointer_location.to_dict()
        if self.default_map_location:
            d["default_map_location"] = self.default_map_location.to_dict()
        if self.title:
            d["title"] = self.title
        return d


@dataclass
class Button:
    id: str
    type: ButtonType = ButtonType.SIMPLE
    button_text: Optional[str] = None
    button_selection: Optional[ButtonSelection] = None
    button_calendar: Optional[ButtonCalendar] = None
    button_number_picker: Optional[ButtonNumberPicker] = None
    button_string_picker: Optional[ButtonStringPicker] = None
    button_location: Optional[ButtonLocation] = None
    button_textbox: Optional[ButtonTextbox] = None

    def to_dict(self) -> dict:
        d = {"id": self.id, "type": self.type.value}
        if self.button_text:
            d["button_text"] = self.button_text
        if self.button_selection:
            d["button_selection"] = self.button_selection.to_dict()
        if self.button_calendar:
            d["button_calendar"] = self.button_calendar.to_dict()
        if self.button_number_picker:
            d["button_number_picker"] = self.button_number_picker.to_dict()
        if self.button_string_picker:
            d["button_string_picker"] = self.button_string_picker.to_dict()
        if self.button_location:
            d["button_location"] = self.button_location.to_dict()
        if self.button_textbox:
            d["button_textbox"] = self.button_textbox.to_dict()
        return d


@dataclass
class KeypadRow:
    buttons: List[Button] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"buttons": [b.to_dict() for b in self.buttons]}


@dataclass
class Keypad:
    rows: List[KeypadRow] = field(default_factory=list)
    resize_keyboard: bool = False
    one_time_keyboard: bool = False

    def to_dict(self) -> dict:
        return {
            "rows": [r.to_dict() for r in self.rows],
            "resize_keyboard": self.resize_keyboard,
            "one_time_keyboard": self.one_time_keyboard,
        }


@dataclass
class MetadataPart:
    type: MetadataType
    from_index: int
    length: int
    link_url: Optional[str] = None
    mention_text_user_id: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "type": self.type.value,
            "from_index": self.from_index,
            "length": self.length,
        }
        if self.link_url:
            d["link_url"] = self.link_url
        if self.mention_text_user_id:
            d["mention_text_user_id"] = self.mention_text_user_id
        return d


@dataclass
class Metadata:
    meta_data_parts: List[MetadataPart] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"meta_data_parts": [p.to_dict() for p in self.meta_data_parts]}


@dataclass
class Message:
    message_id: str
    text: Optional[str] = None
    time: Optional[int] = None
    is_edited: bool = False
    sender_type: Optional[MessageSender] = None
    sender_id: Optional[str] = None
    aux_data: Optional[AuxData] = None
    file: Optional[File] = None
    reply_to_message_id: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    forwarded_no_link: Optional[str] = None
    location: Optional[Location] = None
    sticker: Optional[Sticker] = None
    contact_message: Optional[ContactMessage] = None
    poll: Optional[Poll] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        if not data:
            return None
        return cls(
            message_id=data.get("message_id", ""),
            text=data.get("text"),
            time=data.get("time"),
            is_edited=data.get("is_edited", False),
            sender_type=MessageSender(data["sender_type"]) if data.get("sender_type") else None,
            sender_id=data.get("sender_id"),
            aux_data=AuxData.from_dict(data.get("aux_data")),
            file=File.from_dict(data.get("file")),
            reply_to_message_id=data.get("reply_to_message_id"),
            forwarded_from=ForwardedFrom.from_dict(data.get("forwarded_from")),
            forwarded_no_link=data.get("forwarded_no_link"),
            location=Location.from_dict(data.get("location")),
            sticker=Sticker.from_dict(data.get("sticker")),
            contact_message=ContactMessage.from_dict(data.get("contact_message")),
            poll=Poll.from_dict(data.get("poll")),
        )


@dataclass
class Update:
    type: Optional[UpdateType] = None
    chat_id: Optional[str] = None
    removed_message_id: Optional[str] = None
    new_message: Optional[Message] = None
    updated_message: Optional[Message] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Update":
        if not data:
            return None
        return cls(
            type=UpdateType(data["type"]) if data.get("type") else None,
            chat_id=data.get("chat_id"),
            removed_message_id=data.get("removed_message_id"),
            new_message=Message.from_dict(data.get("new_message")),
            updated_message=Message.from_dict(data.get("updated_message")),
        )


@dataclass
class InlineMessage:
    sender_id: str
    chat_id: str
    message_id: str
    text: Optional[str] = None
    file: Optional[File] = None
    location: Optional[Location] = None
    aux_data: Optional[AuxData] = None

    @classmethod
    def from_dict(cls, data: dict) -> "InlineMessage":
        if not data:
            return None
        return cls(
            sender_id=data.get("sender_id", ""),
            chat_id=data.get("chat_id", ""),
            message_id=data.get("message_id", ""),
            text=data.get("text"),
            file=File.from_dict(data.get("file")),
            location=Location.from_dict(data.get("location")),
            aux_data=AuxData.from_dict(data.get("aux_data")),
        )
