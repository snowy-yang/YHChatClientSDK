"""``v1`` 用户接口集合（token 放请求头）。由 ``tools/gen_v1_api.py`` 生成，勿手改。"""

from ...transport import HttpTransport
from .beta import BetaAPI
from .bot import BotAPI
from .captcha import CaptchaAPI
from .chat_background import ChatBackgroundAPI
from .check import CheckAPI
from .coin import CoinAPI
from .community import CommunityAPI
from .conversation import ConversationAPI
from .disk import DiskAPI
from .event import EventAPI
from .expression import ExpressionAPI
from .file import FileAPI
from .friend import FriendAPI
from .group import GroupAPI
from .group_tag import GroupTagAPI
from .instruction import InstructionAPI
from .live import LiveAPI
from .menu import MenuAPI
from .misc import MiscAPI
from .mount_setting import MountSettingAPI
from .msg import MsgAPI
from .report import ReportAPI
from .search import SearchAPI
from .share import ShareAPI
from .sticker import StickerAPI
from .sticky import StickyAPI
from .user import UserAPI
from .verification import VerificationAPI
from .vip import VipAPI
from .web_bot import WebBotAPI
from .web_common import WebCommonAPI
from .web_community import WebCommunityAPI
from .web_document import WebDocumentAPI
from .web_group import WebGroupAPI
from .web_misc import WebMiscAPI
from .web_rss import WebRssAPI
from .web_user import WebUserAPI

__all__ = [
    "V1API",
    "BetaAPI",
    "BotAPI",
    "CaptchaAPI",
    "ChatBackgroundAPI",
    "CheckAPI",
    "CoinAPI",
    "CommunityAPI",
    "ConversationAPI",
    "DiskAPI",
    "EventAPI",
    "ExpressionAPI",
    "FileAPI",
    "FriendAPI",
    "GroupAPI",
    "GroupTagAPI",
    "InstructionAPI",
    "LiveAPI",
    "MenuAPI",
    "MiscAPI",
    "MountSettingAPI",
    "MsgAPI",
    "ReportAPI",
    "SearchAPI",
    "ShareAPI",
    "StickerAPI",
    "StickyAPI",
    "UserAPI",
    "VerificationAPI",
    "VipAPI",
    "WebBotAPI",
    "WebCommonAPI",
    "WebCommunityAPI",
    "WebDocumentAPI",
    "WebGroupAPI",
    "WebMiscAPI",
    "WebRssAPI",
    "WebUserAPI",
]


class V1API:
    """``v1/*`` 用户接口：按文档分组挂属性，token 由传输层放进请求头。"""

    def __init__(self, http: HttpTransport) -> None:
        self.beta = BetaAPI(http)
        self.bot = BotAPI(http)
        self.captcha = CaptchaAPI(http)
        self.chat_background = ChatBackgroundAPI(http)
        self.check = CheckAPI(http)
        self.coin = CoinAPI(http)
        self.community = CommunityAPI(http)
        self.conversation = ConversationAPI(http)
        self.disk = DiskAPI(http)
        self.event = EventAPI(http)
        self.expression = ExpressionAPI(http)
        self.file = FileAPI(http)
        self.friend = FriendAPI(http)
        self.group = GroupAPI(http)
        self.group_tag = GroupTagAPI(http)
        self.instruction = InstructionAPI(http)
        self.live = LiveAPI(http)
        self.menu = MenuAPI(http)
        self.misc = MiscAPI(http)
        self.mount_setting = MountSettingAPI(http)
        self.msg = MsgAPI(http)
        self.report = ReportAPI(http)
        self.search = SearchAPI(http)
        self.share = ShareAPI(http)
        self.sticker = StickerAPI(http)
        self.sticky = StickyAPI(http)
        self.user = UserAPI(http)
        self.verification = VerificationAPI(http)
        self.vip = VipAPI(http)
        self.web_bot = WebBotAPI(http)
        self.web_common = WebCommonAPI(http)
        self.web_community = WebCommunityAPI(http)
        self.web_document = WebDocumentAPI(http)
        self.web_group = WebGroupAPI(http)
        self.web_misc = WebMiscAPI(http)
        self.web_rss = WebRssAPI(http)
        self.web_user = WebUserAPI(http)
