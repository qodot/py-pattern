from enum import StrEnum
from typing import assert_type

import pytest

from match_expression import ExhaustiveError, match


class Platform(StrEnum):
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"


class InstagramManager: ...


class TiktokManager: ...


class YoutubeManager: ...


@pytest.mark.parametrize(
    ("platform", "expected_type"),
    [
        (Platform.INSTAGRAM, InstagramManager),
        (Platform.TIKTOK, TiktokManager),
        (Platform.YOUTUBE, YoutubeManager),
    ],
)
def test__valid_enum(platform: Platform, expected_type: type) -> None:
    result = (
        match(platform)
        .case(Platform.INSTAGRAM, InstagramManager())
        .case(Platform.TIKTOK, TiktokManager())
        .case(Platform.YOUTUBE, YoutubeManager())
        .exhaustive()
    )

    assert_type(result, InstagramManager | TiktokManager | YoutubeManager)
    assert isinstance(result, expected_type)


def test__exhaustive__raises_error() -> None:
    platform: Platform = Platform.YOUTUBE

    with pytest.raises(ExhaustiveError) as exc_info:
        match(platform).case(Platform.INSTAGRAM, "IG").case(Platform.TIKTOK, "TT").exhaustive()

    assert exc_info.value.value == Platform.YOUTUBE


def test_enum_match_with_otherwise() -> None:
    platform: Platform = Platform.YOUTUBE

    result = match(platform).case(Platform.INSTAGRAM, "IG").case(Platform.TIKTOK, "TT").otherwise("Other")

    assert_type(result, str)
    assert result == "Other"


def test_enum_match__returns_class_without_instantiation() -> None:
    platform: Platform = Platform.INSTAGRAM

    result = (
        match(platform)
        .case(Platform.INSTAGRAM, InstagramManager)
        .case(Platform.TIKTOK, TiktokManager)
        .case(Platform.YOUTUBE, YoutubeManager)
        .exhaustive()
    )

    assert result is InstagramManager
    assert not isinstance(result, InstagramManager)


def test_enum_match__no_eval_exhaustive() -> None:
    platform: Platform = Platform.INSTAGRAM

    result = (
        match(platform)
        .case(Platform.INSTAGRAM, lambda: "IG")
        .case(Platform.TIKTOK, lambda: "TT")
        .case(Platform.YOUTUBE, lambda: "YT")
        .exhaustive(eval=False)
    )

    # Should return the lambda function itself, not its result
    assert callable(result)
    assert result() == "IG"


def test_enum_match__no_eval_otherwise() -> None:
    platform: Platform = Platform.YOUTUBE

    result = (
        match(platform)
        .case(Platform.INSTAGRAM, lambda: "IG")
        .case(Platform.TIKTOK, lambda: "TT")
        .otherwise(lambda: "Other", eval=False)
    )

    # Should return the default lambda function itself
    assert callable(result)
    assert result() == "Other"
