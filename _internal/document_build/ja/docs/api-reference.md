<!-- shikumi-devdoc:translation-metadata
{
  "version": 1,
  "publication": "omit-this-comment",
  "preserve_spelling": [
    {
      "source": "_internal.document_source.vocabulary.canonical",
      "identifier": "TERM_1",
      "text": "Shikumi"
    },
    {
      "source": "_internal.document_source.vocabulary.canonical",
      "identifier": "TERM_33",
      "text": "shikumi_lib"
    },
    {
      "source": "_internal.document_source.vocabulary.canonical",
      "identifier": "TERM_34",
      "text": "norms"
    },
    {
      "source": "_internal.document_source.vocabulary.canonical",
      "identifier": "TERM_35",
      "text": "realizers"
    }
  ]
}
-->

<!--
この文書は自動生成された翻訳元の中間文書です。
正本は `_internal/document_source/api_reference/canonical.py` です。
直接編集しないでください。

公開文書作成方針

- `_internal/document_build/ja/` にある日本語中間文書はリポジトリへ commit し、正本からの実現結果をレビュー可能にする。
- 公開文書はこの中間文書を翻訳元とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- `preserve_spelling @= True` が指定された用語は表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックと翻訳メタデータは公開文書には含めない。
- 内容の変更は公開文書や中間文書を直接編集するのではなく、正本へ戻って行う。
-->

# Shikumi API Reference

この文書は Shikumi の公開 API と、その意味上の契約を定義する。

[`glossary.md`](./glossary.md) は概念の正規定義であり、この文書はその概念を Python API としてどのように公開するかを定める。概念上の意味に不一致がある場合は `glossary.md` を優先する。

この文書に記載しないモジュール、クラス、関数、属性は内部実装として扱う。公開 API は `shikumi` と `shikumi.standard` から提供する。

この API 仕様は実装に先行して定義されることがある。公開実装はこの文書へ適合させる。

## 基本契約

Shikumi は Python の実行後に成立した対象と情報を扱う。Python source を AST として解釈して意味状態を再構成しない。

情報は Shikumi インスタンスに所有されない。規定側は情報接続を通じて Python の実行時対象へ情報を接続し、Shikumi は自身が認識する情報型だけを意味像へ取り込む。

記述器の具体的な形式は公開 API によって制限しない。デコレータ、`@=`、docstring、通常の関数呼び出し、その他の実行時処理を利用できる。記述器使用と情報接続は別の実行時事実として扱い、規定側は必要な場合だけ `record_descriptor_use()` で使用事実を記録し、`attach_information()` で情報を接続する。

検証は意味像を対象とし、実現器は意味像から成果物を生成する。実現器は Shikumi に所有されない。

---

# Core API: `shikumi`

## 情報

### `Cardinality`

```python
class Cardinality(str, Enum):
    ONE = "one"
    MANY = "many"
```

情報型に許される情報の個数を表す。

`ONE` は意味上の単一値を表すが、情報接続そのものは不正状態を禁止しない。複数値が接続された状態を保持したうえで、検証規則が不適合として診断できる。

### `InformationType`

```python
class InformationType(Generic[T]):
    name: str
    value_type: type[T] | tuple[type[Any], ...]
    cardinality: Cardinality
```

情報型を定義する。単一の `value_type` を指定した場合、その Python 型を型変数 `T` として静的型情報にも伝える。

情報型の同一性はオブジェクト identity による。同じ `name` を持つ二つの `InformationType` は別の情報型である。

コンストラクタは `name` が空でない `str`、`value_type` が `type` または空でない `tuple[type, ...]` で、かつ `isinstance()` の第2引数として利用可能であること、`cardinality` が `Cardinality` であることを検証する。不正な型を後段の `accepts()` まで持ち越さない。

#### 属性

```python
name: str
value_type: type[T] | tuple[type[Any], ...]
cardinality: Cardinality
```

#### `accepts(value)`

```python
def accepts(self, value: object) -> bool
```

`value` が `value_type` に適合するかを返す。これは値型の判定のみを行い、個数やその他の検証を行わない。

情報型は、値が別の実体、`module`、関数その他の Python オブジェクトである場合も特別扱いしない。Shikumi は参照解決や到達可能性の判定を行わず、その値をどのように利用するかは規定側が定める。

### `Information`

```python
@dataclass(frozen=True)
class Information(Generic[T]):
    type: InformationType[T]
    value: T
    subject: object
```

実行時対象へ接続された一件の情報を表す。記述器が使用された事実は `Information` に埋め込まず、`DescriptorUse` として独立して記録する。

### `attach_information()`

```python
def attach_information(
    subject: object,
    information_type: InformationType[T],
    value: T,
) -> Information[T]
```

**情報接続の標準導線。**

`value` を `information_type` の情報として `subject` へ接続し、生成した `Information` を返す。

この関数は記述構文ではない。規定側が独自の記述器を定義するときに利用する低水準 API である。

`attach_information()` 自体は次を検証しない。

- `value_type` への適合
- `cardinality` への適合
- Shikumi がその情報型を認識しているか

これらは意味状態を保持した後、必要な検証規則によって検証する。

`subject` は弱参照可能な実行時対象でなければならない。接続不能な対象に対しては `TypeError` を送出する。

情報 registry は `subject` の `__eq__` / `__hash__` を用いず、runtime identity で管理する。registry 内部の記録は `subject` を直接保持せず、`information_of()` の取得時に公開 `Information` を組み立てる。したがって registry 自体は `subject` を直接強参照しない。ただし、`Information.value` に相当する内部値や、その値から到達可能な Python object が `subject` を参照している場合、その参照によって `subject` の寿命が延びることがある。Shikumi は情報値自身の参照関係を弱参照化したり切断したりしない。

### `information_of()`

```python
def information_of(subject: object) -> tuple[Information[Any], ...]
```

`subject` に直接接続された情報を、接続順に返す。

Shikumi による情報型の選別や意味構造の解釈は行わない。

### `clear_information()`

```python
def clear_information(subject: object) -> None
```

`subject` に直接接続された情報を削除する。

主にテスト、対話的ツール、実行時ライフサイクルを明示的に管理する用途の API とする。通常の規定・記述では使用しない。

## 記述器使用

### `DescriptorUse`

```python
@dataclass(frozen=True)
class DescriptorUse:
    descriptor: object
    subject: object
```

ある記述器がある実行時対象に使用されたという事実を表す。情報接続とは独立しており、一回の記述器使用がゼロ件、一件、複数件の情報接続を行ってよい。

### `record_descriptor_use()`

```python
def record_descriptor_use(
    subject: object,
    descriptor: object,
) -> DescriptorUse
```

`descriptor` が `subject` に使用されたことを記録する低水準 API。記述器の import 元やソース上の名称は追跡せず、渡された Python object を実行時 identity として扱う。bound method は同じ instance と underlying function の組として照合されるため、`writer.describe` を属性アクセスし直しても同じ記述器として判定できる。

### `descriptor_uses_of()` / `clear_descriptor_uses()`

```python
def descriptor_uses_of(subject: object) -> tuple[DescriptorUse, ...]
def clear_descriptor_uses(subject: object) -> None
```

対象へ直接記録された記述器使用を取得または削除する。`clear_descriptor_uses()` は主にテストや実行時ライフサイクル管理のための API である。

記述器使用 registry も情報 registry と同様に、対象の `__eq__` / `__hash__` ではなく runtime identity で管理する。内部記録は対象を直接保持せず、取得時に公開 `DescriptorUse` を組み立てるため、registry 自体は対象を直接強参照しない。ただし、記録された `descriptor` 自身、またはそこから到達可能な Python object が対象を参照している場合、その参照によって対象の寿命が延びることがある。たとえば instance の bound method は通常その instance を保持する。Shikumi は記述器自身の参照関係を弱参照化したり切断したりしない。

### `StructureSelector`

```python
StructureSelector(
    *,
    kind: StructuralKind | None = None,
    at: tuple[str, ...] | None = None,
    under: tuple[str, ...] | None = None,
)
```

記述器使用規則が対象とする構造上の位置を選択する。`kind` は構造種別、`at` は一つの有効 path との完全一致、`under` は指定 path 自身を含むその配下を表す。`at` と `under` は同時に指定できない。何も指定しない selector はすべての位置に一致する。複数の候補位置を許可する場合は `StructureSelector.one_of(a, b, ...)` または `a | b` で selector を OR 合成できる。

#### `one_of()` / `|`

```python
@classmethod
def one_of(
    cls,
    *selectors: StructureSelector,
) -> StructureSelector
```

複数の selector のいずれかに一致する selector を返す。`a | b` は `StructureSelector.one_of(a, b)` と同じ意味を持つ。

path は構造規定と同じ規定ルート基準で評価する。package 全体を焦点にした場合は package 自身をルート `()` とし、単独 module に `placement` を指定した場合はその予定配置を有効 path として用いる。

### `DescriptorUseRule`

```python
DescriptorUseRule(
    descriptor: object,
    allowed: StructureSelector,
    recommended: StructureSelector | None = None,
    name: str | None = None,
)
```

一つの記述器を構造上のどこで使用可能または推奨とするかを定める。`allowed` に一致しない使用は error、`allowed` には一致するが `recommended` に一致しない使用は warning となる。`recommended=None` の場合、許可範囲内の位置をすべて同等に扱う。

規則が存在しない記述器は、この仕組みによる構造上の制約を受けない。情報型、情報値、import 元などから暗黙の使用範囲を推論しない。

## `@=` 用のクラス接続

### `class_binding()`

```python
def class_binding(
    value: T,
    connect: Callable[[type, T], None],
) -> object
```

クラス本体の実行中にはまだ存在しないクラス実体に対して、クラス成立後に処理を適用するための低水準 API。

`@=` を用いる独自記述器の著者が利用する。Shikumi は `value` の型や意味を解釈せず、クラス成立後に `connect(subject, value)` を呼び出すことだけを保証する。

返されたオブジェクトは、同じ名前に対する連続した `@=` を受け取れる。

```python
class Tags:
    def __init__(self, information_type: InformationType) -> None:
        self.information_type = information_type

    def __imatmul__(self, value: str):
        return class_binding(value, self._connect)

    def _connect(self, subject: type, value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(
            subject,
            self.information_type,
            value,
        )


tags = Tags(Tag)

class Page:
    tags @= "python"
    tags @= "runtime"
```

`class_binding()` はクラス成立後の処理タイミングを提供するだけであり、記述器使用の記録や情報接続そのものを強制しない。Shikumi の記述器として利用する場合、必要に応じて `connect` から `record_descriptor_use()` と `attach_information()` をそれぞれ呼び出す。

`class_binding()` の内部実装方法は公開契約に含めない。

---

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

### `StructuralKind`

```python
class StructuralKind(str, Enum):
    PACKAGE = "package"
    MODULE = "module"
    ENTITY = "entity"
```

Core が表現する構造上の種別。

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

### `ResolvedStructure`

```python
@dataclass(frozen=True)
class ResolvedStructure:
    focus: Focus
    nodes: tuple[StructureNode, ...]
```

一つの焦点について解決された意味構造。

#### `node_for(subject)`

```python
def node_for(self, subject: object) -> StructureNode | None
```

identity が一致する対象のノードを返す。

`ResolvedStructure` は生成時に構造の不変条件を検証する。少なくとも、焦点対象がちょうど一度だけ存在すること、`path` が一意であること、`subject` が identity で一意であること、すべてのノードが焦点 root の配下にあること、焦点以外の各 path に構造上の親 path が存在することを要求する。独自 `Structure` はこれらを満たさない `ResolvedStructure` を返せない。

### `Structure`

```python
class Structure(ABC):
    @abstractmethod
    def resolve(self, focus: Focus) -> ResolvedStructure:
        ...
```

構造を解釈するための抽象基底。

独自構造は `resolve()` を実装し、焦点を含む `ResolvedStructure` を返す。

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

### `StructureElement`

```python
@dataclass(frozen=True)
class StructureElement:
    path: tuple[str, ...]
    kind: StructuralKind
```

構造規定において、ルートからの相対 path に要求される構造上の種別を表す。ルート自身の path は `()` とする。

### `StructureSpecification`

```python
StructureSpecification(elements: Iterable[StructureElement])
```

構造規定を、ルート相対の `StructureElement` の集合として表す。要素 path は一意でなければならず、ルート要素 `()` と、各要素の親 path が存在しなければならない。

現在の構造照合は完全一致であり、必要な要素の欠落だけでなく、規定にない追加要素もerrorとする。

規定体は `StructureSpecification` を通常の Python object として明示的に公開できる。別の記述体から構造規定を得る場合も、最終的には同じ `StructureSpecification` として表現する。Shikumi はこの二つの取得方法を自動で切り替えない。

#### `from_resolved()`

```python
@classmethod
def from_resolved(
    cls,
    structure: ResolvedStructure,
) -> StructureSpecification
```

解決済み構造から、その焦点をルート `()` とする構造規定を導出する。

#### `element_at()` / `subtree()`

```python
def element_at(self, path: tuple[str, ...]) -> StructureElement | None
def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]
```

指定位置の要素、または指定位置以下の部分構造を返す。

---

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

#### `subject`

```python
@property
def subject(self) -> object
```

`node.subject` を返す。

#### `kind`

```python
@property
def kind(self) -> StructuralKind
```

`node.kind` を返す。

#### `records(information_type)`

```python
def records(
    self,
    information_type: InformationType[T],
) -> tuple[Information[T], ...]
```

指定した情報型の情報を identity によって選別して返す。

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

#### `has(information_type)`

```python
def has(self, information_type: InformationType[T]) -> bool
```

指定した情報型の情報を一件以上持つかを返す。

#### `uses(descriptor)`

```python
def uses(self, descriptor: object) -> tuple[DescriptorUse, ...]
```

この対象へ記録された、指定記述器による使用を返す。bound method は同じ bound instance と underlying function によって照合する。

### `SemanticView`

```python
@dataclass(frozen=True)
class SemanticView:
    focus: Focus
    structure: ResolvedStructure
    items: tuple[ViewItem, ...]
```

一つの焦点について構成された意味像。

#### `focused`

```python
@property
def focused(self) -> ViewItem
```

焦点そのものに対応する `ViewItem` を返す。

#### `entities`

```python
@property
def entities(self) -> tuple[ViewItem, ...]
```

実体に対応する項目を返す。

#### `modules`

```python
@property
def modules(self) -> tuple[ViewItem, ...]
```

module に対応する項目を返す。

#### `packages`

```python
@property
def packages(self) -> tuple[ViewItem, ...]
```

package に対応する項目を返す。

#### `item(subject)`

```python
def item(self, subject: object) -> ViewItem
```

identity が一致する対象の `ViewItem` を返す。意味像に存在しない場合は `UnknownViewSubjectError` を送出する。

#### `subview(subject)`

```python
def subview(self, subject: object) -> SemanticView
```

この意味像にすでに含まれている対象を新しい焦点とし、その構造上の subtree から部分意味像を返す。元の `ResolvedStructure`、情報、記述器使用を再利用し、Python runtime を再解釈しない。元の焦点自身を指定した場合は同じ `SemanticView` を返す。意味像に存在しない対象では `UnknownViewSubjectError` を送出する。

`SemanticView` は iterable であり、`items` の順序で `ViewItem` を反復する。

---

## Shikumi

### `Shikumi`

```python
Shikumi(
    *,
    structure: Structure | None = None,
    information_types: Iterable[InformationType[Any]] = (),
    validators: Iterable[ValidationRule] = (),
    descriptor_rules: Iterable[DescriptorUseRule] = (),
)
```

構造、認識する情報型、検証規則、記述器使用規則を一つの意味体系として構成する。

`structure=None` の場合は `PythonStructure()` を使用する。明示的に指定する場合は `Structure` のインスタンスでなければならない。独自の構造解釈は `Structure` を継承して実装できる。

`information_types`、`validators`、`descriptor_rules` の各要素は、それぞれ `InformationType`、`ValidationRule`、`DescriptorUseRule` でなければならない。同一のオブジェクトを同じ Shikumi に重複登録してはならない。種類が異なる構成要素は constructor で `TypeError` とし、重複は `ValueError` とする。

constructor が保証するのは、構成要素の種類と局所的な登録不変条件までである。`Structure.resolve()` を試行したり、検証規則同士の意味的整合性、記述器使用規則が実際の構造で到達可能かといった意味的妥当性を事前評価したりはしない。これらは各構成要素の実行時の責務であり、独自拡張の表現力を constructor 検証のために狭めない。

### `recognizes()`

```python
def recognizes(self, information_type: InformationType[Any]) -> bool
```

その情報型を identity によって認識するかを返す。

### `view()`

```python
def view(
    self,
    subject: object | Focus,
    *,
    placement: tuple[str, ...] | None = None,
) -> SemanticView
```

対象を焦点として解釈し、意味像を返す。`placement` を指定すると、その位置を焦点の構造上の配置として使用する。`Focus` 自体に配置が含まれる場合、method 引数として重ねて指定してはならない。

意味像に取り込む情報は、その Shikumi が `information_types` として認識するものだけである。対象へ接続されている未認識の情報は削除されず、単にその意味像には現れない。記述器使用は情報型とは独立して意味像へ取り込まれ、`descriptor_rules` が必要な使用だけを構造との関係で検証する。

### `derive_structure_specification()`

```python
def derive_structure_specification(
    self,
    subject: object | Focus,
    *,
    placement: tuple[str, ...] | None = None,
) -> StructureSpecification
```

記述体をこの Shikumi の `Structure` で解釈し、その焦点をルートとする構造規定を導出する。これは明示的な構造規定を探索する method ではなく、呼び出し側が「記述体から導出する」ことを選択した場合に使用する。

### `validate()`

```python
def validate(
    self,
    subject: object | Focus,
    *,
    placement: tuple[str, ...] | None = None,
    structure_specification: StructureSpecification | None = None,
) -> ValidationResult
```

対象を焦点として意味像を構成し、適用可能な検証規則と `descriptor_rules` を評価する。`structure_specification` が指定された場合は、同じ検証操作の中で構造規定への適合も確認する。

単独の module を `validate()` する場合は `placement` が必須である。現在の import path を予定配置として暗黙採用しない。package 全体の検証中に下位 module へ検証規則を適用する場合は、解決済み構造の位置を配置として自動的に引き継ぐ。

ルートとなる焦点だけでなく、その意味像に含まれる各構造要素について、その `StructuralKind` を要求する検証規則を適用する。下位要素に規則を適用するときは、最初に構成した意味像から `SemanticView.subview()` で部分意味像を切り出して渡す。一回の `validate()` の途中で `Structure.resolve()` や情報・記述器使用の取得を繰り返さず、一回解釈した runtime 状態を検証操作全体で共有する。

構造規定の照合では、焦点に配置が指定されている場合、その位置以下の部分構造だけを厳密に照合する。これにより、module 単体の検証では外側の兄弟 module 等を観測したかのようには扱わない。

---

## 検証

### `DiagnosticSeverity`

```python
class DiagnosticSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
```

診断情報の重大度。

### `Diagnostic`

```python
Diagnostic(
    message: str,
    code: str | None = None,
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR,
    subject: object | None = None,
)
```

一件の診断情報。`message` と `code`、`severity` は生成時に型を検証し、`severity` は `DiagnosticSeverity` そのものを要求する。文字列 `"error"` 等を暗黙変換しない。

検証規則が `subject=None` の診断情報を返した場合、その規則へ渡された意味像の焦点が自動的に `subject` として設定される。

### `ValidationRule`

```python
ValidationRule(
    focus_kind: StructuralKind,
    check: Callable[[SemanticView], ValidationOutput],
    name: str,
)
```

一つの検証規則。

`ValidationRule` は identity によって区別する。生成時に `focus_kind` が `StructuralKind`、`check` が callable、`name` が空でない `str` であることを検証する。

呼び出し時には `focus_kind` と一致する焦点の意味像を要求し、診断情報の tuple を返す。

### `validator()`

```python
def validator(
    *,
    focus: StructuralKind,
    name: str | None = None,
) -> Callable[[ValidationFunction], ValidationRule]
```

通常の Python 関数から `ValidationRule` を定義するための補助デコレータ。

検証関数は `SemanticView` を受け取り、次のいずれかを返せる。

```python
None
Diagnostic
Iterable[Diagnostic]
```

例:

```python
@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic(
            "title is required",
            code="title.required",
        )
```

### `check_descriptor_uses()`

```python
def check_descriptor_uses(
    view: SemanticView,
    rules: Iterable[DescriptorUseRule],
) -> tuple[Diagnostic, ...]
```

意味像に記録された記述器使用を、記述器使用規則と照合して診断情報を返す。`Shikumi.validate()` は登録された `descriptor_rules` に対してこの検査を自動的に行う。

### `StructureCheck` / `check_structure()`

```python
@dataclass(frozen=True)
class StructureCheck:
    specification: StructureSpecification
    placement: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]


def check_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
) -> StructureCheck
```

解決済み構造を構造規定と照合した結果を表す。焦点の `placement` が指定されている場合はその部分構造を、指定されていない場合は構造規定のルートを照合する。

`StructureCheck.is_valid` は error 診断がない場合に `True`。

### `ValidationResult`

```python
@dataclass(frozen=True)
class ValidationResult:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...]
    structure_check: StructureCheck | None = None
```

一回の検証結果。構造規定を指定した場合、その照合結果を `structure_check` に保持し、構造上の診断情報も `diagnostics` に含める。

#### `is_valid`

```python
@property
def is_valid(self) -> bool
```

`ERROR` の診断情報が一件もない場合に `True`。

`bool(result)` は `result.is_valid` と同じ意味を持つ。

---

## 実現

### `RealizationCheck`

```python
@dataclass(frozen=True)
class RealizationCheck:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...] = ()
```

成果物を生成せずに、特定の実現器が意味像を実現可能か問い合わせた結果。`is_realizable` は error 診断がない場合に `True`。規定への適合性とは独立している。

### `Realizer`

```python
class Realizer(ABC, Generic[ArtifactT]):
    def check(self, view: SemanticView) -> RealizationCheck:
        ...

    @abstractmethod
    def realize(self, view: SemanticView) -> ArtifactT:
        ...
```

意味像から成果物を生成するための抽象基底。`check()` は成果物を生成せず、与えられた意味像を実現可能か問い合わせる。実現条件を持つ実現器は `check()` を override し、満たされない条件を `Diagnostic` として返す。既定実装は追加の実現条件なしとして扱う。

実現器は Shikumi を所有せず、Shikumi からも所有されない。同じ意味像に複数の実現器を適用できる。

```python
view = docs.view(source)

markdown = MarkdownRealizer().realize(view)
json_data = JsonRealizer().realize(view)
```

成果物の型は Shikumi によって制限しない。

---

## 例外

### `ShikumiError`

Shikumi が定義する例外の基底。

### `UnsupportedFocusError`

```python
class UnsupportedFocusError(ShikumiError, TypeError):
    ...
```

構造が与えられた焦点を解釈できない場合に送出する。

### `UnknownViewSubjectError`

```python
class UnknownViewSubjectError(ShikumiError, LookupError):
    ...
```

意味像に存在しない対象を `SemanticView.item()` で取得しようとした場合に送出する。

---

# 記述器を定義する

Shikumi は具体的な記述器の形を規定しない。規定体の著者は通常の Python を使って記述器を定義し、その中から情報接続を行う。

## 引数を取らないデコレータ

```python
Kind = InformationType(
    "kind",
    str,
    cardinality=Cardinality.MANY,
)


class KindDescriptions:
    def attr(self, subject):
        """属性として扱われる実体。"""
        record_descriptor_use(subject, self.attr)
        attach_information(
            subject,
            Kind,
            "attr",
        )
        return subject

    def service(self, subject):
        """サービスとして扱われる実体。"""
        record_descriptor_use(subject, self.service)
        attach_information(
            subject,
            Kind,
            "service",
        )
        return subject


kind = KindDescriptions()
```

記述体では通常の Python デコレータとして使用する。

```python
@kind.attr
class Owner:
    pass


@kind.service
class UserService:
    pass
```

`attr` や `service` は通常の Python method として存在するため、IDE の定義ジャンプ、docstring 表示、型注釈などを通常どおり利用できる。

## 引数を取るデコレータ

```python
Uses = InformationType(
    "uses",
    type,
    cardinality=Cardinality.MANY,
)


class RelationDescriptions:
    def uses(self, target: type):
        """対象の実体を利用する関係。"""

        def decorate(subject):
            record_descriptor_use(subject, self.uses)
            attach_information(
                subject,
                Uses,
                target,
            )
            return subject

        return decorate


relation = RelationDescriptions()
```

```python
@relation.uses(UserRepository)
class UserService:
    pass
```

引数、戻り値、デコレータの生成方法は記述器の著者の責務である。Shikumi はそれらをラップしたり、signature から情報を推測したりしない。

## 独自の `@=` 記述器

`@=` の評価時点では、記述先となる class はまだ成立していない。このため `class_binding()` を用いて、class 成立後に情報接続を行う。

```python
Tag = InformationType(
    "tag",
    str,
    cardinality=Cardinality.MANY,
)


class TagDescriptions:
    def __imatmul__(self, value: str):
        return class_binding(value, self._connect)

    def _connect(self, subject: type, value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(
            subject,
            Tag,
            value,
        )


tag = TagDescriptions()
```

```python
class UserService:
    tag @= "application"
    tag @= "users"
```

Shikumi は `value` の型や構造を解釈しない。`@=` にどのような型を受け付け、その値をどの情報型として接続するかは記述器の著者が決める。

### 記述器使用規則の例

```python
endpoint_rule = DescriptorUseRule(
    descriptor=kind.service,
    allowed=StructureSelector(kind=StructuralKind.ENTITY),
    recommended=StructureSelector(
        kind=StructuralKind.ENTITY,
        under=("api",),
    ),
    name="kind.service",
)

system = Shikumi(
    information_types=[Kind],
    descriptor_rules=[endpoint_rule],
)
```

この規則は `kind.service` を entity でのみ許可し、規定ルートの `api` 以下での使用を推奨する。`api` 外の entity での使用は warning、entity 以外での使用は error になる。

---

# Standard API: `shikumi.standard`

Standard は Core の公開 API を組み合わせた再利用可能な具体機能を提供する。Standard は新しい意味モデルを導入しない。

## `assignment()`

```python
def assignment(information_type: InformationType)
```

与えられた値をそのまま指定情報型として情報接続する、標準的な `@=` 記述器を返す。使用時には記述器使用も記録する。

```python
Title = InformationType("title", str)
title = assignment(Title)

class Page:
    title @= "Overview"
```

同じ名前に対する連続した `@=` を許可する。

## `decorator()`

```python
def decorator(information_type: InformationType)
```

与えられた値をそのまま指定情報型として情報接続する、単純なデコレータ生成記述器を返す。適用時には記述器使用も記録する。

```python
Kind = InformationType("kind", str)
kind = decorator(Kind)

@kind("service")
class Service:
    pass
```

語彙名そのものを IDE から追跡可能にしたい場合や、引数に独自の意味を持たせたい場合は、この便利機能ではなく通常の Python デコレータを規定体で定義する。

## `DocstringWriter` / `docstring()`

```python
DocstringWriter(
    information_type: InformationType,
    *,
    clean: bool = True,
    required: bool = False,
)
```

```python
def docstring(
    information_type: InformationType,
    *,
    clean: bool = True,
    required: bool = False,
) -> DocstringWriter
```

明示的に適用された対象の `__doc__` を情報として接続する標準記述器。適用時には記述器使用を記録し、docstring が存在しない場合でも「記述器が使用された」という事実は残る。

```python
Content = content_type()
content = docstring(Content)

@content
class Overview:
    """Overview document."""
```

`clean=True` の場合は Python の docstring 整形規則に従って余分なインデントを除去する。

`required=False` で docstring が存在しない場合は何も接続しない。情報の必須性は通常、検証規則で表現することを推奨する。

## `content_type()`

```python
def content_type(
    name: str = "content",
    *,
    value_type: type | tuple[type, ...] = str,
) -> InformationType
```

主要内容を表す単一値の情報型を生成する便利関数。

## `PackageTreeStructure`

```python
PackageTreeStructure()
```

import 済み package を焦点としたとき、その物理 package tree を探索し、子 package / module を Python の通常の import 機構で読み込んで意味構造を構成する。

module または実体を焦点とした場合は `PythonStructure` と同等の局所解釈を行う。各 module では、module 直下の class に加えて字句上の入れ子 class も実体として意味構造へ含める。

この構造は Python import の実行結果を意味状態の正とする。source を AST として解析しない。

## `information_type_rule()`

```python
def information_type_rule(
    information_type: InformationType,
    *,
    focus: StructuralKind = StructuralKind.ENTITY,
) -> ValidationRule
```

一つの情報型について、次を検証する標準検証規則を生成する。

- `Cardinality.ONE` に対する複数値
- `value_type` に適合しない値

情報の存在必須性や、値に規定固有の意味を与える検証は行わない。

---

# 公開 API の層分け

Core と Standard の境界は次のように扱う。

```text
Core (`shikumi`)
├─ 情報型・情報
├─ 情報接続
├─ class 成立後への低水準接続
├─ 構造・焦点・意味像
├─ Shikumi
├─ 検証
└─ 実現

Standard (`shikumi.standard`)
├─ 汎用 `@=` 記述器
├─ 汎用デコレータ記述器
├─ docstring 記述器
├─ 標準情報型生成補助
├─ package tree 構造
└─ 標準検証規則
```

`kind`、`attr`、`rel` など特定用途の語彙は Standard の責務としない。規定体が必要な語彙を通常の Python 定義として記述する。

---

# 動作保証の境界

Shikumi は通常の Python class 作成と import / execution の振る舞いを前提とする。

利用者または規定体が独自のデコレータ、metaclass、base class、mixin などを使用した場合、それらとの相互作用に対して Shikumi は互換処理を提供しない。組み合わせによって Python 標準の class 作成過程や記述器の実行順序が変化する場合、その動作は保証しない。

Shikumi は次を行わない。

- Python source の AST 解析による意味復元
- 記述器関数の signature や戻り値からの自動的な情報推論
- 特定語彙の自動登録
- 未認識情報の自動削除
- 検証前の不正状態の自動補正
- 実現器の Shikumi への登録や所有

この境界により、規定体の著者は通常の Python を使って記述方法を自由に定義し、Shikumi は情報接続以降の意味解釈に集中する。

---

# CLI: `shikumi`

Shikumi は、規定体が公開する `Shikumi`、記述体となる Python object、独立した実現器を実行時に結線する薄い CLI を提供する。

CLI は規定体、記述体、実現器の登録・探索・所有関係を管理しない。指定された Python 参照を通常の import によって読み込み、その場で処理する。

Python 参照は次の形式を用いる。

```text
module
module:object
module:outer.inner
```

`--shikumi` と `--realizer` は `module:object` を要求する。`--body` は module/package 自体を指定する場合は `module`、実体を焦点にする場合は `module:object` を使用できる。

## `validate`

```bash
shikumi validate \
  --shikumi SPEC_MODULE:SHIKUMI \
  --body DESCRIPTION_MODULE[:OBJECT] \
  [--at PLACEMENT] \
  [--structure-spec SPEC_MODULE:STRUCTURE | --structure-from DESCRIPTION_MODULE[:OBJECT]] \
  [--realizer REALIZER_MODULE:REALIZER] \
  [--format text|json]
```

指定した記述体または実体を `Shikumi.validate()` で検証する。

単独の module を `--body` に指定する場合、`--at` は必須である。値は `api.users` のような構造上の予定配置を dotted path で表し、`.` は構造規定のルートを表す。package 全体を指定した場合は配置を省略できる。

構造規定を利用する場合は、次のどちらか一方を利用者が明示的に選ぶ。

- `--structure-spec MODULE:OBJECT`: 規定体などが Python object として公開した `StructureSpecification` をそのまま使用する。指定 object が存在しない、または型が異なる場合は CLI 設定エラーとし、記述体からの導出へフォールバックしない。
- `--structure-from MODULE[:OBJECT]`: 指定した記述体を現在の Shikumi で解釈し、その構造から `StructureSpecification` を導出する。

`--realizer` を指定すると、通常の検証に加えて `Realizer.check()` を呼び、成果物を生成せずに実現可能性を問い合わせる。規定への適合と実現可能性は別結果として JSON 応答に保持する。どちらかに error があれば command 全体の `ok` は `false` となる。

検証と、指定されている場合の実現可能性検査の双方に error がなければ exit code `0`、一件以上あれば `1` を返す。warning / info のみの場合は `0` とする。

`validate` は成果物を生成しない。

## `realize`

```bash
shikumi realize \
  --shikumi SPEC_MODULE:SHIKUMI \
  --body DESCRIPTION_MODULE[:OBJECT] \
  [--at PLACEMENT] \
  --realizer REALIZER_MODULE:REALIZER \
  --output PATH \
  [--format text|json]
```

指定した記述体から意味像を構成し、指定した `Realizer` へ渡して成果物を生成する。`--at` を指定した場合、その構造上の配置を意味像へ反映する。

`realize` は暗黙に validation も `Realizer.check()` も実行しない。規定への適合、実現可能性の問い合わせ、実際の実現は独立した操作として扱う。必要であれば先に `validate --realizer ...` を実行する。

CLI からファイルへ書き出せる成果物は次のいずれかとする。

- `str`: UTF-8 text として書き出す
- `bytes` / bytes-like: binary として書き出す
- JSON serialization 可能な Python 値: UTF-8 JSON として書き出す

それ以外の成果物を返す実現器は、CLI の標準出力契約では直接利用できない。

## `--format`

```text
text
json
```

既定値は `text`。

`--format` は **CLI 自身の応答形式**を決める。実現器が生成する成果物の形式を決めるものではない。

`text` は端末で読むために整形されたテキストを出力する。

`json` は LLM、CI、その他のツールから扱うための構造化応答を stdout に出力する。JSON 応答には `format_version` を含める。現在の version は `1`。

例:

```json
{
  "format_version": 1,
  "command": "validate",
  "ok": false,
  "shikumi": "api_spec:api",
  "body": "my_api",
  "focus_kind": "package",
  "placement": null,
  "diagnostic_counts": {
    "error": 1,
    "warning": 0,
    "info": 0
  },
  "diagnostics": [
    {
      "severity": "error",
      "code": "endpoint.path.required",
      "message": "endpoint path is required",
      "subject": "my_api.users.GetUser"
    }
  ],
  "structure": null,
  "realization": null
}
```

実現時に `--output` を指定した場合、成果物はそのファイルへ書き出し、stdout には CLI 応答だけを出力する。この分離により、成果物自体が JSON であっても `--format json` の CLI 応答と混在しない。

CLI が処理できる import、解釈、検証、実現、成果物書き出しの失敗は、`json` 形式では `ok: false` と `error.type` / `error.message` を持つ構造化応答として報告する。
