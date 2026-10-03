"""Canonical Japanese API reference source for Standard API."""

from shikumi_devdoc.fields.api_reference import (
    NAMESPACE,
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
from devdocs.canonical_sources.docs.specification.public_api import (
    SPECIFICATION_PART as PUBLIC_API_SPEC,
)
from devdocs.canonical_sources.docs.specification.structure import (
    SPECIFICATION_PART as STRUCTURE_SPEC,
)
from devdocs.canonical_sources.docs.specification.validation import (
    SPECIFICATION_PART as VALIDATION_SPEC,
)
from devdocs.canonical_sources.docs.vocabulary import TERMS

assignment_example = test_target_field("assignment example")
decorator_example = test_target_field("decorator example")
docstring_example = test_target_field("docstring example")
information_type_rule_example = test_target_field("information type rule example")


@summary("`shikumi.standard` が提供する再利用可能な記述器、情報型、構造、検証規則。")
@canonical_source("Standard API", filename="standard.md", order=70, heading="title")
class API_REFERENCE_PART:
    """Core の公開プリミティブを組み合わせた `shikumi.standard` の公開 API。"""

    related @= PUBLIC_API_SPEC.API_003
    related @= PUBLIC_API_SPEC.API_004

    class TITLE_76:
        r"""
        Standard は Core の公開 API を組み合わせた再利用可能な具体機能を提供する。Standard は新しい意味モデルを導入しない。
        """

        title @= "`shikumi.standard`"

        name @= "shikumi.standard"
        kind @= NAMESPACE

        class TITLE_77:
            r"""
            ```python
            def assignment(information_type: InformationType[T])
            ```

            与えられた値をそのまま指定{{TERM_12}}として{{TERM_14}}する、標準的な `@=` {{TERM_15}}を返す。使用時には{{TERM_16}}も記録する。

            ```python
            {{assignment_example}}
            ```
            同じ名前に対する連続した `@=` を許可する。
            """

            title @= "`assignment()`"
            assignment_example @= r"""
            from shikumi import InformationType, information_of
            from shikumi.standard import assignment

            Title = InformationType("title", str)
            title = assignment(Title)

            class Page:
                title @= "Overview"

            assert information_of(Page)[0].value == "Overview"
            """

            related @= DESCRIPTION_SPEC.DESC_003
            name @= "assignment()"
            kind @= OPERATION
            input @= "information_type: InformationType[T]"
            output @= "descriptor supporting @="

            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_14
            merge @= TERMS.TERM_15
            merge @= TERMS.TERM_16

        class TITLE_78:
            r"""
            ```python
            def decorator(information_type: InformationType[T])
            ```

            与えられた値をそのまま指定{{TERM_12}}として{{TERM_14}}する、単純なデコレータ生成{{TERM_15}}を返す。適用時には{{TERM_16}}も記録する。

            ```python
            {{decorator_example}}
            ```
            語彙名そのものを IDE から追跡可能にしたい場合や、引数に独自の意味を持たせたい場合は、この便利機能ではなく通常の Python デコレータを{{TERM_3}}で定義する。
            """

            title @= "`decorator()`"
            decorator_example @= r"""
            from shikumi import InformationType, information_of
            from shikumi.standard import decorator

            Kind = InformationType("kind", str)
            kind = decorator(Kind)

            @kind("service")
            class Service:
                pass

            assert information_of(Service)[0].value == "service"
            """

            related @= DESCRIPTION_SPEC.DESC_003
            name @= "decorator()"
            kind @= OPERATION
            input @= "information_type: InformationType[T]"
            output @= "value-taking decorator descriptor"

            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_14
            merge @= TERMS.TERM_15
            merge @= TERMS.TERM_16
            merge @= TERMS.TERM_3

        class TITLE_79:
            r"""
            ```python
            DocstringWriter(
                information_type: InformationType[Any],
                *,
                clean: bool = True,
                required: bool = False,
            )
            ```

            明示的に適用された対象の `__doc__` を{{TERM_13}}として接続する標準{{TERM_15}}。適用時には{{TERM_16}}を記録し、docstring が存在しない場合でも「{{TERM_15}}が使用された」という事実は残る。

            `clean=True` の場合は Python の docstring 整形規則に従って余分なインデントを除去する。`required=True` で docstring が存在しない場合は `ValueError` を送出する。
            """

            title @= "`DocstringWriter`"
            related @= DESCRIPTION_SPEC.DESC_003
            name @= "DocstringWriter"
            kind @= TYPE
            input @= "information_type: InformationType[Any]"
            input @= "clean: bool = True"
            input @= "required: bool = False"

            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_15
            merge @= TERMS.TERM_16

        class TITLE_79A:
            r"""
            ```python
            def docstring(
                information_type: InformationType[Any],
                *,
                clean: bool = True,
                required: bool = False,
            ) -> DocstringWriter
            ```

            `DocstringWriter` を生成する便利関数。

            ```python
            {{docstring_example}}
            ```
            `required=False` で docstring が存在しない場合は何も接続しない。{{TERM_13}}の必須性は通常、{{TERM_22}}で表現することを推奨する。
            """

            title @= "`docstring()`"
            docstring_example @= r'''
            from shikumi import information_of
            from shikumi.standard import content_type, docstring

            Content = content_type()
            content = docstring(Content)

            @content
            class Overview:
                """Overview document."""

            assert information_of(Overview)[0].value == "Overview document."
            '''

            related @= DESCRIPTION_SPEC.DESC_003
            name @= "docstring()"
            kind @= OPERATION
            input @= "information_type: InformationType[Any]"
            input @= "clean: bool = True"
            input @= "required: bool = False"
            output @= "DocstringWriter"

            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_22

        class TITLE_80:
            r"""
            ```python
            def content_type(
                name: str = "content",
                *,
                value_type: type[Any] | tuple[type[Any], ...] = str,
            ) -> InformationType[Any]
            ```

            主要内容を表す `Cardinality.ONE` の{{TERM_12}}を生成する便利関数。`value_type` は生成される `InformationType` へそのまま渡す。
            """

            title @= "`content_type()`"
            name @= "content_type()"
            kind @= OPERATION
            input @= 'name: str = "content"'
            input @= "value_type: type[Any] | tuple[type[Any], ...] = str"
            output @= "InformationType[Any]"

            merge @= TERMS.TERM_12

        class TITLE_81:
            r"""
            ```python
            PackageTreeStructure()
            ```

            import 済み package を{{TERM_20}}としたとき、その物理 package tree を探索し、子 package / module を Python の通常の import 機構で読み込んで{{TERM_10}}を構成する。

            module または{{TERM_11}}を{{TERM_20}}とした場合は `PythonStructure` と同等の局所{{TERM_18}}を行う。各 module では、module 直下の class に加えて字句上の入れ子 class も{{TERM_11}}として{{TERM_10}}へ含める。

            この{{TERM_7}}は Python import の実行結果を意味状態の正とする。source を AST として解析しない。package discovery によって見つかった module は通常の import と同様に実行される。
            """

            title @= "`PackageTreeStructure`"
            related @= STRUCTURE_SPEC.STRUCT_001
            name @= "PackageTreeStructure"
            kind @= TYPE

            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_10
            merge @= TERMS.TERM_11
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_7

        class TITLE_82:
            r"""
            ```python
            def information_type_rule(
                information_type: InformationType[Any],
                *,
                focus: StructuralKind = StructuralKind.ENTITY,
            ) -> ValidationRule
            ```

            一つの{{TERM_12}}について、次を{{TERM_21}}する標準{{TERM_22}}を生成する。

            - `Cardinality.ONE` に対する複数値
            - `value_type` に適合しない値

            {{TERM_13}}の存在必須性や、値に{{TERM_2}}固有の意味を与える{{TERM_21}}は行わない。

            ```python
            {{information_type_rule_example}}
            ```
            """

            title @= "`information_type_rule()`"
            information_type_rule_example @= r"""
            from shikumi import InformationType, Shikumi
            from shikumi.standard import assignment, information_type_rule

            Title = InformationType("title", str)
            title = assignment(Title)

            class Page:
                title @= "First"
                title @= "Second"

            docs = Shikumi(
                information_types=[Title],
                validators=[information_type_rule(Title)],
            )
            result = docs.validate(Page)

            assert not result.is_valid
            assert tuple(item.code for item in result.diagnostics) == (
                "information.cardinality",
            )
            """

            related @= VALIDATION_SPEC.VAL_001
            name @= "information_type_rule()"
            kind @= OPERATION
            input @= "information_type: InformationType[Any]"
            input @= "focus: StructuralKind = StructuralKind.ENTITY"
            output @= "ValidationRule"

            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_21
            merge @= TERMS.TERM_22
            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_2
