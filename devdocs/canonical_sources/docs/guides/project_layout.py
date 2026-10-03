"""Canonical Japanese guide for project-local Shikumi layout and CLI wiring."""

from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import table_field, test_target_field, title

from devdocs.canonical_sources.docs.vocabulary import TERMS

validate_command = test_target_field("validate command")
role_table = table_field("project roles", columns=("location", "role"))


@summary(
    "規定体、実現器、記述体をprojectへ配置し、通常のPython参照としてCLIから結線するガイド。"
)
@canonical_source(
    "Project Layout and CLI", filename="project-layout.md", order=30, heading="title"
)
class GUIDE:
    """
    {{TERM_1}}は専用の配布形式や登録機構を要求しません。{{TERM_3}}、{{TERM_5}}、{{TERM_26}}が通常のPython objectとしてimport可能であれば、library codeからもCLIからも利用できます。
    """

    merge @= TERMS.TERM_1
    merge @= TERMS.TERM_3
    merge @= TERMS.TERM_5
    merge @= TERMS.TERM_26

    class LAYOUT:
        """
        project固有のShikumi関連コードは、用途に応じた通常のPython packageへ配置します。`{{TERM_33}}`のような専用名は必須ではありません。次の役割分割は、大きくなったprojectで責務を見分けやすくするための一例です。

        {{role_table}}

        小さなprojectでは一つのmoduleへまとめても構いません。別distributionへ分離しても構いません。重要なのは物理名ではなく、それぞれのobjectが通常のPython importで取得できることです。
        """

        title @= "推奨する役割分割"

        role_table @= (
            "`shikumi_lib/norms/`",
            "情報型、記述器、構造、検証規則、Shikumi instanceなどの規定体。",
        )
        role_table @= (
            "`shikumi_lib/realizers/`",
            "意味像から成果物を作る独立した実現器。",
        )
        role_table @= (
            "application package",
            "検証・実現対象となる通常の記述体。shikumi_lib配下へ移す必要はない。",
        )

        merge @= TERMS.TERM_33

    class CLI:
        """
        CLIでは`MODULE:OBJECT`形式で{{TERM_1}} instanceや{{TERM_26}}を指定し、`MODULE`または`MODULE:OBJECT`で{{TERM_5}}を指定します。

        repositoryに同梱した structure showcase は、次のコマンドで実際の package tree を構造規定に対して検証できます。

        ```bash
        {{validate_command}}
        ```
        `realize`も同じ `MODULE:OBJECT` 参照で{{TERM_26}}を結線しますが、公式 showcase は構造規定に焦点を絞るため実現器を持ちません。`realize`は暗黙に{{TERM_21}}や{{TERM_27}}を実行しないため、必要な検証と実現可能性確認は別の操作として行います。
        """

        title @= "CLIはPython参照を結線する"

        validate_command @= r"""
        python -m shikumi validate \
          --shikumi structure_showcase.specification:showcase \
          --body structure_showcase.valid.combined \
          --at . \
          --structure-spec structure_showcase.specification:showcase_structure \
          --format text
        """

        merge @= TERMS.TERM_1
        merge @= TERMS.TERM_26
        merge @= TERMS.TERM_5
        merge @= TERMS.TERM_21
        merge @= TERMS.TERM_27

    class DISTRIBUTION:
        """
        {{TERM_3}}や{{TERM_26}}は{{TERM_1}}本体とは独立したPython codeとして配布できます。同じdistributionへ同梱しても、別libraryとして配布しても構いません。

        Shikumi repositoryの structure showcase は学習用の参考ソースです。repositoryでは`examples/`、wheelでは`shikumi/_examples/`へ配置し、利用者が依存する公開import surfaceから分離します。
        """

        title @= "配布"

        merge @= TERMS.TERM_3
        merge @= TERMS.TERM_26
        merge @= TERMS.TERM_1
