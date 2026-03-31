from __future__ import annotations

import os

import grpc

from remote.proto_loader import load_proto_modules


class RemoteClient:
    def __init__(self, address: str | None = None, token: str | None = None) -> None:
        self._address = address or os.environ.get("TREELAND_RPC_ADDR", "127.0.0.1:50051")
        self._token = token or os.environ.get("TREELAND_RPC_TOKEN", "").strip()
        if not self._token:
            raise RuntimeError("TREELAND_RPC_TOKEN is not set")
        self._pb2, self._pb2_grpc = load_proto_modules()
        self._channel = grpc.insecure_channel(self._address)
        self._stub = self._pb2_grpc.RemoteControlStub(self._channel)

    def _metadata(self) -> list[tuple[str, str]]:
        return [("authorization", f"Bearer {self._token}")]

    def get_screenshot(self):
        resp = self._stub.GetScreenshot(self._pb2.Empty(), metadata=self._metadata())
        return resp.png, resp.width, resp.height

    def get_keys(self) -> list[str]:
        resp = self._stub.GetKeys(self._pb2.Empty(), metadata=self._metadata())
        return list(resp.keys)

    def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> None:
        req = self._pb2.ClickRequest(x=x, y=y, button=button, clicks=clicks)
        self._stub.Click(req, metadata=self._metadata())

    def drag(
        self,
        from_x: int,
        from_y: int,
        to_x: int,
        to_y: int,
        button: str = "left",
        key: str = "",
    ) -> None:
        req = self._pb2.DragRequest(
            from_x=from_x,
            from_y=from_y,
            to_x=to_x,
            to_y=to_y,
            button=button,
            key=key,
        )
        self._stub.Drag(req, metadata=self._metadata())

    def move(self, x: int, y: int) -> None:
        req = self._pb2.MoveRequest(x=x, y=y)
        self._stub.Move(req, metadata=self._metadata())

    def type_text(self, text: str, use_clipboard: bool = True) -> None:
        req = self._pb2.TypeRequest(text=text, use_clipboard=use_clipboard)
        self._stub.Type(req, metadata=self._metadata())

    def hotkey(self, keys: list[str]) -> None:
        req = self._pb2.HotkeyRequest(keys=keys)
        self._stub.Hotkey(req, metadata=self._metadata())

    def scroll(self, clicks: int, direction: str = "down") -> None:
        req = self._pb2.ScrollRequest(clicks=clicks, direction=direction)
        self._stub.Scroll(req, metadata=self._metadata())
