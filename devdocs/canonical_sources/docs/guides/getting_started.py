"""Canonical Japanese getting-started guide."""

from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import table_field, test_target_field, title

from devdocs.canonical_sources.docs.vocabulary import TERMS

complete_example = test_target_field("complete example")
responsibilities = table_field(
    "responsibilities",
    columns=("part", "responsibility"),
)


@summary("情報型、記述器、検証、実現を一つの小さな例で通して理解する入門ガイド。")
@canonical_source(
    "Getting Started", filename="getting-started.md", order=10, heading="title"
)
class GUIDE:
    """
    このガイドでは、一つのPython classへ意味情報を記述し、{{TERM_1}}で{{TERM_19}}を構成し、{{TERM_21}}し、最後に文字列へ{{TERM_25}}するまでを一周します。

    目的はAPIを網羅することではなく、各責務の境界を最小の実行可能な例で確認することです。
    """

    merge @= TERMS.TERM_1
    merge @= TERMS.TERM_19
    merge @= TERMS.TERM_21
    merge @= TERMS.TERM_25

    class COMPLETE_EXAMPLE:
        """
        ```python
        {{complete_example}}
        ```
        このコードは、`Title`という{{TERM_12}}、`title`という{{TERM_15}}、titleを必須にする{{TERM_22}}、Markdown見出しを生成する{{TERM_26}}を別々に定義しています。
        """

        title @= "完全な例"

        complete_example @= r"""
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
        """

        merge @= TERMS.TERM_12
        merge @= TERMS.TERM_15
        merge @= TERMS.TERM_22
        merge @= TERMS.TERM_26

    class RESPONSIBILITIES:
        """
        {{responsibilities}}

        この分離がShikumiの中心です。情報の意味、Python上の記法、妥当性、成果物生成を同じ仕組みに押し込めず、必要な組み合わせを用途側で構成します。
        """

        title @= "責務を分けて読む"

        responsibilities @= (
            "`InformationType`",
            "値が何を意味し、どの型・個数を持つかを定義する。",
        )
        responsibilities @= (
            "Descriptor (`assignment`)",
            "Pythonコード上の記述を実行時の情報へ接続する。",
        )
        responsibilities @= (
            "`Shikumi`",
            "認識する情報型、構造、検証規則などを一つの解釈体系として束ねる。",
        )
        responsibilities @= (
            "Validator",
            "構成済みの意味像へ用途固有の条件を適用する。",
        )
        responsibilities @= (
            "Realizer",
            "意味像を読み、Shikumi本体から独立して成果物を生成する。",
        )

    class NEXT:
        """
        - 独自のdecoratorや`@=`記述器を作る場合は [`Descriptor Authoring`](./descriptor-authoring.md)。
        - 規定体・実現器をprojectへ配置してCLIから結線する場合は [`Project Layout and CLI`](./project-layout.md)。
        - 個々の公開名を調べる場合は [`API Reference`](../api/INDEX.md)。
        - 実行時確定、構造、検証、実現の厳密な契約は [`Specification`](../specification/INDEX.md)。
        """

        title @= "次に読む"
