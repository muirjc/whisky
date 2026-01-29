"""Unit tests for similarity matching algorithm."""

import pytest

from src.services.matching import compute_similarity


class TestComputeSimilarity:
    def test_identical_profiles(self) -> None:
        profile = {"smoky_peaty": 5, "fruity": 3, "sherried": 2}
        score = compute_similarity(profile, profile)
        assert score == 1.0

    def test_completely_different(self) -> None:
        a = {f: 0 for f in ["smoky_peaty", "fruity", "sherried", "spicy",
                             "floral_grassy", "maritime", "honey_sweet",
                             "vanilla_caramel", "oak_woody", "nutty",
                             "malty_biscuity", "medicinal_iodine"]}
        b = {f: 5 for f in a}
        score = compute_similarity(a, b)
        assert 0 < score < 0.2  # Should be very low

    def test_similar_profiles(self) -> None:
        a = {"smoky_peaty": 5, "maritime": 4, "medicinal_iodine": 3}
        b = {"smoky_peaty": 4, "maritime": 4, "medicinal_iodine": 3}
        score = compute_similarity(a, b)
        assert score > 0.4  # Should be high

    def test_symmetry(self) -> None:
        a = {"smoky_peaty": 5, "fruity": 1}
        b = {"smoky_peaty": 2, "fruity": 4}
        assert compute_similarity(a, b) == compute_similarity(b, a)

    def test_score_range(self) -> None:
        a = {"smoky_peaty": 3}
        b = {"smoky_peaty": 1}
        score = compute_similarity(a, b)
        assert 0 <= score <= 1

    def test_missing_keys_default_to_zero(self) -> None:
        a = {"smoky_peaty": 5}
        b = {}
        score = compute_similarity(a, b)
        assert 0 < score < 1
