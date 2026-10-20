"""进程内事件总线：把云湖事件扇出给所有 Satori 连接。"""

import asyncio
import contextlib
from collections.abc import AsyncGenerator

from .models import Event

_MAX_QUEUE = 1024


class EventBus:
    """极简发布/订阅；队列满时丢最旧一条（聊天事件尽力而为，不阻塞上游）。"""

    def __init__(self, *, queue_size: int = _MAX_QUEUE) -> None:
        self._queue_size = queue_size
        self._subscribers: set[asyncio.Queue[Event]] = set()
        self._sn = 0

    @property
    def subscriber_count(self) -> int:
        """当前订阅者数量。"""
        return len(self._subscribers)

    def next_sn(self) -> int:
        """分配下一个事件序号。"""
        self._sn += 1
        return self._sn

    async def publish(self, event: Event) -> None:
        """发布事件并补齐 ``sn``。"""
        if event.sn == 0:
            event.sn = self.next_sn()
        for queue in tuple(self._subscribers):
            if queue.full():
                with contextlib.suppress(asyncio.QueueEmpty):
                    queue.get_nowait()
            queue.put_nowait(event)

    @contextlib.asynccontextmanager
    async def subscribe(self) -> AsyncGenerator[asyncio.Queue[Event]]:
        """订阅事件；退出上下文时自动退订。"""
        queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=self._queue_size)
        self._subscribers.add(queue)
        try:
            yield queue
        finally:
            self._subscribers.discard(queue)
