"""adbkit — wrapper gọn cho UI automation qua ADB (test app của chính bạn).

Ví dụ nhanh::

    from adbkit import list_devices, run_on_all

    def task(device):
        device.launch("com.android.settings")
        device.sleep()
        device.tap(500, 800)

    run_on_all(task, list_devices())
"""

from __future__ import annotations

from .device import Device
from .runner import connect, list_devices, run_on_all

__all__ = ["Device", "connect", "list_devices", "run_on_all"]
