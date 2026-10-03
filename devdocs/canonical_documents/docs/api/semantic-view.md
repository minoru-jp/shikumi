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
canonical source は `devdocs/canonical_sources/docs/api/semantic_view.py` です。
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

# Semantic View API

Shikumi が構成した SemanticView と ViewItem を読み取る公開 API。

related: [Core Semantics](../specification/core.md)

## 意味像

### `ViewItem`

```python
@dataclass(frozen=True)
class ViewItem:
    node: StructureNode
    information: tuple[Information[Any], ...]
    descriptor_uses: tuple[DescriptorUse, ...] = ()
```

意味像に含まれる一つの解釈対象を表す。

name: ViewItem

kind: Type

#### `subject`

```python
@property
def subject(self) -> object
```

`node.subject` を返す。

name: subject

kind: Value

#### `kind`

```python
@property
def kind(self) -> StructuralKind
```

`node.kind` を返す。

name: kind

kind: Value

#### `records(information_type)`

```python
def records(
    self,
    information_type: InformationType[T],
) -> tuple[Information[T], ...]
```

指定した情報型の情報を identity によって選別して返す。

name: records(information_type)

kind: Operation

input: information_type: InformationType[T]

output: tuple[Information[T], ...]

#### `values(information_type)`

```python
def values(
    self,
    information_type: InformationType[T],
) -> tuple[T, ...]
```

指定した情報型の値を接続順に返す。

単一値の情報型であっても、検証前には複数値が存在し得るため、常に tuple を返す。

`InformationType[T]` の型変数は `records()` / `values()` まで伝播する。例えば `Title = InformationType("title", str)` を静的型検査器が `InformationType[str]` と解釈した場合、`item.values(Title)` は `tuple[str, ...]` になる。Shikumi は `py.typed` を配布し、この Core の情報型から取得までの型関係を公開契約に含める。

複数の Python 型を `value_type=(str, int)` のように指定する場合は、現段階では型変数を精密な union として導出することを保証しない。また、Standard の `assignment()` / `decorator()` や任意の独自記述器へ `T` を完全に伝播させることも、この第一段階の契約には含めない。記述器の runtime 上の自由度を保ち、型付けのためだけに記述器 API を複雑化しない。

name: values(information_type)

kind: Operation

input: information_type: InformationType[T]

output: tuple[T, ...]

#### `has(information_type)`

```python
def has(self, information_type: InformationType[T]) -> bool
```

指定した情報型の情報を一件以上持つかを返す。

name: has(information_type)

kind: Operation

input: information_type: InformationType[Any]

output: bool

#### `uses(descriptor)`

```python
def uses(self, descriptor: object) -> tuple[DescriptorUse, ...]
```

この対象へ記録された、指定記述器による使用を返す。bound method は同じ bound instance と underlying function によって照合する。

name: uses(descriptor)

kind: Operation

input: descriptor: object

output: tuple[DescriptorUse, ...]

### `SemanticView`

```python
@dataclass(frozen=True)
class SemanticView:
    focus: Focus
    structure: ResolvedStructure
    items: tuple[ViewItem, ...]
```

一つの焦点について構成された意味像。

```python
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
```

related: [CORE_008](../specification/core.md#core_008)

name: SemanticView

kind: Type

#### `focused`

```python
@property
def focused(self) -> ViewItem
```

焦点そのものに対応する `ViewItem` を返す。

name: focused

kind: Value

#### `entities`

```python
@property
def entities(self) -> tuple[ViewItem, ...]
```

実体に対応する項目を返す。

name: entities

kind: Value

#### `modules`

```python
@property
def modules(self) -> tuple[ViewItem, ...]
```

module に対応する項目を返す。

name: modules

kind: Value

#### `packages`

```python
@property
def packages(self) -> tuple[ViewItem, ...]
```

package に対応する項目を返す。

name: packages

kind: Value

#### `item(subject)`

```python
def item(self, subject: object) -> ViewItem
```

identity が一致する対象の `ViewItem` を返す。意味像に存在しない場合は `UnknownViewSubjectError` を送出する。

name: item(subject)

kind: Operation

input: subject: object

output: ViewItem

#### `subview(subject)`

```python
def subview(self, subject: object) -> SemanticView
```

この意味像にすでに含まれている対象を新しい焦点とし、その構造上の subtree から部分意味像を返す。元の `ResolvedStructure`、情報、記述器使用を再利用し、Python runtime を再解釈しない。元の焦点自身を指定した場合は同じ `SemanticView` を返す。意味像に存在しない対象では `UnknownViewSubjectError` を送出する。

`SemanticView` は iterable であり、`items` の順序で `ViewItem` を反復する。

---

related: [CORE_008](../specification/core.md#core_008)

name: subview(subject)

kind: Operation

input: subject: object

output: SemanticView
