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
canonical source は `devdocs/canonical_sources/docs/api/errors.py` です。
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

# Error API

公開 API が明示的に利用者へ伝える例外型。

related: [Public API Boundary](../specification/public-api.md)

## 例外

        

### `ShikumiError`

Shikumi が定義する例外の基底。

name: ShikumiError

kind: Type

### `UnsupportedFocusError`

```python
class UnsupportedFocusError(ShikumiError, TypeError):
    ...
```

構造が与えられた焦点を解釈できない場合に送出する。

name: UnsupportedFocusError

kind: Type

### `UnknownViewSubjectError`

```python
class UnknownViewSubjectError(ShikumiError, LookupError):
    ...
```

意味像に存在しない対象を `SemanticView.item()` で取得しようとした場合に送出する。

---

name: UnknownViewSubjectError

kind: Type
