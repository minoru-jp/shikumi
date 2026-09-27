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
canonical source は `devdocs/canonical_sources/docs/api/descriptors.py` です。
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

# Descriptor API

記述器使用の記録、構造上の使用規則、class 成立後の binding を扱う。

related: [Description Semantics](../specification/description.md)

## 記述器使用

        

### `DescriptorUse`

```python
@dataclass(frozen=True)
class DescriptorUse:
    descriptor: object
    subject: object
```

ある記述器がある実行時対象に使用されたという事実を表す。情報接続とは独立しており、一回の記述器使用がゼロ件、一件、複数件の情報接続を行ってよい。

related: [DESC_003](../specification/description.md#desc_003)

name: DescriptorUse

kind: Type

### `record_descriptor_use()`

```python
def record_descriptor_use(
    subject: object,
    descriptor: object,
) -> DescriptorUse
```

`descriptor` が `subject` に使用されたことを記録する低水準 API。記述器の import 元やソース上の名称は追跡せず、渡された Python object を実行時 identity として扱う。bound method は同じ instance と underlying function の組として照合されるため、`writer.describe` を属性アクセスし直しても同じ記述器として判定できる。

name: record_descriptor_use()

kind: Operation

input: subject: object, descriptor: object

output: DescriptorUse

### 記述器使用 registry

記述器使用 registry は情報 registry と同様に、対象の `__eq__` / `__hash__` ではなく runtime identity で管理する。内部記録は対象を直接保持せず、取得時に公開 `DescriptorUse` を組み立てるため、registry 自体は対象を直接強参照しない。ただし、記録された `descriptor` 自身、またはそこから到達可能な Python object が対象を参照している場合、その参照によって対象の寿命が延びることがある。たとえば instance の bound method は通常その instance を保持する。Shikumi は記述器自身の参照関係を弱参照化したり切断したりしない。

#### `descriptor_uses_of()`

```python
def descriptor_uses_of(subject: object) -> tuple[DescriptorUse, ...]
```

対象へ直接記録された記述器使用を使用順に返す。

name: descriptor_uses_of()

kind: Operation

input: subject: object

output: tuple[DescriptorUse, ...]

#### `clear_descriptor_uses()`

```python
def clear_descriptor_uses(subject: object) -> None
```

対象へ直接記録された記述器使用を削除する。主にテストや実行時ライフサイクル管理のための API である。

name: clear_descriptor_uses()

kind: Operation

input: subject: object

output: None

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

name: StructureSelector

kind: Type

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

name: one_of()

kind: Operation

input: *selectors: StructureSelector

output: StructureSelector

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

related: [VAL_003](../specification/validation.md#val_003)

name: DescriptorUseRule

kind: Type

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
```
`class_binding()` はクラス成立後の処理タイミングを提供するだけであり、記述器使用の記録や情報接続そのものを強制しない。Shikumi の記述器として利用する場合、必要に応じて `connect` から `record_descriptor_use()` と `attach_information()` をそれぞれ呼び出す。

`class_binding()` の内部実装方法は公開契約に含めない。

---

related: [DESC_006](../specification/description.md#desc_006)

name: class_binding()

kind: Operation

input: value: T, connect: Callable[[type[object], T], None]

output: object
