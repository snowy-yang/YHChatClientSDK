# AGENT.md

给 AI 编码助手（以及人类贡献者）的项目说明。动手前先读完。

## 项目是什么

云湖（YHChat）的**非官方** Python SDK，目标是覆盖 [yhchatAPI 文档站](https://github.com/snowy-yang/yhchatAPI) 里全部 242 个端点，
并在此之上提供 Satori v1 协议端（聊天子集）与 HTTP/2 服务。
与云湖官方无关，接口行为以实际返回为准。

## 语言与分支

- 文档、提交信息、代码注释用中文；标识符、字段名用英文。
- `main` 承载实现代码与文档；`v1.5` / `v1` 是旧版同步实现，只作存档，**不要**把旧代码搬回来。
- 每阶段结束时 `ruff check`、`pyright`、`pytest` 必须全绿；提交信息中文、一次提交一件事。
- 当前约定：只本地提交，不 push（除非用户明确要求）。

## 工具链

```bash
uv sync                 # 同步 .venv（Python 3.12 由 .python-version 固定）
uv run ruff check .     # lint：E/W/F/I/UP/B/SIM/C4/RUF/PERF/TCH/RET/PIE/ASYNC/LOG/G/PYI
uv run ruff format .    # format（docstring 里的代码块也会格式化）
uv run pyright          # strict 模式，禁 type: ignore
uv run pytest -q        # respx 模拟 HTTP，不碰真实接口
```

- 依赖用 `uv add` / `uv remove`，不要手改 `uv.lock`。
- `*.md` 被排除在 ruff 之外（ruff 0.17 会格式化 Markdown 代码块，已有意关掉）。
- 中文全角标点触发的 `RUF001/002/003` 已忽略。

## 代码约定

- **异步优先**：`httpx.AsyncClient`，不引入同步封装；不允许阻塞调用进事件循环。
- **传输层唯一出口**：所有请求走 `transport.HttpTransport.request()`，它负责注入 `token`、解析 `{code,msg,data}`、
  把网络错误转成 `TransportError`、把 `code != 1` 转成 `APIError`。不要绕过它直接 new httpx。
- **模型**：继承 `models.base.ApiModel`（`populate_by_name=True`、`extra="allow"`）；云湖字段是 camelCase，
  用 `Field(alias=...)` 映射，Python 侧用 snake_case。
- **pydantic 构造不要用字段名**：pyright 认不出别名，统一 `Model.model_validate({"msgId": ...})`。
- **类型注解在运行时求值**（没有 `from __future__ import annotations`），所以注解里用到的类型要正常 import，
  不要塞进 `if TYPE_CHECKING`。
- **错误**：`APIError(code, message, endpoint=...)`；缺字段一律 `TransportError`，不要用 `KeyError`/`AssertionError`。
- **消息记录**：发送/接收到的消息登记进 `MessageRegistry`（LRU，进程内），编辑/撤回据此补全会话信息。

## 服务器与 CLI 约定

- `yhchat serve` 默认 `--server granian` 且 HTTP/2 默认开启（`--no-http2` 关闭）；uvicorn 是备选，
  h2 需显式 `--http2` 并依赖 `zttp`（已在 `server` extra，缺依赖启动前报错退出）。不要删掉 h2c 兼容。
- Granian 的 `dotenv`/`pname`/`reload`/`rloop` extras 只对 Granian CLI 生效，嵌入 `Server` 不消费，
  不要为了"功能齐全"把它们塞进依赖。
- `create_app()`（`server/app.py`）从 `YHCHAT_*` 环境变量构造应用，供
  `uvicorn yhchat.server.app:create_app --factory` 使用；`close_client=True` 保证 lifespan 退出时关连接池。
- 新增 runner 时把 TLS 参数逐项译成对应库的 `ssl_*` 参数；不要在这里写业务逻辑。

## Satori 约定

- `SatoriChatServer`（`satori/server.py`）只认 `SatoriBackend` 协议；云湖字段假设全部写在
  `satori/backend.py` 的 `YHChatBackend` 里。改云湖映射不要动协议层，反之亦然。
- 消息内容是**标记文本**（`<at id="..."/>`、`<quote id="..."/>`、`<img src="..."/>`、`<br/>`），
  解析/渲染在 `satori/elements.py`；未知标签按原文当文本保留。
- Satori 响应是裸 JSON，没有 `{code,msg,data}` 包封；不支持的动作返回 **404**，不要用 501。
- WS 帧：`op:3`→`op:4` 握手、`op:1`→`op:2` 心跳、`op:0` 推事件；token 错误关闭码 3000。
- 事件统一走 `EventBus`（`satori/bus.py`），webhook 接入后由它投递；`sn` 在 publish 时分配。
- 测试：HTTP 用 `httpx.ASGITransport`，WS 用 `starlette.testclient.TestClient`
  （starlette 1.x 需要 `httpx2`，已在 dev 依赖里）。

## v1 端点约定

- 文档仓库（`~/Default/yhchatAPI`）是 **GPLv3**：只取协议事实（路径、方法、字段名、收发格式），
  不要复制文档/注释原文；proto 也按字段号手写最小子集。
- `v1/*` 的 token 在**请求头 `token`**，`open-apis` 在查询参数；由 `HttpTransport(auth="query"|"header")` 区分，
  客户端里 `client.bot` 用前者、`client.v1` 用后者（需要 `user_token`）。
- `src/yhchat/api/v1/` 全部由 `tools/gen_v1_api.py` 生成，**不要手改**；新增/修正端点先改生成规则再重跑：
  `uv run python tools/gen_v1_api.py && uv run python tools/gen_endpoints.py`。
- 生成的方法是「路径 + 原始 JSON 透传」（未建模），所以新增端点的测试至少覆盖：路径、header token、
  body/params 透传、`code != 1` 抛 `APIError`。
- protobuf/XML/外部地址端点一律跳过并写进 `docs/v1_pending.md`，不要生成半成品。

## protobuf 端点约定

- 消息定义在 `proto/yhchat/proto/_pb/full.proto`：**只按字段名/字段号手写需要的最小子集**，
  不复制文档站 `full.proto` 的文本/注释（文档仓库 GPLv3）；`package yh` 必须保持，否则 wire 不兼容。
- 生成：`uv run python tools/gen_proto.py` → `src/yhchat/proto/_pb/`；该目录进了 ruff/pyright 的 exclude，
  靠同时生成的 `.pyi` 提供类型。新增 proto 后必须重跑生成，别手改生成物。
- 端点实现在 `src/yhchat/api/v1/_proto.py`（手写，挂在 `client.v1.proto.<组>`）；新增一条要同步
  `PROTO_ENDPOINTS`，生成器扫描 `api/v1/_*.py` 里的 `*_ENDPOINTS` 据此算覆盖率并写 `implemented.txt`。
- 非 JSON/protobuf 的端点在 `_extra.py`（`client.v1.extra`），同样登记进 `EXTRA_ENDPOINTS`；
  外部地址（如七牛上传 URL）不算云湖端点，不登记。
- 登录端点（`/v1/user/verification-login`、`email-login`、`captcha`）**不需要 token**，走
  `client.auth`（`HttpTransport(auth="none")`）；生成器产出的 `client.v1.user.*` 版本会带用户 token，
  只适合已登录场景。`logout` 的 body 字段是 `device-id`（连字符），token 在请求头。
- 登录后切账号用 `await client.use_user_token(token)`，它会关掉旧的 v1 连接池；不要手改 `_v1_http`。
- **会话持久化归服务端**：SDK 侧（`client.auth`、`LoginSession`）只发请求/校验响应，不落盘；
  落盘逻辑只在 `server/sessions.py`，`YHChatServer` 负责登录/退出路由和启动恢复。不要在 SDK 里加文件 IO。
- `/session/*` 接口可选 `session_token` 鉴权；新增会话路由时必须调用 `_session_authorized`，
  且响应里**不能出现 token**（用 `StoredSession.public()`）。
- `/v1/user/info` 是 **GET + protobuf**（已实测），不是 web 文档写的 JSON；生成器会跳过所有
  `_*.py` 里登记过的手写路径，避免同一路径再生成一个 JSON 方法。
- `group/list-member` 与 `msg/list-message` 的 `total` 服务端恒为 0，分页/判空不要依赖它。
- 错误处理：响应消息体的 `Status.code != 1` 抛 `APIError`（带 `endpoint`），HTTP 4xx/5xx 抛 `TransportError`。
- 测试用 respx 断言「请求字节能被反序列化回原消息」+「响应字节能被解析成嵌套结构」，不要只断言路径。

## 服务与 CLI 约定

- webhook 按 `header.eventId` 做 LRU 去重（`dedupe_size` 默认 1024）；改动回调处理时不要绕过它，否则
  云湖重投会产生重复事件。
- TLS 参数（`--ssl-cert/--ssl-key/--ssl-key-password/--ssl-ca/--ssl-client-verify`）直接透传给 Granian；
  `--ssl-cert` 与 `--ssl-key` 必须成对，缺一个返回退出码 2。

- `server/app.py` 只做装配：`/health`、`/webhook`、`Mount("/satori", ...)`；把云湖回调翻译成 Satori 事件在
  `server/webhook.py`（`parse_webhook` → `to_satori_event`），不要在 app 里堆映射逻辑。
- 非消息事件（`eventType` 不是 `message.receive.*`）必须 200 应答并忽略：云湖对非 2xx 会重试。
- CLI 入口在 `cli.py`，granian 在 `run_granian` 里**延迟导入**，保证核心 SDK 不背 server 依赖。
  新增参数时同步 `tests/test_cli.py` 的默认值断言。
- h2c / HTTP/1.1 都走 granian 的 `HTTPModes.auto`；WS 走 HTTP/1.1。改动服务层后用真实进程冒烟：
  `uv run yhchat serve ...` 然后 curl `/health`。

## 新端点接入流程

1. 在 `docs/ENDPOINTS.md` 里找到目标端点（清单由 `uv run python tools/gen_endpoints.py` 生成）；
2. 在 `src/yhchat/models/` 加请求/响应模型，在 `src/yhchat/api/` 加方法（按文档分组建模块）；
3. 用 `tests/` 里的 respx 契约测试固定"请求长什么样"（路径、query、body 字段名）与"响应怎么解析"；
4. 更新 `docs/ENDPOINTS.md` 的覆盖状态，跑绿 ruff / pyright / pytest。

## 验证方式

- 单测只验证契约（请求形状 + 响应解析），**没有**真实接口的端到端测试：没有 token、也没有公网回调地址。
- 需要真机验证的改动，在提交信息里写清"未验证"，不要声称已测试。

## 已知风险与待确认

- 三个上传接口（`image/video/file upload`）不在文档站内，字段名来自旧实现。
- `/bot/messages` 文档用 `message-id`，旧实现用 `msg-id`，二者必有一错。
- 文档把按钮 `actionType` 的 1/2 注释写反了；按示例语义实现为 1=跳转、2=复制。
- `v1/*` 接口只有 proto、无 JSON 示例，字段命名（snake_case）与鉴权方式（用户 token）都是假设，
  实现时必须标注"未验证"。
- 环境里有 `HTTP(S)_PROXY`，测试里统一 `trust_env=False`，否则 respx 会被代理配置干扰。

## 参考资料

- 云湖 API 文档站：<https://github.com/snowy-yang/yhchatAPI>，本机浅克隆在 `~/Default/yhchatAPI`（仓库外，不要复制进来）。
- Satori 协议 v1：HTTP RPC `POST /v1/{resource}.{method}` + WS `/v1/events`；握手 `op3 → op4`、心跳 `op1/op2`；
  事件体 `{sn,type,timestamp,login,<提升的资源>}`；不支持的 API 返 404；分页 `{data,next}`。
- 云湖官网：<https://www.yhchat.com/>
