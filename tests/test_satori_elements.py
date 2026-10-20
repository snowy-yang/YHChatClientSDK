"""Satori content 标记文本的解析与渲染。"""

from yhchat.satori.elements import At, Br, File, Image, Quote, Text, parse, serialize


def test_roundtrip_mixed_content() -> None:
    content = 'hi <at id="u1"/> &lt;x&gt;<br/><img src="a.png"/><file src="f.bin" title="报告.pdf"/>'

    elements = parse(content)

    assert elements == [
        Text("hi "),
        At(id="u1"),
        Text(" <x>"),
        Br(),
        Image(src="a.png"),
        File(src="f.bin", title="报告.pdf"),
    ]
    assert serialize(elements) == content


def test_quote_and_at_attributes() -> None:
    elements = parse('<quote id="m0"/><at type="all"/><at id="u2" name="小明"/>')

    assert elements == [Quote(id="m0"), At(type="all"), At(id="u2", name="小明")]
    assert serialize(elements) == '<quote id="m0"/><at type="all"/><at id="u2" name="小明"/>'


def test_unknown_tag_kept_as_text() -> None:
    assert parse('<foo a="1"/>') == [Text('<foo a="1"/>')]


def test_escape_text() -> None:
    assert serialize(Text('<a href="x"> & </a>')) == "&lt;a href=&quot;x&quot;&gt; &amp; &lt;/a&gt;"


def test_empty_content() -> None:
    assert parse("") == []
    assert serialize([]) == ""
