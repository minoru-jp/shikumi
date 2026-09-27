<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/examples/structure_showcase/canonical.py` です。
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

# 構造ショーケース

この作例は特定の用途ドメインを模倣せず、Shikumi の構造規定が表現できる一般的なパターンを一つの実行可能な fixture 集として示します。

規定本体は [`specification.py`](./specification.py) にあり、`valid/` は受理される構造、`invalid/` は意図的に規定へ違反する構造です。各 fixture は通常の Python package なので、`PackageTreeStructure` が実際の package tree を解決して検証します。

## 含まれる構造パターン

- required / optional な具体名称の要素
- 自由名称および列挙名称を持つ logical element と cardinality
- 同じ parent に置く kind 別の任意名 package / module
- StructureFragment による部分構造の再利用と unconstrained subtree
- StructureFragment.recursive() による任意深度の再帰構造
- StructureGroup による異種 exact sibling の集合 cardinality
- 明示 exact element が logical element より優先される override

## fixture の構成

`valid/minimal/` は required element だけを持つ最小構造です。`valid/combined/` は上記のパターンを一つの package tree にまとめています。

`invalid/` には missing required element、空の logical collection、列挙外名称、group cardinality 違反、closed subtree への余分な要素をそれぞれ分離して置いています。invalid fixture は「失敗する作例」であり、その診断コードもテストで固定します。

## 試す

repository checkout では `examples/` を Python path に置いて実行できます。

```python
from structure_showcase.invalid import group_both
from structure_showcase.specification import showcase, showcase_structure
from structure_showcase.valid import combined

valid_result = showcase.validate(
    combined,
    placement=(),
    structure_specification=showcase_structure,
)
assert valid_result.is_valid
assert valid_result.structure_check is not None
assert {binding.logical_element.logical_name for binding in valid_result.structure_check.bindings} >= {
    "entry",
    "variant",
    "package_child",
    "module_child",
    "branch",
    "module_leaf",
    "ordinary",
}

invalid_result = showcase.validate(
    group_both,
    placement=(),
    structure_specification=showcase_structure,
)
assert not invalid_result.is_valid
assert {diagnostic.code for diagnostic in invalid_result.diagnostics} == {
    "structure.group.maximum",
}
```
