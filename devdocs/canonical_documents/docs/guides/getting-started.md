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
canonical source は `devdocs/canonical_sources/docs/guides/getting_started.py` です。
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

# Getting Started

このガイドでは、一つのPython classへ意味情報を記述し、Shikumiで意味像を構成し、検証し、最後に文字列へ実現するまでを一周します。

目的はAPIを網羅することではなく、各責務の境界を最小の実行可能な例で確認することです。

## 完全な例

```python
from shikumi import (
    Diagnostic,
    InformationType,
    Realizer,
    Shikumi,
    StructuralKind,
    validator,
)
from shikumi.standard import assignment, information_type_rule

Title = InformationType("title", str)
title = assignment(Title)


class Overview:
    title @= "Overview"


@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic("title is required")


docs = Shikumi(
    information_types=[Title],
    validators=[require_title, information_type_rule(Title)],
)


class HeadingRealizer(Realizer[str]):
    def realize(self, view):
        value = view.focused.values(Title)[0]
        return f"# {value}\n"


result = docs.validate(Overview)
assert result.is_valid

markdown = HeadingRealizer().realize(result.view)
assert markdown == "# Overview\n"
```
このコードは、`Title`という情報型、`title`という記述器、titleを必須にする検証規則、Markdown見出しを生成する実現器を別々に定義しています。

## 責務を分けて読む

| part | responsibility |
| --- | --- |
| `InformationType` | 値が何を意味し、どの型・個数を持つかを定義する。 |
| Descriptor (`assignment`) | Pythonコード上の記述を実行時の情報へ接続する。 |
| `Shikumi` | 認識する情報型、構造、検証規則などを一つの解釈体系として束ねる。 |
| Validator | 構成済みの意味像へ用途固有の条件を適用する。 |
| Realizer | 意味像を読み、Shikumi本体から独立して成果物を生成する。 |

この分離がShikumiの中心です。情報の意味、Python上の記法、妥当性、成果物生成を同じ仕組みに押し込めず、必要な組み合わせを用途側で構成します。

## 次に読む

- 独自のdecoratorや`@=`記述器を作る場合は [`Descriptor Authoring`](./descriptor-authoring.md)。
- 規定体・実現器をprojectへ配置してCLIから結線する場合は [`Project Layout and CLI`](./project-layout.md)。
- 個々の公開名を調べる場合は [`API Reference`](../api/INDEX.md)。
- 実行時確定、構造、検証、実現の厳密な契約は [`Specification`](../specification/INDEX.md)。
