"""Chuẩn hoá / bỏ dấu tiếng Việt (và Unicode nói chung)."""

from __future__ import annotations

import unicodedata

# Một vài ký tự không được ``NFKD`` tách dấu nên xử lý tay.
_SPECIAL_MAP = {
    "đ": "d",
    "Đ": "D",
    "ð": "d",
    "Ð": "D",
    "ø": "o",
    "Ø": "O",
    "ł": "l",
    "Ł": "L",
}


def remove_accents(text: str) -> str:
    """Trả về ``text`` sau khi bỏ toàn bộ dấu.

    Dùng ``unicodedata`` để tách dấu combining thay vì bảng tra thủ công,
    nên hoạt động với mọi ngôn ngữ Latin chứ không riêng tiếng Việt.

    >>> remove_accents("Nguyễn Đăng Khoa")
    'Nguyen Dang Khoa'
    """
    result = []
    for char in text:
        if char in _SPECIAL_MAP:
            result.append(_SPECIAL_MAP[char])
            continue
        decomposed = unicodedata.normalize("NFKD", char)
        stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
        result.append(stripped or char)
    return "".join(result)
