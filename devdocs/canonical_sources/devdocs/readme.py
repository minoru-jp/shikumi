"""Canonical Japanese source for the devdocs workspace README."""

from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import test_target_field, title

render_command = test_target_field("render command")
check_command = test_target_field("check command")


@canonical_source(
    "devdocs",
    filename="README.md",
    merge_policy="local",
    heading="title",
)
class DEVDOCS_README:
    """
    このリポジトリでは、公開文書とリポジトリ専用文書を `devdocs/` の canonical source から生成する。

    配置済み Markdown は正本ではない。変更は canonical source から開始し、`shikumi-devdoc` による validation / realization、canonical document のレビュー、翻訳、配置という一方向の工程で反映する。
    """

    class SECTION_001:
        """
        `shikumi-devdoc` はこのリポジトリの文書生成に使う開発時ツールであり、`shikumi` package の実行時依存ではない。

        package としては `shikumi-devdoc` が `shikumi` を利用する。一方、このリポジトリは開発工程で `shikumi-devdoc` を利用する。そのため `shikumi-devdoc` の version 制約は `[dependency-groups].docs` に一元化し、test group は docs group を include して test extra を追加する。CI もこれらの dependency group を利用し、`[project.dependencies]` には追加しない。

        文書生成時には checkout 中の `src/shikumi` を import 可能にし、開発中の Shikumi 実装で canonical source を解釈する。
        """

        title @= "依存関係"

    class SECTION_002:
        """
        文書内容の正本は `devdocs/canonical_sources/` に置く Python の **canonical source** である。

        `devdocs/canonical_documents/` の日本語 Markdown は、canonical source と realization context を `shikumi-devdoc` で実現した **canonical document** である。生成結果をレビュー可能にするため commit するが、直接編集しない。

        リポジトリ直下、`docs/`、`examples/*/README.md`、この `devdocs/README.md` などに置く英語 Markdown は canonical document から翻訳・配置した **published document** である。

        canonical source、canonical document、published document に差異がある場合、文書内容については canonical source を基準とする。文書が説明する Python 実装そのものはこの規則の対象外であり、通常どおり実装側が正本である。
        """

        title @= "文書の三つの境界"

    class SECTION_003:
        """
        `devdocs/` は次の責務で分ける。

        - `README.md`: この文書開発 workspace の入口と運用規則。
        - `canonical_sources/`: Python で記述する文書の正本。
        - `canonical_documents/`: commit する日本語 canonical document。
        - `config/`: realization 時に明示的に与える固定設定。現在は生成 notice を保持する。

        Vocabulary term の参照用 Python module は生成しない。文書は Vocabulary の canonical term class を `merge` で直接参照する。Glossary は公開を既定値とし、非公開にする term だけ `glossary @= False` を明示する。
        """

        title @= "ワークスペース"

    class SECTION_003A:
        """
        リポジトリに配置する文書は責務ごとに次のように分ける。

        - `README.md`: project の入口、用途、最小例、主要な導線。
        - `docs/glossary.md`: 用語の正規定義。
        - `docs/api/`: 現在の公開 Python API / CLI surface を名前から引くための reference collection。
        - `docs/specification/`: 実装と互換性が従う意味上の契約を、独立して参照可能な規則として記録する specification collection。
        - `docs/guides/`: Getting Started、記述器 authoring、project 配置と CLI 結線などの実践手順をまとめる guide collection。
        - `examples/`: 一般的な構造規定を valid / invalid fixture で示す実行可能なショーケース。
        - `CHANGELOG.md`: release 単位の過去の変更。
        - `devdocs/README.md`: リポジトリ保守者向けの文書 authoring / generation workflow。

        API Reference に設計契約や長い tutorial を混在させない。契約は Specification、実践手順は Guides、概念定義は Glossary へ置く。README は入口と最小例に絞り、詳細な手順を抱え込まない。
        """

        title @= "文書の責務"

    class SECTION_004:
        """
        canonical source を変更したら、次のコマンドで canonical document を再生成する。

        ```bash
        {{render_command}}
        ```
        生成結果を確認した後、英語の published document へ翻訳・配置する。最後に drift 検査を行う。

        ```bash
        {{check_command}}
        ```
        基本手順は次のとおり。

        1. canonical source を作成または更新する。
        2. canonical document を再生成する。
        3. 日本語 canonical document の差分を確認する。
        4. canonical document を英語へ翻訳する。
        5. 翻訳結果を published document の位置へ配置する。
        6. drift、文書上のコード例、リンク、公開名、distribution 配置をテストする。
        """

        title @= "基本フロー"

        render_command @= "python scripts/render_canonical_docs.py"
        check_command @= "python scripts/render_canonical_docs.py --check"

    class SECTION_005:
        """
        project 名、version、`requires-python`、公開 import package、CLI entry point、distribution 名など、すでに `pyproject.toml` に正本を持つ値は canonical source に重複して固定しない。

        `scripts/render_canonical_docs.py` が `pyproject.toml` から realization context を構築して `shikumi-devdoc` へ渡す。固定的な生成上の注意事項は `devdocs/config/notice.toml` から明示的に渡す。
        """

        title @= "Realization context"

    class SECTION_006:
        """
        文書に掲載するコード、command、設定、期待出力などのうち、値そのものを通常のテストから直接検証する価値があるものは `test_target_field` として prose から分離し、対応するテストを作る。

        特に公開 API の使用例、import、descriptor の定義、validation / realization の例は原則としてテスト対象にする。単独では成立しない短い式、疑似コード、構造図などは、機械的に `test_target_field` へ移さず用途に応じて扱う。

        `test_target_field` は Markdown presentation を所有しない。掲載時の fenced block と language は docstring / prose template 側へ明示し、field はテスト対象となる literal text だけを保持する。API signature、dataclass の形状、列挙値など、実行例ではなく公開面そのものを示す fence は prose 側に直接書いてよい。

        intentionally invalid なコードを掲載する場合は、失敗することが契約として重要なら、その失敗もテストする。
        """

        title @= "文書上のコード"

    class SECTION_007:
        """
        新しい文書では、最初に読者と責務を決める。既存ファイルへ追加するか collection を作るかは、行数ではなく変更責務・参照先・読者の目的が独立しているかで判断する。

        canonical source は generic document model を基盤とし、構造化する意味がある情報だけを field に分離する。nested node の human-readable title は `title @= ...` に統一し、必要なら同じ node の `merge` を通じて Vocabulary reference を title でも利用する。

        `@canonical_source(...)` では nested heading policy を `heading="title"` または `heading="identity"` として明示する。通常の narrative / API / guide 文書では human-readable title を見出しにする `title` policy を使い、nested node が semantic reference の安定した target になる Specification では `identity` policy を使う。

        API Reference、Specification、CHANGELOG などでは `shikumi_devdoc.fields` の標準 field set を目的に応じて利用できる。collection にする場合は各ページを独立 canonical document とし、`@summary(...)` と必要な `order` を metadata として与え、`render index` で `INDEX.md` を別 realization する。
        """

        title @= "新しい文書を追加する"

    class SECTION_008:
        """
        published document は英語で提供する。翻訳では canonical document が持つ意味、章構造、semantic field、コード例、公開 API 名、Python 名、CLI 名、パスを保つ。API Reference と Specification では、見出し階層と field の配置を翻訳都合で組み替えない。

        translation-source metadata で `preserve_spelling` 対象となった用語は表記を変更しない。canonical document 先頭の生成 notice と translation metadata は published document へ含めない。

        翻訳中に仕様の不足や曖昧さを見つけた場合は published document だけを補正せず、canonical source を修正して canonical document の生成からやり直す。
        """

        title @= "翻訳と公開"

    class SECTION_009:
        """
        wheel は Shikumi を利用するための distribution とし、実装、公開文書、公式作例を含める。`tests/`、`devdocs/`、`scripts/` など、release の開発・検証に使う repository source は wheel へ含めない。

        sdist はその release を再構成・検証・理解できる完全な release source とする。`src/`、公開文書、`examples/` に加えて、`tests/`、`devdocs/`、`scripts/`、project metadata を含める。`.github/` などの repository operation 設定、VCS metadata、仮想環境、cache、build output など release source ではないものは含めない。

        `devdocs/` の canonical source と canonical document は sdist に含まれるが、公開 Python API ではない。
        """

        title @= "配置と配布"

    class SECTION_010:
        """
        文書変更では少なくとも次を確認する。

        - 全 canonical source が対応する shikumi-devdoc regulation を満たす。
        - `python scripts/render_canonical_docs.py --check` が成功し、commit 済み canonical document を再現できる。
        - canonical document に未解決の Vocabulary / context placeholder が残っていない。
        - `test_target_field` として掲載した検証対象コードのテストが成功する。
        - API Reference / Specification の published document が canonical document の見出し階層と semantic field 構造を保持している。
        - published document のコード、リンク、公開名が壊れていない。
        - distribution 対象文書の配置が packaging test と一致する。

        GitHub Actions の hosted CI でもこれらの検査を実行する。`main` への push と pull request では reusable checks を通して Ruff の lint / format check、本体コードの basedpyright、`tests/typing` の consumer typing contract、Python 3.11 から 3.14 の test suite、canonical document の drift 検査を行い、別 job で wheel / sdist を build して distribution 内容も検査する。consumer typing contract は専用の basedpyright 設定で、公開型 API の受理・拒否契約と不要になった ignore を検査する。release workflow も同じ reusable checks を release tag の commit に対して再実行し、成功した場合だけ build / publish へ進む。ローカル検証は引き続き変更を公開する前の基本手順とする。
        """

        title @= "確認"
