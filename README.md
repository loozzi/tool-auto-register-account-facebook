# textkit & adbkit

Hai thư viện Python nhỏ, không phụ thuộc nặng, dùng để **test app trên Android
của chính bạn**:

- **`textkit`** — sinh dữ liệu giả (tên, ngày sinh, số điện thoại, mật khẩu, hồ
  sơ) cho test fixture, seed database, load testing. Không cần thư viện ngoài.
- **`adbkit`** — wrapper gọn quanh [`pure-python-adb`](https://pypi.org/project/pure-python-adb/)
  để điều khiển thiết bị / máy ảo qua ADB: tap, gõ chữ, cài/gỡ app, cấp quyền,
  mở app, chạy song song nhiều thiết bị.

> ⚠️ Các thư viện này dùng để tự động hoá test cho ứng dụng bạn sở hữu hoặc được
> phép kiểm thử. Đừng dùng để tạo tài khoản hàng loạt hay vi phạm điều khoản dịch
> vụ của bên thứ ba.

## Cấu trúc

```
src/
├── textkit/            # thư viện sinh dữ liệu giả
│   ├── accents.py      # remove_accents() — bỏ dấu tiếng Việt/Unicode
│   ├── names.py        # random_name(), Name
│   ├── generators.py   # random_person/password/phone/birthday
│   └── data/names.json # kho tên (vi, en)
├── adbkit/             # thư viện automation qua ADB
│   ├── device.py       # class Device: tap, input_text, install, grant...
│   └── runner.py       # connect, list_devices, run_on_all
└── main.py             # demo ghép 2 thư viện chạy trên nhiều thiết bị
tests/                  # test cho cả hai thư viện (pytest)
```

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # chỉ cần cho adbkit
```

`textkit` không cần cài gì thêm. Yêu cầu Python 3.10+.

## textkit — ví dụ

```python
import sys; sys.path.insert(0, "src")
from textkit import random_person, random_name, remove_accents

remove_accents("Nguyễn Đăng Khoa")      # 'Nguyen Dang Khoa'

random_name("vi").full                   # 'Ngọ Thiên'

p = random_person("vi")
p.name.full       # tên có dấu
p.ascii_name.full # tên đã bỏ dấu
p.phone           # '+84...'
p.birthday        # datetime.date
p.password        # chuỗi ngẫu nhiên
```

Mọi hàm nhận tham số `rng=random.Random(seed)` để **tái lập** kết quả trong test:

```python
import random
random_person("vi", rng=random.Random(42))   # luôn ra cùng kết quả
```

Hàm chính:

| Hàm | Mô tả |
|-----|-------|
| `remove_accents(s)` | Bỏ dấu (dùng `unicodedata`, không giới hạn tiếng Việt) |
| `random_name(lang)` | Trả về `Name(first, last)`; `.full` là họ tên đầy đủ |
| `random_password(length)` | Chuỗi chữ+số ngẫu nhiên |
| `random_phone(prefix, total_digits)` | Số điện thoại giả |
| `random_birthday(min_year, max_year)` | `date` ngẫu nhiên trong khoảng năm |
| `random_person(lang)` | Gộp tất cả thành một `Person` |
| `available_languages()` | Danh sách ngôn ngữ (`["vi", "en"]`) |

## adbkit — ví dụ

Bật ADB server và kết nối thiết bị (hoặc mở máy ảo LDPlayer/BlueStacks... rồi
`adb connect`). Kiểm tra bằng `adb devices`.

```python
import sys; sys.path.insert(0, "src")
from adbkit import list_devices, run_on_all

def task(device):
    device.launch("com.android.settings")   # mở app
    device.sleep(2)
    device.tap(500, 800)                     # chạm toạ độ
    device.input_text("hello")               # gõ chữ (đã escape an toàn)
    device.key("KEYCODE_TAB")                # gửi keyevent

# Chạy `task` song song trên mọi thiết bị đang kết nối.
results = run_on_all(task, list_devices())
# results = {serial: None nếu OK / Exception nếu lỗi}
```

`Device` cung cấp: `tap`, `swipe`, `input_text`, `key`, `launch`, `stop`,
`install`, `uninstall`, `is_installed`, `grant`, `grant_all`, `pull`, `shell`,
`sleep`. `run_on_all` gom lỗi theo từng thiết bị nên một máy lỗi không làm dừng
các máy còn lại.

## Chạy demo

`src/main.py` ghép hai thư viện: sinh dữ liệu test bằng `textkit` rồi điều khiển
mọi thiết bị bằng `adbkit`. Đây là **template** — hãy sửa hàm `automation_task`
theo luồng test cho app của bạn.

```bash
python src/main.py                 # app mặc định: com.android.settings
python src/main.py com.your.app    # chỉ định package của bạn
```

## Chạy test

```bash
pip install pytest
python -m pytest tests/ -q
```

Test của `adbkit` dùng device giả nên **không cần** ADB hay thiết bị thật.
