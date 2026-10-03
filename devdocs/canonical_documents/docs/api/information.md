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
canonical source は `devdocs/canonical_sources/docs/api/information.py` です。
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

# Information API

InformationType と runtime information attachment の公開 API。

related: [Description Semantics](../specification/description.md)

## 情報

### `Cardinality`

```python
class Cardinality(str, Enum):
    ONE = "one"
    MANY = "many"
```

情報型に許される情報の個数を表す。

`ONE` は意味上の単一値を表すが、情報接続そのものは不正状態を禁止しない。複数値が接続された状態を保持したうえで、検証規則が不適合として診断できる。

name: Cardinality

kind: Type

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

related: [DESC_001](../specification/description.md#desc_001)

name: InformationType

kind: Type

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

name: accepts(value)

kind: Operation

input: value: object

output: bool

### `Information`

```python
@dataclass(frozen=True)
class Information(Generic[T]):
    type: InformationType[T]
    value: T
    subject: object
```

実行時対象へ接続された一件の情報を表す。記述器が使用された事実は `Information` に埋め込まず、`DescriptorUse` として独立して記録する。

name: Information

kind: Type

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

例:

```python
from shikumi import (
    InformationType,
    attach_information,
    clear_information,
    information_of,
)

Title = InformationType("title", str)

class Page:
    pass

assert Title.accepts("Overview")
assert not Title.accepts(42)

record = attach_information(Page, Title, "Overview")
assert record.subject is Page
assert tuple(item.value for item in information_of(Page)) == ("Overview",)

clear_information(Page)
assert information_of(Page) == ()
```
情報 registry は `subject` の `__eq__` / `__hash__` を用いず、runtime identity で管理する。registry 内部の記録は `subject` を直接保持せず、`information_of()` の取得時に公開 `Information` を組み立てる。したがって registry 自体は `subject` を直接強参照しない。ただし、`Information.value` に相当する内部値や、その値から到達可能な Python object が `subject` を参照している場合、その参照によって `subject` の寿命が延びることがある。Shikumi は情報値自身の参照関係を弱参照化したり切断したりしない。

related: [DESC_002](../specification/description.md#desc_002)

name: attach_information()

kind: Operation

input: subject: object, information_type: InformationType[T], value: T

output: Information[T]

### `information_of()`

```python
def information_of(subject: object) -> tuple[Information[Any], ...]
```

`subject` に直接接続された情報を、接続順に返す。

Shikumi による情報型の選別や意味構造の解釈は行わない。

name: information_of()

kind: Operation

input: subject: object

output: tuple[Information[Any], ...]

### `clear_information()`

```python
def clear_information(subject: object) -> None
```

`subject` に直接接続された情報を削除する。

主にテスト、対話的ツール、実行時ライフサイクルを明示的に管理する用途の API とする。通常の規定・記述では使用しない。

name: clear_information()

kind: Operation

input: subject: object

output: None
