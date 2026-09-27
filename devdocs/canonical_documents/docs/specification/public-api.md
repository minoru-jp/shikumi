<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/specification/public_api.py` です。
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

# Public API Boundary

Shikumi distribution が利用者へ約束する import surface。

## API_001

公開 Python API は `shikumi` と `shikumi.standard` が明示的に export する名前から構成する。文書化されない内部 module の import path は公開契約に含めない。

title: Documented exports define the public surface

level: MUST

## API_002

Core (`shikumi`) は情報、runtime binding、構造、意味像、Shikumi、validation、realization の抽象契約を提供する。

title: Core owns the semantic primitives

level: INFORMATIVE

## API_003

Standard (`shikumi.standard`) は Core を組み合わせた再利用可能な記述器、標準構造、標準 validation rule を提供し、新しい意味モデルを導入しない。

title: Standard builds on Core

level: MUST

## API_004

`kind`、`attr`、`rel` のような用途固有語彙を Standard が暗黙に定義または登録してはならない。用途固有語彙は規定体が通常の Python 定義として所有する。

title: Domain vocabulary belongs to the specification author

level: MUST NOT

related: [CORE_007](core.md#core_007)

## API_005

独自 decorator、metaclass、base class、mixin が Python 標準の class creation や記述器実行順序を変更する組合せについて、Shikumi は互換処理を保証しない。

title: Python class-creation interactions are outside compatibility guarantees

level: INFORMATIVE
