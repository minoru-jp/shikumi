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
正本は `_internal/document_source/changelog/canonical.py` です。
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

# Changelog

Shikumiの公開リリースごとの主な変更を記録します。

## Unreleased

次の公開リリースへ向けた変更です。

### Changed

- **Breaking:** 公式作例をトップレベルの`shikumi_examples` import packageから`examples/`の参考ソースへ移し、wheelでは`shikumi/_examples/`に同梱するよう変更しました。作例の`python -m`実行入口を削除し、利用者コードが依存する公開面から分離しました。

## 0.1.0 - 2026-09-12

初回公開リリースです。

### Added

- 情報、記述器使用、構造、意味像を分離したCoreの意味モデルを追加しました。
- 実体・module・packageを同じ仕組みで扱う検証と、独立した実現器による実現を追加しました。
- デコレータ、`@=`、docstring、package treeなど、再利用可能なStandardの記述器と構造実装を追加しました。
- 規定体、記述体、実現器を通常のPython参照として結線するCLIを追加しました。
- README、Glossary、API Reference、Distribution Guideからなる英語の公開文書体系を追加しました。公開文書は日本語のcanonical document sourceを正本として生成・翻訳します。
- architecture、structured docs、Web API、`structure-from`の4方向を示す公式作例を追加しました。
