# AGENT.md

给 AI 编码助手（以及人类贡献者）的项目说明。动手前先读完。

## 项目是什么

云湖（YHChat）的**非官方** Python SDK，目标是覆盖 [yhchatAPI 文档站](https://github.com/snowy-yang/yhchatAPI) 里全部 242 个端点，
并在此之上提供 Satori v1 协议端（聊天子集）、gRPC 层与 HTTP/2 服务。
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

## gRPC 约定

- proto 在 `proto/yhchat/grpc/_pb/yhchat.proto`；路径特意与生成目录对齐，生成的 import 才是 `yhchat.grpc._pb.yhchat_pb2`。
- 改 proto 后跑 `uv run python tools/gen_proto.py`；`src/yhchat/grpc/_pb/` 是生成物，**不要手改**，且被 ruff/pyright 排除。
- 生成的 `_grpc.py` 没有类型标注，所以客户端不用生成的 stub，而是 `channel.unary_unary(...)` +
  `grpc.aio.UnaryUnaryMultiCallable[...]` 自己建强类型调用器（见 `grpc/client.py`）。
- 服务端用生成模块里的 `add_YHChatServicer_to_server` 注册（唯一的 `pyright: ignore` 点），业务方法全部委托给核心 SDK。
- RPC 方法名保持 proto 的 CamelCase；错误统一经 `_grpc_errors` 映射成 gRPC 状态码。

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
