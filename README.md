# YHChatClientSDK

云湖（YHChat）的**非官方** Python SDK。

> 本项目为社区实现，与云湖官方无关。接口行为以[云湖开放平台](https://www.yhchat.com/)的实际返回为准。

## 项目状态

| 分支 | 内容 |
| --- | --- |
| `main` | 文档、许可证与发布准备（当前分支） |
| `v1.5` | 新版 SDK 代码，开发中 |
| `v1` | 旧版 SDK 代码 |

- 新版尚未发布到 PyPI，仓库里也还没有 `pyproject.toml`，需要 clone 后直接使用。
- 新版代码尚未经过完整测试，接口可能随云湖开放平台调整而变化。

## 环境要求

- Python ≥ 3.11（代码使用了 `enum.StrEnum`）
- 依赖当前未写进包元数据，需要手动安装：

```bash
pip install pydantic httpx sqlalchemy pyee bottle
```

## 获取代码

```bash
git clone -b v1.5 https://github.com/snowy-yang/YHChatClientSDK.git
cd YHChatClientSDK
```

## 快速开始

### 发送消息

```python
from openapi import Openapi
from message import MessageSegment, MessageType

client = Openapi("你的机器人 token")

client.send_message(
    recv_type="group",  # 会话类型，取值见云湖开放平台文档
    recv_id="会话 ID",
    message=MessageSegment(type=MessageType.text, text="Hello, 云湖"),
)
```

- `message` 可以是单个 `MessageSegment`，也可以是 `MessageSegment` 列表，按顺序逐条发送。
- `image` / `video` / `file` 类型会先调用上传接口，再用返回的 `imageKey` / `videoKey` / `fileKey` 发送。
- `markdown` / `html` 目前都按 `text` 字段提交。
- 返回值是云湖返回的 `messageInfo` 列表。

### 订阅事件

在云湖开放平台配置 HTTP 回调地址后，用 `subscription.py` 起一个 HTTP 服务接收事件：

```python
from bottle import run
from subscription import app, event_emitter

@event_emitter.on("message.receive.normal")
def on_normal(header, event):
    print(header.event_id, event.message.msg_id)

run(app, host="0.0.0.0", port=8080)
```

- 目前只处理 `message.receive.normal`（普通消息）和 `message.receive.instruction`（指令消息）两种事件，其余事件直接返回 200。
- 事件回调通过 `pyee` 的 `ExecutorEventEmitter` 投递到线程池执行，单个回调阻塞不影响 HTTP 响应。
- 接收到的消息会自动写入消息记录，供后续编辑、删除时复用会话信息。

## 数据存储

导入 `message.py` 时会用 SQLAlchemy 在当前工作目录创建 SQLite 数据库 `message.db`，表 `message` 记录 `msg_id → recv_type / recv_id` 的映射。
该记录用于 `edit_message` / `delete_message` 未显式传入 `recv_type`、`recv_id` 时补全会话信息，删除文件后记录会丢失。

## 功能进度

### 事件

- [x] 普通消息事件
- [x] 指令消息事件
- [ ] 关注机器人事件
- [ ] 取消关注机器人事件
- [ ] 加入群事件
- [ ] 退出群事件
- [ ] 消息中按钮点击事件

### 接口

- [x] 发送消息
- [ ] 编辑消息（已有实现，未测试）
- [ ] 删除消息（已有实现，未测试）
- [ ] 拉取消息（已有实现，未测试）
- [ ] 批量发送消息
- [ ] 设置用户看板
- [ ] 设置全局看板
- [ ] 取消用户看板
- [ ] 取消全局看板

## 目录结构

```text
.
├── message.py       # 数据模型（MessageSegment / MessageType / Button / MessageInfo）与消息记录
├── openapi.py       # Openapi 类：主动调用云湖开放接口
└── subscription.py  # Webhook 事件订阅（bottle + pyee）
```

## 分支说明

- `main`：文档、许可证与发布准备。
- `v1.5`：新版实现，日常开发分支。
- `v1`：旧版实现。

## 许可证

本项目使用 [Mozilla Public License 2.0](LICENSE)（SPDX：`MPL-2.0`）。
分发源码形式时，请保留 `LICENSE` 中的条款说明，并按下述方式标注文件级许可：

```text
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
```

## 链接

- 云湖官网：[云湖社交](https://www.yhchat.com/)
