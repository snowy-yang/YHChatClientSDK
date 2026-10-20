"""消息记录缓存。

云湖的编辑/撤回接口需要 ``recvId`` + ``recvType``，而调用方通常只有 ``msgId``。
发送和接收到的消息都会登记在这里，便于后续补全会话信息。
"""

from collections import OrderedDict

from .models import MessageInfo


class MessageRegistry:
    """``msgId → MessageInfo`` 的 LRU 缓存（进程内，不落盘）。"""

    def __init__(self, max_entries: int = 4096) -> None:
        self._max_entries = max_entries
        self._items: OrderedDict[str, MessageInfo] = OrderedDict()

    def add(self, info: MessageInfo) -> None:
        """登记一条消息；超出容量时淘汰最旧的记录。"""
        self._items[info.msg_id] = info
        self._items.move_to_end(info.msg_id)
        while len(self._items) > self._max_entries:
            self._items.popitem(last=False)

    def get(self, msg_id: str) -> MessageInfo | None:
        """查找消息记录，命中时刷新其 LRU 位置。"""
        info = self._items.get(msg_id)
        if info is not None:
            self._items.move_to_end(msg_id)
        return info

    def pop(self, msg_id: str) -> MessageInfo | None:
        """取出并删除一条记录。"""
        return self._items.pop(msg_id, None)

    def clear(self) -> None:
        """清空缓存。"""
        self._items.clear()

    def __len__(self) -> int:
        return len(self._items)
