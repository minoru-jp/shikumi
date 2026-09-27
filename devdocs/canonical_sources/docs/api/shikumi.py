"""Canonical Japanese API reference source for Shikumi API."""

from devdocs.canonical_sources.docs.vocabulary import TERMS
from shikumi_devdoc.fields.api_reference import (
    NAMESPACE, OPERATION, OTHER, TYPE, VALUE,
    input, kind, name, output, related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title
from devdocs.canonical_sources.docs.specification.core import SPECIFICATION_PART as CORE_SPEC
from devdocs.canonical_sources.docs.specification.validation import SPECIFICATION_PART as VALIDATION_SPEC


composition_example = test_target_field("composition example")
@summary('Shikumi 本体の構成・解釈・検証 API。')
@canonical_source('Shikumi API', filename='shikumi.md', order=40, heading="title")
class API_REFERENCE_PART:
    """Shikumi インスタンスの構成、view、structure derivation、validation を扱う。"""

    related @= CORE_SPEC

    class TITLE_49:
        r'''
        '''
        title @= "{{TERM_1}}"

        merge @= TERMS.TERM_1

        class TITLE_50:
            r'''
            ```python
            {{TERM_1}}(
                *,
                structure: Structure | None = None,
                information_types: Iterable[InformationType[Any]] = (),
                validators: Iterable[ValidationRule] = (),
                descriptor_rules: Iterable[DescriptorUseRule] = (),
            )
            ```

            {{TERM_7}}、認識する{{TERM_12}}、{{TERM_22}}、{{TERM_17}}を一つの意味体系として構成する。

            `structure=None` の場合は `PythonStructure()` を使用する。明示的に指定する場合は `Structure` のインスタンスでなければならない。独自の{{TERM_7}}{{TERM_18}}は `Structure` を継承して実装できる。

            `information_types`、`validators`、`descriptor_rules` の各要素は、それぞれ `InformationType`、`ValidationRule`、`DescriptorUseRule` でなければならない。同一のオブジェクトを同じ {{TERM_1}} に重複登録してはならない。種類が異なる構成要素は constructor で `TypeError` とし、重複は `ValueError` とする。

            constructor が保証するのは、構成要素の種類と局所的な登録{{TERM_24}}までである。`Structure.resolve()` を試行したり、{{TERM_22}}同士の意味的整合性、{{TERM_17}}が実際の{{TERM_7}}で到達可能かといった意味的妥当性を事前評価したりはしない。これらは各構成要素の実行時の責務であり、独自拡張の表現力を constructor 検証のために狭めない。
            '''
            title @= '`Shikumi`'
            related @= CORE_SPEC.CORE_007

            name @= 'Shikumi'
            kind @= TYPE


            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_22
            merge @= TERMS.TERM_17
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_24

        class TITLE_51:
            r'''
            ```python
            def recognizes(self, information_type: InformationType[Any]) -> bool
            ```

            その{{TERM_12}}を identity によって認識するかを返す。
            '''
            title @= '`recognizes()`'
            name @= 'recognizes()'
            kind @= OPERATION
            input @= 'information_type: InformationType[Any]'
            output @= 'bool'


            merge @= TERMS.TERM_12

        class TITLE_52:
            r'''
            ```python
            def view(
                self,
                subject: object | Focus,
                *,
                placement: tuple[str, ...] | None = None,
            ) -> SemanticView
            ```

            対象を{{TERM_20}}として{{TERM_18}}し、{{TERM_19}}を返す。`placement` を指定すると、その位置を{{TERM_20}}の{{TERM_7}}上の配置として使用する。`Focus` 自体に配置が含まれる場合、method 引数として重ねて指定してはならない。

            {{TERM_19}}に取り込む{{TERM_13}}は、その {{TERM_1}} が `information_types` として認識するものだけである。対象へ接続されている未認識の{{TERM_13}}は削除されず、単にその{{TERM_19}}には現れない。{{TERM_16}}は{{TERM_12}}とは独立して{{TERM_19}}へ取り込まれ、`descriptor_rules` が必要な使用だけを{{TERM_7}}との関係で{{TERM_21}}する。

            ```python
            {{composition_example}}
            ```
            '''
            title @= '`view()`'
            composition_example @= r"""
            from shikumi import InformationType, Shikumi, attach_information

            Title = InformationType("title", str)
            InternalId = InformationType("internal-id", int)

            class Page:
                pass

            attach_information(Page, Title, "Overview")
            attach_information(Page, InternalId, 42)

            docs = Shikumi(information_types=[Title])
            assert docs.recognizes(Title)
            assert not docs.recognizes(InternalId)

            item = docs.view(Page).focused
            assert item.values(Title) == ("Overview",)
            assert not item.has(InternalId)
            """

            related @= CORE_SPEC.CORE_004
            related @= CORE_SPEC.CORE_008

            name @= 'view()'
            kind @= OPERATION
            input @= 'subject: object | Focus'
            input @= 'placement: tuple[str, ...] | None = None'
            output @= 'SemanticView'


            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_16
            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_21

        class TITLE_53:
            r'''
            ```python
            def derive_structure_specification(
                self,
                subject: object | Focus,
                *,
                placement: tuple[str, ...] | None = None,
            ) -> StructureSpecification
            ```

            {{TERM_5}}をこの {{TERM_1}} の `Structure` で{{TERM_18}}し、その{{TERM_20}}をルートとする{{TERM_8}}を導出する。これは明示的な{{TERM_8}}を探索する method ではなく、呼び出し側が「{{TERM_5}}から導出する」ことを選択した場合に使用する。
            '''
            title @= '`derive_structure_specification()`'
            name @= 'derive_structure_specification()'
            kind @= OPERATION
            input @= 'subject: object | Focus'
            input @= 'placement: tuple[str, ...] | None = None'
            output @= 'StructureSpecification'


            merge @= TERMS.TERM_5
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_8

        class TITLE_54:
            r'''
            ```python
            def validate(
                self,
                subject: object | Focus,
                *,
                placement: tuple[str, ...] | None = None,
                structure_specification: StructureSpecification | None = None,
            ) -> ValidationResult
            ```

            対象を{{TERM_20}}として{{TERM_19}}を構成し、適用可能な{{TERM_22}}と `descriptor_rules` を評価する。`structure_specification` が指定された場合は、同じ{{TERM_21}}操作の中で{{TERM_8}}への適合も確認する。

            単独の module を `validate()` する場合は `placement` が必須である。現在の import path を予定配置として暗黙採用しない。package 全体の{{TERM_21}}中に下位 module へ{{TERM_22}}を適用する場合は、解決済み{{TERM_7}}の位置を配置として自動的に引き継ぐ。

            ルートとなる{{TERM_20}}だけでなく、その{{TERM_19}}に含まれる各{{TERM_7}}要素について、その `StructuralKind` を要求する{{TERM_22}}を適用する。下位要素に規則を適用するときは、最初に構成した{{TERM_19}}から `SemanticView.subview()` で部分{{TERM_19}}を切り出して渡す。一回の `validate()` の途中で `Structure.resolve()` や{{TERM_13}}・{{TERM_16}}の取得を繰り返さず、一回{{TERM_18}}した runtime 状態を{{TERM_21}}操作全体で共有する。

            {{TERM_8}}の照合では、{{TERM_20}}に配置が指定されている場合、その位置以下の部分{{TERM_7}}だけを厳密に照合する。これにより、module 単体の{{TERM_21}}では外側の兄弟 module 等を観測したかのようには扱わない。

            ---
            '''
            title @= '`validate()`'
            related @= CORE_SPEC.CORE_005
            related @= VALIDATION_SPEC.VAL_005

            related @= CORE_SPEC.CORE_008

            name @= 'validate()'
            kind @= OPERATION
            input @= 'subject: object | Focus'
            input @= 'placement: tuple[str, ...] | None = None'
            input @= 'structure_specification: StructureSpecification | None = None'
            output @= 'ValidationResult'


            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_22
            merge @= TERMS.TERM_21
            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_16
            merge @= TERMS.TERM_18

