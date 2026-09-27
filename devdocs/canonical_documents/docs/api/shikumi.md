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
canonical source は `devdocs/canonical_sources/docs/api/shikumi.py` です。
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

# Shikumi API

Shikumi インスタンスの構成、view、structure derivation、validation を扱う。

related: [Core Semantics](../specification/core.md)

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

related: [CORE_007](../specification/core.md#core_007)

name: Shikumi

kind: Type

### `recognizes()`

```python
def recognizes(self, information_type: InformationType[Any]) -> bool
```

その情報型を identity によって認識するかを返す。

name: recognizes()

kind: Operation

input: information_type: InformationType[Any]

output: bool

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

```python
from shikumi import InformationType, Shikumi, attach_information

Title = InformationType("title", str)
InternalId = InformationType("internal-id", int)

class Page:
    pass

attach_information(Page, Title, "Overview")
attach_information(Page, InternalId, 42)

docs = Shikumi(information_types=[Title])
assert docs.recognizes(Title)
assert not docs.recognizes(InternalId)

item = docs.view(Page).focused
assert item.values(Title) == ("Overview",)
assert not item.has(InternalId)
```

related: [CORE_004](../specification/core.md#core_004), [CORE_008](../specification/core.md#core_008)

name: view()

kind: Operation

input: subject: object | Focus, placement: tuple[str, ...] | None = None

output: SemanticView

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

name: derive_structure_specification()

kind: Operation

input: subject: object | Focus, placement: tuple[str, ...] | None = None

output: StructureSpecification

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

related: [CORE_005](../specification/core.md#core_005), [VAL_005](../specification/validation.md#val_005), [CORE_008](../specification/core.md#core_008)

name: validate()

kind: Operation

input: subject: object | Focus, placement: tuple[str, ...] | None = None, structure_specification: StructureSpecification | None = None

output: ValidationResult
