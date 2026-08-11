"""Test cho thư viện textkit."""

import random
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from textkit import (  # noqa: E402
    Name,
    available_languages,
    random_birthday,
    random_name,
    random_password,
    random_person,
    random_phone,
    remove_accents,
)


def test_remove_accents_vietnamese():
    assert remove_accents("Nguyễn Đăng Khoa") == "Nguyen Dang Khoa"
    assert remove_accents("đĐáàảãạ") == "dDaaaaa"


def test_remove_accents_keeps_ascii():
    assert remove_accents("Hello 123!") == "Hello 123!"


def test_available_languages():
    langs = available_languages()
    assert "vi" in langs and "en" in langs


def test_random_name_type_and_lang():
    name = random_name("vi")
    assert isinstance(name, Name)
    assert name.full == f"{name.first} {name.last}"


def test_random_name_invalid_lang():
    with pytest.raises(ValueError):
        random_name("xx")


def test_random_name_is_reproducible_with_seed():
    a = random_name("vi", rng=random.Random(42))
    b = random_name("vi", rng=random.Random(42))
    assert a == b


def test_random_password_length_and_alphabet():
    pwd = random_password(20, rng=random.Random(1))
    assert len(pwd) == 20
    assert all(c.isalnum() for c in pwd)


def test_random_password_rejects_nonpositive():
    with pytest.raises(ValueError):
        random_password(0)


def test_random_birthday_in_range():
    for _ in range(50):
        bday = random_birthday(min_year=1990, max_year=2000)
        assert isinstance(bday, date)
        assert 1990 <= bday.year <= 2000


def test_random_phone_prefix_and_length():
    phone = random_phone("+84364", total_digits=11)
    assert phone.startswith("+84364")
    assert sum(c.isdigit() for c in phone) == 11


def test_random_person_complete_and_ascii():
    person = random_person("vi", rng=random.Random(7))
    assert person.name.full
    assert remove_accents(person.name.full) == person.ascii_name.full
    assert person.phone.startswith("+84")
    assert len(person.password) == 15
