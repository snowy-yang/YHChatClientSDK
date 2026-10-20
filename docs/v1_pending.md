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
| `/v1/group-tag/members` | POST | v1/group-tag.md | protobuf 收发，待接 proto 层 |
| `/v1/group/bot-list` | POST | v1/group.md | protobuf 收发，待接 proto 层 |
| `/v1/group/create-group` | POST | v1/group.md | protobuf 收发，待接 proto 层 |
| `/v1/group/dismiss-group` | POST | v1/group.md | protobuf 收发，待接 proto 层 |
| `/v1/group/edit-group` | POST | v1/group.md | protobuf 收发，待接 proto 层 |
| `/v1/group/info` | POST | v1/group.md | protobuf 收发，待接 proto 层 |
| `/v1/group/info-add-friend` | POST | v1/group.md | protobuf 收发，待接 proto 层 |
| `/v1/group/list-member` | POST | v1/group.md | protobuf 收发，待接 proto 层 |
| `/v1/instruction/list` | POST | v1/instruction.md | protobuf 收发，待接 proto 层 |
| `/v1/misc/auto-update` | GET | v1/misc.md | XML 响应，未建模 |
| `/v1/user/edit-avatar` | POST | v1/user.md | protobuf 收发，待接 proto 层 |
| `/v1/user/edit-nickname` | POST | v1/user.md | protobuf 收发，待接 proto 层 |
| `/v1/user/get-user` | POST | v1/user.md | protobuf 收发，待接 proto 层 |
| `/v1/user/medal` | POST | v1/user.md | protobuf 收发，待接 proto 层 |
| ``https://api.qiniu.com/v4/query` | GET | v1/misc.md | 外部地址，不是云湖路径 |
