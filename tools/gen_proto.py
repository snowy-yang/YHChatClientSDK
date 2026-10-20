"""生成 gRPC 代码。

proto 放在 ``proto/yhchat/grpc/_pb/`` 下，这样生成的模块路径是
``yhchat.grpc._pb.yhchat_pb2``，与源码包结构一致（生成的 import 不用改）。

用法::

    uv run python tools/gen_proto.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO_DIR = ROOT / "proto"
OUT_DIR = ROOT / "src"


def main() -> int:
    """调用 grpc_tools.protoc 生成 pb2 / pb2_grpc / pyi。"""
    protos = sorted(PROTO_DIR.rglob("*.proto"))
    if not protos:
        print(f"没有找到 proto 文件: {PROTO_DIR}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{PROTO_DIR}",
        f"--python_out={OUT_DIR}",
        f"--pyi_out={OUT_DIR}",
        f"--grpc_python_out={OUT_DIR}",
        *(str(proto) for proto in protos),
    ]
    print(" ".join(command))
    result = subprocess.run(command, check=False)
    if result.returncode == 0:
        print(f"已生成 {len(protos)} 个 proto → {OUT_DIR}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
