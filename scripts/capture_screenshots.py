#!/usr/bin/env python3
"""Capture representative screenshots of the exact static Control UI demo."""
from __future__ import annotations

import contextlib
import http.server
import os
import shutil
import socket
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import ViewportSize, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "screenshots"


def resolve_chrome() -> Path:
    env = os.environ.get("PLAYWRIGHT_CHROME")
    if env:
        return Path(env)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        found = shutil.which(name)
        if found:
            return Path(found)
    candidates = sorted(Path.home().glob(".hermes/profiles/*/home/.linkedin-mcp/patchright-browsers/chromium-*/chrome-linux64/chrome"))
    if candidates:
        return candidates[-1]
    return Path("/nonexistent/chrome")


CHROME = resolve_chrome()
VIEWPORT: ViewportSize = {"width": 1440, "height": 1050}


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@contextlib.contextmanager
def static_server():
    port = free_port()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format: str, *args):  # noqa: A002 - inherited stdlib name
            return

    class TCP(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    old_cwd = Path.cwd()
    os.chdir(ROOT)
    server = TCP(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}/"
    finally:
        server.shutdown()
        server.server_close()
        os.chdir(old_cwd)


def wait_app(page):
    page.wait_for_selector("#appView:not(.hidden)", timeout=10000)
    page.wait_for_timeout(700)


def shot(page, name: str):
    page.screenshot(path=str(OUT / name), full_page=True)


def dom_click(page, selector: str):
    page.locator(selector).evaluate("el => el.click()")
    page.wait_for_timeout(650)


def main() -> None:
    if not CHROME.exists():
        raise SystemExit(f"Browser not found: {CHROME}. Set PLAYWRIGHT_CHROME to a Chromium/Chrome executable.")
    OUT.mkdir(parents=True, exist_ok=True)
    for existing in OUT.glob("*.png"):
        existing.unlink()

    with static_server() as base, sync_playwright() as p:
        browser = p.chromium.launch(executable_path=str(CHROME), headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=1)
        page.goto(base, wait_until="networkidle")
        wait_app(page)

        # Login page screenshot: force the real login section visible; no custom mock layout.
        page.evaluate("""
        () => {
          document.body.classList.add('authing');
          document.querySelector('#appView')?.classList.add('hidden');
          document.querySelector('#setupView')?.classList.add('hidden');
          document.querySelector('#loginView')?.classList.remove('hidden');
          document.querySelector('#loginUser')?.setAttribute('value', '');
          document.querySelector('#loginPass')?.setAttribute('value', '');
        }
        """)
        page.wait_for_timeout(500)
        shot(page, "01-login.png")

        page.reload(wait_until="networkidle")
        wait_app(page)
        shot(page, "02-acl-rules.png")

        dom_click(page, "#tab-approvals")
        shot(page, "03-approvals.png")

        dom_click(page, "#tab-access")
        shot(page, "04-access-logs.png")

        dom_click(page, "#tab-mcp")
        shot(page, "05-mcp-tools.png")

        dom_click(page, "#tab-gatewaySetup")
        shot(page, "06-gateway-setup-mcp-authorization.png")

        dom_click(page, "#adminNav-workspace")
        shot(page, "07-workspace-configuration.png")

        dom_click(page, "#adminNav-channels")
        shot(page, "08-channel-configuration.png")

        dom_click(page, "#tab-adminSettings")
        dom_click(page, "#adminNav-system")
        shot(page, "09-runtime-status.png")

        dom_click(page, "#runtimeTab-backups")
        shot(page, "10-runtime-backups.png")

        browser.close()

    print("Captured screenshots:")
    for p in sorted(OUT.glob("*.png")):
        print(f"- {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
