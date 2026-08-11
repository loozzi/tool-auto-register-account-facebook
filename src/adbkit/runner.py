"""Kết nối tới ADB server và chạy một tác vụ trên nhiều thiết bị song song."""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable

from .device import Device

log = logging.getLogger(__name__)


def connect(host: str = "127.0.0.1", port: int = 5037) -> Any:
    """Tạo client kết nối tới ADB server (mặc định localhost:5037).

    ``ppadb`` chỉ được import khi thực sự cần kết nối, nên có thể import và
    unit-test phần logic của module mà không cần cài ADB stack.
    """
    from ppadb.client import Client as AdbClient  # import trễ

    return AdbClient(host=host, port=port)


def list_devices(
    client: Any | None = None, *, default_delay: float = 1.0
) -> list[Device]:
    """Trả về danh sách :class:`Device` đang kết nối."""
    client = client or connect()
    return [Device(raw, default_delay=default_delay) for raw in client.devices()]


def run_on_all(
    task: Callable[[Device], None],
    devices: list[Device] | None = None,
    *,
    max_workers: int | None = None,
) -> dict[str, Exception | None]:
    """Chạy ``task(device)`` trên mọi thiết bị bằng thread song song.

    Trả về dict ``{serial: None nếu OK, hoặc Exception nếu lỗi}`` — một thiết bị
    lỗi không làm dừng các thiết bị còn lại.
    """
    devices = devices if devices is not None else list_devices()
    if not devices:
        log.warning("Không tìm thấy thiết bị ADB nào.")
        return {}

    results: dict[str, Exception | None] = {}
    with ThreadPoolExecutor(max_workers=max_workers or len(devices)) as pool:
        future_to_serial = {
            pool.submit(task, dev): dev.serial for dev in devices
        }
        for future in as_completed(future_to_serial):
            serial = future_to_serial[future]
            try:
                future.result()
                results[serial] = None
                log.info("[%s] xong", serial)
            except Exception as exc:  # noqa: BLE001 - gom lỗi từng thiết bị
                results[serial] = exc
                log.error("[%s] lỗi: %s", serial, exc)
    return results
