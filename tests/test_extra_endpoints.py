"""非 JSON/protobuf 端点：``/v1/misc/auto-update`` 返回 XML 文本。"""

from collections.abc import AsyncIterator

import httpx
import pytest
import respx

from yhchat import YHChatClient

BASE_URL = "https://chat-go.jwzhd.com"
APPCAST = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>云湖社交</title><item><title>1.2.3</title></item></channel></rss>
"""


@pytest.fixture
async def client() -> AsyncIterator[YHChatClient]:
    async with YHChatClient("bot-token", user_token="user-token", http2=False, trust_env=False) as sdk:
        yield sdk


async def test_auto_update_returns_xml_text(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/misc/auto-update").mock(
            return_value=httpx.Response(200, text=APPCAST, headers={"Content-Type": "application/xml"})
        )

        result = await client.v1.extra.auto_update(platform="windows", user_id="123")

        request = route.calls.last.request
        assert request.headers["token"] == "user-token"
        assert request.url.params["platform"] == "windows"
        assert request.url.params["userId"] == "123"
        assert "<title>1.2.3</title>" in result


async def test_auto_update_http_error(client: YHChatClient) -> None:
    from yhchat.errors import TransportError

    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/misc/auto-update").mock(return_value=httpx.Response(503))

        with pytest.raises(TransportError, match="503"):
            await client.v1.extra.auto_update(platform="ios")
