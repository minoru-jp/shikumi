"""Canonical Japanese API reference source for Semantic View API."""

from shikumi_devdoc.fields.api_reference import (
    OPERATION,
    TYPE,
    VALUE,
    input,
    kind,
    name,
    output,
    related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title

from devdocs.canonical_sources.docs.specification.core import (
    SPECIFICATION_PART as CORE_SPEC,
)
from devdocs.canonical_sources.docs.vocabulary import TERMS

query_example = test_target_field("semantic view query example")


@summary("意味像と ViewItem の公開 API。")
@canonical_source(
    "Semantic View API", filename="semantic-view.md", order=30, heading="title"
)
class API_REFERENCE_PART:
    """Shikumi が構成した SemanticView と ViewItem を読み取る公開 API。"""

    related @= CORE_SPEC

    class TITLE_34:
        r""  # noqa: D419 - heading-only canonical node

        title @= "{{TERM_19}}"

        merge @= TERMS.TERM_19

        class TITLE_35:
            r"""
            ```python
            @dataclass(frozen=True)
            class ViewItem:
                node: StructureNode
                information: tuple[Information[Any], ...]
                descriptor_uses: tuple[DescriptorUse, ...] = ()
            ```

            {{TERM_19}}に含まれる一つの{{TERM_6}}を表す。
            """

            title @= "`ViewItem`"
            name @= "ViewItem"
            kind @= TYPE

            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_6

            class TITLE_36:
                r"""
                ```python
                @property
                def subject(self) -> object
                ```

                `node.subject` を返す。
                """

                title @= "`subject`"
                name @= "subject"
                kind @= VALUE

            class TITLE_37:
                r"""
                ```python
                @property
                def kind(self) -> StructuralKind
                ```

                `node.kind` を返す。
                """

                title @= "`kind`"
                name @= "kind"
                kind @= VALUE

            class TITLE_38:
                r"""
                ```python
                def records(
                    self,
                    information_type: InformationType[T],
                ) -> tuple[Information[T], ...]
                ```

                指定した{{TERM_12}}の{{TERM_13}}を identity によって選別して返す。
                """

                title @= "`records(information_type)`"
                name @= "records(information_type)"
                kind @= OPERATION
                input @= "information_type: InformationType[T]"
                output @= "tuple[Information[T], ...]"

                merge @= TERMS.TERM_12
                merge @= TERMS.TERM_13

            class TITLE_39:
                r"""
                ```python
                def values(
                    self,
                    information_type: InformationType[T],
                ) -> tuple[T, ...]
                ```

                指定した{{TERM_12}}の値を接続順に返す。

                単一値の{{TERM_12}}であっても、{{TERM_21}}前には複数値が存在し得るため、常に tuple を返す。

                `InformationType[T]` の型変数は `records()` / `values()` まで伝播する。例えば `Title = InformationType("title", str)` を静的型検査器が `InformationType[str]` と解釈した場合、`item.values(Title)` は `tuple[str, ...]` になる。{{TERM_1}} は `py.typed` を配布し、この Core の{{TERM_12}}から取得までの型関係を公開契約に含める。

                複数の Python 型を `value_type=(str, int)` のように指定する場合は、現段階では型変数を精密な union として導出することを保証しない。また、Standard の `assignment()` / `decorator()` や任意の独自{{TERM_15}}へ `T` を完全に伝播させることも、この第一段階の契約には含めない。{{TERM_15}}の runtime 上の自由度を保ち、型付けのためだけに{{TERM_15}} API を複雑化しない。
                """

                title @= "`values(information_type)`"
                name @= "values(information_type)"
                kind @= OPERATION
                input @= "information_type: InformationType[T]"
                output @= "tuple[T, ...]"

                merge @= TERMS.TERM_12
                merge @= TERMS.TERM_21
                merge @= TERMS.TERM_1
                merge @= TERMS.TERM_15

            class TITLE_40:
                r"""
                ```python
                def has(self, information_type: InformationType[T]) -> bool
                ```

                指定した{{TERM_12}}の{{TERM_13}}を一件以上持つかを返す。
                """

                title @= "`has(information_type)`"
                name @= "has(information_type)"
                kind @= OPERATION
                input @= "information_type: InformationType[Any]"
                output @= "bool"

                merge @= TERMS.TERM_12
                merge @= TERMS.TERM_13

            class TITLE_41:
                r"""
                ```python
                def uses(self, descriptor: object) -> tuple[DescriptorUse, ...]
                ```

                この対象へ記録された、指定{{TERM_15}}による使用を返す。bound method は同じ bound instance と underlying function によって照合する。
                """

                title @= "`uses(descriptor)`"
                name @= "uses(descriptor)"
                kind @= OPERATION
                input @= "descriptor: object"
                output @= "tuple[DescriptorUse, ...]"

                merge @= TERMS.TERM_15

        class TITLE_42:
            r"""
            ```python
            @dataclass(frozen=True)
            class SemanticView:
                focus: Focus
                structure: ResolvedStructure
                items: tuple[ViewItem, ...]
            ```

            一つの{{TERM_20}}について構成された{{TERM_19}}。

            ```python
            {{query_example}}
            ```
            """

            title @= "`SemanticView`"
            query_example @= r"""
            from shikumi import InformationType, Shikumi, UnknownViewSubjectError, attach_information

            Title = InformationType("title", str)

            class Page:
                pass

            attach_information(Page, Title, "Overview")
            view = Shikumi(information_types=[Title]).view(Page)

            assert view.focused.values(Title) == ("Overview",)
            assert view.focused.has(Title)
            assert view.item(Page) is view.focused
            assert view.subview(Page) is view

            class Other:
                pass

            try:
                view.item(Other)
            except UnknownViewSubjectError:
                pass
            else:
                raise AssertionError("unknown subjects must be rejected")
            """

            related @= CORE_SPEC.CORE_008

            name @= "SemanticView"
            kind @= TYPE

            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_19

            class TITLE_43:
                r"""
                ```python
                @property
                def focused(self) -> ViewItem
                ```

                {{TERM_20}}そのものに対応する `ViewItem` を返す。
                """

                title @= "`focused`"
                name @= "focused"
                kind @= VALUE

                merge @= TERMS.TERM_20

            class TITLE_44:
                r"""
                ```python
                @property
                def entities(self) -> tuple[ViewItem, ...]
                ```

                {{TERM_11}}に対応する項目を返す。
                """

                title @= "`entities`"
                name @= "entities"
                kind @= VALUE

                merge @= TERMS.TERM_11

            class TITLE_45:
                r"""
                ```python
                @property
                def modules(self) -> tuple[ViewItem, ...]
                ```

                module に対応する項目を返す。
                """

                title @= "`modules`"
                name @= "modules"
                kind @= VALUE

            class TITLE_46:
                r"""
                ```python
                @property
                def packages(self) -> tuple[ViewItem, ...]
                ```

                package に対応する項目を返す。
                """

                title @= "`packages`"
                name @= "packages"
                kind @= VALUE

            class TITLE_47:
                r"""
                ```python
                def item(self, subject: object) -> ViewItem
                ```

                identity が一致する対象の `ViewItem` を返す。{{TERM_19}}に存在しない場合は `UnknownViewSubjectError` を送出する。
                """

                title @= "`item(subject)`"
                name @= "item(subject)"
                kind @= OPERATION
                input @= "subject: object"
                output @= "ViewItem"

                merge @= TERMS.TERM_19

            class TITLE_48:
                r"""
                ```python
                def subview(self, subject: object) -> SemanticView
                ```

                この{{TERM_19}}にすでに含まれている対象を新しい{{TERM_20}}とし、その{{TERM_7}}上の subtree から部分{{TERM_19}}を返す。元の `ResolvedStructure`、{{TERM_13}}、{{TERM_16}}を再利用し、Python runtime を再{{TERM_18}}しない。元の{{TERM_20}}自身を指定した場合は同じ `SemanticView` を返す。{{TERM_19}}に存在しない対象では `UnknownViewSubjectError` を送出する。

                `SemanticView` は iterable であり、`items` の順序で `ViewItem` を反復する。

                ---
                """

                title @= "`subview(subject)`"
                related @= CORE_SPEC.CORE_008

                name @= "subview(subject)"
                kind @= OPERATION
                input @= "subject: object"
                output @= "SemanticView"

                merge @= TERMS.TERM_19
                merge @= TERMS.TERM_20
                merge @= TERMS.TERM_7
                merge @= TERMS.TERM_13
                merge @= TERMS.TERM_16
                merge @= TERMS.TERM_18
