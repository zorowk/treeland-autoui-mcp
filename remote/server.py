from __future__ import annotations

import logging
import os
from concurrent.futures import ThreadPoolExecutor

import grpc

from remote import actions, auth, exec_cmd, screenshot
from remote.proto_loader import load_proto_modules


LOG = logging.getLogger("treeland.remote.server")


def _bind_address() -> str:
    host = os.environ.get("TREELAND_RPC_HOST", "0.0.0.0")
    port = os.environ.get("TREELAND_RPC_PORT", "50051")
    return f"{host}:{port}"


def _max_workers() -> int:
    value = os.environ.get("TREELAND_RPC_WORKERS", "4")
    try:
        return max(1, int(value))
    except ValueError:
        return 4


def _configure_logging() -> None:
    level = os.environ.get("TREELAND_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def serve() -> None:
    _configure_logging()
    pb2, pb2_grpc = load_proto_modules()

    class RemoteControlServicer(pb2_grpc.RemoteControlServicer):
        def GetScreenshot(self, request, context):
            auth.require_auth(context)
            png_bytes, width, height = screenshot.take_screenshot()
            return pb2.ScreenshotResponse(png=png_bytes, width=width, height=height)

        def Click(self, request, context):
            auth.require_auth(context)
            actions.click(request.x, request.y, request.button or "left", max(1, request.clicks))
            return pb2.Ack(ok=True, message="clicked")

        def GetKeys(self, request, context):
            auth.require_auth(context)
            return pb2.KeysList(keys=list(actions.keyboard_keys()))

        def Exec(self, request, context):
            auth.require_auth(context)
            timeout_s = request.timeout_s if request.timeout_s > 0 else 10
            stdout, stderr, code, duration_ms = exec_cmd.run(request.command, timeout_s=timeout_s)
            return pb2.ExecResponse(stdout=stdout, stderr=stderr, exit_code=code, duration_ms=duration_ms)

        def Drag(self, request, context):
            auth.require_auth(context)
            actions.drag(
                request.from_x,
                request.from_y,
                request.to_x,
                request.to_y,
                request.button or "left",
                request.key or "",
            )
            return pb2.Ack(ok=True, message="dragged")

        def Type(self, request, context):
            auth.require_auth(context)
            actions.type_text(request.text, request.use_clipboard)
            return pb2.Ack(ok=True, message="typed")

        def Hotkey(self, request, context):
            auth.require_auth(context)
            actions.hotkey(list(request.keys))
            return pb2.Ack(ok=True, message="hotkey")

        def Scroll(self, request, context):
            auth.require_auth(context)
            clicks = max(1, abs(request.clicks))
            actions.scroll(clicks, request.direction or "down")
            return pb2.Ack(ok=True, message="scrolled")

        def Move(self, request, context):
            auth.require_auth(context)
            actions.move(request.x, request.y)
            return pb2.Ack(ok=True, message="moved")

    server = grpc.server(ThreadPoolExecutor(max_workers=_max_workers()))
    pb2_grpc.add_RemoteControlServicer_to_server(RemoteControlServicer(), server)
    address = _bind_address()
    server.add_insecure_port(address)
    server.start()
    LOG.info("gRPC server listening on %s", address)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
