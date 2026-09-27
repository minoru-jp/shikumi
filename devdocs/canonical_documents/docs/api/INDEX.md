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
canonical source は `devdocs/canonical_sources/docs/api/__init__.py` です。
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

# Shikumi API Reference

| Document | Summary |
| --- | --- |
| [Information API](information.md) | 情報型と実行時情報接続の公開 API。 |
| [Descriptor API](descriptors.md) | 記述器使用、構造上の使用規則、class binding の公開 API。 |
| [Structure API](structure.md) | 構造、焦点、構造規定の公開 API。 |
| [Semantic View API](semantic-view.md) | 意味像と ViewItem の公開 API。 |
| [Shikumi API](shikumi.md) | Shikumi 本体の構成・解釈・検証 API。 |
| [Validation API](validation.md) | 診断、検証規則、構造検証結果の公開 API。 |
| [Realization API](realization.md) | Realizer と realization check の公開 API。 |
| [Standard API](standard.md) | `shikumi.standard` が提供する再利用可能な記述器、情報型、構造、検証規則。 |
| [Error API](errors.md) | 公開例外型。 |
| [CLI Reference](cli.md) | shikumi CLI の command と option。 |
