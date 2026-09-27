"""Validation semantics specification."""

from shikumi_devdoc.fields.specification import MUST, MUST_NOT, detail, level, related
from shikumi_devdoc.norms.common import canonical_source, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.docs.specification.description import SPECIFICATION_PART as DESCRIPTION
from devdocs.canonical_sources.docs.specification.structure import SPECIFICATION_PART as STRUCTURE


@summary("検証規則、診断、構造検証、記述器使用検証の契約。")
@canonical_source("Validation Semantics", filename="validation.md", order=30, heading="identity")
class SPECIFICATION_PART:
    """SemanticView に対する validation の契約。"""

    class VAL_001:
        """ValidationRule は SemanticView を評価し、ゼロ件以上の Diagnostic を返す。validation は runtime state を自動補正してはならない。"""

        title @= "Validation diagnoses without repair"
        level @= MUST

    class VAL_002:
        """ValidationResult.is_valid は ERROR severity の diagnostic が一件もない場合にだけ true とする。warning と info は validation failure として扱わない。"""

        title @= "Validity is determined by error diagnostics"
        level @= MUST

    class VAL_003:
        """DescriptorUseRule は記述器使用対象の構造位置を評価し、allowed に不適合なら error、allowed には適合するが recommended に不適合なら warning を報告する。"""

        title @= "Descriptor-use rule severity"
        level @= MUST
        related @= DESCRIPTION.DESC_003

    class VAL_004:
        """構造検証は focus に対応する StructureSpecification の範囲について placement と StructuralKind の一致を評価する。"""

        title @= "Structural validation compares the focused subtree"
        level @= MUST
        related @= STRUCTURE.STRUCT_004

    class VAL_005:
        """Shikumi.validate() は view construction、descriptor-use check、任意の structure check、登録 ValidationRule の評価を一つの ValidationResult として集約する。"""

        title @= "Shikumi validation aggregates semantic checks"
        level @= MUST

    class VAL_006:
        """validation は Realizer.check() を暗黙に実行してはならない。realizer の実現可能性は規定への適合とは独立した判定である。"""

        title @= "Validation does not imply realization checks"
        level @= MUST_NOT

    class VAL_007:
        """構造照合は選択された StructureSpecification の closed な規定範囲で、必要要素の欠落、kind 不一致、規定にない追加要素を error として報告する。LogicalStructureElement は解決された各 actual instance へ同じ closed fragment を適用し、unconstrained StructureFragment が明示された subtree だけは子孫の一致を要求しない。"""

        title @= "Structure checking is closed unless explicitly unconstrained"
        level @= MUST
        related @= STRUCTURE.STRUCT_004
        related @= STRUCTURE.STRUCT_009
        related @= STRUCTURE.STRUCT_012

    class VAL_008:
        """ValidationRule が subject=None の Diagnostic を返した場合、その規則へ渡された SemanticView の focus subject を diagnostic subject として補う。"""

        title @= "Validation diagnostics default to the rule focus"
        level @= MUST
