"""Canonical Japanese API reference source for Validation API."""

from devdocs.canonical_sources.docs.vocabulary import TERMS
from shikumi_devdoc.fields.api_reference import (
    NAMESPACE, OPERATION, OTHER, TYPE, VALUE,
    input, kind, name, output, related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title
from devdocs.canonical_sources.docs.specification.validation import SPECIFICATION_PART as VALIDATION_SPEC
from devdocs.canonical_sources.docs.specification.structure import SPECIFICATION_PART as STRUCTURE_SPEC


validator_example = test_target_field("validator example")
structure_check_example = test_target_field("structure check example")
@summary('診断、検証規則、構造検証結果の公開 API。')
@canonical_source('Validation API', filename='validation.md', order=50, heading="title")
class API_REFERENCE_PART:
    """ValidationRule、Diagnostic、ValidationResult など検証の公開 API。"""

    related @= VALIDATION_SPEC

    class TITLE_55:
        r'''
        '''
        title @= "{{TERM_21}}"

        merge @= TERMS.TERM_21

        class TITLE_56:
            r'''
            ```python
            class DiagnosticSeverity(str, Enum):
                ERROR = "error"
                WARNING = "warning"
                INFO = "info"
            ```

            {{TERM_23}}の重大度。
            '''
            title @= '`DiagnosticSeverity`'
            name @= 'DiagnosticSeverity'
            kind @= TYPE


            merge @= TERMS.TERM_23

        class TITLE_57:
            r'''
            ```python
            Diagnostic(
                message: str,
                code: str | None = None,
                severity: DiagnosticSeverity = DiagnosticSeverity.ERROR,
                subject: object | None = None,
            )
            ```

            一件の{{TERM_23}}。`message` と `code`、`severity` は生成時に型を検証し、`severity` は `DiagnosticSeverity` そのものを要求する。文字列 `"error"` 等を暗黙変換しない。

            {{TERM_22}}が `subject=None` の{{TERM_23}}を返した場合、その規則へ渡された{{TERM_19}}の{{TERM_20}}が自動的に `subject` として設定される。
            '''
            title @= '`Diagnostic`'
            related @= VALIDATION_SPEC.VAL_008

            name @= 'Diagnostic'
            kind @= TYPE


            merge @= TERMS.TERM_23
            merge @= TERMS.TERM_22
            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_20

        class TITLE_58:
            r'''
            ```python
            ValidationRule(
                focus_kind: StructuralKind,
                check: Callable[[SemanticView], ValidationOutput],
                name: str,
            )
            ```

            一つの{{TERM_22}}。

            `ValidationRule` は identity によって区別する。生成時に `focus_kind` が `StructuralKind`、`check` が callable、`name` が空でない `str` であることを検証する。

            呼び出し時には `focus_kind` と一致する{{TERM_20}}の{{TERM_19}}を要求し、{{TERM_23}}の tuple を返す。
            '''
            title @= '`ValidationRule`'
            name @= 'ValidationRule'
            kind @= TYPE


            merge @= TERMS.TERM_22
            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_23

        class TITLE_59:
            r'''
            ```python
            def validator(
                *,
                focus: StructuralKind,
                name: str | None = None,
            ) -> Callable[[ValidationFunction], ValidationRule]
            ```

            通常の Python 関数から `ValidationRule` を定義するための補助デコレータ。

            {{TERM_21}}関数は `SemanticView` を受け取り、次のいずれかを返せる。

            ```python
            None
            Diagnostic
            Iterable[Diagnostic]
            ```

            例:

            ```python
            {{validator_example}}
            ```
            '''
            title @= '`validator()`'
            validator_example @= r"""
            from shikumi import (
                Diagnostic,
                InformationType,
                Shikumi,
                StructuralKind,
                attach_information,
                validator,
            )

            Title = InformationType("title", str)

            @validator(focus=StructuralKind.ENTITY)
            def require_title(view):
                if not view.focused.has(Title):
                    yield Diagnostic("title is required", code="title.required")

            docs = Shikumi(information_types=[Title], validators=[require_title])

            class MissingTitle:
                pass

            invalid = docs.validate(MissingTitle)
            assert not invalid.is_valid
            assert invalid.diagnostics[0].code == "title.required"
            assert invalid.diagnostics[0].subject is MissingTitle

            class Titled:
                pass

            attach_information(Titled, Title, "Overview")
            assert docs.validate(Titled).is_valid
            """

            name @= 'validator()'
            kind @= OPERATION
            input @= 'function: Callable[[SemanticView], Diagnostic | Iterable[Diagnostic] | None]'
            output @= 'ValidationRule'


            merge @= TERMS.TERM_21

        class TITLE_60:
            r'''
            ```python
            def check_descriptor_uses(
                view: SemanticView,
                rules: Iterable[DescriptorUseRule],
            ) -> tuple[Diagnostic, ...]
            ```

            {{TERM_19}}に記録された{{TERM_16}}を、{{TERM_17}}と照合して{{TERM_23}}を返す。`{{TERM_1}}.validate()` は登録された `descriptor_rules` に対してこの検査を自動的に行う。
            '''
            title @= '`check_descriptor_uses()`'
            related @= VALIDATION_SPEC.VAL_003

            name @= 'check_descriptor_uses()'
            kind @= OPERATION
            input @= 'view: SemanticView'
            input @= 'rules: Iterable[DescriptorUseRule]'
            output @= 'tuple[Diagnostic, ...]'


            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_16
            merge @= TERMS.TERM_17
            merge @= TERMS.TERM_23
            merge @= TERMS.TERM_1

        class TITLE_60C:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureBinding:
                logical_element: LogicalStructureElement
                actual_path: tuple[str, ...]
            ```

            {{TERM_36}}と、構造照合でその規定へ解決された具体 path の対応を表す。`ResolvedStructure` の actual path 自体は変更しない。
            '''
            title @= '`StructureBinding`'
            related @= STRUCTURE_SPEC.STRUCT_013

            name @= 'StructureBinding'
            kind @= TYPE

            merge @= TERMS.TERM_36

        class TITLE_61:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureCheck:
                specification: StructureSpecification
                placement: tuple[str, ...]
                diagnostics: tuple[Diagnostic, ...]
                bindings: tuple[StructureBinding, ...] = ()
            ```

            解決済み{{TERM_7}}を{{TERM_8}}と照合した結果を表す。`placement` は照合対象になった{{TERM_8}}上の actual position を保持し、{{TERM_36}}が解決された場合は `bindings` に logical-to-actual の対応を保持する。
            '''
            title @= '`StructureCheck`'
            related @= VALIDATION_SPEC.VAL_004
            related @= VALIDATION_SPEC.VAL_007

            name @= 'StructureCheck'
            kind @= TYPE

            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_36

            class TITLE_61A:
                r'''
                ```python
                @property
                def is_valid(self) -> bool
                ```

                `ERROR` の{{TERM_23}}が一件もない場合に `True`。`bool(check)` は `check.is_valid` と同じ意味を持つ。
                '''
                title @= '`is_valid`'
                name @= 'is_valid'
                kind @= VALUE

                merge @= TERMS.TERM_23

        class TITLE_61B:
            r'''
            ```python
            def check_structure(
                structure: ResolvedStructure,
                specification: StructureSpecification,
            ) -> StructureCheck
            ```

            解決済み{{TERM_7}}を{{TERM_8}}と照合する。{{TERM_20}}の `placement` が指定されている場合はその subtree だけを、指定されていない場合は{{TERM_8}}のルートを照合する。closed な exact / logical 規定では必要要素の欠落、kind 不一致、規定にない追加要素を error とする。unconstrained な構造断片では、その root より下の topology は検査しない。

            ```python
            {{structure_check_example}}
            ```
            '''
            title @= '`check_structure()`'
            related @= VALIDATION_SPEC.VAL_004
            related @= VALIDATION_SPEC.VAL_007

            structure_check_example @= r"""
            from shikumi import (
                Focus,
                PythonStructure,
                StructuralKind,
                StructureElement,
                StructureSpecification,
                check_structure,
            )

            class Page:
                pass

            resolved = PythonStructure().resolve(Focus(Page))
            expected = StructureSpecification(
                [StructureElement(path=(), kind=StructuralKind.ENTITY)]
            )
            assert check_structure(resolved, expected).is_valid

            wrong = StructureSpecification(
                [StructureElement(path=(), kind=StructuralKind.MODULE)]
            )
            mismatch = check_structure(resolved, wrong)
            assert not mismatch.is_valid
            assert mismatch.diagnostics[0].code == "structure.kind.mismatch"
            """

            name @= 'check_structure()'
            kind @= OPERATION
            input @= 'structure: ResolvedStructure'
            input @= 'specification: StructureSpecification'
            output @= 'StructureCheck'

            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_20

        class TITLE_62:
            r'''
            ```python
            @dataclass(frozen=True)
            class ValidationResult:
                view: SemanticView
                diagnostics: tuple[Diagnostic, ...]
                structure_check: StructureCheck | None = None
            ```

            一回の{{TERM_21}}結果。{{TERM_8}}を指定した場合、その照合結果を `structure_check` に保持し、{{TERM_7}}上の{{TERM_23}}も `diagnostics` に含める。
            '''
            title @= '`ValidationResult`'
            related @= VALIDATION_SPEC.VAL_002

            name @= 'ValidationResult'
            kind @= TYPE


            merge @= TERMS.TERM_21
            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_23

            class TITLE_63:
                r'''
                ```python
                @property
                def is_valid(self) -> bool
                ```

                `ERROR` の{{TERM_23}}が一件もない場合に `True`。

                `bool(result)` は `result.is_valid` と同じ意味を持つ。

                ---
                '''
                title @= '`is_valid`'
                name @= 'is_valid'
                kind @= VALUE


                merge @= TERMS.TERM_23

