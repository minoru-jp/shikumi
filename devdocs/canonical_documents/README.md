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
canonical source は `devdocs/canonical_sources/readme.py` です。
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

# Shikumi

Shikumiは、**Python上に独自の意味・構造・規則を持つ仕組みを作るためのライブラリ**です。

構造化ドキュメント生成器、独自DSL、アーキテクチャ検証などを直接提供するのではなく、用途側が情報型、記述器、構造、検証規則、実現器を組み合わせてそれらを構築するための共通基盤を提供します。

ShikumiはPythonの実行後に成立した対象を解釈し、意味像を構成します。同じ意味像を検証にも実現にも利用できます。

## 主な用途

- Pythonコード上の記述からMarkdown、設定、レポートなどの成果物を生成する。
- 用途固有の属性・分類・関係を持つPythonベースのDSLを構築する。
- package、module、classの構造や依存方向を定義して検証する。
- 同じ規定を複数のPython packageへ適用する。
- LLMとの協調作業で、意味と構造を明示した機械可読な記述を利用する。

これらの用途固有の意味はShikumi本体には組み込まれていません。利用者が目的に応じた規定として定義します。

## インストール

```bash
pip install shikumi
```

現在のバージョンは `0.2.0` です。Python `>=3.11` を対象としています。0.2.0 から開発段階は Beta です。

## 最小例

次の例では、`title`という情報型を定義し、`@=`とdecoratorから同じ意味情報を記述します。さらに、実体にはtitleが必要という検証規則を適用します。

```python
from shikumi import (
    DescriptorUseRule,
    Diagnostic,
    InformationType,
    Shikumi,
    StructuralKind,
    StructureSelector,
    validator,
)
from shikumi.standard import assignment, decorator, information_type_rule

Title = InformationType("title", str)
title = assignment(Title)
titled = decorator(Title)


class Overview:
    title @= "Overview"


@titled("Tutorial")
class Tutorial:
    pass


@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic("title is required")


docs = Shikumi(
    information_types=[Title],
    validators=[require_title, information_type_rule(Title)],
    descriptor_rules=[
        DescriptorUseRule(
            descriptor=title,
            allowed=StructureSelector(kind=StructuralKind.ENTITY),
            name="title",
        )
    ],
)

assert docs.view(Overview).focused.values(Title) == ("Overview",)
assert docs.validate(Overview).is_valid
```
`InformationType`は「何を意味するか」を定義し、Python上で「どう書くか」は記述器が担います。`view()`は意味像を構成し、`validate()`はその意味像へ検証規則を適用します。

続けて実現まで含む一連の流れを試す場合は [`Getting Started`](./docs/guides/getting-started.md) を参照してください。

## 実行モデルと安全性

ShikumiはsourceをASTとして意味解析する静的解析器ではありません。moduleやpackageを対象にすると通常のPython importとして実行され、その後に成立したruntime object、情報、記述器使用を解釈します。

したがって、**Shikumiへ渡すmoduleやpackageは信頼できるPythonコードだけにしてください。** 検証目的であってもimport時のコードは通常の権限で実行されます。

実行時確定、構造、検証、実現の厳密な契約は [`Specification`](./docs/specification/INDEX.md) にまとめています。

## 公式作例

[`structure_showcase`](./examples/structure_showcase/README.md) は、特定用途の完成例ではなく、構造規定で表現できる一般的な構造パターンを valid / invalid fixture としてまとめた実行可能なショーケースです。

単一機能の使い方は Guides と API Reference の検証済みコード例へ置き、`examples/` は複数の構造プリミティブを組み合わせた完成形だけを扱います。

## 文書

- [`Guides`](./docs/guides/INDEX.md): はじめ方、記述器の実装、project配置とCLI結線。
- [`Glossary`](./docs/glossary.md): 用語の正規定義。
- [`API Reference`](./docs/api/INDEX.md): 公開Python APIとCLI surface。
- [`Specification`](./docs/specification/INDEX.md): Shikumiが保証する意味上・互換性上の契約。
- [`STATUS`](./STATUS.md): 現在の開発段階、互換性方針、1.0への移行基準、配布上の既知制約。
- [`CHANGELOG`](./CHANGELOG.md): 公開releaseごとの主な変更。

概念の意味はGlossary、規範的な挙動はSpecification、名前単位の利用方法はAPI Referenceを基準とします。

## License

MIT License. See [`LICENSE`](./LICENSE).
