# 待实现的 v1 端点

由 `tools/gen_v1_api.py` 生成：这些端点不是 JSON 收发，等 proto 层或单独处理。

| 端点 | 方法 | 文档 | 原因 |
| --- | --- | --- | --- |
| `/v1/bot/board` | POST | v1/bot.md | protobuf 收发，待接 proto 层 |
| `/v1/bot/create-bot` | POST | v1/bot.md | protobuf 收发，待接 proto 层 |
| `/v1/bot/follower-list` | POST | v1/bot.md | protobuf 收发，待接 proto 层 |
| `/v1/bot/join-group-list` | POST | v1/bot.md | protobuf 收发，待接 proto 层 |
| `/v1/conversation/list` | POST | v1/conversation.md | protobuf 收发，待接 proto 层 |
| `/v1/friend/address-book-list` | POST | v1/friend.md | protobuf 收发，待接 proto 层 |
| `/v1/friend/request-list` | POST | v1/friend.md | protobuf 收发，待接 proto 层 |
| `/v1/misc/auto-update` | GET | v1/misc.md | XML 响应，未建模 |
| ``https://api.qiniu.com/v4/query` | GET | v1/misc.md | 外部地址，不是云湖路径 |
