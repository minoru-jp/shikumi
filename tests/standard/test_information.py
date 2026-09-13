from __future__ import annotations

from shikumi import Cardinality
from shikumi.standard import content_type


def test_content_type_is_single_valued_string_information() -> None:
    Content = content_type()

    assert Content.name == "content"
    assert Content.value_type is str
    assert Content.cardinality is Cardinality.ONE
