"""Canonical Japanese API reference source for Descriptor API."""

from shikumi_devdoc.fields.api_reference import (
    OPERATION,
    TYPE,
    input,
    kind,
    name,
    output,
    related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title

from devdocs.canonical_sources.docs.specification.description import (
    SPECIFICATION_PART as DESCRIPTION_SPEC,
)
from devdocs.canonical_sources.docs.specification.validation import (
    SPECIFICATION_PART as VALIDATION_SPEC,
)
from devdocs.canonical_sources.docs.vocabulary import TERMS

class_binding_example = test_target_field("class binding example")


@summary("記述器使用、構造上の使用規則、class binding の公開 API。")
@canonical_source(
    "Descriptor API", filename="descriptors.md", order=10, heading="title"
)
class API_REFERENCE_PART:
    """記述器使用の記録、構造上の使用規則、class 成立後の binding を扱う。"""

    related @= DESCRIPTION_SPEC

    class TITLE_13:
        r""  # noqa: D419 - heading-only canonical node

        title @= "{{TERM_16}}"

        merge @= TERMS.TERM_16

        class TITLE_14:
            r"""
            ```python
            @dataclass(frozen=True)
            class DescriptorUse:
                descriptor: object
                subject: object
            ```

            ある{{TERM_15}}がある実行時対象に使用されたという事実を表す。{{TERM_14}}とは独立しており、一回の{{TERM_16}}がゼロ件、一件、複数件の{{TERM_14}}を行ってよい。
            """

            title @= "`DescriptorUse`"
            related @= DESCRIPTION_SPEC.DESC_003

            name @= "DescriptorUse"
            kind @= TYPE

            merge @= TERMS.TERM_15
            merge @= TERMS.TERM_14
            merge @= TERMS.TERM_16

        class TITLE_15:
            r"""
            ```python
            def record_descriptor_use(
                subject: object,
                descriptor: object,
            ) -> DescriptorUse
            ```

            `descriptor` が `subject` に使用されたことを記録する低水準 API。{{TERM_15}}の import 元やソース上の名称は追跡せず、渡された Python object を実行時 identity として扱う。bound method は同じ instance と underlying function の組として照合されるため、`writer.describe` を属性アクセスし直しても同じ{{TERM_15}}として判定できる。
            """

            title @= "`record_descriptor_use()`"
            name @= "record_descriptor_use()"
            kind @= OPERATION
            input @= "subject: object"
            input @= "descriptor: object"
            output @= "DescriptorUse"

            merge @= TERMS.TERM_15

        class TITLE_16:
            r"""
            {{TERM_16}} registry は{{TERM_13}} registry と同様に、対象の `__eq__` / `__hash__` ではなく runtime identity で管理する。内部記録は対象を直接保持せず、取得時に公開 `DescriptorUse` を組み立てるため、registry 自体は対象を直接強参照しない。ただし、記録された `descriptor` 自身、またはそこから到達可能な Python object が対象を参照している場合、その参照によって対象の寿命が延びることがある。たとえば instance の bound method は通常その instance を保持する。{{TERM_1}} は{{TERM_15}}自身の参照関係を弱参照化したり切断したりしない。
            """

            title @= "記述器使用 registry"

            merge @= TERMS.TERM_16
            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_15

            class TITLE_16A:
                r"""
                ```python
                def descriptor_uses_of(subject: object) -> tuple[DescriptorUse, ...]
                ```

                対象へ直接記録された{{TERM_16}}を使用順に返す。
                """

                title @= "`descriptor_uses_of()`"
                name @= "descriptor_uses_of()"
                kind @= OPERATION
                input @= "subject: object"
                output @= "tuple[DescriptorUse, ...]"

                merge @= TERMS.TERM_16

            class TITLE_16B:
                r"""
                ```python
                def clear_descriptor_uses(subject: object) -> None
                ```

                対象へ直接記録された{{TERM_16}}を削除する。主にテストや実行時ライフサイクル管理のための API である。
                """

                title @= "`clear_descriptor_uses()`"
                name @= "clear_descriptor_uses()"
                kind @= OPERATION
                input @= "subject: object"
                output @= "None"

                merge @= TERMS.TERM_16

        class TITLE_17:
            r"""
            ```python
            StructureSelector(
                *,
                kind: StructuralKind | None = None,
                at: tuple[str, ...] | None = None,
                under: tuple[str, ...] | None = None,
            )
            ```

            {{TERM_17}}が対象とする{{TERM_7}}上の位置を選択する。`kind` は{{TERM_7}}種別、`at` は一つの有効 path との完全一致、`under` は指定 path 自身を含むその配下を表す。`at` と `under` は同時に指定できない。何も指定しない selector はすべての位置に一致する。複数の候補位置を許可する場合は `StructureSelector.one_of(a, b, ...)` または `a | b` で selector を OR 合成できる。
            """

            title @= "`StructureSelector`"
            name @= "StructureSelector"
            kind @= TYPE

            merge @= TERMS.TERM_17
            merge @= TERMS.TERM_7

            class TITLE_18:
                r"""
                ```python
                @classmethod
                def one_of(
                    cls,
                    *selectors: StructureSelector,
                ) -> StructureSelector
                ```

                複数の selector のいずれかに一致する selector を返す。`a | b` は `StructureSelector.one_of(a, b)` と同じ意味を持つ。

                path は{{TERM_8}}と同じ{{TERM_2}}ルート基準で評価する。package 全体を{{TERM_20}}にした場合は package 自身をルート `()` とし、単独 module に `placement` を指定した場合はその予定配置を有効 path として用いる。
                """

                title @= "`one_of()` / `|`"
                name @= "one_of()"
                kind @= OPERATION
                input @= "*selectors: StructureSelector"
                output @= "StructureSelector"

                merge @= TERMS.TERM_8
                merge @= TERMS.TERM_2
                merge @= TERMS.TERM_20

        class TITLE_19:
            r"""
            ```python
            DescriptorUseRule(
                descriptor: object,
                allowed: StructureSelector,
                recommended: StructureSelector | None = None,
                name: str | None = None,
            )
            ```

            一つの{{TERM_15}}を{{TERM_7}}上のどこで使用可能または推奨とするかを定める。`allowed` に一致しない使用は error、`allowed` には一致するが `recommended` に一致しない使用は warning となる。`recommended=None` の場合、許可範囲内の位置をすべて同等に扱う。

            規則が存在しない{{TERM_15}}は、この仕組みによる{{TERM_7}}上の制約を受けない。{{TERM_12}}、{{TERM_13}}値、import 元などから暗黙の使用範囲を推論しない。
            """

            title @= "`DescriptorUseRule`"
            related @= VALIDATION_SPEC.VAL_003

            name @= "DescriptorUseRule"
            kind @= TYPE

            merge @= TERMS.TERM_15
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_13

    class TITLE_20:
        r""  # noqa: D419 - heading-only canonical node

        title @= "`@=` 用のクラス接続"

        class TITLE_21:
            r"""
            ```python
            def class_binding(
                value: T,
                connect: Callable[[type, T], None],
            ) -> object
            ```

            クラス本体の実行中にはまだ存在しないクラス{{TERM_11}}に対して、クラス成立後に処理を適用するための低水準 API。

            `@=` を用いる独自{{TERM_15}}の著者が利用する。{{TERM_1}} は `value` の型や意味を{{TERM_18}}せず、クラス成立後に `connect(subject, value)` を呼び出すことだけを保証する。

            返されたオブジェクトは、同じ名前に対する連続した `@=` を受け取れる。

            ```python
            {{class_binding_example}}
            ```
            `class_binding()` はクラス成立後の処理タイミングを提供するだけであり、{{TERM_16}}の記録や{{TERM_14}}そのものを強制しない。{{TERM_1}} の{{TERM_15}}として利用する場合、必要に応じて `connect` から `record_descriptor_use()` と `attach_information()` をそれぞれ呼び出す。

            `class_binding()` の内部実装方法は公開契約に含めない。

            ---
            """

            title @= "`class_binding()`"
            class_binding_example @= r"""
            from shikumi import (
                InformationType,
                attach_information,
                class_binding,
                descriptor_uses_of,
                information_of,
                record_descriptor_use,
            )

            Tag = InformationType("tag", str)

            class Tags:
                def __init__(self, information_type: InformationType) -> None:
                    self.information_type = information_type

                def __imatmul__(self, value: str):
                    return class_binding(value, self._connect)

                def _connect(self, subject: type, value: str) -> None:
                    record_descriptor_use(subject, self)
                    attach_information(subject, self.information_type, value)

            tags = Tags(Tag)

            class Page:
                tags @= "python"
                tags @= "runtime"

            assert tuple(record.value for record in information_of(Page)) == (
                "python",
                "runtime",
            )
            assert len(descriptor_uses_of(Page)) == 2
            """

            related @= DESCRIPTION_SPEC.DESC_006

            name @= "class_binding()"
            kind @= OPERATION
            input @= "value: T"
            input @= "connect: Callable[[type[object], T], None]"
            output @= "object"

            merge @= TERMS.TERM_11
            merge @= TERMS.TERM_15
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_16
            merge @= TERMS.TERM_14
