"""textkit — thư viện sinh dữ liệu giả (tên, ngày sinh, mật khẩu, hồ sơ...).

Dùng cho test fixture, seed database, load testing. Không phụ thuộc thư viện
ngoài.

Ví dụ nhanh::

    from textkit import random_person
    p = random_person("vi")
    print(p.name.full, p.phone, p.birthday)
"""

from __future__ import annotations

from .accents import remove_accents
from .generators import (
    Person,
    random_birthday,
    random_password,
    random_person,
    random_phone,
)
from .names import Name, available_languages, random_name

__all__ = [
    "remove_accents",
    "Name",
    "random_name",
    "available_languages",
    "Person",
    "random_person",
    "random_password",
    "random_phone",
    "random_birthday",
]
