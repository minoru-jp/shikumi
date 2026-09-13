"""Shikumi README の正本の記述体。

``TITLE_N`` の数値部分は Python 上で各見出しを識別するためだけに存在し、
順序、階層、見出し名その他の意味を一切表さない。
"""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("{{TERM_1}}")
class TITLE_1:
    '''
    {{TERM_1}}は、**構造化ドキュメント生成器、独自DSL、アーキテクチャ{{TERM_21}}ツールなどをPython上に構築するためのライブラリ**です。

    ただし、{{TERM_1}}自身がそれらの機能を個別に提供するわけではありません。

    どのような要素が存在し、どのような属性や関係を持ち、どのような{{TERM_7}}に属し、何を正しい状態とみなし、
    その{{TERM_19}}から何を作り出すかを、利用者自身が{{TERM_2}}として定義します。

    たとえば、その{{TERM_19}}をMarkdownへ変換すればドキュメント生成になります。
    「service」「entity」「uses」といった独自の{{TERM_12}}と{{TERM_4}}方法を作ればDSLになります。
    「application層からdomain層への依存だけを許可する」という規則を作ればアーキテクチャ{{TERM_21}}になります。

    つまり{{TERM_1}}が扱うのは、アーキテクチャ、DSL、文書そのものではありません。
    **Python上に独自の意味とルールを持つ仕組みを作り、それを{{TERM_18}}し、利用するための共通基盤です。**
    '''

    vocabulary_refs @= (
        terms.TERM_1,
        terms.TERM_21,
        terms.TERM_7,
        terms.TERM_19,
        terms.TERM_2,
        terms.TERM_12,
        terms.TERM_4,
        terms.TERM_18,
    )


    @title("主な用途")
    class TITLE_2:
        '''
        {{TERM_1}}は、たとえば次のような用途に利用できます。

        - Pythonコード上の{{TERM_4}}から構成された{{TERM_19}}から、文書、設定、レポートなどの{{TERM_28}}を生成する
        - LLMとの迅速な意思疎通のために、意味と構造を明示した文書を作成する
        - Pythonのclassやmoduleに、用途固有の属性・分類・関係を{{TERM_4}}する
        - 独自の{{TERM_15}}や{{TERM_12}}を持つPythonベースのDSLを構築する
        - プロジェクトが持つべきpackage、module、classの{{TERM_7}}を定義する
        - 同じ{{TERM_2}}を複数のPython packageへ適用する
        - ソフトウェアアーキテクチャの{{TERM_7}}や依存方向を表現し、それを{{TERM_21}}する仕組みを構築する

        これらは{{TERM_1}}自身に組み込まれた用途ではありません。
        利用者が目的に応じた{{TERM_2}}を作ることで実現します。
        '''

        vocabulary_refs @= (
            terms.TERM_1,
            terms.TERM_4,
            terms.TERM_19,
            terms.TERM_28,
            terms.TERM_15,
            terms.TERM_12,
            terms.TERM_7,
            terms.TERM_2,
            terms.TERM_21,
        )

    @title("インストール")
    class TITLE_3:
        '''
        ```bash
        pip install {{PROJECT.distribution}}
        ```

        現在のバージョンは `{{PROJECT.version}}` です。

        {{TERM_1}}はPython `{{PROJECT.requires_python}}` を対象としています。
        '''

        vocabulary_refs @= (
            terms.TERM_1,
        )

    @title("クイックスタート")
    class TITLE_4:
        '''
        次の例では、`title`という{{TERM_12}}を作り、`@=`とデコレータという2種類の{{TERM_15}}から{{TERM_4}}します。

        ```python
        from {{PROJECT.import_package}} import (
            DescriptorUseRule,
            Diagnostic,
            InformationType,
            {{TERM_1}},
            StructuralKind,
            StructureSelector,
            validator,
        )
        from {{PROJECT.import_package}}.standard import assignment, decorator, information_type_rule

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


        docs = {{TERM_1}}(
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

        `InformationType`は「何を意味するか」を定義し、Python上で「どう書くか」は{{TERM_15}}が担います。
        `{{TERM_1}}`は認識する{{TERM_12}}、{{TERM_22}}、{{TERM_17}}などを組み合わせ、`view()`で{{TERM_19}}を構成し、`validate()`で{{TERM_21}}します。

        `title @= "Overview"`は通常の属性代入ではありません。
        `assignment(Title)`が作る{{TERM_15}}が、class成立後に`Overview`へ{{TERM_13}}を接続します。
        `@=`は、class本体の自然な形を保ったまま、{{TERM_2}}側で定めた意味を{{TERM_4}}するためのStandardの記法です。
        '''

        vocabulary_refs @= (
            terms.TERM_12,
            terms.TERM_15,
            terms.TERM_4,
            terms.TERM_1,
            terms.TERM_22,
            terms.TERM_17,
            terms.TERM_19,
            terms.TERM_21,
            terms.TERM_13,
            terms.TERM_2,
        )

    @title("警告")
    class TITLE_13:
        '''
        **{{TERM_1}}に渡すmoduleやpackageは、信頼できるPythonコードだけにしてください。**

        {{TERM_1}}はPythonの実行後に成立した対象を{{TERM_18}}します。moduleやpackageをimport pathで指定した場合、それらは通常のPythonとしてimportされ、実際に実行されたうえで{{TERM_19}}が構成されます。
        これは、その{{TERM_19}}を{{TERM_21}}に使う場合でも、{{TERM_25}}に使う場合でも変わりません。対象コードは、通常のimportと同じ権限で任意の処理を実行できます。

        特に{{TERM_21}}は、安全な隔離環境で対象を静的に検査する機能ではありません。内容を信頼できないmoduleやpackageを、安全性確認のために{{TERM_1}}へ渡してはいけません。
        '''

        vocabulary_refs @= (
            terms.TERM_1,
            terms.TERM_18,
            terms.TERM_19,
            terms.TERM_21,
            terms.TERM_25,
        )

    @title("{{TERM_29}}")
    class TITLE_5:
        '''
        {{TERM_1}}はPython sourceをASTとして読み直しません。
        {{TERM_5}}となるmoduleやpackageは通常のPythonとしてimportされ、その実行後に成立したruntime object、{{TERM_13}}、{{TERM_16}}を観測します。

        ```text
        Python source
            ↓ execute / import
        実行時の対象 + {{TERM_13}} + {{TERM_16}}
            ↓
        {{TERM_1}}
            ↓ interpretation
        {{TERM_19}}
           /          \\
        {{TERM_21}}           {{TERM_25}}
                         ↓
                      {{TERM_28}}
        ```

        したがって、{{TERM_21}}のために対象moduleを読み込む場合も、そのmoduleのトップレベルコードは通常のimportと同様に実行されます。
        {{TERM_1}}は、実行せずに安全性を判定する静的解析器ではありません。
        '''

        vocabulary_refs @= (
            terms.TERM_29,
            terms.TERM_1,
            terms.TERM_5,
            terms.TERM_13,
            terms.TERM_16,
            terms.TERM_19,
            terms.TERM_21,
            terms.TERM_25,
            terms.TERM_28,
        )

    @title("自動では解析しないもの")
    class TITLE_14:
        '''
        {{TERM_1}}は、Python ASTやsource syntax、実際のimport graphやcall graph、まだimportされていないmoduleを自動では解析しません。
        また、標準の`PythonStructure`はfunctionやmethodを{{TERM_11}}として扱いません。必要な情報や対象は、用途側の{{TERM_2}}や独自{{TERM_7}}で明示します。
        '''

        vocabulary_refs @= (
            terms.TERM_1,
            terms.TERM_11,
            terms.TERM_2,
            terms.TERM_7,
        )

    @title("{{TERM_21}}と{{TERM_25}}")
    class TITLE_6:
        '''
        {{TERM_1}}は、Python上の対象とそこに接続された{{TERM_13}}を{{TERM_7}}に従って読み取り、{{TERM_19}}を構成します。

        {{TERM_21}}では、その{{TERM_19}}に{{TERM_22}}を適用します。
        package内に必要なmoduleが存在するか、classに必要な{{TERM_13}}があるか、要素間の関係が規則を満たすか、といった条件を用途ごとに定義できます。

        {{TERM_19}}は{{TERM_21}}だけのためのものではありません。
        独立した{{TERM_26}}を適用することで、Markdown、設定、レポートなど任意の{{TERM_28}}へ{{TERM_25}}できます。
        同じ{{TERM_19}}へ複数の{{TERM_26}}を適用することもできます。
        '''

        vocabulary_refs @= (
            terms.TERM_21,
            terms.TERM_25,
            terms.TERM_1,
            terms.TERM_13,
            terms.TERM_7,
            terms.TERM_19,
            terms.TERM_22,
            terms.TERM_26,
            terms.TERM_28,
        )

    @title("Standard")
    class TITLE_7:
        '''
        `{{PROJECT.import_package}}.standard`は、Coreの仕組みから構成した再利用可能な具体機能を提供します。

        主なものには、`@=`用の`assignment`、デコレータ用の`decorator`、docstringを{{TERM_13}}化する`docstring`、package treeを通常のimportで{{TERM_18}}する`PackageTreeStructure`があります。

        `service`、`entity`、`layer`、`term`など用途固有の意味はStandardには含まれません。
        それらは利用者の{{TERM_2}}として定義します。
        '''

        vocabulary_refs @= (
            terms.TERM_13,
            terms.TERM_18,
            terms.TERM_2,
        )

    @title("CLI")
    class TITLE_8:
        '''
        CLIでは、{{TERM_3}}が公開する`{{TERM_1}}`、{{TERM_5}}、独立した{{TERM_26}}を通常のPython importで指定して結線できます。

        CLIのentry pointは`{{PROJECT.cli_entry_point}}`です。`python -m {{PROJECT.import_package}}`からも同じCLIを実行できます。

        {{TERM_21}}:

        ```bash
        {{PROJECT.cli_entry_point}} validate \\
          --shikumi myproject.{{TERM_33}}.{{TERM_34}}:app \\
          --body myproject.application \\
          --structure-spec myproject.{{TERM_33}}.{{TERM_34}}:app_structure \\
          --format text
        ```

        {{TERM_25}}:

        ```bash
        {{PROJECT.cli_entry_point}} realize \\
          --shikumi myproject.{{TERM_33}}.{{TERM_34}}:app \\
          --body myproject.application \\
          --realizer myproject.{{TERM_33}}.{{TERM_35}}.markdown:markdown \\
          --output API.md \\
          --format json
        ```

        `realize`は暗黙に{{TERM_21}}や{{TERM_27}}の問い合わせを行いません。
        それぞれは独立した操作として扱われます。
        '''

        vocabulary_refs @= (
            terms.TERM_3,
            terms.TERM_1,
            terms.TERM_5,
            terms.TERM_26,
            terms.TERM_21,
            terms.TERM_33,
            terms.TERM_34,
            terms.TERM_25,
            terms.TERM_35,
            terms.TERM_27,
        )

    @title("サンプル")
    class TITLE_9:
        '''
        [`examples/`](./examples/)には、異なる方向から{{TERM_1}}を使う4つの公式作例があります。これらは参考ソースとしてdistributionにも同梱しますが、公開import packageやCLI entry pointではありません。

        - [`architecture`](./examples/architecture/README.md) — 用途固有の依存規則を{{TERM_22}}として定義し、アーキテクチャを{{TERM_21}}する
        - [`structured_docs`](./examples/structured_docs/README.md) — Python上の{{TERM_4}}から{{TERM_19}}を構成し、Markdownへ{{TERM_25}}する
        - [`web_api`](./examples/web_api/README.md) — 独自DSL、{{TERM_21}}、{{TERM_25}}を組み合わせた総合例
        - [`structure_from_body`](./examples/structure_from_body/README.md) — ある{{TERM_5}}から{{TERM_8}}を導出し、別の{{TERM_5}}の{{TERM_7}}適合性を{{TERM_21}}する
        '''

        vocabulary_refs @= (
            terms.TERM_1,
            terms.TERM_22,
            terms.TERM_21,
            terms.TERM_4,
            terms.TERM_19,
            terms.TERM_25,
            terms.TERM_5,
            terms.TERM_8,
            terms.TERM_7,
        )

    @title("関連文書")
    class TITLE_10:
        '''
        - [`docs/glossary.md`](./docs/glossary.md) — {{TERM_1}}で使用する用語と、その意味上の境界
        - [`docs/api-reference.md`](./docs/api-reference.md) — 公開APIとその契約
        - [`docs/distribution-guide.md`](./docs/distribution-guide.md) — {{TERM_3}}、{{TERM_5}}、{{TERM_26}}の配置と配布
        - [`CHANGELOG.md`](./CHANGELOG.md) — 公開リリースごとの主な変更
        - [`examples/`](./examples/) — distributionにも参考ソースとして同梱する4つの公式作例

        概念の厳密な定義は用語集を基準とします。
        '''

        vocabulary_refs @= (
            terms.TERM_1,
            terms.TERM_3,
            terms.TERM_5,
            terms.TERM_26,
        )

    @title("公開文書について")
    class TITLE_11:
        '''
        公開文書はすべて英語で提供します。
        `_internal/document_source/`以下のcanonical document sourceを正本とし、`shikumi-devdoc`で`_internal/document_build/ja/`へ生成した日本語中間文書を翻訳元として公開版を配置します。
        中間文書は生成結果をレビューできるようリポジトリへcommitしますが、直接編集しません。内容に差異がある場合はcanonical document sourceを基準とします。
        '''

    @title("License")
    class TITLE_12:
        '''
        MIT License. See [`LICENSE`](./LICENSE).
        '''
