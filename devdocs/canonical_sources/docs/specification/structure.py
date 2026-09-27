"""Structure semantics specification."""

from shikumi_devdoc.fields.specification import MUST, MUST_NOT, condition, detail, level, related
from shikumi_devdoc.norms.common import canonical_source, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.docs.specification.core import SPECIFICATION_PART as CORE


@summary("焦点、構造解決、構造規定の一致判定に関する契約。")
@canonical_source("Structure Semantics", filename="structure.md", order=20, heading="identity")
class SPECIFICATION_PART:
    """runtime object を package、module、entity の構造として扱う契約。"""

    class STRUCT_001:
        """Structure.resolve() は Focus から ResolvedStructure を構成し、各 node に subject、StructuralKind、root-relative path を与える。"""

        title @= "Resolved structure is explicit"
        level @= MUST
        related @= CORE.CORE_001

    class STRUCT_002:
        """placement=None は配置未指定を表し、空 tuple は構造規定 root を明示的に表す。両者を同一視してはならない。"""

        title @= "Unspecified and root placement are distinct"
        level @= MUST

    class STRUCT_003:
        """単独 module は placement なしでも view として解釈できるが、Shikumi.validate() で構造上の位置を前提に検証する場合は予定 placement を明示しなければならない。"""

        title @= "Standalone module validation requires placement"
        level @= MUST
        condition @= "package 全体ではなく単独 module を Shikumi.validate() の focus とする場合。"

    class STRUCT_004:
        """StructureSpecification は位置と StructuralKind の構造契約を表し、情報値、記述器使用、記述 syntax の一致を要求してはならない。"""

        title @= "Structure specification covers topology, not semantic content"
        level @= MUST

    class STRUCT_005:
        """StructureSpecification.from_resolved() は解決済み構造から相対 placement と StructuralKind を保持する規定を導出する。"""

        title @= "Structure specifications may be derived from resolved structure"
        level @= MUST

    class STRUCT_006:
        """明示的 StructureSpecification と structure-from-body による導出は利用者が選択する別経路であり、一方が失敗した場合に他方へ暗黙フォールバックしてはならない。"""

        title @= "No implicit structure-source fallback"
        level @= MUST_NOT

    class STRUCT_007:
        """StructureElement、StructureSpecification.elements、element_at()、subtree()、from_resolved() は具体名称を持つ exact path の規定として解釈しなければならない。論理名や wildcard を既存 path tuple の意味へ混在させてはならない。"""

        title @= "Exact structure API retains concrete-path semantics"
        level @= MUST

    class STRUCT_008:
        """StructureFragment は自己完結した root-relative な部分規定として再利用できなければならない。具体位置へ mount された fragment の exact 要素は、その位置へ相対展開された StructureElement と同じ意味を持たなければならない。"""

        title @= "Structure fragments compose without changing exact semantics"
        level @= MUST

    class STRUCT_009:
        """LogicalStructureElement は一つの親位置で具体名称が異なる複数実体へ同一の構造規定を適用する。明示的 StructureElement と論理要素の双方が同じ具体名称を受け得る場合、明示的 StructureElement を優先しなければならない。"""

        title @= "Explicit structure overrides logical-name regulation"
        level @= MUST

    class STRUCT_010:
        """一つの親位置では、同じ StructuralKind を受ける LogicalStructureElement を複数定義してはならない。異なる StructuralKind を受ける論理要素は共存でき、実体の kind により規定を選択する。Shikumi は prefix、suffix、glob、regex、任意 predicate その他の名称パターンによって複数の論理規定へ dispatch してはならない。"""

        title @= "Logical-name resolution is kind-disjoint and pattern-free"
        level @= MUST_NOT
        detail @= "異なる規定が必要な名称は exact StructureElement として明示するか、規定体の構造上の区分を分ける。"

    class STRUCT_011:
        """LogicalStructureElement は具体名称を無制限に受け入れるか、列挙された名称へ制限でき、同じ親の直下で解決された実体数へ最小数と最大数を適用できなければならない。"""

        title @= "Logical elements may constrain names and cardinality"
        level @= MUST

    class STRUCT_012:
        """子要素を記述しない closed な構造規定は、その位置を leaf として扱わなければならない。子孫の topology に制約を課さない場合は unconstrained StructureFragment として明示しなければならず、既存の closed semantics を暗黙に変更してはならない。"""

        title @= "Unconstrained subtrees are explicit"
        level @= MUST

    class STRUCT_013:
        """ResolvedStructure は観測された actual path を保持し、LogicalStructureElement の論理名へ path を書き換えてはならない。logical-to-actual の対応は構造照合結果の binding として保持する。"""

        title @= "Logical bindings do not rewrite resolved structure"
        level @= MUST

    class STRUCT_014:
        """Focus.placement は論理構造要素の実体を通過する場合でも actual name を用いる。構造照合はその actual path を exact element 優先規則と LogicalStructureElement によって規定上の位置へ解決しなければならない。"""

        title @= "Placement remains an actual path through logical structure"
        level @= MUST

    class STRUCT_015:
        """StructureElement は exact path の意味を変えずに required / optional を区別できなければならない。required=False の exact element が存在しない場合、その subtree の規定を有効化してはならない。存在する場合は exact 規定を LogicalStructureElement より優先して適用し、その配下の required child と logical cardinality を通常どおり検査しなければならない。root `()` は optional にしてはならない。"""

        title @= "Optional exact elements activate their subtree only when present"
        level @= MUST

    class STRUCT_016:
        """同一 parent に複数の LogicalStructureElement がある場合、actual StructuralKind と fragment root の StructuralKind が一致する論理要素を選択しなければならない。exact element は従来どおり最優先であり、名称文字列による追加 dispatch を導入してはならない。"""

        title @= "Logical regulations may differ by structural kind"
        level @= MUST

    class STRUCT_017:
        """再帰 StructureFragment は有限の規定を事前に無限展開してはならず、実際に観測された recursive child に対して同じ fragment 規定を再適用しなければならない。recursive child の最小数は0とし、有限の実構造が規定上の無限 descend を要求されないようにしなければならない。"""

        title @= "Recursive fragments are lazily reapplied"
        level @= MUST

    class STRUCT_018:
        """StructureGroup は同一 parent 直下の exact StructureElement 群の存在数だけを制約しなければならない。member ごとの kind、required/optional、fragment 規定を置換してはならず、規定選択や名称 dispatch に使用してはならない。"""

        title @= "Structure groups constrain sibling cardinality only"
        level @= MUST


