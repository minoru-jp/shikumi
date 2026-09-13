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
正本は `_internal/document_source/examples/structure_from_body/canonical.py` です。
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

# 記述体から構造規定を導出する

この例は、ある記述体を構造として解釈した結果から構造規定を導出し、別の記述体がその構造に適合するかを検証します。

最初の記述体は、別の記述体に対して構造規定を与える材料として使われます。
これは特別なファイル形式ではなく、通常のPython packageです。

## 試す

repository checkoutでは`examples/`をPython pathに置き、通常のPythonコードとして試せます。

```python
from structure_from_body import candidate, reference
from structure_from_body.shikumi_lib.norms import structure_only

specification = structure_only.derive_structure_specification(reference)
result = structure_only.validate(candidate, structure_specification=specification)
assert result.is_valid
```

`reference` packageから構造規定を導出し、`candidate` packageをそれに対して検証します。両者は同じmodule/class配置を持つため、検証は成功します。

## 何を検証しないか

この仕組みが検証するのは構造規定への適合性です。二つの記述体の内容や意味が一致することは、Shikumi自身からは検証されません。

この例では意図的に、`reference.catalog.ITEM_1`と`candidate.catalog.ITEM_1`のdocstringを全く別の内容にしています。それでも構造が一致しているため、構造検証は成功します。

典型的な応用として、原文の文書構造から構造規定を導出し、翻訳版に同じ見出し構造が存在することを確認できます。しかし、翻訳内容の意味的一致まで必要なら、その条件は用途側の情報型や検証規則として別途定義する必要があります。
内容を意図的に異ならせた二つの記述体へ同じ構造規定を適用することも問題ありません。
