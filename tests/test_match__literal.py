from typing import Literal

import pytest

from py_pattern import match, ExhaustiveError


type Platform = Literal["instagram", "tiktok", "youtube"]


class InstagramManager: ...


class TiktokManager: ...


class YoutubeManager: ...


@pytest.mark.parametrize(
    ("platform", "expected_type"),
    [
        ("instagram", InstagramManager),
        ("tiktok", TiktokManager),
        ("youtube", YoutubeManager),
    ],
)
def test__valid_literal(platform: Platform, expected_type: type) -> None:
    result = (
        match(platform)
        .case("instagram", InstagramManager())
        .case("tiktok", TiktokManager())
        .case("youtube", YoutubeManager())
        .exhaustive()
    )

    assert isinstance(result, expected_type)


def test__exhaustive__raises_error() -> None:
    platform: Platform = "youtube"

    with pytest.raises(ExhaustiveError) as exc_info:
        match(platform).case("instagram", "IG").case("tiktok", "TT").exhaustive()

    assert exc_info.value.value == "youtube"


def test_literal_match_with_otherwise() -> None:
    platform: Platform = "youtube"

    result = (
        match(platform).case("instagram", "IG").case("tiktok", "TT").otherwise("Other")
    )

    assert result == "Other"
