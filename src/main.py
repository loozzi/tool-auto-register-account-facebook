"""Demo: dùng ``textkit`` + ``adbkit`` để chạy UI automation trên nhiều thiết bị.

Đây là một *template* trung tính cho việc test app của chính bạn: sinh dữ liệu
giả bằng textkit rồi điều khiển các thiết bị/máy ảo đang kết nối bằng adbkit.
Thay phần thân hàm ``automation_task`` bằng luồng thao tác cho app của bạn.

Chạy::

    python src/main.py                       # dùng app mặc định (Settings)
    python src/main.py com.your.app          # chỉ định package của bạn
"""

from __future__ import annotations

import logging
import sys

from adbkit import Device, list_devices, run_on_all
from textkit import random_person


def automation_task(device: Device, package: str) -> None:
    """Luồng thao tác mẫu chạy trên MỘT thiết bị.

    Mở app, rồi minh hoạ việc gõ dữ liệu giả (ví dụ để điền vào một ô tìm kiếm
    trong app của bạn). Hãy thay bằng luồng test thật của bạn.
    """
    person = random_person(lang="vi")
    logging.info(
        "[%s] dữ liệu test: %s | %s | %s",
        device.serial,
        person.name.full,
        person.phone,
        person.birthday,
    )

    device.launch(package)
    device.sleep(2)

    # Ví dụ minh hoạ: gõ tên (đã bỏ dấu) như một chuỗi input bất kỳ.
    device.input_text(person.ascii_name.full)
    device.sleep()


def main(package: str) -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    devices = list_devices()
    if not devices:
        logging.error("Không có thiết bị ADB nào. Hãy `adb devices` để kiểm tra.")
        return

    logging.info("Tìm thấy %d thiết bị: %s", len(devices),
                 [d.serial for d in devices])

    results = run_on_all(lambda dev: automation_task(dev, package), devices)

    ok = sum(1 for err in results.values() if err is None)
    logging.info("Hoàn tất: %d/%d thiết bị OK", ok, len(results))


if __name__ == "__main__":
    pkg = sys.argv[1] if len(sys.argv) > 1 else "com.android.settings"
    main(pkg)
