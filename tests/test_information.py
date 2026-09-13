from __future__ import annotations

from shikumi import (
    Cardinality,
    InformationType,
    Shikumi,
    attach_information,
    clear_information,
    information_of,
)


def test_information_types_are_identity_based() -> None:
    left = InformationType("title", str)
    right = InformationType("title", str)

    assert left is not right
    assert left != right


def test_information_is_independent_of_shikumi() -> None:
    title = InformationType("title", str)

    class Page:
        pass

    try:
        record = attach_information(Page, title, "Overview")

        assert information_of(Page) == (record,)
        assert record.subject is Page
        assert record.type is title
        assert record.value == "Overview"
    finally:
        clear_information(Page)


def test_shikumi_only_observes_recognized_information_types() -> None:
    title = InformationType("title", str)
    hidden = InformationType("hidden", bool)

    class Page:
        pass

    try:
        attach_information(Page, title, "Overview")
        attach_information(Page, hidden, True)

        view = Shikumi(information_types=[title]).view(Page)

        assert view.focused.values(title) == ("Overview",)
        assert view.focused.values(hidden) == ()
    finally:
        clear_information(Page)


def test_information_type_exposes_declared_semantics_without_enforcing_them() -> None:
    tags = InformationType("tag", str, cardinality=Cardinality.MANY)

    assert tags.cardinality is Cardinality.MANY
    assert tags.accepts("python")
    assert not tags.accepts(1)


def test_information_registry_is_identity_based_even_for_equal_subjects() -> None:
    class EqualSubject:
        def __init__(self, key: str) -> None:
            self.key = key

        def __eq__(self, other: object) -> bool:
            return isinstance(other, EqualSubject) and self.key == other.key

        def __hash__(self) -> int:
            return hash(self.key)

    title = InformationType("title", str)
    left = EqualSubject("same")
    right = EqualSubject("same")

    try:
        attach_information(left, title, "left")
        attach_information(right, title, "right")

        assert [record.value for record in information_of(left)] == ["left"]
        assert [record.value for record in information_of(right)] == ["right"]
        assert information_of(left)[0].subject is left
        assert information_of(right)[0].subject is right
    finally:
        clear_information(left)
        clear_information(right)


def test_information_registry_does_not_keep_subject_alive() -> None:
    import gc
    import weakref

    title = InformationType("title", str)

    def attach_temporary_subject():
        class Temporary:
            pass

        subject_ref = weakref.ref(Temporary)
        attach_information(Temporary, title, "temporary")
        return subject_ref

    subject_ref = attach_temporary_subject()
    gc.collect()

    assert subject_ref() is None


def test_information_registry_accepts_weakrefable_unhashable_subjects() -> None:
    class UnhashableSubject:
        __hash__ = None

    title = InformationType("title", str)
    subject = UnhashableSubject()

    try:
        attach_information(subject, title, "value")
        assert information_of(subject)[0].value == "value"
    finally:
        clear_information(subject)


def test_information_type_rejects_invalid_constructor_values() -> None:
    import pytest

    with pytest.raises(TypeError, match="name must be a string"):
        InformationType(1, str)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="value_type"):
        InformationType("title", "str")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="value_type"):
        InformationType("title", (str, "int"))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must not be empty"):
        InformationType("title", ())
    from typing import Any

    with pytest.raises(TypeError, match="usable with isinstance"):
        InformationType("title", Any)
    with pytest.raises(TypeError, match="cardinality"):
        InformationType("title", str, cardinality="one")  # type: ignore[arg-type]
