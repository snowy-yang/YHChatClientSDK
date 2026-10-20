"""覆盖率自检：``docs/endpoints.json``（242 条）= 已实现 + ``docs/v1_pending.md``。

这些文件都是生成物，这个测试防止「文档数了 242 个、实际却对不上」这种漂移。
计数按**文档条目**算：文档里同一个 (method, path) 可能出现两次（不同页面各写一遍），
条目级会各算一次，路径级去重后会少几个，两种口径不要混用。
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PENDING_ROW = re.compile(r"\| `(?P<path>[^`]+)` \| (?P<method>\w+) \|")

# 文档条目漏了前导斜杠，生成器归一化后实现的路径；以及文档站里没进 242 清单的上传接口
NORMALIZED_PATHS = {
    "/v1/instruction/edit",
    "/v1/msg/msg-forward",
    "/v1/msg/pic-list-message-by-mid-seq",
}
EXTRA_IMPLEMENTED = {
    "/open-apis/v1/image/upload",
    "/open-apis/v1/video/upload",
    "/open-apis/v1/file/upload",
}


def endpoint_inventory() -> list[dict[str, str]]:
    data = json.loads((ROOT / "docs/endpoints.json").read_text(encoding="utf-8"))
    return data["endpoints"]


def implemented_paths() -> set[str]:
    text = (ROOT / "docs/implemented.txt").read_text(encoding="utf-8")
    return {line.strip() for line in text.splitlines() if line.strip()}


def pending_endpoints() -> list[tuple[str, str]]:
    text = (ROOT / "docs/v1_pending.md").read_text(encoding="utf-8")
    return [(match.group("method"), match.group("path")) for match in PENDING_ROW.finditer(text)]


def test_inventory_is_242_entries() -> None:
    assert len(endpoint_inventory()) == 242


def test_implemented_and_pending_partition_inventory() -> None:
    inventory = endpoint_inventory()
    implemented = implemented_paths()
    pending = pending_endpoints()

    done = [entry for entry in inventory if entry["path"] in implemented]
    assert len(done) + len(pending) == len(inventory), "已实现 + 待实现 必须正好 242 条"
    assert {path for _, path in pending}.isdisjoint(implemented), "同一个端点不能既已实现又待实现"


def test_implemented_paths_are_known_paths() -> None:
    inventory_paths = {entry["path"] for entry in endpoint_inventory()}
    unknown = implemented_paths() - inventory_paths
    assert unknown == NORMALIZED_PATHS | EXTRA_IMPLEMENTED, f"出现未登记的实现路径: {unknown}"
