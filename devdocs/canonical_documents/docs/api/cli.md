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
canonical source は `devdocs/canonical_sources/docs/api/cli.py` です。
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

# CLI Reference

CLI の command line surface。意味上の契約は CLI Specification に分離する。

related: [CLI Semantics](../specification/cli.md)

## CLI: `shikumi`

Shikumi は、規定体が公開する `Shikumi`、記述体となる Python object、独立した実現器を実行時に結線する薄い CLI を提供する。

CLI は規定体、記述体、実現器の登録・探索・所有関係を管理しない。指定された Python 参照を通常の import によって読み込み、その場で処理する。

Python 参照は次の形式を用いる。

```text
module
module:object
module:outer.inner
```

`--shikumi` と `--realizer` は `module:object` を要求する。`--body` は module/package 自体を指定する場合は `module`、実体を焦点にする場合は `module:object` を使用できる。

### `validate`

```bash
shikumi validate \
  --shikumi SPEC_MODULE:SHIKUMI \
  --body DESCRIPTION_MODULE[:OBJECT] \
  [--at PLACEMENT] \
  [--structure-spec SPEC_MODULE:STRUCTURE | --structure-from DESCRIPTION_MODULE[:OBJECT]] \
  [--realizer REALIZER_MODULE:REALIZER] \
  [--format text|json]
```

指定した記述体または実体を `Shikumi.validate()` で検証する。

単独の module を `--body` に指定する場合、`--at` は必須である。値は `api.users` のような構造上の予定配置を dotted path で表し、`.` は構造規定のルートを表す。package 全体を指定した場合は配置を省略できる。

構造規定を利用する場合は、次のどちらか一方を利用者が明示的に選ぶ。

- `--structure-spec MODULE:OBJECT`: 規定体などが Python object として公開した `StructureSpecification` をそのまま使用する。指定 object が存在しない、または型が異なる場合は CLI 設定エラーとし、記述体からの導出へフォールバックしない。
- `--structure-from MODULE[:OBJECT]`: 指定した記述体を現在の Shikumi で解釈し、その構造から `StructureSpecification` を導出する。

`--realizer` を指定すると、通常の検証に加えて `Realizer.check()` を呼び、成果物を生成せずに実現可能性を問い合わせる。規定への適合と実現可能性は別結果として JSON 応答に保持する。どちらかに error があれば command 全体の `ok` は `false` となる。

検証と、指定されている場合の実現可能性検査の双方に error がなければ exit code `0`、一件以上あれば `1` を返す。warning / info のみの場合は `0` とする。

`validate` は成果物を生成しない。

related: [CLI_005](../specification/cli.md#cli_005), [CLI_006](../specification/cli.md#cli_006)

name: validate

kind: Operation

input: --shikumi, --body, --at, --structure-spec | --structure-from, --realizer, --format

output: exit status 0 or 1

### `realize`

```bash
shikumi realize \
  --shikumi SPEC_MODULE:SHIKUMI \
  --body DESCRIPTION_MODULE[:OBJECT] \
  [--at PLACEMENT] \
  --realizer REALIZER_MODULE:REALIZER \
  --output PATH \
  [--format text|json]
```

指定した記述体から意味像を構成し、指定した `Realizer` へ渡して成果物を生成する。`--at` を指定した場合、その構造上の配置を意味像へ反映する。

`realize` は暗黙に validation も `Realizer.check()` も実行しない。規定への適合、実現可能性の問い合わせ、実際の実現は独立した操作として扱う。必要であれば先に `validate --realizer ...` を実行する。

CLI からファイルへ書き出せる成果物は次のいずれかとする。

- `str`: UTF-8 text として書き出す
- `bytes` / bytes-like: binary として書き出す
- JSON serialization 可能な Python 値: UTF-8 JSON として書き出す

それ以外の成果物を返す実現器は、CLI の標準出力契約では直接利用できない。

related: [CLI_007](../specification/cli.md#cli_007), [CLI_008](../specification/cli.md#cli_008)

name: realize

kind: Operation

input: --shikumi, --body, --at, --realizer, --output, --format

output: output file + CLI response

### `--format`

```text
text
json
```

既定値は `text`。

`--format` は **CLI 自身の応答形式**を決める。実現器が生成する成果物の形式を決めるものではない。

`text` は端末で読むために整形されたテキストを出力する。

`json` は LLM、CI、その他のツールから扱うための構造化応答を stdout に出力する。JSON 応答には `format_version` を含める。現在の version は `1`。

例:

```json
{
  "format_version": 1,
  "command": "validate",
  "ok": false,
  "shikumi": "api_spec:api",
  "body": "my_api",
  "focus_kind": "package",
  "placement": null,
  "diagnostic_counts": {
    "error": 1,
    "warning": 0,
    "info": 0
  },
  "diagnostics": [
    {
      "severity": "error",
      "code": "endpoint.path.required",
      "message": "endpoint path is required",
      "subject": "my_api.users.GetUser"
    }
  ],
  "structure": null,
  "realization": null
}
```

実現時に `--output` を指定した場合、成果物はそのファイルへ書き出し、stdout には CLI 応答だけを出力する。この分離により、成果物自体が JSON であっても `--format json` の CLI 応答と混在しない。

CLI が処理できる import、解釈、検証、実現、成果物書き出しの失敗は、`json` 形式では `ok: false` と `error.type` / `error.message` を持つ構造化応答として報告する。

related: [CLI_009](../specification/cli.md#cli_009), [CLI_010](../specification/cli.md#cli_010)

name: --format

kind: Value
