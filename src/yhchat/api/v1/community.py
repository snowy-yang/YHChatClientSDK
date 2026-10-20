"""``community`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/community.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class CommunityAPI(V1GroupAPI):
    """``community`` 组，共 35 个 JSON 端点。"""

    async def posts_create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """创建文章。

        ``POST /v1/community/posts/create``
        请求字段: baId, groupId, title, content, contentType, draftId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/create", body=body)

    async def posts_delete(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除文章。

        ``POST /v1/community/posts/delete``
        请求字段: postId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/delete", body=body)

    async def posts_post_reward(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """打赏文章。

        ``POST /v1/community/posts/post-reward``
        请求字段: postId, recvId, amount。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/post-reward", body=body)

    async def comment_comment_reward(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """打赏文章评论。

        ``POST /v1/community/comment/comment-reward``
        请求字段: postId, commentId, amount。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/comment/comment-reward", body=body)

    async def posts_post_like(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """点赞/取消点赞文章。

        ``POST /v1/community/posts/post-like``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/post-like", body=body)

    async def posts_post_collect(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """收藏/取消收藏文章。

        ``POST /v1/community/posts/post-collect``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/post-collect", body=body)

    async def posts_edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """编辑文章。

        ``POST /v1/community/posts/edit``
        请求字段: postId, title, content, contentType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/edit", body=body)

    async def posts_post_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取文章列表。

        ``POST /v1/community/posts/post-list``
        请求字段: typ, baId, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/post-list", body=body)

    async def ba_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """分区信息获取。

        ``POST /v1/community/ba/info``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/info", body=body)

    async def ba_following_ba_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取分区列表。

        ``POST /v1/community/ba/following-ba-list``
        请求字段: typ, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/following-ba-list", body=body)

    async def reward_record(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取文章打赏记录。

        ``POST /v1/community/reward-record``
        请求字段: typ, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/reward-record", body=body)

    async def comment_comment(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """评论文章。

        ``POST /v1/community/comment/comment``
        请求字段: postId, commentId, content。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/comment/comment", body=body)

    async def comment_comment_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取文章评论列表。

        ``POST /v1/community/comment/comment-list``
        请求字段: postId, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/comment/comment-list", body=body)

    async def search(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """查找文章。

        ``POST /v1/community/search``
        请求字段: typ, keyword, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/search", body=body)

    async def set_black_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """屏蔽指定用户文章。

        ``POST /v1/community/set-black-list``
        请求字段: isAdd, authorId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/set-black-list", body=body)

    async def black_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取屏蔽指定用户文章列表。

        ``POST /v1/community/black-list``
        请求字段: size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/black-list", body=body)

    async def posts_post_detail(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """查看文章详情。

        ``POST /v1/community/posts/post-detail``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/post-detail", body=body)

    async def posts_my_post_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """查看自己发布的文章。

        ``POST /v1/community/posts/my-post-list``
        请求字段: size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/my-post-list", body=body)

    async def ba_group_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """查看分区下绑定的群聊列表。

        ``POST /v1/community/ba/group-list``
        请求字段: baId, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/group-list", body=body)

    async def ba_forward(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """分享文章分区。

        ``POST /v1/community/ba/forward``
        请求字段: baId, receive, chatId, chatType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/forward", body=body)

    async def ba_manage(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """管理文章分区。

        ``POST /v1/community/ba/manage``
        请求字段: baId, visibleRange, publishAuthority。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/manage", body=body)

    async def ba_create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """创建文章分区。

        ``POST /v1/community/ba/create``
        请求字段: name, avatar。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/create", body=body)

    async def ba_edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """编辑文章分区。

        ``POST /v1/community/ba/edit``
        请求字段: baId, name, avatar。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/edit", body=body)

    async def ba_delete(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除文章分区。

        ``POST /v1/community/ba/delete``
        请求字段: baId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/delete", body=body)

    async def posts_create_draft(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """创建文章草稿。

        ``POST /v1/community/posts/create-draft``
        请求字段: baId, title, content, contentType, draftId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/create-draft", body=body)

    async def posts_get_draft(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取文章草稿信息。

        ``POST /v1/community/posts/get-draft``
        请求字段: baId, draftId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/get-draft", body=body)

    async def posts_cancel_draft(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除文章草稿。

        ``POST /v1/community/posts/cancel-draft``
        请求字段: draftId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/cancel-draft", body=body)

    async def ba_user_follow_ba(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """关注分区。

        ``POST /v1/community/ba/user-follow-ba``
        请求字段: baId, followSource。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/user-follow-ba", body=body)

    async def ba_user_unfollow_ba(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """取关分区。

        ``POST /v1/community/ba/user-unfollow-ba``
        请求字段: baId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/user-unfollow-ba", body=body)

    async def posts_edit_sticky(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """置顶/取消置顶文章。

        ``POST /v1/community/posts/edit-sticky``
        请求字段: postId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/edit-sticky", body=body)

    async def ba_follower_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取分区关注者列表。

        ``POST /v1/community/ba/follower-list``
        请求字段: id, size, page, memberName。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/follower-list", body=body)

    async def ba_manage_setting(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置分区管理员。

        ``POST /v1/community/ba/manage-setting``
        请求字段: baId, userId, userLevel。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/manage-setting", body=body)

    async def ba_list_by_create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取用户创建的分区。

        ``POST /v1/community/ba/list-by-create``
        请求字段: userId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/ba/list-by-create", body=body)

    async def posts_post_list_recommend(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取推荐文章。

        ``POST /v1/community/posts/post-list-recommend``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/posts/post-list-recommend", body=body)

    async def report(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """举报文章/评论。

        ``POST /v1/community/report``
        请求字段: typ, id, content, url, reason。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/report", body=body)
