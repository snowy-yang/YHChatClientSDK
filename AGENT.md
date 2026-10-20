# AGENT.md

给 AI 编码助手（以及人类贡献者）的项目说明。动手改代码前先读完这份文件。

## 项目是什么

云湖（YHChat）的**非官方** Python SDK，用同步 HTTP 方式调用云湖开放接口，并接收 Webhook 事件。
仓库作者与云湖官方无关，接口行为以云湖开放平台的文档和实际返回为准。

## 语言约定

- 文档、提交信息、代码注释用中文；标识符、字段名用英文。
- README 中文优先，不需要英文镜像。

## 分支模型

| 分支 | 用途 |
| --- | --- |
| `main` | 文档、许可证、工具链配置（`pyproject.toml` / ruff / pyright），不放实现代码 |
| `v1.5` | 新版实现（`message.py` / `openapi.py` / `subscription.py`），日常开发 |
| `v1` | 旧版实现，只做必要修复 |

- 实现代码的改动提交到 `v1.5`，不要顺手塞进 `main` 的文档提交里。
- `main` 的历史被重写过（首个提交是许可证与 README），再次改写前先跟用户确认。

## 工具链

- 依赖与虚拟环境用 uv 管理：`pyproject.toml` + `uv.lock`，Python 3.11 由 `.python-version` 固定。
- 改依赖用 `uv add` / `uv remove`，不要手改 `uv.lock`。
- 静态检查与类型检查：

```bash
uv sync                 # 同步 .venv（首次会装 Python 3.11）
uv run ruff check .     # lint
uv run ruff format .    # format
uv run pyright          # 类型检查
```

- 配置都在 `pyproject.toml`：ruff 选 `E/F/I/UP/B/SIM/RUF`、行宽 120、`target-version = py311`，排除 `.venv` 与 `*.md`
  （ruff 0.17 会格式化 Markdown 里的代码块，已有意关掉）；pyright 用 `standard` 模式。

## 代码结构（v1.5）

- `message.py`：pydantic 模型 `MessageSegment` / `MessageType` / `Button` / `ButtonType` / `MessageInfo`；
  同时用 SQLAlchemy 建表 `message`（`sqlite:///message.db`，message.py:7），提供
  `add_message_record` / `query_message_record` / `delete_message_record`，记录 `msg_id → recv_type / recv_id`。
- `openapi.py`：`Openapi` 类持有 `httpx.Client`（`base_url = https://chat-go.jwzhd.com/open-apis/v1`，
  token 作为查询参数），方法 `send_message` / `edit_message` / `delete_message` / `get_message`。
- `subscription.py`：`bottle` 应用，路由 `/`（subscription.py:55）接云湖回调；`pyee` 的
  `ExecutorEventEmitter` 把事件投递到线程池；事件模型为 `MessageEvent*`。

## 代码约定

- pydantic v2：云湖字段是 camelCase，用 `Field(alias=...)` 映射；对象级校验用 `@model_validator(mode="after")`。
- 云湖返回 `code == 1` 视为成功，失败抛 `ValueError(resp["msg"])`；新代码保持这一风格。
- 同步实现：`httpx.Client` + 线程池，暂不引入 `async` / `asyncio`。
- SQLAlchemy 2.x 写法（`declarative_base`、`sessionmaker`），每个函数内 session 用完即 `close()`。
- 最低 Python 3.11（用到了 `enum.StrEnum`）。

## 验证方式

- 仓库没有测试套件、没有 CI，所以不要声称"已测试"。
- 提交前至少跑通 `uv run ruff check .` 与 `uv run pyright`。
- 冒烟检查：`uv run python -c "import message, openapi, subscription"`（需要实现代码在工作区里）；
  注意导入 `message` 会在当前工作目录创建 `message.db`。
- 真实接口验证需要机器人 token 和可公网访问的回调地址，只能手工做。

## 提交与安全

- 提交信息用中文，一次提交做一件事。
- 不要提交 token、`message.db`、日志；`.gitignore` 已排除 `.venv/`、`__pycache__/`、`.ruff_cache/`、`message.db`。
- `uv.lock` 要提交，`.venv/` 不提交。
- 涉及真实机器人调用时先在测试群验证，避免向用户群发消息。

## 参考资料

- 云湖 API 文档站：<https://github.com/snowy-yang/yhchatAPI>（TypeScript + VuePress，接口正文在 `src/api/**/*.md`，
  另有 `src/full.proto`）。本机参考副本在仓库外的 `~/Default/yhchatAPI`，**不要**接入本仓库或复制其文件进来。
- 云湖官网：<https://www.yhchat.com/>

## 已知问题与待办

- README「功能进度」里未勾选的接口与事件尚未实现：批量发送、看板相关接口、关注/取关、入群/退群、按钮点击。
- `delete_message` 与 `edit_message` 共用 `/bot/edit` 端点，删除请求没带 `contentType` / `content`（openapi.py:102），需对照云湖文档核实。
- `send_message` 里 `elif isinstance(message, MessageSegment)`（openapi.py:84）恒为真，`message` 是循环变量，
  所以列表模式遇到失败也会立刻抛错、不会跳过，需确认是否符合预期。
- 事件转 `MessageSegment` 依赖 `content` 的键与模型字段同名（subscription.py:46），新增内容类型时要同步改。
- `message.db` 按当前工作目录创建，从不同目录启动会产生多个库。
- `get_message` 直接返回 `.json()`，未做状态码/`code` 校验；网络异常会让 `httpx` 异常直接冒泡。
