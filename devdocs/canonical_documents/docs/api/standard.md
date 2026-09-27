<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/api/standard.py` です。
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

# Standard API

Core の公開プリミティブを組み合わせた `shikumi.standard` の公開 API。

related: [API_003](../specification/public-api.md#api_003), [API_004](../specification/public-api.md#api_004)

## `shikumi.standard`

Standard は Core の公開 API を組み合わせた再利用可能な具体機能を提供する。Standard は新しい意味モデルを導入しない。

name: shikumi.standard

kind: Namespace

### `assignment()`

```python
def assignment(information_type: InformationType[T])
```

与えられた値をそのまま指定情報型として情報接続する、標準的な `@=` 記述器を返す。使用時には記述器使用も記録する。

```python
from shikumi import InformationType, information_of
from shikumi.standard import assignment

Title = InformationType("title", str)
title = assignment(Title)

class Page:
    title @= "Overview"

assert information_of(Page)[0].value == "Overview"
```
同じ名前に対する連続した `@=` を許可する。

related: [DESC_003](../specification/description.md#desc_003)

name: assignment()

kind: Operation

input: information_type: InformationType[T]

output: descriptor supporting @=

### `decorator()`

```python
def decorator(information_type: InformationType[T])
```

与えられた値をそのまま指定情報型として情報接続する、単純なデコレータ生成記述器を返す。適用時には記述器使用も記録する。

```python
from shikumi import InformationType, information_of
from shikumi.standard import decorator

Kind = InformationType("kind", str)
kind = decorator(Kind)

@kind("service")
class Service:
    pass

assert information_of(Service)[0].value == "service"
```
語彙名そのものを IDE から追跡可能にしたい場合や、引数に独自の意味を持たせたい場合は、この便利機能ではなく通常の Python デコレータを規定体で定義する。

related: [DESC_003](../specification/description.md#desc_003)

name: decorator()

kind: Operation

input: information_type: InformationType[T]

output: value-taking decorator descriptor

### `DocstringWriter`

```python
DocstringWriter(
    information_type: InformationType[Any],
    *,
    clean: bool = True,
    required: bool = False,
)
```

明示的に適用された対象の `__doc__` を情報として接続する標準記述器。適用時には記述器使用を記録し、docstring が存在しない場合でも「記述器が使用された」という事実は残る。

`clean=True` の場合は Python の docstring 整形規則に従って余分なインデントを除去する。`required=True` で docstring が存在しない場合は `ValueError` を送出する。

related: [DESC_003](../specification/description.md#desc_003)

name: DocstringWriter

kind: Type

input: information_type: InformationType[Any], clean: bool = True, required: bool = False

### `docstring()`

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
from shikumi import information_of
from shikumi.standard import content_type, docstring

Content = content_type()
content = docstring(Content)

@content
class Overview:
    """Overview document."""

assert information_of(Overview)[0].value == "Overview document."
```
`required=False` で docstring が存在しない場合は何も接続しない。情報の必須性は通常、検証規則で表現することを推奨する。

related: [DESC_003](../specification/description.md#desc_003)

name: docstring()

kind: Operation

input: information_type: InformationType[Any], clean: bool = True, required: bool = False

output: DocstringWriter

### `content_type()`

```python
def content_type(
    name: str = "content",
    *,
    value_type: type[Any] | tuple[type[Any], ...] = str,
) -> InformationType[Any]
```

主要内容を表す `Cardinality.ONE` の情報型を生成する便利関数。`value_type` は生成される `InformationType` へそのまま渡す。

name: content_type()

kind: Operation

input: name: str = "content", value_type: type[Any] | tuple[type[Any], ...] = str

output: InformationType[Any]

### `PackageTreeStructure`

```python
PackageTreeStructure()
```

import 済み package を焦点としたとき、その物理 package tree を探索し、子 package / module を Python の通常の import 機構で読み込んで意味構造を構成する。

module または実体を焦点とした場合は `PythonStructure` と同等の局所解釈を行う。各 module では、module 直下の class に加えて字句上の入れ子 class も実体として意味構造へ含める。

この構造は Python import の実行結果を意味状態の正とする。source を AST として解析しない。package discovery によって見つかった module は通常の import と同様に実行される。

related: [STRUCT_001](../specification/structure.md#struct_001)

name: PackageTreeStructure

kind: Type

### `information_type_rule()`

```python
def information_type_rule(
    information_type: InformationType[Any],
    *,
    focus: StructuralKind = StructuralKind.ENTITY,
) -> ValidationRule
```

一つの情報型について、次を検証する標準検証規則を生成する。

- `Cardinality.ONE` に対する複数値
- `value_type` に適合しない値

情報の存在必須性や、値に規定固有の意味を与える検証は行わない。

```python
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
```

related: [VAL_001](../specification/validation.md#val_001)

name: information_type_rule()

kind: Operation

input: information_type: InformationType[Any], focus: StructuralKind = StructuralKind.ENTITY

output: ValidationRule
