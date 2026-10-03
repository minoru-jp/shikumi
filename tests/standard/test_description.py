from __future__ import annotations

import pytest

from shikumi import (
    InformationType,
    Shikumi,
    clear_descriptor_uses,
    clear_information,
    descriptor_uses_of,
    information_of,
)
from shikumi.standard import assignment, content_type, decorator, docstring


def _defined_class(source: str, **names: object) -> type[object]:
    namespace: dict[str, object] = {"__name__": "tests.standard.description", **names}
    exec(compile(source, "<standard-description-test>", "exec"), namespace)  # noqa: S102 - trusted in-test source is executed intentionally
    return namespace["Page"]  # type: ignore[return-value]


def test_assignment_writer_connects_value_as_information() -> None:
    title_type = InformationType("title", str)
    title = assignment(title_type)
    Page = _defined_class(
        'class Page:\n    title @= "Overview"\n',
        title=title,
    )

    try:
        records = information_of(Page)
        assert len(records) == 1
        assert records[0].type is title_type
        assert records[0].value == "Overview"
        assert descriptor_uses_of(Page)[0].descriptor is title
        assert "title" not in Page.__dict__
    finally:
        clear_information(Page)
        clear_descriptor_uses(Page)


def test_assignment_writer_supports_multiple_writes() -> None:
    tag_type = InformationType("tag", str)
    tag = assignment(tag_type)
    Page = _defined_class(
        'class Page:\n    tag @= "python"\n    tag @= "runtime"\n',
        tag=tag,
    )

    try:
        assert tuple(record.value for record in information_of(Page)) == (
            "python",
            "runtime",
        )
    finally:
        clear_information(Page)


def test_decorator_writer_connects_the_same_information_model() -> None:
    title_type = InformationType("title", str)
    title = decorator(title_type)

    @title("Overview")
    class Page:
        pass

    try:
        record = information_of(Page)[0]
        assert record.type is title_type
        assert record.value == "Overview"
        assert descriptor_uses_of(Page)[0].descriptor is title
    finally:
        clear_information(Page)
        clear_descriptor_uses(Page)


def test_standard_writers_can_write_the_same_information_type() -> None:
    title_type = InformationType("title", str)
    title_assignment = assignment(title_type)
    title_decorator = decorator(title_type)
    AssignmentPage = _defined_class(
        'class Page:\n    title_assignment @= "Assignment"\n',
        title_assignment=title_assignment,
    )

    @title_decorator("Decorator")
    class DecoratorPage:
        pass

    try:
        shikumi = Shikumi(information_types=[title_type])
        assert shikumi.view(AssignmentPage).focused.values(title_type) == (
            "Assignment",
        )
        assert shikumi.view(DecoratorPage).focused.values(title_type) == ("Decorator",)
    finally:
        clear_information(AssignmentPage)
        clear_information(DecoratorPage)


def test_docstring_writer_turns_runtime_docstring_into_information() -> None:
    Content = content_type()
    content = docstring(Content)

    @content
    class Page:
        """
        First line.

        Second line.
        """

    try:
        records = information_of(Page)
        assert len(records) == 1
        assert records[0].type is Content
        assert records[0].value == "First line.\n\nSecond line."
        assert descriptor_uses_of(Page)[0].descriptor is content
        assert Shikumi(information_types=[Content]).view(Page).focused.values(
            Content
        ) == ("First line.\n\nSecond line.",)
    finally:
        clear_information(Page)
        clear_descriptor_uses(Page)


def test_docstring_writer_does_not_attach_missing_optional_docstring() -> None:
    Content = content_type()
    content = docstring(Content)

    @content
    class Page:
        __doc__ = None

    assert information_of(Page) == ()


def test_required_docstring_writer_rejects_missing_docstring() -> None:
    Content = content_type()
    content = docstring(Content, required=True)

    with pytest.raises(ValueError, match="requires a docstring"):

        @content
        class Page:
            __doc__ = None


def test_docstring_writer_requires_string_compatible_information_type() -> None:
    Count = InformationType("count", int)

    with pytest.raises(TypeError, match="accepting str"):
        docstring(Count)


def test_standard_assignment_records_descriptor_use() -> None:
    kind_type = InformationType("kind", str)
    kind = assignment(kind_type)

    namespace = {"kind": kind, "__name__": "tests.standard.descriptor_assignment"}
    exec(  # noqa: S102 - trusted in-test source is executed intentionally
        compile('class Page:\n    kind @= "page"\n', "<descriptor-assignment>", "exec"),
        namespace,
    )
    Page = namespace["Page"]

    try:
        uses = descriptor_uses_of(Page)
        assert len(uses) == 1
        assert uses[0].descriptor is kind
    finally:
        clear_information(Page)
        clear_descriptor_uses(Page)


def test_standard_docstring_records_use_even_without_information() -> None:
    content_type = InformationType("content", str)
    writer = docstring(content_type)

    @writer
    class Page:
        __doc__ = None

    try:
        assert information_of(Page) == ()
        uses = descriptor_uses_of(Page)
        assert len(uses) == 1
        assert uses[0].descriptor is writer
    finally:
        clear_information(Page)
        clear_descriptor_uses(Page)
