"""Shikumi README canonical source."""

from devdocs.canonical_sources.docs.vocabulary import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import test_target_field, title


quickstart_code = test_target_field("quickstart code")
@canonical_source("Shikumi", filename="README.md", heading="title")
class README:
    '''
    {{TERM_1}}は、**Python上に独自の意味・構造・規則を持つ仕組みを作るためのライブラリ**です。

    構造化ドキュメント生成器、独自DSL、アーキテクチャ{{TERM_21}}などを直接提供するのではなく、用途側が{{TERM_12}}、{{TERM_15}}、{{TERM_7}}、{{TERM_22}}、{{TERM_26}}を組み合わせてそれらを構築するための共通基盤を提供します。

    {{TERM_1}}はPythonの実行後に成立した対象を{{TERM_18}}し、{{TERM_19}}を構成します。同じ{{TERM_19}}を{{TERM_21}}にも{{TERM_25}}にも利用できます。
    '''

    merge @= TERMS.TERM_1
    merge @= TERMS.TERM_21
    merge @= TERMS.TERM_12
    merge @= TERMS.TERM_15
    merge @= TERMS.TERM_7
    merge @= TERMS.TERM_22
    merge @= TERMS.TERM_26
    merge @= TERMS.TERM_18
    merge @= TERMS.TERM_19
    merge @= TERMS.TERM_25

    class USE_CASES:
        '''
        - Pythonコード上の{{TERM_4}}からMarkdown、設定、レポートなどの{{TERM_28}}を生成する。
        - 用途固有の属性・分類・関係を持つPythonベースのDSLを構築する。
        - package、module、classの{{TERM_7}}や依存方向を定義して{{TERM_21}}する。
        - 同じ{{TERM_2}}を複数のPython packageへ適用する。
        - LLMとの協調作業で、意味と構造を明示した機械可読な記述を利用する。

        これらの用途固有の意味は{{TERM_1}}本体には組み込まれていません。利用者が目的に応じた{{TERM_2}}として定義します。
        '''
        title @= '主な用途'

        merge @= TERMS.TERM_4
        merge @= TERMS.TERM_28
        merge @= TERMS.TERM_7
        merge @= TERMS.TERM_21
        merge @= TERMS.TERM_2
        merge @= TERMS.TERM_1

    class INSTALLATION:
        '''
        ```bash
        pip install {{PROJECT.distribution}}
        ```

        現在のバージョンは `{{PROJECT.version}}` です。Python `{{PROJECT.requires_python}}` を対象としています。0.2.0 から開発段階は Beta です。
        '''
        title @= 'インストール'

    class QUICKSTART:
        '''
        次の例では、`title`という{{TERM_12}}を定義し、`@=`とdecoratorから同じ意味情報を{{TERM_4}}します。さらに、実体にはtitleが必要という{{TERM_22}}を適用します。

        ```python
        {{quickstart_code}}
        ```
        `InformationType`は「何を意味するか」を定義し、Python上で「どう書くか」は{{TERM_15}}が担います。`view()`は{{TERM_19}}を構成し、`validate()`はその意味像へ{{TERM_22}}を適用します。

        続けて実現まで含む一連の流れを試す場合は [`Getting Started`](https://github.com/minoru-jp/shikumi/blob/main/docs/guides/getting-started.md) を参照してください。
        '''
        title @= '最小例'

        quickstart_code @= r'''
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
        '''

        merge @= TERMS.TERM_12
        merge @= TERMS.TERM_4
        merge @= TERMS.TERM_22
        merge @= TERMS.TERM_15
        merge @= TERMS.TERM_19

    class RUNTIME_MODEL:
        '''
        {{TERM_1}}はsourceをASTとして意味解析する静的解析器ではありません。moduleやpackageを対象にすると通常のPython importとして実行され、その後に成立したruntime object、{{TERM_13}}、{{TERM_16}}を{{TERM_18}}します。

        したがって、**{{TERM_1}}へ渡すmoduleやpackageは信頼できるPythonコードだけにしてください。** 検証目的であってもimport時のコードは通常の権限で実行されます。

        実行時確定、構造、検証、実現の厳密な契約は [`Specification`](https://github.com/minoru-jp/shikumi/blob/main/docs/specification/INDEX.md) にまとめています。
        '''
        title @= '実行モデルと安全性'

        merge @= TERMS.TERM_1
        merge @= TERMS.TERM_13
        merge @= TERMS.TERM_16
        merge @= TERMS.TERM_18

    class EXAMPLES:
        '''
        [`structure_showcase`](https://github.com/minoru-jp/shikumi/blob/main/examples/structure_showcase/README.md) は、特定用途の完成例ではなく、{{TERM_8}}で表現できる一般的な構造パターンを valid / invalid fixture としてまとめた実行可能なショーケースです。

        単一機能の使い方は Guides と API Reference の検証済みコード例へ置き、`examples/` は複数の構造プリミティブを組み合わせた完成形だけを扱います。
        '''
        title @= '公式作例'

        merge @= TERMS.TERM_8

    class DOCUMENTATION:
        '''
        - [`Guides`](https://github.com/minoru-jp/shikumi/blob/main/docs/guides/INDEX.md): はじめ方、記述器の実装、project配置とCLI結線。
        - [`Glossary`](https://github.com/minoru-jp/shikumi/blob/main/docs/glossary.md): 用語の正規定義。
        - [`API Reference`](https://github.com/minoru-jp/shikumi/blob/main/docs/api/INDEX.md): 公開Python APIとCLI surface。
        - [`Specification`](https://github.com/minoru-jp/shikumi/blob/main/docs/specification/INDEX.md): Shikumiが保証する意味上・互換性上の契約。
        - [`STATUS`](https://github.com/minoru-jp/shikumi/blob/main/STATUS.md): 現在の開発段階、互換性方針、1.0への移行基準、配布上の既知制約。
        - [`CHANGELOG`](https://github.com/minoru-jp/shikumi/blob/main/CHANGELOG.md): 公開releaseごとの主な変更。

        概念の意味はGlossary、規範的な挙動はSpecification、名前単位の利用方法はAPI Referenceを基準とします。
        '''
        title @= '文書'

    class LICENSE:
        '''MIT License. See [`LICENSE`](https://github.com/minoru-jp/shikumi/blob/main/LICENSE).'''
        title @= 'License'
