"""发送用的消息段。

每个模型对应云湖 ``contentType`` 的一种取值，并负责生成请求体里的 ``content``。
"""

from collections.abc import Sequence
from typing import ClassVar

from pydantic import Field

from .base import ApiModel


class Button(ApiModel):
    """消息按钮。

    注意：文档注释把 1/2 的含义写反了。按示例（``actionType=1`` 配 ``url``、
    ``actionType=2`` 配 ``value``）以及旧版实现，**1 是跳转、2 是复制**。
    """

    text: str
    action_type: int = Field(alias="actionType")
    url: str | None = None
    value: str | None = None


class BaseSegment(ApiModel):
    """消息段基类：子类只需声明 ``content_type`` 并实现 :meth:`to_content`。"""

    content_type: ClassVar[str]

    def to_content(self) -> dict[str, object]:
        """生成云湖 ``content`` 字段。"""
        raise NotImplementedError


class TextSegment(BaseSegment):
    """文本消息，可附带 @ 与按钮。"""

    content_type: ClassVar[str] = "text"

    text: str
    at: Sequence[str] | None = None
    buttons: Sequence[Sequence[Button]] | None = None

    def to_content(self) -> dict[str, object]:
        content: dict[str, object] = {"text": self.text}
        if self.at:
            content["at"] = ",".join(self.at)
        if self.buttons:
            content["buttons"] = [
                [button.model_dump(by_alias=True, exclude_none=True) for button in row] for row in self.buttons
            ]
        return content


class MarkdownSegment(BaseSegment):
    """Markdown 消息，云湖把它放在 ``content.text`` 里。"""

    content_type: ClassVar[str] = "markdown"

    text: str

    def to_content(self) -> dict[str, object]:
        return {"text": self.text}


class HtmlSegment(BaseSegment):
    """HTML 消息，同样放在 ``content.text`` 里。"""

    content_type: ClassVar[str] = "html"

    text: str

    def to_content(self) -> dict[str, object]:
        return {"text": self.text}


class ImageSegment(BaseSegment):
    """图片消息，``key`` 是上传接口返回的 imageKey。"""

    content_type: ClassVar[str] = "image"

    key: str

    def to_content(self) -> dict[str, object]:
        return {"imageKey": self.key}


class VideoSegment(BaseSegment):
    """视频消息，``key`` 是上传接口返回的 videoKey。"""

    content_type: ClassVar[str] = "video"

    key: str

    def to_content(self) -> dict[str, object]:
        return {"videoKey": self.key}


class FileSegment(BaseSegment):
    """文件消息，``key`` 是上传接口返回的 fileKey。"""

    content_type: ClassVar[str] = "file"

    key: str

    def to_content(self) -> dict[str, object]:
        return {"fileKey": self.key}
