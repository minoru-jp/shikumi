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
正本は `_internal/document_source/examples/web_api/canonical.py` です。
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

# Web API DSL

この例は、独自の情報型と記述器を組み合わせて小さなWeb API DSLを作り、検証とMarkdown実現まで一周する総合例です。

endpoint classにはmethod、path、tag、本文、関連endpointを情報として記述します。
検証規則はentity、module、packageの複数の焦点で適用され、routeの形式や重複を確認します。

## 試す

repository checkoutでは`examples/`をPython pathに置き、通常のPythonコードとして検証とMarkdown実現を試せます。

```python
from web_api import api
from web_api.shikumi_lib.norms import web_api, web_api_structure
from web_api.shikumi_lib.realizers.markdown import markdown

result = web_api.validate(api, structure_specification=web_api_structure)
assert result.is_valid
output = markdown.realize(result.view)
```

作例自体は参考ソースとして配布され、公開import packageやCLI entry pointにはしません。

## 見るべき点

- `@=`、docstring、class参照を同じDSLの中で組み合わせています。
- 記述器使用規則により、各記述器をentityで使うことを明示しています。
- package全体の意味像を実現器へ渡し、複数moduleの情報を一つの成果物へまとめています。
