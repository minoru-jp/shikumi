"""Canonical Japanese API reference source for Structure API."""

from devdocs.canonical_sources.docs.vocabulary import TERMS
from shikumi_devdoc.fields.api_reference import (
    NAMESPACE, OPERATION, OTHER, TYPE, VALUE,
    input, kind, name, output, related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title
from devdocs.canonical_sources.docs.specification.structure import SPECIFICATION_PART as STRUCTURE_SPEC


resolution_example = test_target_field("structure resolution example")
logical_structure_example = test_target_field("logical structure example")
advanced_structure_example = test_target_field("advanced structure example")
@summary('構造、焦点、構造規定の公開 API。')
@canonical_source('Structure API', filename='structure.md', order=20, heading="title")
class API_REFERENCE_PART:
    """runtime object の構造解釈と StructureSpecification を扱う公開 API。"""

    related @= STRUCTURE_SPEC

    class TITLE_22:
        r'''
        '''
        title @= "{{TERM_7}}と{{TERM_20}}"

        merge @= TERMS.TERM_7
        merge @= TERMS.TERM_20

        class TITLE_23:
            r'''
            ```python
            @dataclass(frozen=True)
            class Focus:
                subject: object
                placement: tuple[str, ...] | None = None
            ```

            {{TERM_19}}を構成するときの{{TERM_20}}を表す。`placement` は、対象を{{TERM_7}}上のどこに配置したものとして{{TERM_18}}するかを明示するための任意の位置である。`None` は配置を指定していないことを表し、空 tuple `()` は{{TERM_8}}のルートを明示的に表す。

            通常は `{{TERM_1}}.view(subject)` / `{{TERM_1}}.validate(subject)` に実行時対象を直接渡せる。単独の module を{{TERM_21}}するときは配置を明示する必要がある。package 全体の{{TERM_21}}中に下位 module へ{{TERM_22}}を適用する場合、その配置は解決済み{{TERM_7}}から引き継がれる。
            '''
            title @= '`Focus`'
            related @= STRUCTURE_SPEC.STRUCT_002
            related @= STRUCTURE_SPEC.STRUCT_003

            name @= 'Focus'
            kind @= TYPE


            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_21
            merge @= TERMS.TERM_22

        class TITLE_24:
            r'''
            ```python
            class StructuralKind(str, Enum):
                PACKAGE = "package"
                MODULE = "module"
                ENTITY = "entity"
            ```

            Core が表現する{{TERM_7}}上の種別。
            '''
            title @= '`StructuralKind`'
            name @= 'StructuralKind'
            kind @= TYPE


            merge @= TERMS.TERM_7

        class TITLE_25:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureNode:
                subject: object
                kind: StructuralKind
                name: str
                path: tuple[str, ...]
                parent: object | None = None
            ```

            {{TERM_10}}上の一位置を表す。

            `subject` は実行時対象、`path` は{{TERM_7}}上の位置を表す。`parent` は親となる実行時対象を持ち得る。
            '''
            title @= '`StructureNode`'
            name @= 'StructureNode'
            kind @= TYPE


            merge @= TERMS.TERM_10
            merge @= TERMS.TERM_7

        class TITLE_26:
            r'''
            ```python
            @dataclass(frozen=True)
            class ResolvedStructure:
                focus: Focus
                nodes: tuple[StructureNode, ...]
            ```

            一つの{{TERM_20}}について解決された{{TERM_10}}。
            '''
            title @= '`ResolvedStructure`'
            name @= 'ResolvedStructure'
            kind @= TYPE


            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_10

            class TITLE_27:
                r'''
                ```python
                def node_for(self, subject: object) -> StructureNode | None
                ```

                identity が一致する対象のノードを返す。

                `ResolvedStructure` は生成時に{{TERM_7}}の{{TERM_24}}を{{TERM_21}}する。少なくとも、{{TERM_20}}対象がちょうど一度だけ存在すること、`path` が一意であること、`subject` が identity で一意であること、すべてのノードが{{TERM_20}} root の配下にあること、{{TERM_20}}以外の各 path に{{TERM_7}}上の親 path が存在することを要求する。独自 `Structure` はこれらを満たさない `ResolvedStructure` を返せない。
                '''
                title @= '`node_for(subject)`'
                name @= 'node_for(subject)'
                kind @= OPERATION
                input @= 'subject: object'
                output @= 'StructureNode | None'


                merge @= TERMS.TERM_7
                merge @= TERMS.TERM_24
                merge @= TERMS.TERM_21
                merge @= TERMS.TERM_20

        class TITLE_28:
            r'''
            ```python
            class Structure(ABC):
                @abstractmethod
                def resolve(self, focus: Focus) -> ResolvedStructure:
                    ...
            ```

            {{TERM_7}}を{{TERM_18}}するための抽象基底。

            独自{{TERM_7}}は `resolve()` を実装し、{{TERM_20}}を含む `ResolvedStructure` を返す。
            '''
            title @= '`Structure`'
            name @= 'Structure'
            kind @= TYPE


            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_20

        class TITLE_29:
            r'''
            ```python
            PythonStructure()
            ```

            Core が提供する最小の Python {{TERM_7}}。`PythonStructure`ではclassを`StructuralKind.ENTITY`として扱い、functionやmethodは{{TERM_11}}に含めない。

            - `class` を{{TERM_20}}にした場合、その{{TERM_11}}だけを{{TERM_18}}する。
            - `module` を{{TERM_20}}にした場合、その module と、その module で定義された class を{{TERM_18}}する。class の内部に字句上定義された入れ子 class も再帰的に{{TERM_11}}として含める。
            - `package` は package として識別するが、子 module を暗黙に import しない。
            - import された外部 class を、その module の{{TERM_11}}として扱わない。
            - 別の場所で定義された class を class 属性として代入しただけの alias は、入れ子{{TERM_11}}として扱わない。
            - `Focus.placement` が指定された場合、runtime object の identity は変えず、解決される{{TERM_7}}上の path をその位置へ再配置する。

            ```python
            {{resolution_example}}
            ```
            '''
            title @= '`PythonStructure`'
            resolution_example @= r"""
            from types import ModuleType

            from shikumi import Focus, PythonStructure, StructureSpecification, StructuralKind

            module = ModuleType("demo")
            exec(
                "class Service:\n"
                "    class Handler:\n"
                "        pass\n",
                module.__dict__,
            )

            resolved = PythonStructure().resolve(Focus(module, placement=("app",)))
            assert tuple(node.path for node in resolved.nodes) == (
                ("app",),
                ("app", "Service"),
                ("app", "Service", "Handler"),
            )

            specification = StructureSpecification.from_resolved(resolved)
            assert tuple((element.path, element.kind) for element in specification.elements) == (
                ((), StructuralKind.MODULE),
                (("Service",), StructuralKind.ENTITY),
                (("Service", "Handler"), StructuralKind.ENTITY),
            )
            """

            related @= STRUCTURE_SPEC.STRUCT_001

            name @= 'PythonStructure'
            kind @= TYPE


            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_11
            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_18

        class TITLE_30:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureElement:
                path: tuple[str, ...]
                kind: StructuralKind
                required: bool = True
            ```

            {{TERM_8}}における、具体名称を持つ exact な構造要素を表す。`path` はルートからの相対 path で、ルート自身は `()` とする。

            `required=True` は親規定が有効なときにその要素の存在を要求する。`required=False` は、その具体名称が存在する場合だけ規定を有効化する。optional な要素が存在した場合も exact 規定は{{TERM_36}}より優先される。root `()` は常に required でなければならない。

            `StructureElement` の path に wildcard や{{TERM_36}}の論理名を埋め込まない。既存の `elements`、`element_at()`、`subtree()`、`from_resolved()` は0.2.0でもこの exact path の意味を維持する。
            '''
            title @= '`StructureElement`'
            related @= STRUCTURE_SPEC.STRUCT_007
            related @= STRUCTURE_SPEC.STRUCT_015
            name @= 'StructureElement'
            kind @= TYPE

            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_36

        class TITLE_30A:
            r'''
            ```python
            StructureFragment(
                elements: Iterable[StructureElement],
                *,
                logical_elements: Iterable[LogicalStructureElement] = (),
                mounts: Iterable[StructureMount] = (),
                groups: Iterable[StructureGroup] = (),
            )
            ```

            {{TERM_37}}を表す。fragment は `()` の root element を持つ自己完結した規定で、別の具体位置へ mount して再利用したり、{{TERM_36}}の各実体へ同一規定として適用したりできる。

            通常の fragment は closed であり、記述していない子孫は許可しない。
            '''
            title @= '`StructureFragment`'
            related @= STRUCTURE_SPEC.STRUCT_008
            related @= STRUCTURE_SPEC.STRUCT_012
            name @= 'StructureFragment'
            kind @= TYPE

            merge @= TERMS.TERM_37
            merge @= TERMS.TERM_36

            class TITLE_30A1:
                r'''
                ```python
                @classmethod
                def unconstrained(cls, kind: StructuralKind) -> StructureFragment
                ```

                root の `StructuralKind` だけを規定し、その配下の構造には制約を課さない fragment を返す。

                「子要素を記述しない closed fragment」と「子孫を自由にする unconstrained fragment」は異なる。前者は leaf を意味し、後者だけが任意の子孫を受け入れる。
                '''
                title @= '`unconstrained()`'
                related @= STRUCTURE_SPEC.STRUCT_012
                name @= 'unconstrained()'
                kind @= OPERATION
                input @= 'kind: StructuralKind'
                output @= 'StructureFragment'

            class TITLE_30A2:
                r'''
                ```python
                def at(self, path: tuple[str, ...]) -> StructureMount
                ```

                この fragment を具体的な path へ再利用するための `StructureMount` を返す。
                '''
                title @= '`at()`'
                name @= 'at()'
                kind @= OPERATION
                input @= 'path: tuple[str, ...]'
                output @= 'StructureMount'

            class TITLE_30A3:
                r'''
                ```python
                def recursive(
                    self,
                    *,
                    parent: tuple[str, ...] = (),
                    logical_name: str,
                    names: Iterable[str] | None = None,
                    max_count: int | None = None,
                ) -> StructureFragment
                ```

                fragment 自身を同じ `StructuralKind` の論理 child として再適用できる fragment を返す。recursive child の最小数は常に0であり、有限の実構造に対して観測された深さだけ規定を再適用する。`names` と `max_count` は各 recursive parent 直下の実体へ適用される。
                '''
                title @= '`recursive()`'
                related @= STRUCTURE_SPEC.STRUCT_017
                name @= 'recursive()'
                kind @= OPERATION
                input @= 'parent: tuple[str, ...] = (), logical_name: str, names: Iterable[str] | None = None, max_count: int | None = None'
                output @= 'StructureFragment'

        class TITLE_30B:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureMount:
                path: tuple[str, ...]
                fragment: StructureFragment
            ```

            具体的な `StructureElement` の位置へ{{TERM_37}}を再利用する authoring object。mount target は既存の exact element でなければならず、target と fragment root の `StructuralKind` は一致しなければならない。

            mount された fragment の exact 要素は `StructureSpecification.elements` へ展開されるため、既存の exact lookup API の意味は変わらない。
            '''
            title @= '`StructureMount`'
            related @= STRUCTURE_SPEC.STRUCT_008
            name @= 'StructureMount'
            kind @= TYPE

            merge @= TERMS.TERM_37

        class TITLE_30C:
            r'''
            ```python
            LogicalStructureElement(
                *,
                parent: tuple[str, ...],
                logical_name: str,
                fragment: StructureFragment,
                names: Iterable[str] | None = None,
                min_count: int = 1,
                max_count: int | None = None,
            )
            ```

            {{TERM_36}}を表す。`parent` 直下に現れる具体要素のうち、明示的 `StructureElement` によって先に解決されなかったものへ同一の `fragment` を適用する。

            `names=None` では具体名称を制限しない。`names` を指定した場合は列挙された名称だけがこの論理要素へ解決される。`min_count` / `max_count` は一つの親の直下で解決される実体数を規定する。

            同じ親では、同じ `StructuralKind` を受ける{{TERM_36}}を複数置くことはできない。一方、PACKAGE と MODULE のように kind が異なる場合はそれぞれ一つずつ定義でき、実体の kind によって一意に規定を選択する。prefix、suffix、glob、regex、任意 predicate で異なる規定へ dispatch する機能は提供しない。
            '''
            title @= '`LogicalStructureElement`'
            related @= STRUCTURE_SPEC.STRUCT_009
            related @= STRUCTURE_SPEC.STRUCT_010
            related @= STRUCTURE_SPEC.STRUCT_011
            name @= 'LogicalStructureElement'
            kind @= TYPE

            merge @= TERMS.TERM_36

        class TITLE_30D:
            r'''
            ```python
            StructureGroup(
                *,
                parent: tuple[str, ...],
                members: Iterable[str],
                min_count: int = 0,
                max_count: int | None = None,
            )
            ```

            {{TERM_38}}を表す。異なる exact `StructureElement` の sibling 群へ集合としての出現数制約を与える。`members` は `parent` 直下に定義された exact child 名でなければならない。それぞれの member は独自の kind、optionality、fragment 規定を保持し、group はどの規定を選ぶかには関与しない。

            `min_count=1, max_count=1` なら「列挙した exact sibling のうちちょうど一つ」を表せる。
            '''
            title @= '`StructureGroup`'
            related @= STRUCTURE_SPEC.STRUCT_018
            name @= 'StructureGroup'
            kind @= TYPE

            merge @= TERMS.TERM_38

        class TITLE_31:
            r'''
            ```python
            StructureSpecification(
                elements: Iterable[StructureElement],
                *,
                logical_elements: Iterable[LogicalStructureElement] = (),
                mounts: Iterable[StructureMount] = (),
                groups: Iterable[StructureGroup] = (),
            )
            ```

            {{TERM_8}}を表す。`elements` は従来どおり exact `StructureElement` の集合であり、要素 path は一意、root `()` と各親 path は定義されなければならない。root は常に required だが、子の exact element は `required=False` により optional にできる。

            optional exact element が存在しない場合、その subtree の required child や logical cardinality は評価されない。存在した場合は subtree が有効化され、通常どおり配下の規定を検査する。

            `mounts` は{{TERM_37}}を具体位置へ再利用する。`logical_elements` は実体名を固定しない{{TERM_36}}を追加する。`groups` は exact sibling の集合へ cardinality を追加する。明示的な exact element は optional であっても、同じ名称を受け得る logical element より常に優先される。

            `elements`、`element_at()`、`subtree()`、`from_resolved()` の exact semantics は0.1.xから変更しない。論理名は `ResolvedStructure` の actual path へ書き込まず、構造照合時の binding として扱う。

            ```python
            {{logical_structure_example}}
            ```

            kind別の論理要素、再帰 fragment、group cardinality は互いに独立して合成できる。

            ```python
            {{advanced_structure_example}}
            ```
            '''
            title @= '`StructureSpecification`'
            related @= STRUCTURE_SPEC.STRUCT_004
            related @= STRUCTURE_SPEC.STRUCT_007
            related @= STRUCTURE_SPEC.STRUCT_009
            related @= STRUCTURE_SPEC.STRUCT_013
            related @= STRUCTURE_SPEC.STRUCT_015
            related @= STRUCTURE_SPEC.STRUCT_016
            related @= STRUCTURE_SPEC.STRUCT_017
            related @= STRUCTURE_SPEC.STRUCT_018

            logical_structure_example @= r'''
            from shikumi import (
                LogicalStructureElement,
                StructuralKind,
                StructureElement,
                StructureFragment,
                StructureSpecification,
            )

            actor = StructureFragment(
                [
                    StructureElement((), StructuralKind.PACKAGE),
                    StructureElement(("GUI",), StructuralKind.PACKAGE),
                ]
            )

            specification = StructureSpecification(
                [
                    StructureElement((), StructuralKind.PACKAGE),
                    StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
                    StructureElement(
                        ("INTERACTION", "NON_SWDESC"),
                        StructuralKind.PACKAGE,
                        required=False,
                    ),
                ],
                logical_elements=[
                    LogicalStructureElement(
                        parent=("INTERACTION",),
                        logical_name="actor",
                        fragment=actor,
                        min_count=0,
                    )
                ],
                mounts=[
                    StructureFragment.unconstrained(StructuralKind.PACKAGE).at(
                        ("INTERACTION", "NON_SWDESC")
                    )
                ],
            )

            assert specification.element_at(("INTERACTION", "NON_SWDESC")) is not None
            assert specification.logical_elements[0].logical_name == "actor"
            '''

            advanced_structure_example @= r'''
            from shikumi import (
                LogicalStructureElement,
                StructuralKind,
                StructureElement,
                StructureFragment,
                StructureGroup,
                StructureSpecification,
            )

            module = StructureFragment([StructureElement((), StructuralKind.MODULE)])
            package_tree = StructureFragment(
                [
                    StructureElement((), StructuralKind.PACKAGE),
                    StructureElement(("LOCAL",), StructuralKind.PACKAGE, required=False),
                    StructureElement(("REMOTE",), StructuralKind.PACKAGE, required=False),
                ],
                logical_elements=[
                    LogicalStructureElement(
                        parent=(),
                        logical_name="module",
                        fragment=module,
                        min_count=0,
                    )
                ],
                groups=[
                    StructureGroup(
                        parent=(),
                        members=("LOCAL", "REMOTE"),
                        min_count=0,
                        max_count=1,
                    )
                ],
            ).recursive(logical_name="package")

            specification = StructureSpecification(
                [
                    StructureElement((), StructuralKind.PACKAGE),
                    StructureElement(("src",), StructuralKind.PACKAGE),
                ],
                mounts=[package_tree.at(("src",))],
            )

            assert specification.element_at(("src", "LOCAL")) is not None
            assert specification.groups[0].max_count == 1
            '''

            name @= 'StructureSpecification'
            kind @= TYPE

            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_37
            merge @= TERMS.TERM_36

            class TITLE_32:
                r'''
                ```python
                @classmethod
                def from_resolved(
                    cls,
                    structure: ResolvedStructure,
                ) -> StructureSpecification
                ```

                解決済み{{TERM_7}}から、その{{TERM_20}}をルート `()` とする exact な{{TERM_8}}を導出する。runtime structure だけから{{TERM_36}}を推論しない。
                '''
                title @= '`from_resolved()`'
                related @= STRUCTURE_SPEC.STRUCT_005
                related @= STRUCTURE_SPEC.STRUCT_007

                name @= 'from_resolved()'
                kind @= OPERATION
                input @= 'structure: ResolvedStructure'
                output @= 'StructureSpecification'

                merge @= TERMS.TERM_7
                merge @= TERMS.TERM_20
                merge @= TERMS.TERM_8
                merge @= TERMS.TERM_36

            class TITLE_33:
                r'''
                ```python
                def element_at(self, path: tuple[str, ...]) -> StructureElement | None
                ```

                指定位置の exact `StructureElement` を返す。{{TERM_36}}の logical name や concrete binding の lookup には使用しない。
                '''
                title @= '`element_at()`'
                related @= STRUCTURE_SPEC.STRUCT_007
                name @= 'element_at()'
                kind @= OPERATION
                input @= 'path: tuple[str, ...]'
                output @= 'StructureElement | None'

                merge @= TERMS.TERM_36

            class TITLE_33A:
                r'''
                ```python
                def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]
                ```

                指定位置自身とその配下にある exact `StructureElement` を、規定内の順序で返す。{{TERM_36}}によって実行時に生じる具体 path は返さない。
                '''
                title @= '`subtree()`'
                related @= STRUCTURE_SPEC.STRUCT_007
                name @= 'subtree()'
                kind @= OPERATION
                input @= 'placement: tuple[str, ...]'
                output @= 'tuple[StructureElement, ...]'

                merge @= TERMS.TERM_36
