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
正本は `_internal/document_source/examples/architecture/canonical.py` です。
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

# アーキテクチャ検証

この例は、Shikumiを使って用途固有のアーキテクチャ規則を定義し、Python上の記述を検証する最小例です。

`domain`、`application`、`infrastructure`という層を情報型として定義し、class間の依存関係を別の情報型として記述します。
Shikumi自身はこれらの層や依存規則を知りません。どの依存方向を許可するかは、この例の規定体が定めています。

この例が検証するのは`DependsOn`として明示された依存です。実際のPython importやcall graphを自動検出する例ではありません。

## 試す

repository checkoutでは`examples/`をPython pathに置けば、通常のPythonコードとして試せます。

```python
from architecture import body
from architecture.shikumi_lib.norms import architecture

result = architecture.validate(body)
assert result.is_valid
```

`domain`のclassから`application`のclassへ依存するように記述を変更すると、検証規則が依存方向の違反を報告します。

## 見るべき点

- `Layer`と`DependsOn`はこの例が定義した情報型です。
- `@layer(...)`と`depends_on @= ...`は、この例の意味をPython上へ書くための記述器です。
- 依存方向の判定はpackageを焦点とする検証規則として実装されています。
- classはShikumiのbase classやmetaclassを必要としません。
