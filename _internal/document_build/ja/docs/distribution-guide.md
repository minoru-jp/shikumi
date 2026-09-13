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
正本は `_internal/document_source/distribution_guide/canonical.py` です。
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

# 規定体・記述体・実現器の配置

この文書は、規定体、記述体、実現器を、最終的に CLI から通常の Python import で参照できる形へ分かりやすく配置するための指針を示す。

Shikumi は専用の配布形式や登録機構を要求しない。重要なのは、利用する Python object が import 可能であり、CLI からその参照を指定できることである。

## 目的

CLI は、規定体が公開する `Shikumi`、記述体、実現器などを `MODULE:OBJECT` 形式の Python 参照として受け取る。

したがって配置の目的は、これらを特別な Shikumi 用形式へ変換することではなく、通常の Python module/package として import 可能にし、どの object がどの役割を担うかを分かりやすく保つことである。

規定体、記述体、実現器は物理形式ではなく役割であり、同じ module/package や distribution に同梱してもよい。

## 推奨配置

プロジェクト固有の Shikumi 関連コードは、公式の作例では `shikumi_lib` package にまとめ、その中を `norms` と `realizers` に分ける。

```text
project/
├─ shikumi_lib/
│  ├─ __init__.py
│  ├─ norms/
│  │  ├─ __init__.py
│  │  └─ ...
│  └─ realizers/
│     ├─ __init__.py
│     └─ ...
└─ application/
   └─ ...
```

`norms` には、規定体として利用する情報型、記述器、構造、検証規則、`Shikumi` インスタンスなどを置く。`realizers` には、意味像から成果物を生成する実現器を置く。

記述体は、検証や実現の対象となる通常の Python module/package そのものであり、`shikumi_lib` の下へ移す必要はない。

`shikumi_lib` という名前は、本体の import package `shikumi` との衝突を避けつつ、そのプロジェクト固有の Shikumi 関連コードであることを一目で示すための作例である。

## CLI から参照する

たとえば、次のような配置を想定する。

```text
myproject/
├─ shikumi_lib/
│  ├─ norms/
│  └─ realizers/
└─ application/
```

検証では、規定体と記述体を通常の import path で指定する。

```bash
shikumi validate \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --structure-spec myproject.shikumi_lib.norms:structure \
  --format text
```

実現では、さらに実現器を指定する。

```bash
shikumi realize \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --realizer myproject.shikumi_lib.realizers.markdown:markdown \
  --output OUTPUT.md \
  --format json
```

CLI から参照できることが確認できれば、配置上の目的は達成されている。

## 配置と配布の自由

`shikumi_lib/norms` と `shikumi_lib/realizers` は、役割を分かりやすくするための推奨作例であり、Shikumi の要求ではない。

小さな構成では単一 module にまとめてもよい。複数の役割を同じ distribution に同梱しても、別々のライブラリとして配布してもよい。名前や分割方法も、通常の Python ライブラリ設計として変更できる。

規定体や実現器は Shikumi 本体とは独立した Python コードとして配布でき、独立して作成したコードには作者が任意のライセンスを設定できる。ただし、取り込んだ第三者コードにはそのライセンスが適用される。

公式作例は参考ソースとして本体distributionに同梱する。ただし、作例そのものは公開import packageやCLI entry pointではない。repositoryでは`examples/`、wheelでは`shikumi/_examples/`に配置し、利用者コードが依存する公開面から分離する。

実際の利用者プロジェクトでは、必要な object が通常の Python import で取得でき、利用時に明示的に参照できればよい。
