"""``v1/*`` 用户接口：header token、GET/POST、错误映射与生成结果的自检。"""

import inspect
import json
from collections.abc import AsyncIterator
from typing import Any, cast

import httpx
import pytest
import respx

from yhchat import YHChatClient
from yhchat.errors import APIError, YHChatError

BASE_URL = "https://chat-go.jwzhd.com"


def body_of(request: httpx.Request) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(request.content))


@pytest.fixture
async def client() -> AsyncIterator[YHChatClient]:
    async with YHChatClient("bot-token", user_token="user-token", http2=False, trust_env=False) as sdk:
        yield sdk


async def test_v1_requires_user_token() -> None:
    async with YHChatClient("bot-token", http2=False, trust_env=False) as sdk:
        with pytest.raises(YHChatError, match="user_token"):
            _ = sdk.v1


async def test_v1_post_uses_header_token(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/community/posts/create").mock(
            return_value=httpx.Response(200, json={"code": 1, "msg": "success", "data": {"postId": 7}})
        )

        result = await client.v1.community.posts_create({"title": "标题", "content": "正文"})

        request = route.calls.last.request
        assert request.headers["token"] == "user-token"
        assert "token" not in request.url.params
        assert body_of(request) == {"title": "标题", "content": "正文"}
        assert result["data"] == {"postId": 7}


async def test_v1_get_uses_query_params(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/user/homepage").mock(
            return_value=httpx.Response(200, json={"code": 1, "msg": "success", "data": {}})
        )

        await client.v1.web_user.homepage(params={"userId": "123"})

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.params["userId"] == "123"
        assert request.headers["token"] == "user-token"


async def test_v1_without_body_sends_nothing(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/user/captcha").mock(
            return_value=httpx.Response(200, json={"code": 1, "msg": "success", "data": {}})
        )

        await client.v1.user.captcha()

        assert route.calls.last.request.content == b""


async def test_v1_api_error_is_raised(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/community/posts/create").mock(
            return_value=httpx.Response(200, json={"code": -101, "msg": "未登录"})
        )

        with pytest.raises(APIError) as excinfo:
            await client.v1.community.posts_create({"title": "x"})

        assert excinfo.value.code == -101
        assert excinfo.value.message == "未登录"


async def test_every_generated_method_has_optional_params(client: YHChatClient) -> None:
    groups = {name: value for name, value in vars(client.v1).items() if not name.startswith("_")}
    assert len(groups) >= 30

    checked = 0
    for group_name, group in groups.items():
        for method_name in dir(group):
            if method_name.startswith("_"):
                continue
            method = getattr(group, method_name)
            if not inspect.ismethod(method):
                continue
            for parameter in inspect.signature(method).parameters.values():
                assert parameter.default is not inspect.Parameter.empty, (
                    f"{group_name}.{method_name}.{parameter.name} 成了必填"
                )
            checked += 1
    assert checked >= 200


async def test_protobuf_endpoints_are_not_generated(client: YHChatClient) -> None:
    # 这 29 个是 protobuf 收发，等 proto 层接入后再实现，先确认没有半成品
    assert not hasattr(client.v1.msg, "send_message")
    assert not hasattr(client.v1.group, "info")
