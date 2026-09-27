<!-- shikumi-devdoc:translation-metadata
{
  "version": 1,
  "publication": "omit-this-comment",
  "preserve_spelling": [
    {
      "source": "devdocs.canonical_sources.docs.vocabulary",
      "identifier": "TERM_1",
      "text": "Shikumi"
    }
  ]
}
-->

<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/api/structure.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` の日本語 canonical document はリポジトリへ commit し、canonical source からの実現結果をレビュー可能にする。
- 英語の published document は canonical document を翻訳元とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- `preserve_spelling @= True` が指定された用語は表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックと翻訳メタデータは published document には含めない。
- 内容の変更は published document や canonical document を直接編集せず、canonical source へ戻って行う。
-->

# Structure API

runtime object の構造解釈と StructureSpecification を扱う公開 API。

related: [Structure Semantics](../specification/structure.md)

## 構造と焦点

        

### `Focus`

```python
@dataclass(frozen=True)
class Focus:
    subject: object
    placement: tuple[str, ...] | None = None
```

意味像を構成するときの焦点を表す。`placement` は、対象を構造上のどこに配置したものとして解釈するかを明示するための任意の位置である。`None` は配置を指定していないことを表し、空 tuple `()` は構造規定のルートを明示的に表す。

通常は `Shikumi.view(subject)` / `Shikumi.validate(subject)` に実行時対象を直接渡せる。単独の module を検証するときは配置を明示する必要がある。package 全体の検証中に下位 module へ検証規則を適用する場合、その配置は解決済み構造から引き継がれる。

related: [STRUCT_002](../specification/structure.md#struct_002), [STRUCT_003](../specification/structure.md#struct_003)

name: Focus

kind: Type

### `StructuralKind`

```python
class StructuralKind(str, Enum):
    PACKAGE = "package"
    MODULE = "module"
    ENTITY = "entity"
```

Core が表現する構造上の種別。

name: StructuralKind

kind: Type

### `StructureNode`

```python
@dataclass(frozen=True)
class StructureNode:
    subject: object
    kind: StructuralKind
    name: str
    path: tuple[str, ...]
    parent: object | None = None
```

意味構造上の一位置を表す。

`subject` は実行時対象、`path` は構造上の位置を表す。`parent` は親となる実行時対象を持ち得る。

name: StructureNode

kind: Type

### `ResolvedStructure`

```python
@dataclass(frozen=True)
class ResolvedStructure:
    focus: Focus
    nodes: tuple[StructureNode, ...]
```

一つの焦点について解決された意味構造。

name: ResolvedStructure

kind: Type

#### `node_for(subject)`

```python
def node_for(self, subject: object) -> StructureNode | None
```

identity が一致する対象のノードを返す。

`ResolvedStructure` は生成時に構造の不変条件を検証する。少なくとも、焦点対象がちょうど一度だけ存在すること、`path` が一意であること、`subject` が identity で一意であること、すべてのノードが焦点 root の配下にあること、焦点以外の各 path に構造上の親 path が存在することを要求する。独自 `Structure` はこれらを満たさない `ResolvedStructure` を返せない。

name: node_for(subject)

kind: Operation

input: subject: object

output: StructureNode | None

### `Structure`

```python
class Structure(ABC):
    @abstractmethod
    def resolve(self, focus: Focus) -> ResolvedStructure:
        ...
```

構造を解釈するための抽象基底。

独自構造は `resolve()` を実装し、焦点を含む `ResolvedStructure` を返す。

name: Structure

kind: Type

### `PythonStructure`

```python
PythonStructure()
```

Core が提供する最小の Python 構造。`PythonStructure`ではclassを`StructuralKind.ENTITY`として扱い、functionやmethodは実体に含めない。

- `class` を焦点にした場合、その実体だけを解釈する。
- `module` を焦点にした場合、その module と、その module で定義された class を解釈する。class の内部に字句上定義された入れ子 class も再帰的に実体として含める。
- `package` は package として識別するが、子 module を暗黙に import しない。
- import された外部 class を、その module の実体として扱わない。
- 別の場所で定義された class を class 属性として代入しただけの alias は、入れ子実体として扱わない。
- `Focus.placement` が指定された場合、runtime object の identity は変えず、解決される構造上の path をその位置へ再配置する。

```python
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
```

related: [STRUCT_001](../specification/structure.md#struct_001)

name: PythonStructure

kind: Type

### `StructureElement`

```python
@dataclass(frozen=True)
class StructureElement:
    path: tuple[str, ...]
    kind: StructuralKind
    required: bool = True
```

構造規定における、具体名称を持つ exact な構造要素を表す。`path` はルートからの相対 path で、ルート自身は `()` とする。

`required=True` は親規定が有効なときにその要素の存在を要求する。`required=False` は、その具体名称が存在する場合だけ規定を有効化する。optional な要素が存在した場合も exact 規定は論理構造要素より優先される。root `()` は常に required でなければならない。

`StructureElement` の path に wildcard や論理構造要素の論理名を埋め込まない。既存の `elements`、`element_at()`、`subtree()`、`from_resolved()` は0.2.0でもこの exact path の意味を維持する。

related: [STRUCT_007](../specification/structure.md#struct_007), [STRUCT_015](../specification/structure.md#struct_015)

name: StructureElement

kind: Type

### `StructureFragment`

```python
StructureFragment(
    elements: Iterable[StructureElement],
    *,
    logical_elements: Iterable[LogicalStructureElement] = (),
    mounts: Iterable[StructureMount] = (),
    groups: Iterable[StructureGroup] = (),
)
```

構造断片を表す。fragment は `()` の root element を持つ自己完結した規定で、別の具体位置へ mount して再利用したり、論理構造要素の各実体へ同一規定として適用したりできる。

通常の fragment は closed であり、記述していない子孫は許可しない。

related: [STRUCT_008](../specification/structure.md#struct_008), [STRUCT_012](../specification/structure.md#struct_012)

name: StructureFragment

kind: Type

#### `unconstrained()`

```python
@classmethod
def unconstrained(cls, kind: StructuralKind) -> StructureFragment
```

root の `StructuralKind` だけを規定し、その配下の構造には制約を課さない fragment を返す。

「子要素を記述しない closed fragment」と「子孫を自由にする unconstrained fragment」は異なる。前者は leaf を意味し、後者だけが任意の子孫を受け入れる。

related: [STRUCT_012](../specification/structure.md#struct_012)

name: unconstrained()

kind: Operation

input: kind: StructuralKind

output: StructureFragment

#### `at()`

```python
def at(self, path: tuple[str, ...]) -> StructureMount
```

この fragment を具体的な path へ再利用するための `StructureMount` を返す。

name: at()

kind: Operation

input: path: tuple[str, ...]

output: StructureMount

#### `recursive()`

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

related: [STRUCT_017](../specification/structure.md#struct_017)

name: recursive()

kind: Operation

input: parent: tuple[str, ...] = (), logical_name: str, names: Iterable[str] | None = None, max_count: int | None = None

output: StructureFragment

### `StructureMount`

```python
@dataclass(frozen=True)
class StructureMount:
    path: tuple[str, ...]
    fragment: StructureFragment
```

具体的な `StructureElement` の位置へ構造断片を再利用する authoring object。mount target は既存の exact element でなければならず、target と fragment root の `StructuralKind` は一致しなければならない。

mount された fragment の exact 要素は `StructureSpecification.elements` へ展開されるため、既存の exact lookup API の意味は変わらない。

related: [STRUCT_008](../specification/structure.md#struct_008)

name: StructureMount

kind: Type

### `LogicalStructureElement`

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

論理構造要素を表す。`parent` 直下に現れる具体要素のうち、明示的 `StructureElement` によって先に解決されなかったものへ同一の `fragment` を適用する。

`names=None` では具体名称を制限しない。`names` を指定した場合は列挙された名称だけがこの論理要素へ解決される。`min_count` / `max_count` は一つの親の直下で解決される実体数を規定する。

同じ親では、同じ `StructuralKind` を受ける論理構造要素を複数置くことはできない。一方、PACKAGE と MODULE のように kind が異なる場合はそれぞれ一つずつ定義でき、実体の kind によって一意に規定を選択する。prefix、suffix、glob、regex、任意 predicate で異なる規定へ dispatch する機能は提供しない。

related: [STRUCT_009](../specification/structure.md#struct_009), [STRUCT_010](../specification/structure.md#struct_010), [STRUCT_011](../specification/structure.md#struct_011)

name: LogicalStructureElement

kind: Type

### `StructureGroup`

```python
StructureGroup(
    *,
    parent: tuple[str, ...],
    members: Iterable[str],
    min_count: int = 0,
    max_count: int | None = None,
)
```

構造グループを表す。異なる exact `StructureElement` の sibling 群へ集合としての出現数制約を与える。`members` は `parent` 直下に定義された exact child 名でなければならない。それぞれの member は独自の kind、optionality、fragment 規定を保持し、group はどの規定を選ぶかには関与しない。

`min_count=1, max_count=1` なら「列挙した exact sibling のうちちょうど一つ」を表せる。

related: [STRUCT_018](../specification/structure.md#struct_018)

name: StructureGroup

kind: Type

### `StructureSpecification`

```python
StructureSpecification(
    elements: Iterable[StructureElement],
    *,
    logical_elements: Iterable[LogicalStructureElement] = (),
    mounts: Iterable[StructureMount] = (),
    groups: Iterable[StructureGroup] = (),
)
```

構造規定を表す。`elements` は従来どおり exact `StructureElement` の集合であり、要素 path は一意、root `()` と各親 path は定義されなければならない。root は常に required だが、子の exact element は `required=False` により optional にできる。

optional exact element が存在しない場合、その subtree の required child や logical cardinality は評価されない。存在した場合は subtree が有効化され、通常どおり配下の規定を検査する。

`mounts` は構造断片を具体位置へ再利用する。`logical_elements` は実体名を固定しない論理構造要素を追加する。`groups` は exact sibling の集合へ cardinality を追加する。明示的な exact element は optional であっても、同じ名称を受け得る logical element より常に優先される。

`elements`、`element_at()`、`subtree()`、`from_resolved()` の exact semantics は0.1.xから変更しない。論理名は `ResolvedStructure` の actual path へ書き込まず、構造照合時の binding として扱う。

```python
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
```

kind別の論理要素、再帰 fragment、group cardinality は互いに独立して合成できる。

```python
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
```

related: [STRUCT_004](../specification/structure.md#struct_004), [STRUCT_007](../specification/structure.md#struct_007), [STRUCT_009](../specification/structure.md#struct_009), [STRUCT_013](../specification/structure.md#struct_013), [STRUCT_015](../specification/structure.md#struct_015), [STRUCT_016](../specification/structure.md#struct_016), [STRUCT_017](../specification/structure.md#struct_017), [STRUCT_018](../specification/structure.md#struct_018)

name: StructureSpecification

kind: Type

#### `from_resolved()`

```python
@classmethod
def from_resolved(
    cls,
    structure: ResolvedStructure,
) -> StructureSpecification
```

解決済み構造から、その焦点をルート `()` とする exact な構造規定を導出する。runtime structure だけから論理構造要素を推論しない。

related: [STRUCT_005](../specification/structure.md#struct_005), [STRUCT_007](../specification/structure.md#struct_007)

name: from_resolved()

kind: Operation

input: structure: ResolvedStructure

output: StructureSpecification

#### `element_at()`

```python
def element_at(self, path: tuple[str, ...]) -> StructureElement | None
```

指定位置の exact `StructureElement` を返す。論理構造要素の logical name や concrete binding の lookup には使用しない。

related: [STRUCT_007](../specification/structure.md#struct_007)

name: element_at()

kind: Operation

input: path: tuple[str, ...]

output: StructureElement | None

#### `subtree()`

```python
def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]
```

指定位置自身とその配下にある exact `StructureElement` を、規定内の順序で返す。論理構造要素によって実行時に生じる具体 path は返さない。

related: [STRUCT_007](../specification/structure.md#struct_007)

name: subtree()

kind: Operation

input: placement: tuple[str, ...]

output: tuple[StructureElement, ...]
