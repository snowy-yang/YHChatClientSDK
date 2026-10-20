"""从 yhchatAPI 文档生成 ``v1/*`` 的 JSON 端点方法。

- 只生成 JSON 收发的端点；protobuf / XML / text 端点记进 ``docs/v1_pending.md``，等接 proto 层；
- ``/open-apis/*`` 已手写，跳过；
- 输出：``src/yhchat/api/v1/<group>.py``、``src/yhchat/api/v1/__init__.py``（``V1API`` 聚合），
  并把生成的路径合并进 ``docs/implemented.txt``。

用法::

    uv run python tools/gen_v1_api.py
"""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCS = Path.home() / "Default/yhchatAPI/src/api"

HEADING = re.compile(r"^## (.+)$")
ROUTE = re.compile(r"^(GET|POST|PUT|DELETE|PATCH)\s+(\S+)$")
FIELD = re.compile(r'^\s{2,}"?([A-Za-z_][A-Za-z0-9_]*)"?\s*:')
NON_IDENTIFIER = re.compile(r"[^0-9A-Za-z_]")


@dataclass(slots=True)
class Endpoint:
    """一个文档端点。"""

    source: str
    group: str
    title: str
    method: str
    path: str
    query: str
    request_lang: str
    request_fields: list[str]
    response_lang: str

    @property
    def kind(self) -> str:
        """收发格式，例如 ``json/json``。"""
        return f"{self.request_lang or 'none'}/{self.response_lang or 'none'}"


@dataclass(slots=True)
class Skipped:
    """被跳过的端点。"""

    source: str
    title: str
    method: str
    path: str
    reason: str


def parse_docs(root: Path) -> tuple[list[Endpoint], list[Skipped]]:
    """解析全部文档，按 (method, path) 去重（``v1/`` 优先于 ``web/v1/``）。"""
    files = sorted(
        root.rglob("*.md"), key=lambda item: (not item.relative_to(root).as_posix().startswith("v1/"), str(item))
    )
    endpoints: list[Endpoint] = []
    skipped: list[Skipped] = []
    seen: set[tuple[str, str]] = set()
    for file in files:
        relative = file.relative_to(root).as_posix()
        if file.name in {"README.md", "full_proto.md", "url_scheme.md"}:
            continue
        for endpoint in _parse_file(file, relative):
            key = (endpoint.method, endpoint.path)
            reason = _skip_reason(endpoint)
            if not reason and key in seen:
                reason = "与 v1 文档重复"
            if reason:
                skipped.append(Skipped(endpoint.source, endpoint.title, endpoint.method, endpoint.path, reason))
                continue
            seen.add(key)
            endpoints.append(endpoint)
    return endpoints, skipped


def _parse_file(file: Path, relative: str) -> list[Endpoint]:
    group = _group_name(relative)
    lines = file.read_text(encoding="utf-8").splitlines()
    parsed: list[Endpoint] = []
    index = 0
    while index < len(lines):
        heading = HEADING.match(lines[index])
        if not heading:
            index += 1
            continue
        title = heading.group(1).strip()
        end = index + 1
        while end < len(lines) and not HEADING.match(lines[end]):
            end += 1
        block = lines[index + 1 : end]
        for offset, line in enumerate(block):
            route = ROUTE.match(line.strip())
            if not route:
                continue
            method, raw_path = route.group(1), route.group(2)
            path, _, query = raw_path.partition("?")
            if not path.startswith("/") and path.startswith(("v1/", "web/", "open-apis/")):
                path = "/" + path  # 文档里少数条目漏了前导斜杠
            request_lang, request_block = _fence(block, offset, "请求体")
            response_lang, _ = _fence(block, offset, "响应体")
            parsed.append(
                Endpoint(
                    source=relative,
                    group=group,
                    title=title,
                    method=method,
                    path=path,
                    query=query,
                    request_lang=request_lang,
                    request_fields=_fields(request_block),
                    response_lang=response_lang,
                )
            )
        index = end
    return parsed


def _fence(block: list[str], start: int, marker: str) -> tuple[str, list[str]]:
    for index in range(start, len(block)):
        if marker not in block[index]:
            continue
        for fence in range(index + 1, min(index + 6, len(block))):
            stripped = block[fence].strip()
            if not stripped.startswith("```"):
                continue
            language = stripped[3:].strip().lower()
            content: list[str] = []
            for line in block[fence + 1 :]:
                if line.strip().startswith("```"):
                    break
                content.append(line)
            return language, content
        return "", []
    return "", []


def _fields(block: list[str]) -> list[str]:
    fields: list[str] = []
    for line in block:
        match = FIELD.match(line)
        if match and match.group(1) not in fields:
            fields.append(match.group(1))
    return fields


def _skip_reason(endpoint: Endpoint) -> str:
    if not endpoint.path.startswith("/"):
        return "外部地址，不是云湖路径"
    if not endpoint.path.startswith(("/v1/", "/web/", "/open-apis/")):
        return "非 v1/web/open-apis 路径"
    if endpoint.path.startswith("/open-apis"):
        return "open-apis 已手写"
    kind = endpoint.kind
    if "proto" in kind:
        return "protobuf 收发，待接 proto 层"
    if "xml" in kind:
        return "XML 响应，未建模"
    if "html" in kind:
        return "HTML 响应，未建模"
    if endpoint.request_lang == "text":
        return "text 请求体，未建模"
    return ""


def _group_name(relative: str) -> str:
    parts = relative.split("/")
    stem = Path(parts[-1]).stem
    return f"web_{stem}" if parts[0] == "web" else stem


def _module_name(group: str) -> str:
    return group.replace("-", "_")


def _class_name(group: str) -> str:
    return "".join(part.capitalize() for part in group.replace("-", "_").split("_")) + "API"


def _method_name(endpoint: Endpoint) -> str:
    parts = endpoint.path.strip("/").split("/")
    if parts and parts[0] == "web" and len(parts) > 1 and parts[1] == "v1":
        parts = parts[2:]
    elif parts and parts[0] == "v1":
        parts = parts[1:]
    stem = endpoint.group.removeprefix("web_")
    if parts and parts[0] == stem:
        parts = parts[1:]
    name = NON_IDENTIFIER.sub("_", "_".join(parts)).strip("_") or "index"
    if name[0].isdigit():
        name = f"v_{name}"
    return name


def render_group(group: str, endpoints: list[Endpoint]) -> str:
    """渲染一个分组模块。"""
    sources = ", ".join(sorted({endpoint.source for endpoint in endpoints}))
    class_name = _class_name(group)
    needs_mapping = any(endpoint.request_lang or endpoint.request_fields or endpoint.query for endpoint in endpoints)
    lines = [
        f'"""``{group}`` 组：由 ``tools/gen_v1_api.py`` 根据 ``{sources}`` 生成，勿手改。"""',
        "",
    ]
    if needs_mapping:
        lines.append("from collections.abc import Mapping")
    lines.extend(
        [
            "from typing import Any",
            "",
            "from ._base import V1GroupAPI",
            "",
            "",
            f"class {class_name}(V1GroupAPI):",
            f'    """``{group}`` 组，共 {len(endpoints)} 个 JSON 端点。"""',
            "",
        ]
    )
    used: set[str] = set()
    for endpoint in endpoints:
        name = _method_name(endpoint)
        while name in used:
            name = f"{name}_"
        used.add(name)
        if endpoint.method == "GET" and endpoint.query:
            signature = f"    async def {name}(self, *, params: Mapping[str, Any] | None = None) -> dict[str, Any]:"
            call = f'await self._call("GET", "{endpoint.path}", params=params)'
            extra = f"查询参数: ``{endpoint.query}``。"
        elif endpoint.request_lang or endpoint.request_fields:
            signature = f"    async def {name}(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:"
            call = f'await self._call("{endpoint.method}", "{endpoint.path}", body=body)'
            extra = f"请求字段: {', '.join(endpoint.request_fields)}。" if endpoint.request_fields else "请求体见文档。"
        else:
            signature = f"    async def {name}(self) -> dict[str, Any]:"
            call = f'await self._call("{endpoint.method}", "{endpoint.path}")'
            extra = ""
        doc = [f'        """{endpoint.title}。', "", f"        ``{endpoint.method} {endpoint.path}``"]
        if extra:
            doc.append(f"        {extra}")
        doc.append("        返回原始 JSON 响应（未逐字段建模），见文档。")
        doc.append('        """')
        lines.extend([signature, *doc, f"        return {call}", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_init(groups: dict[str, list[Endpoint]]) -> str:
    """渲染 ``V1API`` 聚合模块。"""
    names = sorted(groups)
    modules = [_module_name(name) for name in names]
    lines = [
        '"""``v1`` 用户接口集合（token 放请求头）。由 ``tools/gen_v1_api.py`` 生成，勿手改。"""',
        "",
        "from ...transport import HttpTransport",
        "from ._proto import V1ProtoAPI",
    ]
    lines.extend(f"from .{module} import {_class_name(name)}" for name, module in zip(names, modules, strict=True))
    lines.extend(
        [
            "",
            "__all__ = [",
            '    "V1API",',
            *(f'    "{_class_name(name)}",' for name in names),
            "]",
            "",
            "",
            "class V1API:",
            '    """``v1/*`` 用户接口：按文档分组挂属性，token 由传输层放进请求头。"""',
            "",
            "    def __init__(self, http: HttpTransport) -> None:",
            "        self.proto = V1ProtoAPI(http)",
        ]
    )
    lines.extend(
        f"        self.{module} = {_class_name(name)}(http)" for name, module in zip(names, modules, strict=True)
    )
    return "\n".join(lines).rstrip() + "\n"


_BASE_MODULE = '''"""``v1/*`` 分组的公共基类：由 ``tools/gen_v1_api.py`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ...transport import HttpTransport


class V1GroupAPI:
    """一组 ``v1/*`` 端点：请求带着 header 里的用户 token。"""

    def __init__(self, http: HttpTransport) -> None:
        self._http = http

    async def _call(
        self,
        method: str,
        path: str,
        *,
        body: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发请求并原样返回响应体（含 ``code`` / ``msg`` / ``data``）。"""
        return await self._http.request(method, path, json=body, params=params)
'''


def render_base() -> str:
    """渲染分组基类模块。"""
    return _BASE_MODULE


def render_pending(skipped: list[Skipped], implemented: set[str]) -> str:
    """渲染待实现清单。"""
    lines = [
        "# 待实现的 v1 端点",
        "",
        "由 `tools/gen_v1_api.py` 生成：这些端点不是 JSON 收发，等 proto 层或单独处理。",
        "",
    ]
    lines.extend(["| 端点 | 方法 | 文档 | 原因 |", "| --- | --- | --- | --- |"])
    relevant = [
        item
        for item in skipped
        if item.reason not in {"open-apis 已手写", "与 v1 文档重复"} and item.path not in implemented
    ]
    lines.extend(
        f"| `{item.path}` | {item.method} | {item.source} | {item.reason} |"
        for item in sorted(relevant, key=lambda i: i.path)
    )
    return "\n".join(lines).rstrip() + "\n"


def proto_paths() -> set[str]:
    """取手写 protobuf 端点路径：解析 ``api/v1/_proto.py`` 的 ``PROTO_ENDPOINTS``。

    不 import 该模块，避免生成器依赖 protobuf 运行时。
    """
    source = ROOT / "src/yhchat/api/v1/_proto.py"
    if not source.exists():
        return set()
    match = re.search(
        r"PROTO_ENDPOINTS[^=]*=\s*frozenset\(\s*\{(?P<body>.*?)\}", source.read_text(encoding="utf-8"), re.S
    )
    return set(re.findall(r'"(/v1/[^"]+)"', match.group("body"))) if match else set()


def update_implemented(paths: list[str]) -> int:
    """把已生成的路径合并进 ``docs/implemented.txt``，返回新增数量。"""
    target = ROOT / "docs/implemented.txt"
    existing: set[str] = set()
    if target.exists():
        existing = {line.strip() for line in target.read_text(encoding="utf-8").splitlines() if line.strip()}
    # 手写实现（open-apis）保留，v1 部分每次按生成结果重写，避免留下过期路径
    handwritten = {path for path in existing if path.startswith("/open-apis/")}
    merged = handwritten | set(paths)
    missing = merged - existing
    if merged != existing:
        target.write_text("\n".join(sorted(merged)) + "\n", encoding="utf-8")
    return len(missing)


def main() -> int:
    """生成全部 v1 分组模块。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS, help="yhchatAPI 的 src/api 目录")
    parser.add_argument("--out", type=Path, default=ROOT / "src/yhchat/api/v1", help="输出目录")
    args = parser.parse_args()

    if not args.docs.is_dir():
        print(f"文档目录不存在: {args.docs}")
        return 1
    endpoints, skipped = parse_docs(args.docs)
    groups: dict[str, list[Endpoint]] = {}
    for endpoint in endpoints:
        groups.setdefault(endpoint.group, []).append(endpoint)

    args.out.mkdir(parents=True, exist_ok=True)
    for group, items in groups.items():
        (args.out / f"{_module_name(group)}.py").write_text(render_group(group, items), encoding="utf-8")
    (args.out / "__init__.py").write_text(render_init(groups), encoding="utf-8")
    (args.out / "_base.py").write_text(render_base(), encoding="utf-8")
    implemented = {endpoint.path for endpoint in endpoints} | proto_paths()
    pending = ROOT / "docs/v1_pending.md"
    pending.write_text(render_pending(skipped, implemented), encoding="utf-8")
    added = update_implemented(sorted(implemented))

    print(
        f"生成 {len(endpoints)} 个 JSON 端点，分 {len(groups)} 组；跳过 {len(skipped)} 个；implemented.txt 新增 {added} 条"
    )
    for group in sorted(groups):
        print(f"  {group:16s} {len(groups[group]):3d}  -> {_module_name(group)}.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
