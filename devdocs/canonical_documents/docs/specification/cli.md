<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/specification/cli.py` です。
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

# CLI Semantics

`shikumi` CLI が runtime object を結線して処理する契約。

## CLI_001

CLI は規定体、記述体、Realizer の registry や discovery mechanism を所有せず、指定された Python reference を通常の import で解決する。

title: CLI is a thin runtime wiring layer

level: MUST

related: [API_001](public-api.md#api_001)

## CLI_002

`--shikumi` と `--realizer` は `module:object` を要求し、`--body` は module/package または `module:object` を受理する。

title: Python reference forms

level: MUST

## CLI_003

単独 module を `--body` として validation する場合、`--at` に予定 placement を明示しなければならない。

title: Module validation requires placement

level: MUST

related: [STRUCT_003](structure.md#struct_003)

## CLI_004

`--structure-spec` と `--structure-from` は利用者が明示的に選択する排他的な structure source とし、一方の解決失敗から他方へフォールバックしてはならない。

title: Explicit structure source

level: MUST NOT

related: [STRUCT_006](structure.md#struct_006)

## CLI_005

`validate` は Shikumi.validate() を実行し、`--realizer` が指定された場合だけ追加で Realizer.check() を実行する。成果物を生成してはならない。

title: Validate does not realize

level: MUST NOT

related: [VAL_006](validation.md#val_006), [REAL_002](realization.md#real_002)

## CLI_006

`validate` は validation と任意 realization check の双方に ERROR がない場合 exit code 0、一件以上ある場合 1 を返す。warning と info だけなら 0 とする。

title: Validate exit status

level: MUST

## CLI_007

`realize` は SemanticView を指定 Realizer へ渡して成果物を生成するが、validation または Realizer.check() を暗黙に実行してはならない。

title: Realize is independent from checks

level: MUST NOT

related: [REAL_001](realization.md#real_001)

## CLI_008

CLI が file output として直接扱える成果物は text、bytes-like、または JSON serialization 可能な値とする。

title: CLI artifact serialization

level: MUST

## CLI_009

`--format` は CLI 自身の response format を選択し、Realizer が生成する成果物形式を変更してはならない。

title: Response format and artifact format are separate

level: MUST

## CLI_010

JSON response は `format_version` を含み、現在の format version は `1` とする。output file を指定した場合、成果物は file へ、CLI response は stdout へ分離する。

title: Structured CLI response

level: MUST

condition: `--format json` を使用する場合。
