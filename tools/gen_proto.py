"""生成 protobuf 代码（``v1/*`` 的 protobuf 端点用）。

proto 放在 ``proto/yhchat/proto/_pb/`` 下，生成的模块路径是
``yhchat.proto._pb.full_pb2``，与源码包结构一致。

编译用 ``grpcio-tools`` 自带的 ``protoc``——它只是编译器提供者，SDK 运行时不依赖 gRPC。

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
    """调用 ``protoc`` 生成 pb2 与 pyi。"""
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
        *(str(proto) for proto in protos),
    ]
    print(" ".join(command))
    code = subprocess.run(command, check=False).returncode
    if code != 0:
        return code
    print(f"已生成 {len(protos)} 个 proto → {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
