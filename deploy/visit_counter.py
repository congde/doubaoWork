#!/usr/bin/env python3.11
"""Local page-view counter for agentc.com.cn."""
from __future__ import annotations

import json
import os
import re
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TZ = timezone(timedelta(hours=8))
DATA = Path("/workspace/doubaoWork/data/visits.json")
HOST = "127.0.0.1"
PORT = 8766
COOKIE = "dw_vid"
BOT_RE = re.compile(
    r"bot|spider|crawler|curl|wget|python-requests|bytespider|yandex|"
    r"baidu|sogou|bingpreview|slurp|facebookexternal|ahrefs|semrush|"
    r"masscan|nmap|scan|infrawatch|softsec|headless",
    re.I,
)

lock = threading.Lock()


def today_str() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def empty_state() -> dict:
    return {
        "pv": 0,
        "uv": 0,
        "today": today_str(),
        "today_pv": 0,
        "today_uv": 0,
    }


def load() -> dict:
    if not DATA.exists():
        return empty_state()
    try:
        with DATA.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return empty_state()
    for key, value in empty_state().items():
        data.setdefault(key, value)
    return data


def save(data: dict) -> None:
    DATA.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA.with_suffix(".tmp")
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(DATA)


def public(data: dict) -> dict:
    return {
        "pv": int(data.get("pv", 0)),
        "uv": int(data.get("uv", 0)),
        "today_pv": int(data.get("today_pv", 0)),
        "today_uv": int(data.get("today_uv", 0)),
        "today": data.get("today") or today_str(),
    }


def roll_today(data: dict) -> None:
    current = today_str()
    if data.get("today") != current:
        data["today"] = current
        data["today_pv"] = 0
        data["today_uv"] = 0


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def _send(self, code: int, payload: dict, headers: dict | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path not in ("/visits", "/"):
            self.send_error(404)
            return
        with lock:
            data = load()
            roll_today(data)
            save(data)
        self._send(200, public(data))

    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path not in ("/visits", "/"):
            self.send_error(404)
            return
        ua = self.headers.get("User-Agent") or ""
        extra = {}
        with lock:
            data = load()
            roll_today(data)
            if not BOT_RE.search(ua):
                cookies = self.headers.get("Cookie") or ""
                has_vid = f"{COOKIE}=" in cookies
                data["pv"] = int(data.get("pv", 0)) + 1
                data["today_pv"] = int(data.get("today_pv", 0)) + 1
                if not has_vid:
                    data["uv"] = int(data.get("uv", 0)) + 1
                    data["today_uv"] = int(data.get("today_uv", 0)) + 1
                    extra["Set-Cookie"] = (
                        f"{COOKIE}=1; Max-Age=31536000; Path=/; SameSite=Lax"
                    )
            save(data)
            payload = public(data)
        self._send(200, payload, extra)


def main() -> None:
    DATA.parent.mkdir(parents=True, exist_ok=True)
    with lock:
        data = load()
        roll_today(data)
        save(data)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
