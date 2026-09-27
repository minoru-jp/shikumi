<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/specification/__init__.py` です。
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

# Shikumi Specification

| Document | Summary |
| --- | --- |
| [Core Semantics](core.md) | 実行後の Python 状態を意味像として解釈する Shikumi の中核契約。 |
| [Description Semantics](description.md) | 情報接続、記述器使用、記述方法の責務境界。 |
| [Structure Semantics](structure.md) | 焦点、構造解決、構造規定の一致判定に関する契約。 |
| [Validation Semantics](validation.md) | 検証規則、診断、構造検証、記述器使用検証の契約。 |
| [Realization Semantics](realization.md) | SemanticView を成果物へ変換する Realizer の独立性と check 契約。 |
| [Public API Boundary](public-api.md) | Core、Standard、内部実装の公開境界。 |
| [CLI Semantics](cli.md) | validate / realize command、Python reference、exit code、JSON 応答の契約。 |
