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
正本は `_internal/document_source/examples/structured_docs/canonical.py` です。
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

# 構造化文書の実現

この例は、Python上の記述から意味像を構成し、独立した実現器でMarkdownへ実現する例です。

command名、category、docstringの本文をそれぞれ情報型として扱います。
検証は記述が規定を満たしているかを確認し、Markdown実現器は同じ意味像から公開用の一覧を生成します。

## 試す

repository checkoutでは`examples/`をPython pathに置き、通常のPythonコードとして検証と実現を試せます。

```python
from structured_docs import body
from structured_docs.shikumi_lib.norms import structured_docs
from structured_docs.shikumi_lib.realizers.markdown import markdown

result = structured_docs.validate(body)
assert result.is_valid
output = markdown.realize(result.view)
```

`output`には`deploy`と`status`の説明を含むMarkdownが入ります。

## 見るべき点

- `@command(...)`、`category @= ...`、docstringという異なる記法が、それぞれ情報として同じ意味像へ現れます。
- 実現器はShikumiに登録されず、意味像を受け取る独立したコンポーネントです。
- `check()`による実現可能性の判定と`realize()`による実現は別の操作です。
