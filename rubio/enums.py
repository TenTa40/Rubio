"""
Rubio - Rubika Bot API Library
Enums module: all official API enums
"""

from enum import Enum


class ChatType(str, Enum):
    USER = "User"
    BOT = "Bot"
    GROUP = "Group"
    CHANNEL = "Channel"


class FileType(str, Enum):
    FILE = "File"
    IMAGE = "Image"
    VOICE = "Voice"
    VIDEO = "Video"
    MUSIC = "Music"
    GIF = "Gif"


class ForwardedFrom(str, Enum):
    USER = "User"
    CHANNEL = "Channel"
    BOT = "Bot"


class PollStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"


class ButtonSelectionType(str, Enum):
    TEXT_ONLY = "TextOnly"
    TEXT_IMG_THU = "TextImgThu"
    TEXT_IMG_BIG = "TextImgBig"


class ButtonSelectionSearch(str, Enum):
    NONE = "None"
    LOCAL = "Local"
    API = "Api"


class ButtonSelectionGet(str, Enum):
    LOCAL = "Local"
    API = "Api"


class ButtonCalendarType(str, Enum):
    DATE_PERSIAN = "DatePersian"
    DATE_GREGORIAN = "DateGregorian"


class ButtonTextboxTypeKeypad(str, Enum):
    STRING = "String"
    NUMBER = "Number"


class ButtonTextboxTypeLine(str, Enum):
    SINGLE_LINE = "SingleLine"
    MULTI_LINE = "MultiLine"


class ButtonLocationType(str, Enum):
    PICKER = "Picker"
    VIEW = "View"


class MessageSender(str, Enum):
    USER = "User"
    BOT = "Bot"


class UpdateType(str, Enum):
    UPDATED_MESSAGE = "UpdatedMessage"
    NEW_MESSAGE = "NewMessage"
    REMOVED_MESSAGE = "RemovedMessage"
    STARTED_BOT = "StartedBot"
    STOPPED_BOT = "StoppedBot"


class ChatKeypadType(str, Enum):
    NONE = "None"
    NEW = "New"
    REMOVE = "Remove"


class UpdateEndpointType(str, Enum):
    RECEIVE_UPDATE = "ReceiveUpdate"
    RECEIVE_INLINE_MESSAGE = "ReceiveInlineMessage"
    RECEIVE_QUERY = "ReceiveQuery"
    GET_SELECTION_ITEM = "GetSelectionItem"
    SEARCH_SELECTION_ITEMS = "SearchSelectionItems"


class MetadataType(str, Enum):
    BOLD = "Bold"
    ITALIC = "Italic"
    MONO = "Mono"
    UNDERLINE = "Underline"
    STRIKE = "Strike"
    SPOILER = "Spoiler"
    LINK = "Link"
    MENTION_TEXT = "MentionText"
    PRE = "Pre"
    QUOTE = "Quote"


class ButtonType(str, Enum):
    SIMPLE = "Simple"
    SELECTION = "Selection"
    CALENDAR = "Calendar"
    NUMBER_PICKER = "NumberPicker"
    STRING_PICKER = "StringPicker"
    LOCATION = "Location"
    CAMERA_IMAGE = "CameraImage"
    CAMERA_VIDEO = "CameraVideo"
    GALLERY_IMAGE = "GalleryImage"
    GALLERY_VIDEO = "GalleryVideo"
    FILE = "File"
    AUDIO = "Audio"
    RECORD_AUDIO = "RecordAudio"
    TEXTBOX = "Textbox"
    LINK = "Link"
    ASK_MY_PHONE_NUMBER = "AskMyPhoneNumber"
    ASK_MY_LOCATION = "AskMyLocation"
    BARCODE = "Barcode"
