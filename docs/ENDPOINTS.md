# 端点清单

> 本文件由 `tools/gen_endpoints.py` 从 yhchatAPI 文档站生成，请勿手工编辑。
> 覆盖状态来自 `docs/implemented.txt`（每行一个已实现路径）；未列出即视为尚未实现。

共 242 个端点，已实现 6 个。

## 按文档分组

| 文档 | 端点数 |
| --- | --- |
| `bot/v1/bot.md` | 6 |
| `v1/beta.md` | 1 |
| `v1/bot.md` | 26 |
| `v1/captcha.md` | 1 |
| `v1/chat-background.md` | 2 |
| `v1/check.md` | 3 |
| `v1/coin.md` | 4 |
| `v1/community.md` | 35 |
| `v1/conversation.md` | 4 |
| `v1/disk.md` | 6 |
| `v1/event.md` | 2 |
| `v1/expression.md` | 5 |
| `v1/file.md` | 3 |
| `v1/friend.md` | 8 |
| `v1/group-tag.md` | 7 |
| `v1/group.md` | 26 |
| `v1/instruction.md` | 3 |
| `v1/live.md` | 7 |
| `v1/menu.md` | 1 |
| `v1/misc.md` | 9 |
| `v1/mount-setting.md` | 2 |
| `v1/msg.md` | 12 |
| `v1/report.md` | 1 |
| `v1/search.md` | 2 |
| `v1/share.md` | 2 |
| `v1/sticker.md` | 12 |
| `v1/sticky.md` | 4 |
| `v1/user.md` | 28 |
| `v1/verification.md` | 2 |
| `v1/vip.md` | 2 |
| `web/v1/bot.md` | 2 |
| `web/v1/common.md` | 1 |
| `web/v1/community.md` | 3 |
| `web/v1/document.md` | 2 |
| `web/v1/group.md` | 1 |
| `web/v1/misc.md` | 1 |
| `web/v1/rss.md` | 2 |
| `web/v1/user.md` | 4 |

### `bot/v1/bot.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [x] | `POST` | `/open-apis/v1/bot/send` | 机器人发送信息 | bot token |
| [x] | `POST` | `/open-apis/v1/bot/batch_send` | 机器人批量发送信息 | bot token |
| [x] | `POST` | `/open-apis/v1/bot/send-stream` | 机器人流式发送信息 | bot token |
| [x] | `POST` | `/open-apis/v1/bot/edit` | 机器人编辑信息 | bot token |
| [x] | `POST` | `/open-apis/v1/bot/recall` | 机器人撤回信息 | bot token |
| [x] | `POST` | `/open-apis/v1/bot/messages` | 机器人获取信息列表 | bot token |

### `v1/beta.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/beta/info` | 获取内测状态 | user token |

### `v1/bot.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/bot/banner` | 机器人商店banner | user token |
| [ ] | `POST` | `/v1/bot/new-list` | 机器人商店列表 | user token |
| [ ] | `POST` | `/v1/bot/bot-detail` | 使用该机器人的群组 | user token |
| [ ] | `POST` | `/v1/bot/bot-group-list` | 获取创建的所有机器人信息 | user token |
| [ ] | `POST` | `/v1/bot/edit-setting-json` | 更改机器人设置 | user token |
| [ ] | `POST` | `/v1/bot/web-edit-bot` | 更改机器人信息 | user token |
| [ ] | `POST` | `/v1/bot/bot-info` | 获取机器人信息 | user token |
| [ ] | `POST` | `/v1/bot/board` | 获取机器人群聊看板 | user token |
| [ ] | `POST` | `/v1/bot/remove-follower` | 删除用户对机器人的添加 | user token |
| [ ] | `POST` | `/v1/bot/remove-group` | 删除群聊对机器人的添加 | user token |
| [ ] | `POST` | `/v1/bot/llm/llm-setting-list` | 获取可用AI模型列表 | user token |
| [ ] | `POST` | `/v1/bot/llm/llm-setting-ref-info` | 获取机器人大模型设置 | user token |
| [ ] | `POST` | `/v1/bot/reset-bot-token` | 重置机器人token | user token |
| [ ] | `POST` | `/v1/bot/create-bot` | 创建机器人 | user token |
| [ ] | `POST` | `/v1/bot/edit-subscribed-link` | 设置机器人消息订阅接口 | user token |
| [ ] | `POST` | `/v1/bot/get-user-settings-json` | 获取群聊内机器人设置 | user token |
| [ ] | `POST` | `/v1/bot/send-setting-json` | 群聊内机器人设置保存 | user token |
| [ ] | `POST` | `/v1/bot/llm/clean-content` | 智能体机器人清除上下文 | user token |
| [ ] | `POST` | `/v1/bot/llm/knowledge/list` | 获取智能体机器人知识库 | user token |
| [ ] | `POST` | `/v1/bot/llm/knowledge/create` | 智能体机器人上传知识文件 | user token |
| [ ] | `POST` | `/v1/bot/console/my-bots` | 获取我创建的机器人 | user token |
| [ ] | `POST` | `/v1/bot/group-permission-get` | 获取群机器人权限列表 | user token |
| [ ] | `POST` | `/v1/bot/llm/llm-setting-ref-params` | 获取智能体机器人参数参考 | user token |
| [ ] | `POST` | `/v1/bot/group-permission-edit` | 更改群机器人权限 | user token |
| [ ] | `POST` | `/v1/bot/follower-list` | 获取使用者列表 | user token |
| [ ] | `POST` | `/v1/bot/join-group-list` | 获取加入群聊列表 | user token |

### `v1/captcha.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/captcha/get` | 获取滑动验证码 | user token |

### `v1/chat-background.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/chat-background/edit` | 设置聊天背景 | user token |
| [ ] | `POST` | `/v1/chat-background/list` | 获取背景设置列表 | user token |

### `v1/check.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/check/check-version-mobile` | 获取云湖新版本（Android 版本） | user token |
| [ ] | `POST` | `/v1/check/get-latest-version` | 获取云湖新版本（Android 版本） | user token |
| [ ] | `POST` | `/v1/check/check-version` | 获取云湖新版本（Windows 版本） | user token |

### `v1/coin.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/coin/shop/product-recommend` | 商品获取 | user token |
| [ ] | `POST` | `/v1/coin/task/my-task-info` | 我的金币任务获取 | user token |
| [ ] | `POST` | `/v1/coin/shop/product-detail` | 获取商品详情 | user token |
| [ ] | `POST` | `/v1/coin/task/raffle` | 让金币机器人给你发领金币信息 | user token |

### `v1/community.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/community/posts/create` | 创建文章 | user token |
| [ ] | `POST` | `/v1/community/posts/delete` | 删除文章 | user token |
| [ ] | `POST` | `/v1/community/posts/post-reward` | 打赏文章 | user token |
| [ ] | `POST` | `/v1/community/comment/comment-reward` | 打赏文章评论 | user token |
| [ ] | `POST` | `/v1/community/posts/post-like` | 点赞/取消点赞文章 | user token |
| [ ] | `POST` | `/v1/community/posts/post-collect` | 收藏/取消收藏文章 | user token |
| [ ] | `POST` | `/v1/community/posts/edit` | 编辑文章 | user token |
| [ ] | `POST` | `/v1/community/posts/post-list` | 获取文章列表 | user token |
| [ ] | `POST` | `/v1/community/ba/info` | 分区信息获取 | user token |
| [ ] | `POST` | `/v1/community/ba/following-ba-list` | 获取分区列表 | user token |
| [ ] | `POST` | `/v1/community/reward-record` | 获取文章打赏记录 | user token |
| [ ] | `POST` | `/v1/community/comment/comment` | 评论文章 | user token |
| [ ] | `POST` | `/v1/community/comment/comment-list` | 获取文章评论列表 | user token |
| [ ] | `POST` | `/v1/community/search` | 查找文章 | user token |
| [ ] | `POST` | `/v1/community/set-black-list` | 屏蔽指定用户文章 | user token |
| [ ] | `POST` | `/v1/community/black-list` | 获取屏蔽指定用户文章列表 | user token |
| [ ] | `POST` | `/v1/community/posts/post-detail` | 查看文章详情 | user token |
| [ ] | `POST` | `/v1/community/posts/my-post-list` | 查看自己发布的文章 | user token |
| [ ] | `POST` | `/v1/community/ba/group-list` | 查看分区下绑定的群聊列表 | user token |
| [ ] | `POST` | `/v1/community/ba/forward` | 分享文章分区 | user token |
| [ ] | `POST` | `/v1/community/ba/manage` | 管理文章分区 | user token |
| [ ] | `POST` | `/v1/community/ba/create` | 创建文章分区 | user token |
| [ ] | `POST` | `/v1/community/ba/edit` | 编辑文章分区 | user token |
| [ ] | `POST` | `/v1/community/ba/delete` | 删除文章分区 | user token |
| [ ] | `POST` | `/v1/community/posts/create-draft` | 创建文章草稿 | user token |
| [ ] | `POST` | `/v1/community/posts/get-draft` | 获取文章草稿信息 | user token |
| [ ] | `POST` | `/v1/community/posts/cancel-draft` | 删除文章草稿 | user token |
| [ ] | `POST` | `/v1/community/ba/user-follow-ba` | 关注分区 | user token |
| [ ] | `POST` | `/v1/community/ba/user-unfollow-ba` | 取关分区 | user token |
| [ ] | `POST` | `/v1/community/posts/edit-sticky` | 置顶/取消置顶文章 | user token |
| [ ] | `POST` | `/v1/community/ba/follower-list` | 获取分区关注者列表 | user token |
| [ ] | `POST` | `/v1/community/ba/manage-setting` | 设置分区管理员 | user token |
| [ ] | `POST` | `/v1/community/ba/list-by-create` | 获取用户创建的分区 | user token |
| [ ] | `POST` | `/v1/community/posts/post-list-recommend` | 获取推荐文章 | user token |
| [ ] | `POST` | `/v1/community/report` | 举报文章/评论 | user token |

### `v1/conversation.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/conversation/dismiss-notification` | 将对话设为已读 | user token |
| [ ] | `POST` | `/v1/conversation/list` | 获取对话列表 | user token |
| [ ] | `POST` | `/v1/conversation/sort-change` | 更改对话排序 | user token |
| [ ] | `POST` | `/v1/conversation/remove` | 删除对话 | user token |

### `v1/disk.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/disk/create-folder` | 创建群网盘文件夹 | user token |
| [ ] | `POST` | `/v1/disk/file-list` | 获取群网盘文件列表 | user token |
| [ ] | `POST` | `/v1/disk/file-size` | 获取群网盘文件总大小 | user token |
| [ ] | `POST` | `/v1/disk/upload-file` | 上传文件 | user token |
| [ ] | `POST` | `/v1/disk/rename` | 更改文件名 | user token |
| [ ] | `POST` | `/v1/disk/remove` | 删除文件 | user token |

### `v1/event.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/event/list` | 获取机器人事件订阅配置 | user token |
| [ ] | `POST` | `/v1/event/edit` | 机器人消息订阅设置 | user token |

### `v1/expression.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/expression/list` | 获取个人表情收藏 | user token |
| [ ] | `POST` | `/v1/expression/create` | 添加图片到个人表情收藏 | user token |
| [ ] | `POST` | `/v1/expression/delete` | 删除个人表情收藏中的表情 | user token |
| [ ] | `POST` | `/v1/expression/topping` | 置顶个人表情收藏中的表情 | user token |
| [ ] | `POST` | `/v1/expression/add` | 添加已有表情包 | user token |

### `v1/file.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/file/send` | 发送超级文件分享申请 | user token |
| [ ] | `POST` | `/v1/file/reply` | 拒绝超级文件分享 | user token |
| [ ] | `POST` | `/v1/file/offer` | 建立超级文件分享 | user token |

### `v1/friend.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/friend/apply` | 添加用户/群聊/机器人 | user token |
| [ ] | `POST` | `/v1/friend/delete-friend` | 删除用户/群聊/机器人 | user token |
| [ ] | `POST` | `/v1/friend/agree-apply` | 处理用户/群聊/机器人添加申请 | user token |
| [ ] | `POST` | `/v1/friend/ignore-apply` | 忽略申请 | user token |
| [ ] | `POST` | `/v1/friend/address-book-list` | 获取通讯录 | user token |
| [ ] | `POST` | `/v1/friend/request-list` | 获取申请/邀请列表 | user token |
| [ ] | `POST` | `/v1/friend/no-notify` | 设置会话免打扰 | user token |
| [ ] | `POST` | `/v1/friend/delete-request` | 删除好友/邀请请求 | user token |

### `v1/group-tag.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/group-tag/list` | 获取群组标签列表 | user token |
| [ ] | `POST` | `/v1/group-tag/relate` | 关联用户标签 | user token |
| [ ] | `POST` | `/v1/group-tag/relate-cancel` | 取消关联用户标签 | user token |
| [ ] | `POST` | `/v1/group-tag/edit` | 编辑群组标签 | user token |
| [ ] | `POST` | `/v1/group-tag/create` | 新增群组标签 | user token |
| [ ] | `POST` | `/v1/group-tag/delete` | 删除群组标签 | user token |
| [ ] | `POST` | `/v1/group-tag/members` | 获取标签绑定的用户列表 | user token |

### `v1/group.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/group/info` | 获取群聊信息 | user token |
| [ ] | `POST` | `/v1/group/list-member` | 获取群成员列表 | user token |
| [ ] | `POST` | `/v1/group/live-room` | 获取群聊语音房间 | user token |
| [ ] | `POST` | `/v1/group/instruction-list` | 获取群指令列表 | user token |
| [ ] | `POST` | `/v1/group/invite` | 邀请加入群聊 | user token |
| [ ] | `POST` | `/v1/group/remove-member` | 踢出用户 | user token |
| [ ] | `POST` | `/v1/group/gag-member` | 禁言用户 | user token |
| [ ] | `GET` | `/v1/group/category` | 获取群聊推荐分类 | user token |
| [ ] | `POST` | `/v1/group/recommend/list` | 搜索推荐群聊 | user token |
| [ ] | `POST` | `/v1/group/msg-type-limit` | 设置消息类型限制 | user token |
| [ ] | `POST` | `/v1/group/edit-group` | 编辑群聊信息 | user token |
| [ ] | `POST` | `/v1/group/bot-list` | 获取群机器人列表 | user token |
| [ ] | `POST` | `/v1/group/remove-bot` | 移除群聊内机器人 | user token |
| [ ] | `POST` | `/v1/group/edit-my-group-nickname` | 设置我的群昵称 | user token |
| [ ] | `POST` | `/v1/group/edit-group-keyword` | 设置群口令 | user token |
| [ ] | `POST` | `/v1/group/info-add-friend` | 获取群口令关联群聊 | user token |
| [ ] | `POST` | `/v1/group/edit-auto-delete-message` | 设置群聊消息自动销毁时间 | user token |
| [ ] | `POST` | `/v1/group/edit-stop-member-upload-group-file` | 设置禁止群成员上传到群云盘 | user token |
| [ ] | `POST` | `/v1/group/create-group` | 创建群聊 | user token |
| [ ] | `POST` | `/v1/group/dismiss-group` | 解散群聊 | user token |
| [ ] | `POST` | `/v1/group/live-room` | 获取语音房间列表 | user token |
| [ ] | `POST` | `/v1/group/agree-invite` | 同意进群申请、同意机器人进群 | user token |
| [ ] | `POST` | `/v1/group/member-is-removed` | 用户被是否被该群踢过 | user token |
| [ ] | `POST` | `/v1/group/switch` | 加入群推荐 | user token |
| [ ] | `GET` | `/v1/group/event-sse` | 连接群聊 SSE | user token |
| [ ] | `POST` | `/v1/group/edit-shop-entry` | 编辑商城入口状态 | user token |

### `v1/instruction.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/instruction/web-list` | 获取机器人指令列表（网页控制台） | user token |
| [ ] | `POST` | `/v1/instruction/create` | 创建机器人指令 | user token |
| [ ] | `POST` | `/v1/instruction/list` | 获取机器人私聊指令 | user token |

### `v1/live.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/live/add` | 获取语音频道进入 token | user token |
| [ ] | `POST` | `/v1/live/close` | 关闭语音频道 | user token |
| [ ] | `POST` | `/v1/live/hang_up` | 挂断语音频道 | user token |
| [ ] | `POST` | `/v1/live/room-info` | 获取语音频道信息 | user token |
| [ ] | `POST` | `/v1/live/title-edit` | 编辑语音频道标题 | user token |
| [ ] | `POST` | `/v1/live/get-calling` | 获取正在发起的通话 | user token |
| [ ] | `POST` | `/v1/live/stream-info` | 获取推流信息 | user token |

### `v1/menu.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/menu/event` | 触发快捷菜单事件 | user token |

### `v1/misc.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `GET` | `/v1/misc/configure-distribution` | 获取功能路由 | user token |
| [ ] | `GET` | `/v1/misc/qiniu-token` | 获取图片上传 token | user token |
| [ ] | `GET` | `/v1/misc/qiniu-token-audio` | 获取音频上传 token | user token |
| [ ] | `GET` | `/v1/misc/qiniu-token2` | 获取文件上传 token | user token |
| [ ] | `GET` | `/v1/misc/qiniu-token-video` | 获取视频上传token | user token |
| [ ] | `GET` | `/v1/misc/qiniu-token-group-disk` | 获取群文件上传 token | user token |
| [ ] | `GET` | `/v1/misc/setting` | 获取云端设置 | user token |
| [ ] | `GET` | `/v1/misc/gray-status` | 获取灰色状态 | user token |
| [ ] | `GET` | `/v1/misc/auto-update` | 获取自动更新最新版本 | user token |

### `v1/mount-setting.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/mount-setting/create` | 添加群WebDAV挂载 | user token |
| [ ] | `POST` | `/v1/mount-setting/delete` | 删除群WebDAV挂载 | user token |

### `v1/msg.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/msg/send-message` | 发送信息 | user token |
| [ ] | `POST` | `/v1/msg/edit-message` | 编辑消息 | user token |
| [ ] | `POST` | `/v1/msg/list-message-by-seq` | 按消息序列列出消息（不包含指定消息） | user token |
| [ ] | `POST` | `/v1/msg/list-message` | 列出消息 | user token |
| [ ] | `POST` | `/v1/msg/list-message-by-mid-seq` | 按消息ID列出消息（包含消息id指定的消息） | user token |
| [ ] | `POST` | `/v1/msg/list-message-edit-record` | 获取信息历史编辑内容 | user token |
| [ ] | `POST` | `/v1/msg/button-report` | 发送按钮点击事件 | user token |
| [ ] | `POST` | `/v1/msg/recall-msg` | 撤回信息 | user token |
| [ ] | `POST` | `/v1/msg/recall-msg-batch` | 批量撤回消息 | user token |
| [ ] | `POST` | `/v1/msg/file-download-record` | 文件消息下载记录 | user token |
| [ ] | `POST` | `/v1/msg/delete` | 删除消息 | user token |
| [ ] | `POST` | `/v1/msg/a2ui-form-report` | 触发A2UI表单提交信息 | user token |

### `v1/report.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/report/create` | 提交举报 | user token |

### `v1/search.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/search/home-search` | 群聊首页搜索 | user token |
| [ ] | `POST` | `/v1/search/chat-search` | 聊天记录搜索 | user token |

### `v1/share.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/share/info` | 分享链接获取群聊信息 | user token |
| [ ] | `POST` | `/v1/share/create` | 创建分享链接 | user token |

### `v1/sticker.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/sticker/list` | 获取收藏表情包 | user token |
| [ ] | `POST` | `/v1/sticker/detail` | 查看表情包详情 | user token |
| [ ] | `POST` | `/v1/sticker/add` | 添加表情包 | user token |
| [ ] | `POST` | `/v1/sticker/remove-sticker-pack` | 移除收藏表情包 | user token |
| [ ] | `POST` | `/v1/sticker/sort` | 更改收藏表情包的排序 | user token |
| [ ] | `POST` | `/v1/sticker/create-pack` | 创建表情包 | user token |
| [ ] | `POST` | `/v1/sticker/rename-pack` | 重命名表情包 | user token |
| [ ] | `POST` | `/v1/sticker/add-sticker` | 添加表情至表情包 | user token |
| [ ] | `POST` | `/v1/sticker/delete-pack` | 删除表情包 | user token |
| [ ] | `POST` | `/v1/sticker/import-pack` | 导入表情包 | user token |
| [ ] | `POST` | `/v1/sticker/rename-sticker` | 重命名表情包里的表情 | user token |
| [ ] | `POST` | `/v1/sticker/remove-sticker` | 删除表情 | user token |

### `v1/sticky.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/sticky/list` | 首页置顶信息获取 | user token |
| [ ] | `POST` | `/v1/sticky/add` | 置顶会话 | user token |
| [ ] | `POST` | `/v1/sticky/delete` | 取消置顶会话 | user token |
| [ ] | `POST` | `/v1/sticky/topping` | 把其中一个已置顶会话移到最前 | user token |

### `v1/user.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/user/captcha` | 获取人机验证图片 | user token |
| [ ] | `POST` | `/v1/user/verification-login` | 短信验证码登录 | user token |
| [ ] | `GET` | `/v1/user/info` | 获取用户自身信息 | user token |
| [ ] | `POST` | `/v1/user/get-user` | 获取用户信息 | user token |
| [ ] | `POST` | `/v1/user/medal` | 获取自身勋章 | user token |
| [ ] | `POST` | `/v1/user/edit-nickname` | 更改自身名称 | user token |
| [ ] | `POST` | `/v1/user/edit-avatar` | 更改自身头像 | user token |
| [ ] | `POST` | `/v1/user/email-login` | 用户邮箱密码登录 | user token |
| [ ] | `POST` | `/v1/user/logout` | 退出登录 | user token |
| [ ] | `POST` | `/v1/user/recommend-category-list` | 获取发现群聊分区 | user token |
| [ ] | `POST` | `/v1/user/recommend-list` | 获取发现群聊列表 | user token |
| [ ] | `POST` | `/v1/user/recommend` | 获取机器人推荐列表 | user token |
| [ ] | `POST` | `/v1/user/module-ignore-info` | 模块忽略信息获取 | user token |
| [ ] | `POST` | `/v1/user/module-ignore` | 设置自定义模块 | user token |
| [ ] | `POST` | `/v1/user/notification-status` | 获取通知状态 | user token |
| [ ] | `POST` | `/v1/user/notification-info` | 获取通知注册信息 | user token |
| [ ] | `POST` | `/v1/user/gold-coin-increase-decrease-record` | 金币增减记录 | user token |
| [ ] | `POST` | `/v1/user/bing-phone` | 绑定手机号 | user token |
| [ ] | `POST` | `/v1/user/bing-email` | 绑定邮箱 | user token |
| [ ] | `POST` | `/v1/user/change-phone-check` | 更改绑定手机号 | user token |
| [ ] | `POST` | `/v1/user/change-email-check` | 更改绑定邮箱 | user token |
| [ ] | `POST` | `/v1/user/forget-password` | 更改登录密码 | user token |
| [ ] | `POST` | `/v1/user/save-user-data` | 修改自身个人资料 | user token |
| [ ] | `POST` | `/v1/user/get-user-data` | 获取自身个人资料 | user token |
| [ ] | `POST` | `/v1/user/get-user-show-adv` | 获取用户显示广告 | user token |
| [ ] | `POST` | `/v1/user/save-user-remarks` | 设置好友备注 | user token |
| [ ] | `POST` | `/v1/user/cancel-user` | 注销账号 | user token |
| [ ] | `POST` | `/v1/user/device-offline` | 下线设备 | user token |

### `v1/verification.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/verification/get-verification-code` | 获取短信验证码 | user token |
| [ ] | `POST` | `/v1/verification/get-email-verification-code` | 获取邮箱验证码 | user token |

### `v1/vip.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/vip/vip-product-list` | vip价格获取 | user token |
| [ ] | `GET` | `/v1/vip/vip-benefits-list` | vip特权获取 | user token |

### `web/v1/bot.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/bot/bot-info` | 获取机器人信息 | user token |
| [ ] | `POST` | `/v1/bot/bot-link-reset` | 恢复机器人订阅 | user token |

### `web/v1/common.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `GET` | `/v1/common/get-version` | 获取全平台最新版本 | user token |

### `web/v1/community.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/community/c/following-ba-list` | 获取分区列表 | user token |
| [ ] | `POST` | `/v1/community/posts/post-list` | 获取文章列表 | user token |
| [ ] | `POST` | `/v1/community/c/info` | 获取分区信息 | user token |

### `web/v1/document.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `GET` | `/v1/document/menus` | 获取开放文档菜单选项 | user token |
| [ ] | `GET` | `/v1/document/detail` | 获取开放文档(Markdown版本) | user token |

### `web/v1/group.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/group/group-info` | 获取群聊信息 | user token |

### `web/v1/misc.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `POST` | `/v1/misc/updates` | 获取更新日志 | user token |

### `web/v1/rss.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `GET` | `/v1/rss/recommend-list` | 获取 RSS 推荐大全 | user token |
| [ ] | `POST` | `/v1/rss/recommend-apply` | 提交 RSS | user token |

### `web/v1/user.md`

| 状态 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| [ ] | `GET` | `/v1/user/info` | 获取用户自身信息 | user token |
| [ ] | `GET` | `/v1/user/homepage` | 获取用户主页信息 | user token |
| [ ] | `GET` | `/v1/user/get-token` | 复制用户token | user token |
| [ ] | `GET` | `/v1/user/gold-coin-increase-decrease-record` | 金币增减记录 | user token |

## 已实现但文档未收录

| 路径 | 说明 |
| --- | --- |
| `/open-apis/v1/file/upload` | 见 `src/yhchat/api/bot.py`，字段来自旧版实现，待验证 |
| `/open-apis/v1/image/upload` | 见 `src/yhchat/api/bot.py`，字段来自旧版实现，待验证 |
| `/open-apis/v1/video/upload` | 见 `src/yhchat/api/bot.py`，字段来自旧版实现，待验证 |
