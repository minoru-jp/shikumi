<!-- shikumi-devdoc:translation-metadata
{
  "version": 1,
  "publication": "omit-this-comment",
  "preserve_spelling": [
    {
      "source": "devdocs.canonical_sources.docs.vocabulary",
      "identifier": "TERM_1",
      "text": "Shikumi"
    },
    {
      "source": "devdocs.canonical_sources.docs.vocabulary",
      "identifier": "TERM_33",
      "text": "shikumi_lib"
    }
  ]
}
-->

<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/guides/__init__.py` です。
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

# Shikumi Guides

| Document | Summary |
| --- | --- |
| [Getting Started](getting-started.md) | 情報型、記述器、検証、実現を一つの小さな例で通して理解する入門ガイド。 |
| [記述器を定義する](descriptor-authoring.md) | 通常の Python を使って decorator や @= 記述器を定義する実装ガイド。 |
| [Project Layout and CLI](project-layout.md) | 規定体、実現器、記述体をprojectへ配置し、通常のPython参照としてCLIから結線するガイド。 |
