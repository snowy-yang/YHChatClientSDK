"""Satori 消息元素：把 ``content`` 字符串（``<at id="..."/>`` 这类标记）解析成对象。

Satori v1 的 ``Message.content`` 是一段标记文本，元素用自闭合标签表示，
文本中的 ``& < > "`` 需要转义。聊天场景只覆盖 text / at / quote / img / file / video / audio / br。
"""

import re
from dataclasses import dataclass

_TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)((?:\s+[a-zA-Z_-]+=\"[^\"]*\")*)\s*/>")
_ATTR_RE = re.compile(r"([a-zA-Z_-]+)=\"([^\"]*)\"")


@dataclass(slots=True)
class Text:
    """纯文本。"""

    text: str = ""


@dataclass(slots=True)
class At:
    """提及用户或全体成员。"""

    id: str | None = None
    name: str | None = None
    role: str | None = None
    type: str | None = None


@dataclass(slots=True)
class Quote:
    """引用消息。"""

    id: str = ""


@dataclass(slots=True)
class Image:
    """图片，``src`` 是资源标识或 URL。"""

    src: str = ""


@dataclass(slots=True)
class File:
    """文件。"""

    src: str = ""
    title: str | None = None


@dataclass(slots=True)
class Video:
    """视频。"""

    src: str = ""


@dataclass(slots=True)
class Audio:
    """语音。"""

    src: str = ""


@dataclass(slots=True)
class Br:
    """独立换行。"""


type SatoriElement = Text | At | Quote | Image | File | Video | Audio | Br

_TAGS: dict[str, type[Text | At | Quote | Image | File | Video | Audio | Br]] = {
    "at": At,
    "quote": Quote,
    "img": Image,
    "file": File,
    "video": Video,
    "audio": Audio,
    "br": Br,
}

_MEDIA_TAGS: dict[str, type[Image | File | Video | Audio]] = {
    "img": Image,
    "file": File,
    "video": Video,
    "audio": Audio,
}


def parse(content: str) -> list[SatoriElement]:
    """解析 content 标记文本；无法识别的标签按原文当作文本保留。"""
    elements: list[SatoriElement] = []
    position = 0
    for match in _TAG_RE.finditer(content):
        if match.start() > position:
            text = unescape(content[position : match.start()])
            if text:
                elements.append(Text(text))
        tag = match.group(1)
        attributes = {key: unescape(value) for key, value in _ATTR_RE.findall(match.group(2) or "")}
        element = _make_element(tag, attributes)
        if element is None:
            elements.append(Text(match.group(0)))
        else:
            elements.append(element)
        position = match.end()
    tail = unescape(content[position:])
    if tail:
        elements.append(Text(tail))
    return elements


def serialize(elements: "list[SatoriElement] | SatoriElement") -> str:
    """把元素序列化成 content 标记文本。"""
    if not isinstance(elements, list):
        elements = [elements]
    return "".join(render(element) for element in elements)


def render(element: SatoriElement) -> str:
    """渲染单个元素。"""
    match element:
        case Text(text=text):
            return escape(text)
        case Br():
            return "<br/>"
        case At():
            return _tag("at", id=element.id, name=element.name, role=element.role, type=element.type)
        case Quote():
            return _tag("quote", id=element.id)
        case Image():
            return _tag("img", src=element.src)
        case File():
            return _tag("file", src=element.src, title=element.title)
        case Video():
            return _tag("video", src=element.src)
        case Audio():
            return _tag("audio", src=element.src)
    return ""


def escape(text: str) -> str:
    """转义文本中的标记字符。"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def unescape(text: str) -> str:
    """反转义文本。"""
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&amp;", "&")


def _tag(tag: str, **attributes: str | None) -> str:
    rendered = "".join(f' {key}="{escape(value)}"' for key, value in attributes.items() if value)
    return f"<{tag}{rendered}/>"


def _make_element(tag: str, attributes: dict[str, str]) -> SatoriElement | None:
    if tag == "br":
        return Br()
    if tag in _MEDIA_TAGS:
        media = _MEDIA_TAGS[tag](src=attributes.get("src", ""))
        if isinstance(media, File) and attributes.get("title"):
            media.title = attributes["title"]
        return media
    if tag == "at":
        return At(
            id=attributes.get("id"),
            name=attributes.get("name"),
            role=attributes.get("role"),
            type=attributes.get("type"),
        )
    if tag == "quote":
        return Quote(id=attributes.get("id", ""))
    return None
