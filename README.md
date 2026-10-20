# YHChatClientSDK

云湖（YHChat）的**非官方** Python SDK。异步、强类型（pydantic v2），按 [yhchatAPI 文档站](https://github.com/snowy-yang/yhchatAPI) 逐端点实现。

> 本项目与云湖官方无关；接口行为以云湖实际返回为准。

## 项目状态

| 能力 | 状态 |
| --- | --- |
| `/open-apis/v1` 机器人接口（发送/批量/流式/编辑/撤回/消息列表） | 已实现 |
| 图片 / 视频 / 文件上传（文档未收录，云端实际提供） | 已实现 |
| 文档站 `v1/*`、`web/v1/*` 的其余端点（共 242 个） | 规划中 |
| Satori v1 协议端（聊天子集） | 规划中 |
| gRPC 层 | 规划中 |
| HTTP/2 ASGI 服务与 CLI | 规划中 |

端点覆盖清单见 [`docs/ENDPOINTS.md`](docs/ENDPOINTS.md)，由 `tools/gen_endpoints.py` 从文档站生成，是覆盖度的唯一起点。

## 环境要求

- Python ≥ 3.12（使用 `type` 别名、PEP 695 泛型、`typing.override` 等新语法）
- 依赖与虚拟环境用 [uv](https://docs.astral.sh/uv/) 管理

## 获取代码

```bash
git clone https://github.com/snowy-yang/YHChatClientSDK.git
cd YHChatClientSDK
uv sync
```

## 快速开始

```python
import asyncio

from yhchat import TextSegment, YHChatClient


async def main() -> None:
    async with YHChatClient("机器人 token") as client:
        info = await client.bot.message.send("group", "群 ID", TextSegment(text="Hello, 云湖"))
        print(info.msg_id)


asyncio.run(main())
```

### 常用操作

```python
from yhchat import ImageSegment, MarkdownSegment, TextSegment

# 批量发送（同一内容发给多个会话）
await client.bot.message.batch_send(["群 1", "群 2"], "group", TextSegment(text="广播"))

# 上传后发送
key = await client.bot.upload.image(data, filename="cat.png", mime_type="image/png")
await client.bot.message.send("group", "群 ID", ImageSegment(key=key))

# 流式发送（chunked）
async def chunks():
    yield "正在"
    yield "生成……"

await client.bot.message.send_stream("group", "群 ID", "text", chunks())

# 编辑 / 撤回：recv_id、recv_type 可省略，客户端从消息记录里补全
await client.bot.message.edit(info.msg_id, MarkdownSegment(text="**改后**"))
await client.bot.message.recall(info.msg_id)

# 拉取消息列表
page = await client.bot.message.list("群 ID", "group", before=20)
for message in page.messages:
    print(message.sender_id, message.content_type, message.content.text)
```

`client.records` 是 `msgId → 会话信息` 的 LRU 缓存（进程内，不落盘），编辑/撤回时用它补全 `recvId`/`recvType`。

### 逃生口

尚未封装的端点可以直接调用，返回完整响应体：

```python
payload = await client.call("POST", "/open-apis/v1/bot/send", json={"recvId": "群 ID", "recvType": "group"})
```

## 错误处理

- `APIError`：云湖返回 `code != 1` 或 HTTP 4xx/5xx，带 `code` / `message` / `endpoint`。
- `TransportError`：网络失败、超时、返回体不是 JSON、响应缺少必需字段。

## 开发

```bash
uv sync                              # 同步 .venv（首次会装 Python 3.12）
uv run ruff check .                  # lint
uv run ruff format .                 # format
uv run pyright                       # 类型检查（strict）
uv run pytest -q                     # 测试
uv run python tools/gen_endpoints.py # 重新生成端点清单
```

`tools/gen_endpoints.py` 默认读取 `~/Default/yhchatAPI/src/api`（文档站浅克隆），可用 `--docs` 指定。

## 目录结构

```text
.
├── src/yhchat/
│   ├── client.py         # YHChatClient：token、传输层、接口分组
│   ├── transport.py      # {code,msg,data} 解析、token 注入、异常映射
│   ├── errors.py         # APIError / TransportError
│   ├── records.py        # msgId → 会话信息 的 LRU 缓存
│   ├── models/           # pydantic 模型与消息段
│   └── api/bot.py        # /open-apis/v1 机器人接口
├── tools/gen_endpoints.py
├── docs/ENDPOINTS.md     # 生成的端点清单（含覆盖状态）
├── tests/
├── pyproject.toml        # 依赖 + ruff / pyright / pytest 配置
├── AGENT.md              # 给 AI 助手与贡献者的实现约定
└── LICENSE               # MPL-2.0
```

## 已知不一致

- 文档把按钮 `actionType` 的 1/2 注释写反了；本 SDK 按示例语义处理：**1=跳转（带 url）、2=复制（带 value）**。
- `/bot/messages` 文档用 `message-id` 查询参数，旧版实现用的是 `msg-id`，本 SDK 按文档实现，待用真实 token 验证。
- 三个上传接口不在文档站里，字段名（`imageKey` / `videoKey` / `fileKey`）来自旧版实现，待验证。
- `v1/*` 接口只有 proto 定义、没有 JSON 示例，字段命名（snake_case）属于假设。

## 许可证

[Mozilla Public License 2.0](LICENSE)（SPDX：`MPL-2.0`）。
