"""Kho tên dùng để sinh dữ liệu giả (test fixture, seed DB...)."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_DATA_FILE = Path(__file__).parent / "data" / "names.json"


@lru_cache(maxsize=1)
def _load() -> dict[str, dict[str, list[str]]]:
    with _DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def available_languages() -> list[str]:
    """Danh sách ngôn ngữ có sẵn trong kho tên, ví dụ ``["vi", "en"]``."""
    return list(_load().keys())


@dataclass(frozen=True)
class Name:
    """Một tên ngẫu nhiên đã tách sẵn họ / tên."""

    first: str
    last: str

    @property
    def full(self) -> str:
        return f"{self.first} {self.last}"


def random_name(lang: str = "vi", rng: random.Random | None = None) -> Name:
    """Sinh ngẫu nhiên một :class:`Name` theo ngôn ngữ ``lang``.

    ``rng`` cho phép truyền ``random.Random(seed)`` để kết quả tái lập được.
    """
    rng = rng or random
    data = _load()
    if lang not in data:
        raise ValueError(
            f"Không có ngôn ngữ {lang!r}. Có sẵn: {available_languages()}"
        )
    pool = data[lang]
    return Name(
        first=rng.choice(pool["firstName"]),
        last=rng.choice(pool["lastName"]),
    )
