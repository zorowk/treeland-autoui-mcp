from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _generated_dir() -> Path:
    return _repo_root() / "remote" / "_generated"


def _proto_path() -> Path:
    return _repo_root() / "proto" / "treeland_remote.proto"


def _needs_regen(proto: Path, out_dir: Path) -> bool:
    if not out_dir.exists():
        return True
    pb2 = out_dir / "treeland_remote_pb2.py"
    pb2_grpc = out_dir / "treeland_remote_pb2_grpc.py"
    if not pb2.exists() or not pb2_grpc.exists():
        return True
    return proto.stat().st_mtime > min(pb2.stat().st_mtime, pb2_grpc.stat().st_mtime)


def _run_protoc(proto: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={proto.parent}",
        f"--python_out={out_dir}",
        f"--grpc_python_out={out_dir}",
        str(proto),
    ]
    subprocess.run(cmd, check=True)


def load_proto_modules():
    proto = _proto_path()
    out_dir = _generated_dir()
    if _needs_regen(proto, out_dir):
        _run_protoc(proto, out_dir)

    if str(out_dir) not in sys.path:
        sys.path.insert(0, str(out_dir))

    pb2 = importlib.import_module("treeland_remote_pb2")
    pb2_grpc = importlib.import_module("treeland_remote_pb2_grpc")
    return pb2, pb2_grpc
