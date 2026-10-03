from __future__ import annotations

import sys

import pytest

from shikumi import (
    ClassBinding,
    InformationType,
    Shikumi,
    attach_information,
    class_binding,
    clear_descriptor_uses,
    clear_information,
    descriptor_uses_of,
    information_of,
    record_descriptor_use,
)


def _defined_class(source: str, **names: object) -> type[object]:
    namespace: dict[str, object] = {"__name__": "tests.description", **names}
    exec(compile(source, "<description-test>", "exec"), namespace)  # noqa: S102 - trusted in-test source is executed intentionally
    return namespace["Page"]  # type: ignore[return-value]


def test_class_binding_connects_before_init_subclass_without_consuming_writer() -> None:
    title_type = InformationType("title", str)
    observed: list[tuple[str, type[object], object | None]] = []

    class Base:
        def __init_subclass__(cls) -> None:
            observed.append(("init_subclass", cls, None))
            super().__init_subclass__()

    class TitleDescriptions:
        def __imatmul__(self, value: object) -> ClassBinding[object]:
            return class_binding(value, self._connect)

        def _connect(self, subject: type[object], value: object) -> None:
            observed.append(("connect", subject, value))
            record_descriptor_use(subject, self)
            attach_information(subject, title_type, value)

    title = TitleDescriptions()
    FirstPage = _defined_class(
        'class Page(Base):\n    title @= "Overview"\n',
        Base=Base,
        title=title,
    )
    SecondPage = _defined_class(
        'class Page(Base):\n    title @= "Details"\n',
        Base=Base,
        title=title,
    )

    try:
        assert observed == [
            ("connect", FirstPage, "Overview"),
            ("init_subclass", FirstPage, None),
            ("connect", SecondPage, "Details"),
            ("init_subclass", SecondPage, None),
        ]
        assert "title" not in FirstPage.__dict__
        assert "title" not in SecondPage.__dict__
        first_record = information_of(FirstPage)[0]
        second_record = information_of(SecondPage)[0]
        assert first_record.type is title_type
        assert first_record.value == "Overview"
        assert second_record.type is title_type
        assert second_record.value == "Details"
        assert descriptor_uses_of(FirstPage)[0].descriptor is title
        assert descriptor_uses_of(SecondPage)[0].descriptor is title
    finally:
        clear_information(FirstPage)
        clear_information(SecondPage)
        clear_descriptor_uses(FirstPage)
        clear_descriptor_uses(SecondPage)


def test_class_binding_supports_repeated_at_equals_without_interpreting_values() -> (
    None
):
    payloads: list[object] = []

    class PayloadDescriptions:
        def __imatmul__(self, value: object) -> ClassBinding[object]:
            return class_binding(value, self._connect)

        @staticmethod
        def _connect(subject: type[object], value: object) -> None:
            payloads.append(value)

    first = object()
    second = object()
    payload = PayloadDescriptions()
    Page = _defined_class(
        "class Page:\n    payload @= first\n    payload @= second\n",
        payload=payload,
        first=first,
        second=second,
    )

    assert payloads == [first, second]
    assert "payload" not in Page.__dict__


def test_custom_at_equals_writer_can_choose_information_connection() -> None:
    left_type = InformationType("left", str)
    right_type = InformationType("right", str)

    class PairDescriptions:
        def __imatmul__(self, value: tuple[str, str]) -> ClassBinding[tuple[str, str]]:
            return class_binding(value, self._connect)

        @staticmethod
        def _connect(subject: type[object], value: tuple[str, str]) -> None:
            left, right = value
            attach_information(subject, left_type, left)
            attach_information(subject, right_type, right)

    pair = PairDescriptions()
    Page = _defined_class(
        'class Page:\n    pair @= ("L", "R")\n',
        pair=pair,
    )

    try:
        view = Shikumi(information_types=[left_type, right_type]).view(Page)
        assert view.focused.values(left_type) == ("L",)
        assert view.focused.values(right_type) == ("R",)
    finally:
        clear_information(Page)


def test_class_binding_connect_exception_follows_python_class_creation_semantics() -> (
    None
):
    def fail(subject: type[object], value: str) -> None:
        raise ValueError(value)

    def define_page() -> type[object]:
        return _defined_class(
            'class Page:\n    field = class_binding("boom", fail)\n',
            class_binding=class_binding,
            fail=fail,
        )

    if sys.version_info < (3, 12):
        with pytest.raises(RuntimeError) as caught:
            define_page()
        assert isinstance(caught.value.__cause__, ValueError)
        assert str(caught.value.__cause__) == "boom"
    else:
        with pytest.raises(ValueError, match="boom") as caught:
            define_page()
        notes = getattr(caught.value, "__notes__", ())
        assert any("Error calling __set_name__" in note for note in notes)


def test_class_binding_requires_callable_connector() -> None:
    try:
        class_binding("value", None)  # type: ignore[arg-type]
    except TypeError as exc:
        assert str(exc) == "connect must be callable"
    else:
        raise AssertionError("class_binding accepted a non-callable connector")


def test_plain_python_marker_decorator_can_connect_information_directly() -> None:
    kind_type = InformationType("kind", str)

    class KindDescriptions:
        def attr(self, subject):
            """Attribute-like entity."""
            record_descriptor_use(subject, self.attr)
            attach_information(subject, kind_type, "attr")
            return subject

    kind = KindDescriptions()

    @kind.attr
    class Field:
        pass

    try:
        assert Shikumi(information_types=[kind_type]).view(Field).focused.values(
            kind_type
        ) == ("attr",)
    finally:
        clear_information(Field)
        clear_descriptor_uses(Field)


def test_plain_python_value_decorator_can_choose_its_own_arguments() -> None:
    uses_type = InformationType("uses", type)

    class RelationDescriptions:
        def uses(self, target: type[object]):
            """Relation to a used entity."""

            def decorate(subject):
                record_descriptor_use(subject, self.uses)
                attach_information(subject, uses_type, target)
                return subject

            return decorate

    relation = RelationDescriptions()

    class Repository:
        pass

    @relation.uses(Repository)
    class Service:
        pass

    try:
        assert Shikumi(information_types=[uses_type]).view(Service).focused.values(
            uses_type
        ) == (Repository,)
    finally:
        clear_information(Service)
        clear_descriptor_uses(Service)
