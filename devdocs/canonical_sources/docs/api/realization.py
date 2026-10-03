"""Canonical Japanese API reference source for Realization API."""

from shikumi_devdoc.fields.api_reference import (
    TYPE,
    VALUE,
    kind,
    name,
    related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title

from devdocs.canonical_sources.docs.specification.realization import (
    SPECIFICATION_PART as REALIZATION_SPEC,
)
from devdocs.canonical_sources.docs.vocabulary import TERMS

realizer_example = test_target_field("realizer example")


@summary("Realizer と realization check の公開 API。")
@canonical_source(
    "Realization API", filename="realization.md", order=60, heading="title"
)
class API_REFERENCE_PART:
    """SemanticView から成果物を生成する独立 Realizer の公開 API。"""

    related @= REALIZATION_SPEC

    class TITLE_64:
        r""  # noqa: D419 - heading-only canonical node

        title @= "{{TERM_25}}"

        merge @= TERMS.TERM_25

        class TITLE_65:
            r"""
            ```python
            @dataclass(frozen=True)
            class RealizationCheck:
                view: SemanticView
                diagnostics: tuple[Diagnostic, ...] = ()
            ```

            {{TERM_28}}を生成せずに、特定の{{TERM_26}}が{{TERM_19}}を{{TERM_25}}可能か問い合わせた結果。`is_realizable` は error 診断がない場合に `True`。{{TERM_2}}への適合性とは独立している。
            """

            title @= "`RealizationCheck`"
            related @= REALIZATION_SPEC.REAL_003
            related @= REALIZATION_SPEC.REAL_006

            name @= "RealizationCheck"
            kind @= TYPE

            merge @= TERMS.TERM_28
            merge @= TERMS.TERM_26
            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_25
            merge @= TERMS.TERM_2

            class TITLE_65A:
                r"""
                ```python
                @property
                def is_realizable(self) -> bool
                ```

                `ERROR` severity の `Diagnostic` が一件もない場合に `True`。`bool(check)` は `check.is_realizable` と同じ意味を持つ。
                """

                title @= "`is_realizable`"
                related @= REALIZATION_SPEC.REAL_003
                name @= "is_realizable"
                kind @= VALUE

        class TITLE_66:
            r"""
            ```python
            class Realizer(ABC, Generic[ArtifactT]):
                def check(self, view: SemanticView) -> RealizationCheck:
                    ...

                @abstractmethod
                def realize(self, view: SemanticView) -> ArtifactT:
                    ...
            ```

            {{TERM_19}}から{{TERM_28}}を生成するための抽象基底。`check()` は{{TERM_28}}を生成せず、与えられた{{TERM_19}}を{{TERM_25}}可能か問い合わせる。{{TERM_25}}条件を持つ{{TERM_26}}は `check()` を override し、満たされない条件を `Diagnostic` として返す。既定実装は追加の{{TERM_25}}条件なしとして扱う。

            {{TERM_26}}は {{TERM_1}} を所有せず、{{TERM_1}} からも所有されない。同じ{{TERM_19}}に複数の{{TERM_26}}を適用できる。

            ```python
            {{realizer_example}}
            ```
            {{TERM_28}}の型は {{TERM_1}} によって制限しない。

            ---
            """

            title @= "`Realizer`"
            realizer_example @= r"""
            from shikumi import InformationType, Realizer, Shikumi, attach_information

            Title = InformationType("title", str)

            class MarkdownTitle(Realizer[str]):
                def realize(self, view):
                    return f"# {view.focused.values(Title)[0]}\n"

            class DictTitle(Realizer[dict[str, str]]):
                def realize(self, view):
                    return {"title": view.focused.values(Title)[0]}

            class Page:
                pass

            attach_information(Page, Title, "Overview")
            view = Shikumi(information_types=[Title]).view(Page)

            markdown = MarkdownTitle()
            data = DictTitle()
            assert markdown.check(view).is_realizable
            assert markdown.realize(view) == "# Overview\n"
            assert data.realize(view) == {"title": "Overview"}
            """

            related @= REALIZATION_SPEC.REAL_001
            related @= REALIZATION_SPEC.REAL_002
            related @= REALIZATION_SPEC.REAL_004

            name @= "Realizer"
            kind @= TYPE

            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_28
            merge @= TERMS.TERM_25
            merge @= TERMS.TERM_26
            merge @= TERMS.TERM_1
