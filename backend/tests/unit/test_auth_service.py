"""Unit tests for authentication service."""

import pytest

from src.services.auth import hash_password, validate_password_strength, verify_password


class TestPasswordHashing:
    def test_hash_and_verify(self) -> None:
        password = "securepass123"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_wrong_password_fails(self) -> None:
        hashed = hash_password("correct123")
        assert not verify_password("wrong123", hashed)

    def test_different_hashes_for_same_password(self) -> None:
        h1 = hash_password("testpass123")
        h2 = hash_password("testpass123")
        assert h1 != h2  # bcrypt uses random salt


class TestPasswordValidation:
    def test_valid_password(self) -> None:
        assert validate_password_strength("securepass123") is None

    def test_too_short(self) -> None:
        assert validate_password_strength("short1") is not None

    def test_no_letter(self) -> None:
        assert validate_password_strength("12345678") is not None

    def test_no_number(self) -> None:
        assert validate_password_strength("abcdefgh") is not None
