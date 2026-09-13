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
正本は `_internal/document_source/readme/canonical.py` です。
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

# Shikumi

Shikumiは、**構造化ドキュメント生成器、独自DSL、アーキテクチャ検証ツールなどをPython上に構築するためのライブラリ**です。

ただし、Shikumi自身がそれらの機能を個別に提供するわけではありません。

どのような要素が存在し、どのような属性や関係を持ち、どのような構造に属し、何を正しい状態とみなし、
その意味像から何を作り出すかを、利用者自身が規定として定義します。

たとえば、その意味像をMarkdownへ変換すればドキュメント生成になります。
「service」「entity」「uses」といった独自の情報型と記述方法を作ればDSLになります。
「application層からdomain層への依存だけを許可する」という規則を作ればアーキテクチャ検証になります。

つまりShikumiが扱うのは、アーキテクチャ、DSL、文書そのものではありません。
**Python上に独自の意味とルールを持つ仕組みを作り、それを解釈し、利用するための共通基盤です。**

## 主な用途

Shikumiは、たとえば次のような用途に利用できます。

- Pythonコード上の記述から構成された意味像から、文書、設定、レポートなどの成果物を生成する
- LLMとの迅速な意思疎通のために、意味と構造を明示した文書を作成する
- Pythonのclassやmoduleに、用途固有の属性・分類・関係を記述する
- 独自の記述器や情報型を持つPythonベースのDSLを構築する
- プロジェクトが持つべきpackage、module、classの構造を定義する
- 同じ規定を複数のPython packageへ適用する
- ソフトウェアアーキテクチャの構造や依存方向を表現し、それを検証する仕組みを構築する

これらはShikumi自身に組み込まれた用途ではありません。
利用者が目的に応じた規定を作ることで実現します。

## インストール

```bash
pip install shikumi
```

現在のバージョンは `0.1.0` です。

ShikumiはPython `>=3.11` を対象としています。

## クイックスタート

次の例では、`title`という情報型を作り、`@=`とデコレータという2種類の記述器から記述します。

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

`InformationType`は「何を意味するか」を定義し、Python上で「どう書くか」は記述器が担います。
`Shikumi`は認識する情報型、検証規則、記述器使用規則などを組み合わせ、`view()`で意味像を構成し、`validate()`で検証します。

`title @= "Overview"`は通常の属性代入ではありません。
`assignment(Title)`が作る記述器が、class成立後に`Overview`へ情報を接続します。
`@=`は、class本体の自然な形を保ったまま、規定側で定めた意味を記述するためのStandardの記法です。

## 警告

**Shikumiに渡すmoduleやpackageは、信頼できるPythonコードだけにしてください。**

ShikumiはPythonの実行後に成立した対象を解釈します。moduleやpackageをimport pathで指定した場合、それらは通常のPythonとしてimportされ、実際に実行されたうえで意味像が構成されます。
これは、その意味像を検証に使う場合でも、実現に使う場合でも変わりません。対象コードは、通常のimportと同じ権限で任意の処理を実行できます。

特に検証は、安全な隔離環境で対象を静的に検査する機能ではありません。内容を信頼できないmoduleやpackageを、安全性確認のためにShikumiへ渡してはいけません。

## 実行時確定原則

ShikumiはPython sourceをASTとして読み直しません。
記述体となるmoduleやpackageは通常のPythonとしてimportされ、その実行後に成立したruntime object、情報、記述器使用を観測します。

```text
Python source
    ↓ execute / import
実行時の対象 + 情報 + 記述器使用
    ↓
Shikumi
    ↓ interpretation
意味像
   /          \
検証           実現
                 ↓
              成果物
```

したがって、検証のために対象moduleを読み込む場合も、そのmoduleのトップレベルコードは通常のimportと同様に実行されます。
Shikumiは、実行せずに安全性を判定する静的解析器ではありません。

## 自動では解析しないもの

Shikumiは、Python ASTやsource syntax、実際のimport graphやcall graph、まだimportされていないmoduleを自動では解析しません。
また、標準の`PythonStructure`はfunctionやmethodを実体として扱いません。必要な情報や対象は、用途側の規定や独自構造で明示します。

## 検証と実現

Shikumiは、Python上の対象とそこに接続された情報を構造に従って読み取り、意味像を構成します。

検証では、その意味像に検証規則を適用します。
package内に必要なmoduleが存在するか、classに必要な情報があるか、要素間の関係が規則を満たすか、といった条件を用途ごとに定義できます。

意味像は検証だけのためのものではありません。
独立した実現器を適用することで、Markdown、設定、レポートなど任意の成果物へ実現できます。
同じ意味像へ複数の実現器を適用することもできます。

## Standard

`shikumi.standard`は、Coreの仕組みから構成した再利用可能な具体機能を提供します。

主なものには、`@=`用の`assignment`、デコレータ用の`decorator`、docstringを情報化する`docstring`、package treeを通常のimportで解釈する`PackageTreeStructure`があります。

`service`、`entity`、`layer`、`term`など用途固有の意味はStandardには含まれません。
それらは利用者の規定として定義します。

## CLI

CLIでは、規定体が公開する`Shikumi`、記述体、独立した実現器を通常のPython importで指定して結線できます。

CLIのentry pointは`shikumi`です。`python -m shikumi`からも同じCLIを実行できます。

検証:

```bash
shikumi validate \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --structure-spec myproject.shikumi_lib.norms:app_structure \
  --format text
```

実現:

```bash
shikumi realize \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --realizer myproject.shikumi_lib.realizers.markdown:markdown \
  --output API.md \
  --format json
```

`realize`は暗黙に検証や実現可能性の問い合わせを行いません。
それぞれは独立した操作として扱われます。

## サンプル

[`examples/`](./examples/)には、異なる方向からShikumiを使う4つの公式作例があります。これらは参考ソースとしてdistributionにも同梱しますが、公開import packageやCLI entry pointではありません。

- [`architecture`](./examples/architecture/README.md) — 用途固有の依存規則を検証規則として定義し、アーキテクチャを検証する
- [`structured_docs`](./examples/structured_docs/README.md) — Python上の記述から意味像を構成し、Markdownへ実現する
- [`web_api`](./examples/web_api/README.md) — 独自DSL、検証、実現を組み合わせた総合例
- [`structure_from_body`](./examples/structure_from_body/README.md) — ある記述体から構造規定を導出し、別の記述体の構造適合性を検証する

## 関連文書

- [`docs/glossary.md`](./docs/glossary.md) — Shikumiで使用する用語と、その意味上の境界
- [`docs/api-reference.md`](./docs/api-reference.md) — 公開APIとその契約
- [`docs/distribution-guide.md`](./docs/distribution-guide.md) — 規定体、記述体、実現器の配置と配布
- [`CHANGELOG.md`](./CHANGELOG.md) — 公開リリースごとの主な変更
- [`examples/`](./examples/) — distributionにも参考ソースとして同梱する4つの公式作例

概念の厳密な定義は用語集を基準とします。

## 公開文書について

公開文書はすべて英語で提供します。
`_internal/document_source/`以下のcanonical document sourceを正本とし、`shikumi-devdoc`で`_internal/document_build/ja/`へ生成した日本語中間文書を翻訳元として公開版を配置します。
中間文書は生成結果をレビューできるようリポジトリへcommitしますが、直接編集しません。内容に差異がある場合はcanonical document sourceを基準とします。

## License

MIT License. See [`LICENSE`](./LICENSE).
