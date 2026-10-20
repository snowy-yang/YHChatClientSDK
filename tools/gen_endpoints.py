"""从 yhchatAPI 文档站生成端点清单。

文档站（https://github.com/snowy-yang/yhchatAPI）用 ``## 标题`` + ```` ```http ```` 代码块
声明端点，这里把它们抽成机器可读的清单，作为 SDK 覆盖度的唯一起点::

    uv run python tools/gen_endpoints.py --docs ~/Default/yhchatAPI/src/api

输出 ``docs/ENDPOINTS.md``（人看）与 ``docs/endpoints.json``（测试/工具用）。
"""

import argparse
import json
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

ENDPOINT_RE = re.compile(r"^(GET|POST|PUT|DELETE|PATCH)\s+(/\S+)", re.MULTILINE)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
DEFAULT_DOCS = Path.home() / "Default" / "yhchatAPI" / "src" / "api"
DEFAULT_OUT = Path("docs")
IMPLEMENTED_FILE = Path("docs/implemented.txt")
"""每行一个已实现端点路径；生成清单时据此打钩。"""


@dataclass(frozen=True)
class Endpoint:
    """一个文档化端点。"""

    source: str
    method: str
    path: str
    title: str

    @property
    def auth(self) -> str:
        """鉴权方式：``open-apis`` 用 bot token，其余（网页端接口）用用户 token。"""
        return "bot token" if self.path.startswith("/open-apis") else "user token"


def parse(docs: Path) -> list[Endpoint]:
    """解析文档目录下的全部 ``*.md``。"""
    endpoints: list[Endpoint] = []
    for md in sorted(docs.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        headings = [(match.start(), match.group(1)) for match in HEADING_RE.finditer(text)]
        for match in ENDPOINT_RE.finditer(text):
            title = next((heading for position, heading in reversed(headings) if position < match.start()), "")
            endpoints.append(
                Endpoint(
                    source=md.relative_to(docs).as_posix(),
                    method=match.group(1),
                    path=match.group(2).split("?", 1)[0],
                    title=title,
                )
            )
    return endpoints


def load_implemented(path: Path) -> set[str]:
    """读取已实现端点清单（``#`` 开头为注释）。"""
    if not path.is_file():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def render_markdown(endpoints: Sequence[Endpoint], implemented: set[str]) -> str:
    """生成 ``docs/ENDPOINTS.md``。"""
    lines = [
        "# 端点清单",
        "",
        "> 本文件由 `tools/gen_endpoints.py` 从 yhchatAPI 文档站生成，请勿手工编辑。",
        "> 覆盖状态来自 `docs/implemented.txt`（每行一个已实现路径）；未列出即视为尚未实现。",
        "",
        f"共 {len(endpoints)} 个端点，已实现 {sum(1 for item in endpoints if item.path in implemented)} 个。",
        "",
    ]

    by_source: dict[str, list[Endpoint]] = {}
    for endpoint in endpoints:
        by_source.setdefault(endpoint.source, []).append(endpoint)

    lines.extend(["## 按文档分组", "", "| 文档 | 端点数 |", "| --- | --- |"])
    lines.extend(f"| `{source}` | {len(items)} |" for source, items in by_source.items())
    lines.append("")

    for source, items in by_source.items():
        lines.extend([f"### `{source}`", "", "| 状态 | 方法 | 路径 | 说明 | 鉴权 |", "| --- | --- | --- | --- | --- |"])
        lines.extend(
            f"| {'[x]' if item.path in implemented else '[ ]'} | `{item.method}` | `{item.path}` | {item.title or '-'} | {item.auth} |"
            for item in items
        )
        lines.append("")

    documented = {item.path for item in endpoints}
    extra = sorted(implemented - documented)
    if extra:
        lines.extend(
            [
                "## 已实现但文档未收录",
                "",
                "| 路径 | 说明 |",
                "| --- | --- |",
                *(f"| `{path}` | 见 `src/yhchat/api/bot.py`，字段来自旧版实现，待验证 |" for path in extra),
                "",
            ]
        )

    return "\n".join(lines)


def render_json(endpoints: Sequence[Endpoint]) -> str:
    """生成 ``docs/endpoints.json``。"""
    payload = {
        "count": len(endpoints),
        "endpoints": [
            {
                "source": endpoint.source,
                "method": endpoint.method,
                "path": endpoint.path,
                "title": endpoint.title,
                "auth": endpoint.auth,
            }
            for endpoint in endpoints
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="从 yhchatAPI 文档站生成端点清单")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS, help="文档站 src/api 目录")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="输出目录")
    args = parser.parse_args(argv)

    docs: Path = args.docs
    out: Path = args.out
    if not docs.is_dir():
        print(f"文档目录不存在: {docs}", file=sys.stderr)
        return 1

    endpoints = parse(docs)
    if not endpoints:
        print(f"没有在 {docs} 下找到端点", file=sys.stderr)
        return 1

    out.mkdir(parents=True, exist_ok=True)
    (out / "ENDPOINTS.md").write_text(render_markdown(endpoints, load_implemented(IMPLEMENTED_FILE)), encoding="utf-8")
    (out / "endpoints.json").write_text(render_json(endpoints), encoding="utf-8")
    covered = sum(1 for endpoint in endpoints if endpoint.path in load_implemented(IMPLEMENTED_FILE))
    print(f"已生成 {len(endpoints)} 个端点（文档内已实现 {covered} 个）→ {out}/ENDPOINTS.md, {out}/endpoints.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
