"""Wrapper tiện dụng quanh một thiết bị ADB (điện thoại thật / máy ảo).

Bọc đối tượng device của ``pure-python-adb`` để cung cấp các thao tác UI
automation thường dùng khi test app: tap, gõ chữ, cài/gỡ app, cấp quyền,
mở app, pull file... với logging và độ trễ có thể cấu hình.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

log = logging.getLogger(__name__)


class Device:
    """Bọc một thiết bị ADB đã kết nối.

    :param raw: đối tượng device trả về từ ``AdbClient.devices()``.
    :param default_delay: độ trễ mặc định (giây) giữa các thao tác UI.
    """

    def __init__(self, raw, default_delay: float = 1.0) -> None:
        self._raw = raw
        self.default_delay = default_delay

    # -- Định danh ---------------------------------------------------------
    @property
    def serial(self) -> str:
        return self._raw.serial

    def __repr__(self) -> str:  # pragma: no cover - chỉ để debug
        return f"<Device {self.serial}>"

    # -- Nguyên thuỷ -------------------------------------------------------
    def shell(self, command: str) -> str:
        """Chạy một lệnh shell trên thiết bị và trả về output."""
        log.debug("[%s] shell: %s", self.serial, command)
        return self._raw.shell(command)

    def sleep(self, seconds: float | None = None) -> None:
        time.sleep(self.default_delay if seconds is None else seconds)

    # -- Thao tác UI -------------------------------------------------------
    def tap(self, x: int, y: int) -> None:
        self.shell(f"input tap {x} {y}")

    def input_text(self, text: str, per_char_delay: float = 0.0) -> None:
        """Gõ ``text`` vào ô đang focus.

        Escape các ký tự đặc biệt của shell để tránh lỗi/injection khi text
        chứa dấu nháy, dấu cách...
        """
        for char in text:
            if char == " ":
                self.shell("input text %s")  # %s = dấu cách với `input text`
            else:
                safe = char.replace("'", "'\\''")
                self.shell(f"input text '{safe}'")
            if per_char_delay:
                time.sleep(per_char_delay)

    def key(self, keycode: int | str) -> None:
        """Gửi một keyevent (mã số hoặc tên, ví dụ 61 / ``KEYCODE_TAB``)."""
        self.shell(f"input keyevent {keycode}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")

    # -- Quản lý app -------------------------------------------------------
    def is_installed(self, package: str) -> bool:
        return self._raw.is_installed(package)

    def install(self, apk_path: str | Path, *, reinstall: bool = True) -> None:
        apk_path = str(apk_path)
        if reinstall:
            self._raw.install(apk_path, reinstall=True)
        else:
            self._raw.install(apk_path)
        log.info("[%s] đã cài %s", self.serial, apk_path)

    def uninstall(self, package: str) -> None:
        if self.is_installed(package):
            self.shell(f"pm clear {package}")
            self._raw.uninstall(package)
            log.info("[%s] đã gỡ %s", self.serial, package)

    def grant(self, package: str, permission: str) -> None:
        self.shell(f"pm grant {package} {permission}")

    def grant_all(self, package: str, permissions: list[str]) -> None:
        for perm in permissions:
            self.grant(package, perm)

    def launch(self, package: str) -> None:
        """Mở app qua LAUNCHER intent."""
        self.shell(
            f"monkey -p {package} -c android.intent.category.LAUNCHER 1"
        )

    def stop(self, package: str) -> None:
        self.shell(f"am force-stop {package}")

    def pull(self, remote: str, local: str | Path) -> None:
        self._raw.pull(remote, str(local))
