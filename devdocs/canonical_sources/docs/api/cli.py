"""Canonical Japanese API reference source for CLI Reference."""

from devdocs.canonical_sources.docs.vocabulary import TERMS
from shikumi_devdoc.fields.api_reference import (
    NAMESPACE, OPERATION, OTHER, TYPE, VALUE,
    input, kind, name, output, related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.docs.specification.cli import SPECIFICATION_PART as CLI_SPEC

@summary('shikumi CLI の command と option。')
@canonical_source('CLI Reference', filename='cli.md', order=90, heading="title")
class API_REFERENCE_PART:
    """CLI の command line surface。意味上の契約は CLI Specification に分離する。"""

    related @= CLI_SPEC

    class TITLE_85:
        r'''
        {{TERM_1}} は、{{TERM_3}}が公開する `{{TERM_1}}`、{{TERM_5}}となる Python object、独立した{{TERM_26}}を実行時に結線する薄い CLI を提供する。

        CLI は{{TERM_3}}、{{TERM_5}}、{{TERM_26}}の登録・探索・所有関係を管理しない。指定された Python 参照を通常の import によって読み込み、その場で処理する。

        Python 参照は次の形式を用いる。

        ```text
        module
        module:object
        module:outer.inner
        ```

        `--shikumi` と `--realizer` は `module:object` を要求する。`--body` は module/package 自体を指定する場合は `module`、{{TERM_11}}を{{TERM_20}}にする場合は `module:object` を使用できる。
        '''
        title @= 'CLI: `{{PROJECT.cli_entry_point}}`'

        merge @= TERMS.TERM_1
        merge @= TERMS.TERM_3
        merge @= TERMS.TERM_5
        merge @= TERMS.TERM_26
        merge @= TERMS.TERM_11
        merge @= TERMS.TERM_20

        class TITLE_86:
            r'''
            ```bash
            {{PROJECT.cli_entry_point}} validate \
              --shikumi SPEC_MODULE:SHIKUMI \
              --body DESCRIPTION_MODULE[:OBJECT] \
              [--at PLACEMENT] \
              [--structure-spec SPEC_MODULE:STRUCTURE | --structure-from DESCRIPTION_MODULE[:OBJECT]] \
              [--realizer REALIZER_MODULE:REALIZER] \
              [--format text|json]
            ```

            指定した{{TERM_5}}または{{TERM_11}}を `{{TERM_1}}.validate()` で{{TERM_21}}する。

            単独の module を `--body` に指定する場合、`--at` は必須である。値は `api.users` のような{{TERM_7}}上の予定配置を dotted path で表し、`.` は{{TERM_8}}のルートを表す。package 全体を指定した場合は配置を省略できる。

            {{TERM_8}}を利用する場合は、次のどちらか一方を利用者が明示的に選ぶ。

            - `--structure-spec MODULE:OBJECT`: {{TERM_3}}などが Python object として公開した `StructureSpecification` をそのまま使用する。指定 object が存在しない、または型が異なる場合は CLI 設定エラーとし、{{TERM_5}}からの導出へフォールバックしない。
            - `--structure-from MODULE[:OBJECT]`: 指定した{{TERM_5}}を現在の {{TERM_1}} で{{TERM_18}}し、その{{TERM_7}}から `StructureSpecification` を導出する。

            `--realizer` を指定すると、通常の{{TERM_21}}に加えて `Realizer.check()` を呼び、{{TERM_28}}を生成せずに{{TERM_27}}を問い合わせる。{{TERM_2}}への適合と{{TERM_27}}は別結果として JSON 応答に保持する。どちらかに error があれば command 全体の `ok` は `false` となる。

            {{TERM_21}}と、指定されている場合の{{TERM_27}}検査の双方に error がなければ exit code `0`、一件以上あれば `1` を返す。warning / info のみの場合は `0` とする。

            `validate` は{{TERM_28}}を生成しない。
            '''
            title @= '`validate`'
            related @= CLI_SPEC.CLI_005
            related @= CLI_SPEC.CLI_006

            name @= 'validate'
            kind @= OPERATION
            input @= '--shikumi'
            input @= '--body'
            input @= '--at'
            input @= '--structure-spec | --structure-from'
            input @= '--realizer'
            input @= '--format'
            output @= 'exit status 0 or 1'


            merge @= TERMS.TERM_5
            merge @= TERMS.TERM_11
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_21
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_8
            merge @= TERMS.TERM_3
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_28
            merge @= TERMS.TERM_27
            merge @= TERMS.TERM_2

        class TITLE_87:
            r'''
            ```bash
            {{PROJECT.cli_entry_point}} realize \
              --shikumi SPEC_MODULE:SHIKUMI \
              --body DESCRIPTION_MODULE[:OBJECT] \
              [--at PLACEMENT] \
              --realizer REALIZER_MODULE:REALIZER \
              --output PATH \
              [--format text|json]
            ```

            指定した{{TERM_5}}から{{TERM_19}}を構成し、指定した `Realizer` へ渡して{{TERM_28}}を生成する。`--at` を指定した場合、その{{TERM_7}}上の配置を{{TERM_19}}へ反映する。

            `realize` は暗黙に validation も `Realizer.check()` も実行しない。{{TERM_2}}への適合、{{TERM_27}}の問い合わせ、実際の{{TERM_25}}は独立した操作として扱う。必要であれば先に `validate --realizer ...` を実行する。

            CLI からファイルへ書き出せる{{TERM_28}}は次のいずれかとする。

            - `str`: UTF-8 text として書き出す
            - `bytes` / bytes-like: binary として書き出す
            - JSON serialization 可能な Python 値: UTF-8 JSON として書き出す

            それ以外の{{TERM_28}}を返す{{TERM_26}}は、CLI の標準出力契約では直接利用できない。
            '''
            title @= '`realize`'
            related @= CLI_SPEC.CLI_007
            related @= CLI_SPEC.CLI_008

            name @= 'realize'
            kind @= OPERATION
            input @= '--shikumi'
            input @= '--body'
            input @= '--at'
            input @= '--realizer'
            input @= '--output'
            input @= '--format'
            output @= 'output file + CLI response'


            merge @= TERMS.TERM_5
            merge @= TERMS.TERM_19
            merge @= TERMS.TERM_28
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_2
            merge @= TERMS.TERM_27
            merge @= TERMS.TERM_25
            merge @= TERMS.TERM_26

        class TITLE_88:
            r'''
            ```text
            text
            json
            ```

            既定値は `text`。

            `--format` は **CLI 自身の応答形式**を決める。{{TERM_26}}が生成する{{TERM_28}}の形式を決めるものではない。

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

            {{TERM_25}}時に `--output` を指定した場合、{{TERM_28}}はそのファイルへ書き出し、stdout には CLI 応答だけを出力する。この分離により、{{TERM_28}}自体が JSON であっても `--format json` の CLI 応答と混在しない。

            CLI が処理できる import、{{TERM_18}}、{{TERM_21}}、{{TERM_25}}、{{TERM_28}}書き出しの失敗は、`json` 形式では `ok: false` と `error.type` / `error.message` を持つ構造化応答として報告する。
            '''
            title @= '`--format`'
            related @= CLI_SPEC.CLI_009
            related @= CLI_SPEC.CLI_010

            name @= '--format'
            kind @= VALUE


            merge @= TERMS.TERM_26
            merge @= TERMS.TERM_28
            merge @= TERMS.TERM_25
            merge @= TERMS.TERM_18
            merge @= TERMS.TERM_21

