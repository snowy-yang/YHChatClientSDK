"""SDK 异常类型。"""


class YHChatError(Exception):
    """SDK 所有异常的基类。"""


class TransportError(YHChatError):
    """网络层失败：连接错误、超时、返回体不是预期 JSON 等。"""


class APIError(YHChatError):
    """云湖接口返回了非成功状态（``code != 1`` 或 HTTP 4xx/5xx）。

    :param code: 云湖返回的状态码，缺失时退化为 HTTP 状态码。
    :param message: 云湖返回的 ``msg``。
    :param endpoint: 出错的接口路径，便于定位。
    """

    def __init__(self, code: int, message: str, *, endpoint: str) -> None:
        super().__init__(f"{endpoint} 调用失败: [{code}] {message}")
        self.code = code
        self.message = message
        self.endpoint = endpoint
