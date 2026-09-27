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
canonical source は `devdocs/canonical_sources/docs/guides/project_layout.py` です。
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

# Project Layout and CLI

Shikumiは専用の配布形式や登録機構を要求しません。規定体、記述体、実現器が通常のPython objectとしてimport可能であれば、library codeからもCLIからも利用できます。

## 推奨する役割分割

project固有のShikumi関連コードは、用途に応じた通常のPython packageへ配置します。`shikumi_lib`のような専用名は必須ではありません。次の役割分割は、大きくなったprojectで責務を見分けやすくするための一例です。

| location | role |
| --- | --- |
| `shikumi_lib/norms/` | 情報型、記述器、構造、検証規則、Shikumi instanceなどの規定体。 |
| `shikumi_lib/realizers/` | 意味像から成果物を作る独立した実現器。 |
| application package | 検証・実現対象となる通常の記述体。shikumi_lib配下へ移す必要はない。 |

小さなprojectでは一つのmoduleへまとめても構いません。別distributionへ分離しても構いません。重要なのは物理名ではなく、それぞれのobjectが通常のPython importで取得できることです。

## CLIはPython参照を結線する

CLIでは`MODULE:OBJECT`形式でShikumi instanceや実現器を指定し、`MODULE`または`MODULE:OBJECT`で記述体を指定します。

repositoryに同梱した structure showcase は、次のコマンドで実際の package tree を構造規定に対して検証できます。

```bash
python -m shikumi validate \
  --shikumi structure_showcase.specification:showcase \
  --body structure_showcase.valid.combined \
  --at . \
  --structure-spec structure_showcase.specification:showcase_structure \
  --format text
```
`realize`も同じ `MODULE:OBJECT` 参照で実現器を結線しますが、公式 showcase は構造規定に焦点を絞るため実現器を持ちません。`realize`は暗黙に検証や実現可能性を実行しないため、必要な検証と実現可能性確認は別の操作として行います。

## 配布

規定体や実現器はShikumi本体とは独立したPython codeとして配布できます。同じdistributionへ同梱しても、別libraryとして配布しても構いません。

Shikumi repositoryの structure showcase は学習用の参考ソースです。repositoryでは`examples/`、wheelでは`shikumi/_examples/`へ配置し、利用者が依存する公開import surfaceから分離します。
