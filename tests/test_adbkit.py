"""Test cho adbkit dùng device giả (không cần ADB thật)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from adbkit import Device, run_on_all  # noqa: E402


class FakeRaw:
    """Giả lập đối tượng device của ppadb, ghi lại lệnh shell đã gọi."""

    def __init__(self, serial="emulator-5554"):
        self.serial = serial
        self.commands: list[str] = []
        self._installed: set[str] = set()

    def shell(self, cmd):
        self.commands.append(cmd)
        return ""

    def is_installed(self, pkg):
        return pkg in self._installed

    def install(self, path, reinstall=False):
        self.commands.append(f"install {path} reinstall={reinstall}")

    def uninstall(self, pkg):
        self.commands.append(f"uninstall {pkg}")

    def pull(self, remote, local):
        self.commands.append(f"pull {remote} {local}")


def test_tap_emits_input_tap():
    raw = FakeRaw()
    Device(raw).tap(100, 200)
    assert "input tap 100 200" in raw.commands


def test_input_text_escapes_quotes():
    raw = FakeRaw()
    Device(raw).input_text("a'b")
    # Không được để dấu nháy đơn thô làm hỏng lệnh shell.
    assert any("'\\''" in c for c in raw.commands)


def test_input_text_handles_space():
    raw = FakeRaw()
    Device(raw).input_text("a b")
    assert "input text %s" in raw.commands


def test_key_event():
    raw = FakeRaw()
    Device(raw).key(61)
    assert "input keyevent 61" in raw.commands


def test_launch_uses_monkey():
    raw = FakeRaw()
    Device(raw).launch("com.example.app")
    assert any("monkey -p com.example.app" in c for c in raw.commands)


def test_grant_all():
    raw = FakeRaw()
    Device(raw).grant_all("com.example", ["A", "B"])
    assert "pm grant com.example A" in raw.commands
    assert "pm grant com.example B" in raw.commands


def test_run_on_all_collects_results_and_errors():
    good = Device(FakeRaw("dev-ok"))
    bad = Device(FakeRaw("dev-bad"))

    def task(dev):
        if dev.serial == "dev-bad":
            raise RuntimeError("boom")
        dev.tap(1, 1)

    results = run_on_all(task, [good, bad])
    assert results["dev-ok"] is None
    assert isinstance(results["dev-bad"], RuntimeError)


def test_run_on_all_empty():
    assert run_on_all(lambda d: None, []) == {}
