# YHChatClientSDK

云湖（YHChat）的**非官方** Python SDK。异步、强类型（pydantic v2），按 [yhchatAPI 文档站](https://github.com/snowy-yang/yhchatAPI) 逐端点实现。

> 本项目与云湖官方无关；接口行为以云湖实际返回为准。

## 项目状态

| 能力 | 状态 |
| --- | --- |
| `/open-apis/v1` 机器人接口（发送/批量/流式/编辑/撤回/消息列表） | 已实现 |
| 图片 / 视频 / 文件上传（文档未收录，云端实际提供） | 已实现 |
| 文档站 242 个端点（`v1/*`、`web/v1/*`，含 protobuf 与 XML 端点） | **已实现 242/242** |
| Satori v1 协议端（聊天子集：HTTP RPC + WebSocket） | 已实现聊天子集，未支持的 action 返回 404 |
| gRPC 层（Send/BatchSend/SendStream/Edit/Recall/ListMessages/Upload） | 已实现 |
| HTTP/2 ASGI 服务与 CLI（webhook 接收 + Satori 挂载） | 已实现 |

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

## v1 用户接口

`v1/*` 把**用户 token 放请求头**（`open-apis` 是查询参数），因此单独挂 `client.v1`：

```python
async with YHChatClient("机器人 token", user_token="用户 token") as client:
    result = await client.v1.community.posts_create({"title": "标题", "content": "正文"})
    print(result["data"])
```

- 分组与文档一一对应：`client.v1.community`、`.user`、`.group`、`.web_user` ……（37 组、205 个 JSON 端点）。
- 方法名由路径生成（`/v1/community/posts/create` → `posts_create`）；**返回原始 JSON 响应**（含 `code/msg/data`），
  未逐字段建模；参数用 `body=...` 透传，GET 用 `params=...`。
- 生成器：`uv run python tools/gen_v1_api.py`（读 `~/Default/yhchatAPI/src/api`，写 `src/yhchat/api/v1/`，
  并把已实现路径合并进 `docs/implemented.txt`）。生成物勿手改，改规则改生成器。
- `docs/v1_pending.md` 记录待实现端点（当前为空）；覆盖率明细见 `docs/ENDPOINTS.md`。

### 客户端登录

登录端点本身**不需要 token**，所以挂在 `client.auth`；拿到 `LoginSession` 后用
`client.use_user_token(session.token)` 切到该账号：

```python
async with YHChatClient("机器人 token") as client:
    session = await client.auth.login_with_email("me@example.com", "密码")
    await client.use_user_token(session.token)

    me = await client.v1.proto.user.info()    # protobuf，GET /v1/user/info
    print(me.data.name)
    await client.auth.logout(session)         # 请求体是 device-id，token 走请求头
```

- 短信登录：`client.auth.login_with_verification("手机号", "验证码")`，验证码图片用 `client.auth.captcha()`。
- `deviceId`：文档明确"登录设备唯一标识符，可自定义"（WS 文档写"可随便写"），SDK 默认随机 16 位十六进制；
  退出登录/下线设备要用同一个 `deviceId`。
- `platform`：HTTP 登录"可自定义,不校验"，但 **WS 登录**要求 `windows`/`macos`/`android` 等固定值且
  大小写敏感，所以默认 `windows`。
- 登录响应只有 `data.token`，文档没给过期时间；SDK 不持久化 token，需要自己存。
- 邮箱密码按文档示例**明文提交**，SDK 不做哈希。
- 已用真实账号核对：邮箱登录返回 36 字符 token；密码错误返回 `{"code": -1, "msg": "密码错误"}`
  （不区分账号是否存在，SDK 抛 `APIError(code=-1)`）；`captcha()` 返回 `data.b64s`，
  形如 `data:image/png;base64,...`。
- 实测中脚本异常退出过两次，留下了两个未 `logout` 的设备会话；token 按次签发，事后无法替它们退出，
  需要在云湖 App 的「登录设备」里手动下线。

### protobuf 端点

`v1` 里 29 个端点用 protobuf 收发（`msg`、`user`、`group`、`bot` 等），它们的错误码在消息体的 `Status` 里，
所以单独挂在 `client.v1.proto`（`msg` 9、`user` 4、`group` 7、`bot` 5、`friend` 2、`group-tag` 1、`conversation` 1、`instruction` 1）：

```python
from yhchat.proto._pb import full_pb2

response = await client.v1.proto.msg.send_message(
    full_pb2.SendMsgRequest(
        chat_id="群 ID",
        chat_type=full_pb2.ChatType.group,
        content_type=full_pb2.ContentType.text,
        content=full_pb2.MsgContent(text="你好"),
    )
)
print(response.status.code, response.status.msg)
```

- 消息定义在 `proto/yhchat/proto/_pb/full.proto`：**只按字段号手写需要的最小子集**（文档站附带的 `full.proto` 是 GPLv3，
  不复制它的文本），生成代码在 `src/yhchat/proto/_pb/`。
- 非 1 的 `Status.code` 抛 `APIError`，HTTP 4xx/5xx 抛 `TransportError`。

### XML 端点

`/v1/misc/auto-update` 返回 Sparkle appcast XML，挂在 `client.v1.extra`：

```python
xml_text = await client.v1.extra.auto_update(platform="windows", user_id="123")
```

## gRPC

gRPC 是可选依赖（`uv sync --extra grpc`），只做传输与类型约束，业务逻辑仍在核心 SDK。

```python
import grpc

from yhchat import YHChatClient
from yhchat.grpc import YHChatRpcClient, serve
from yhchat.grpc._pb import yhchat_pb2
```

服务端：

```python
async with YHChatClient("机器人 token") as client:
    server, port = await serve(client, host="127.0.0.1", port=50051)
    await server.wait_for_termination()
```

客户端：

```python
async with grpc.aio.insecure_channel(f"127.0.0.1:{port}") as channel:
    stub = YHChatRpcClient(channel)
    reply = await stub.send(
        yhchat_pb2.SendRequest(
            recv_type="group",
            recv_id="群 ID",
            content=yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_TEXT, text="你好"),
        )
    )
    print(reply.message.msg_id)
```

- 服务定义：`proto/yhchat/grpc/_pb/yhchat.proto`，用 `uv run python tools/gen_proto.py` 重新生成；
  生成代码在 `src/yhchat/grpc/_pb/`，不参与 lint 与类型检查，不要手改。
- 错误映射：`APIError` → `FAILED_PRECONDITION`；`TransportError` / 参数问题 → `INVALID_ARGUMENT`。
- 流式：`SendStream` 是客户端流，首块带 `recv_type` / `recv_id` / `content_type`，后续只带 `chunk`。

## Satori v1 聊天子集

自研协议端，不依赖 `satori-python` 服务端实现。`SatoriChatServer` 只依赖
`SatoriBackend` 协议，云湖字段假设集中在 `YHChatBackend`，两者解耦。

```python
from yhchat import YHChatClient
from yhchat.satori import YHChatBackend
from yhchat.satori.server import SatoriChatServer
```

```python
async with YHChatClient("机器人 token") as client:
    backend = YHChatBackend(client, self_id="机器人 ID")
    server = SatoriChatServer(backend, token="satori token")   # token 为 None 时不鉴权
    app = server.build_app()   # 交给 granian / uvicorn 跑

    # 有新事件时投递；WS 客户端会收到 op:0 帧
    # await server.bus.publish(event)
```

协议要点：

- `POST /v1/{action}`：参数 snake_case，响应是**裸 JSON**（无 `{code,msg,data}` 包封）；
  鉴权用 `Authorization: Bearer`，缺失/错误返回 401。
- `GET /v1/events`：`op:3 IDENTIFY`（body 带 `token`/`sn`）→ `op:4 READY`；
  `op:1` → `op:2` 心跳；`op:0` 推事件（body 是 Satori Event，`sn` 递增）。
  token 错误用关闭码 **3000**。
- 未实现的动作按协议返回 **404**（不是 501），未知动作同样 404。

已支撑：`message.create/get/list/update/delete`、`login.get`、`channel.get`、
`channel.list`、`guild.get/list`、`guild.member.get/list`、`user.get`、`friend.list`。
映射关系：

- `guild.list` → `bot/join-group-list`（机器人加入的群，`next_token` 是页码）；
- `guild.get` → `group/info`；`guild.member.*` → `group/list-member`（按 `keywords` 过滤单成员）；
- `user.get` → `user/get-user`（`4402`/`7100` 转成 404）；`friend.list` → `friend/address-book-list`
  （只取 `chat_type == user` 的分组，`next_token` 用返回的 `md5`）；
- `channel.list()` 不带 `guild_id` 时用 `conversation/list` 兜底——云湖没有跨群频道列表端点；
- 群成员权限级别塞进 `Member.roles[0].id`，没有真实角色体系。

字段假设（云湖文档没有对应说明，属于推断，已在代码注释标注）：

- `guild` = 群，`channel` = 会话；群聊 `channel.type = 0`、私聊 `1`；
- 发送需要 `recvType` 而 Satori 只给 `channel_id`：`ChannelRegistry` 记住入站事件的类型，
  未知时退回默认 `group`（可构造时改）；
- 图片/视频/文件的 `src` 填云湖的 key，不是真实 URL；
- `message.list` 用 `message-id` 当游标，`before`/`after` 当计数。

wire 形状已用参考实现 `satori-python-client`（1.3.7）的 `Ready/Event/MessageObject/PageResult`
解析器交叉验证；未做真实网络端到端联调（没有 token 与回调地址）。

## HTTP 服务与 CLI

`yhchat serve` 用 Granian 跑 ASGI，同时提供健康检查、云湖回调接收和 Satori 挂载（需要 `server` extra）：

```bash
uv sync --extra server
uv run yhchat serve --token "机器人 token" --self-id "机器人 ID" --port 5140
```

| 路由 | 说明 |
| --- | --- |
| `GET /health` | 健康检查，返回 `{status, satori, subscribers}` |
| `POST /webhook` | 云湖回调（`message.receive.normal` / `message.receive.instruction`）→ Satori 事件 → `EventBus` |
| `/satori/v1/{action}` | Satori HTTP RPC |
| `/satori/v1/events` | Satori WebSocket |
| `GET /session` | 当前登录会话（`user_id` / `device_id` / `platform`，**不含 token**） |
| `POST /session/login` | `{"email","password"}` 或 `{"mobile","captcha"}` 登录，落盘后供后续 v1 调用 |
| `POST /session/logout` | 退出登录并删除会话文件 |

常用参数：`--satori-token`（不传则不鉴权）、`--webhook-path` / `--satori-path`（可改成云湖后台登记的回调路径）、
`--grpc-port`（同时起 gRPC）、`--no-http2`（只留 HTTP/1.1）、`--no-trust-env`
（环境变量里 `HTTP(S)_PROXY`/`NO_PROXY` 非法时用，否则 httpx 会在启动时抛 `InvalidURL`）。

TLS：`--ssl-cert` + `--ssl-key`（必须成对）、`--ssl-key-password`、`--ssl-ca` +
`--ssl-client-verify`（mTLS）。参数直接传给 Granian；只给证书不给私钥会以退出码 2 拒绝启动。

会话：`--session-file`（默认 `$XDG_CONFIG_HOME/yhchat/session.json`，权限 0600）、
`--session-path`（默认 `/session`）、`--no-session`（不启用）、`--session-token`
（会话接口的 Bearer token，公网部署务必设置）。

### 登录会话保存（服务端）

**SDK 不保存会话**：`client.auth.login_*` 只发请求、校验响应，返回内存里的 `LoginSession`。
持久化在服务端做，`yhchat serve` 把它写成 0600 的 JSON 文件，重启时由 lifespan 自动恢复：

```bash
# 登录（token 只在服务端，响应里不会返回）
curl -X POST http://127.0.0.1:5140/session/login \
  -H "Content-Type: application/json" \
  -d '{"email": "me@example.com", "password": "密码"}'

# {"user_id":"450…","name":"…","device_id":"…","platform":"windows","created_at":1760…}

curl http://127.0.0.1:5140/session            # 查当前会话（无 token 字段）
curl -X POST http://127.0.0.1:5140/session/logout
```

- 会话文件内容：`user_id` / `token` / `device_id` / `platform` / `created_at`；原子写、0600、父目录 0700。
- 重启后 `YHChatServer.restore_session()`（lifespan 调用）把 token 注入 `YHChatClient`，
  后续 v1 请求直接可用。
- 登录时 `device_id` 可传，不传随机生成；`platform` 默认 `windows`（WS 登录认这个值）。
- 会话接口默认**不鉴权**，只适合监听 `127.0.0.1`；公网部署请加 `--session-token`，
  客户端带 `Authorization: Bearer <token>`。

已验证（真实进程 + 真实 socket）：HTTP/1.1 与 **h2c（HTTP/2 prior knowledge）** 的 `/health` 都是 200；
`POST /webhook` → WS 收到 `op:0` 的 `message-created`，`sn` 递增、content 为 `<at id="u2"/>hi`。

事件只做了消息类：其它 `eventType` 一律 200 应答并忽略（云湖会重试非 2xx）。
回调按 `eventId` 做 **LRU 去重**（默认 1024 条，`YHChatServer(..., dedupe_size=...)` 可调），重复回调返回
`{"duplicated": true}` 且不再推事件。**未做**：回调签名校验——云湖文档没有签名机制，公网部署请自行加
IP 白名单或反向代理层校验。

## 真实账号实测记录

用真实账号跑过一次登录 + 只读端点（未发消息、未改任何数据，登录会话已 `logout`）：

| 端点 | 结果 |
| --- | --- |
| `POST /v1/user/email-login` | 成功，`data.token` 为 36 字符；错误密码 `code=-1`/`密码错误` |
| `GET /v1/user/info` | 返回 **protobuf**；`id/name/avatarUrl/phone/email/coin/isVip/vipStatus/invitationCode` 全部能解析 |
| `POST /v1/friend/address-book-list` | 成功，返回 3 个分组（`chat_type` 1/2/3），条目数 7/11/5 |
| `POST /v1/conversation/list` | 成功，21 条会话，类型分布 user=6 / group=11 / bot=4 |
| `POST /v1/group/info` | 成功，`headcount`、`admin`、`introduction` 正常 |
| `POST /v1/group/list-member` | 成功，成员 `permission_level` 100/2/0；**`total` 恒为 0**（服务端不填） |
| `POST /v1/user/get-user` | 成功（token 可以随便填，与文档一致） |
| `POST /v1/msg/list-message` | 成功，字段名与 `full.proto` 一致；`direction=left`、`content_type=1`、`msg_seq` 新→旧；**`total` 恒为 0** |

未实测：发消息/撤回/编辑等**写操作**（避免动到真实数据）、WS 登录的 platform 白名单、需要机器人 token 的
`open-apis` 与 `bot/*` 端点、上传接口。

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
uv run python tools/gen_proto.py     # 重新生成 gRPC 代码（proto 改动后）
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
│   ├── api/bot.py        # /open-apis/v1 机器人接口
│   ├── grpc/             # gRPC 门面：convert / client / server / _pb（生成）
│   ├── satori/           # Satori v1 聊天子集：elements / models / bus / backend / server
│   └── server/           # ASGI 组合：health / webhook / Satori 挂载 / 登录会话保存
├── src/yhchat/cli.py     # yhchat serve
├── proto/yhchat/grpc/_pb/yhchat.proto
├── tools/gen_endpoints.py
├── tools/gen_proto.py
├── docs/ENDPOINTS.md     # 生成的端点清单（含覆盖状态）
├── tests/
├── pyproject.toml        # 依赖 + ruff / pyright / pytest 配置
├── AGENT.md              # 给 AI 助手与贡献者的实现约定
└── LICENSE               # MPL-2.0
```

## 已知不一致

- `/v1/user/info`：`v1/user.md` 写 **protobuf**、`web/v1/user.md` 写 **JSON**。**已实测**：真实请求返回
  `200 application/x-protobuf`（171 字节），web 文档的 JSON 版本不成立。SDK 现在只有 protobuf 实现
  `client.v1.proto.user.info()`，生成器不再为这个路径产出 JSON 方法（`web_user.info` 已移除）。

- 文档把按钮 `actionType` 的 1/2 注释写反了；本 SDK 按示例语义处理：**1=跳转（带 url）、2=复制（带 value）**。
- `/bot/messages` 文档用 `message-id` 查询参数，旧版实现用的是 `msg-id`，本 SDK 按文档实现，待用真实 token 验证。
- 三个上传接口不在文档站里，字段名（`imageKey` / `videoKey` / `fileKey`）来自旧版实现，待验证。
- `v1/*` 接口只有 proto 定义、没有 JSON 示例，字段命名（snake_case）属于假设。

## 许可证

[Mozilla Public License 2.0](LICENSE)（SPDX：`MPL-2.0`）。
