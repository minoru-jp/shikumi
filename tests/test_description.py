from __future__ import annotations

from shikumi import (
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


def test_class_binding_connects_after_class_creation() -> None:
    title_type = InformationType("title", str)
    observed: list[tuple[type[object], object]] = []

    class TitleDescriptions:
        def __imatmul__(self, value: object) -> object:
            return class_binding(value, self._connect)

        def _connect(self, subject: type[object], value: object) -> None:
            observed.append((subject, value))
            record_descriptor_use(subject, self)
            attach_information(subject, title_type, value)

    title = TitleDescriptions()
    Page = _defined_class(
        'class Page:\n    title @= "Overview"\n',
        title=title,
    )

    try:
        assert observed == [(Page, "Overview")]
        assert "title" not in Page.__dict__
        record = information_of(Page)[0]
        assert record.type is title_type
        assert record.value == "Overview"
        assert descriptor_uses_of(Page)[0].descriptor is title
    finally:
        clear_information(Page)
        clear_descriptor_uses(Page)


def test_class_binding_supports_repeated_at_equals_without_interpreting_values() -> (
    None
):
    payloads: list[object] = []

    class PayloadDescriptions:
        def __imatmul__(self, value: object) -> object:
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
        def __imatmul__(self, value: tuple[str, str]) -> object:
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
