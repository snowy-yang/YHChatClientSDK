"""云湖接口模型基类。"""

from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    """云湖接口模型基类。

    约定：
    - ``populate_by_name``：既接受云湖返回的别名（camelCase），也接受 Python 字段名；
    - ``extra="allow"``：云湖新增字段不能让模型解析失败。
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")
