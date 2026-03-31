from __future__ import annotations

import os
import sys

import grpc

from remote.proto_loader import load_proto_modules


def _target() -> str:
    return os.environ.get("TREELAND_RPC_ADDR", "127.0.0.1:50051")


def _metadata() -> list[tuple[str, str]]:
    token = os.environ.get("TREELAND_RPC_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TREELAND_RPC_TOKEN is not set")
    return [("authorization", f"Bearer {token}")]


def _save_png(path: str, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


def main() -> None:
    pb2, pb2_grpc = load_proto_modules()
    channel = grpc.insecure_channel(_target())
    stub = pb2_grpc.RemoteControlStub(channel)

    if len(sys.argv) >= 2 and sys.argv[1] == "screenshot":
        resp = stub.GetScreenshot(pb2.Empty(), metadata=_metadata())
        out = sys.argv[2] if len(sys.argv) >= 3 else "screen.png"
        _save_png(out, resp.png)
        print(f"saved {out} ({resp.width}x{resp.height})")
        return

    if len(sys.argv) >= 2 and sys.argv[1] == "click":
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        stub.Click(pb2.ClickRequest(x=x, y=y, button="left", clicks=1), metadata=_metadata())
        print("clicked")
        return

    print("usage:")
    print("  python -m remote.client screenshot [path]")
    print("  python -m remote.client click <x> <y>")


if __name__ == "__main__":
    main()
