from __future__ import annotations

import os

import grpc


AUTH_HEADER = "authorization"


def _expected_token() -> str:
    token = os.environ.get("TREELAND_RPC_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TREELAND_RPC_TOKEN is not set")
    return token


def require_auth(context: grpc.ServicerContext) -> None:
    expected = _expected_token()
    metadata = dict(context.invocation_metadata())
    raw = metadata.get(AUTH_HEADER, "")
    if not raw.startswith("Bearer "):
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "missing bearer token")
    token = raw[len("Bearer ") :].strip()
    if token != expected:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "invalid token")
