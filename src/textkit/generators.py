"""Các hàm sinh dữ liệu giả ngẫu nhiên: mật khẩu, ngày sinh, SĐT, hồ sơ."""

from __future__ import annotations

import random
import string
from dataclasses import dataclass
from datetime import date

from .accents import remove_accents
from .names import Name, random_name


def random_password(
    length: int = 15,
    *,
    alphabet: str = string.ascii_letters + string.digits,
    rng: random.Random | None = None,
) -> str:
    """Chuỗi ký tự ngẫu nhiên độ dài ``length`` (mặc định chữ + số)."""
    rng = rng or random
    if length <= 0:
        raise ValueError("length phải > 0")
    return "".join(rng.choice(alphabet) for _ in range(length))


def random_birthday(
    *,
    min_year: int = 1970,
    max_year: int = 2003,
    rng: random.Random | None = None,
) -> date:
    """Ngày sinh ngẫu nhiên trong khoảng [``min_year``, ``max_year``]."""
    rng = rng or random
    if min_year > max_year:
        raise ValueError("min_year phải <= max_year")
    year = rng.randint(min_year, max_year)
    month = rng.randint(1, 12)
    # Ngày an toàn cho mọi tháng (kể cả tháng 2) để tránh lỗi ngày không hợp lệ.
    day = rng.randint(1, 28)
    return date(year, month, day)


def random_phone(
    prefix: str = "+84",
    *,
    total_digits: int = 11,
    rng: random.Random | None = None,
) -> str:
    """Số điện thoại giả bắt đầu bằng ``prefix``.

    ``total_digits`` là tổng số chữ số (không tính dấu ``+``); phần còn thiếu
    sau ``prefix`` được điền bằng chữ số ngẫu nhiên.
    """
    rng = rng or random
    existing = sum(c.isdigit() for c in prefix)
    remaining = total_digits - existing
    if remaining < 0:
        raise ValueError("prefix đã dài hơn total_digits")
    suffix = "".join(str(rng.randint(0, 9)) for _ in range(remaining))
    return prefix + suffix


@dataclass(frozen=True)
class Person:
    """Một hồ sơ giả hoàn chỉnh dùng cho test/seed dữ liệu."""

    name: Name
    ascii_name: Name
    phone: str
    birthday: date
    password: str


def random_person(
    lang: str = "vi",
    *,
    password_length: int = 15,
    phone_prefix: str = "+84",
    rng: random.Random | None = None,
) -> Person:
    """Sinh một :class:`Person` ngẫu nhiên hoàn chỉnh.

    Truyền ``rng=random.Random(seed)`` nếu cần kết quả tái lập được.
    """
    rng = rng or random
    name = random_name(lang, rng=rng)
    ascii_name = Name(remove_accents(name.first), remove_accents(name.last))
    return Person(
        name=name,
        ascii_name=ascii_name,
        phone=random_phone(phone_prefix, rng=rng),
        birthday=random_birthday(rng=rng),
        password=random_password(password_length, rng=rng),
    )
