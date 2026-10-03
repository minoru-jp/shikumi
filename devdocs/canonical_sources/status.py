"""Shikumi project status canonical source."""

from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source(
    "Shikumi プロジェクトステータス", filename="STATUS.md", heading="title"
)
class STATUS:
    """
    Shikumi の現在の開発段階、互換性方針、および 1.0 へ向けた判断基準を示します。

    0.2.0 から Shikumi は Beta 段階へ移行します。Beta は公開 API を自由に変更する段階を意味しません。現在の基本設計と公開 API を実運用へ投入できる水準まで固めたものとして扱い、以後は互換性を積極的に維持します。
    """

    class CURRENT_STATUS:
        """
        現在の公開バージョンは `{{PROJECT.version}}`、公開バージョン系列は `0.2.x`、開発段階は **Beta** です。

        0.2.0 では文書体系の再構成と構造規定 API の拡張を行い、今後の実運用で検証する基盤を確定しました。Beta 期間は API を作り直すための期間ではなく、現在の設計を依存プロジェクトと実利用の中で検証し、必要な改善を互換性を維持しながら行う期間です。
        """

        title @= "現在のステータス"

    class STABILITY_POLICY:
        """
        0.2.0 以降、公開 API の破壊的変更は重大な理由がある場合を除いて行いません。

        重大な理由には、維持することで正確性・安全性・中核的な設計整合性を損なう欠陥などが含まれます。通常の機能追加や改善は additive に行い、既存 API を置き換える必要が生じた場合は、可能な限り deprecation と移行期間を設けます。

        内部実装、文書生成基盤、非公開の開発用構造はこの互換性方針の対象外ですが、公開された意味上の契約を変えないことを優先します。
        """

        title @= "安定性方針"

    class BETA_GOALS:
        """
        Beta 期間では、特に次の点を確認します。

        - Shikumi を利用する実プロジェクトで、現在の意味モデルと公開 API が無理なく継続利用できること。
        - `shikumi-devdoc` を含む依存プロジェクトが、互換性を保ったまま発展できること。
        - Structure、Validation、Realization、Descriptor などの主要な契約に根本的な再設計が不要であること。
        - API を増やす場合も、既存の概念境界を崩さず additive に拡張できること。
        - 文書、診断、型情報など、利用体験上の改善を継続できること。
        """

        title @= "Beta 期間の目的"

    class PATH_TO_ONE:
        """
        十分な期間の実運用を経て、重大な設計上の問題や破壊的な再設計の必要がないと判断できた時点で、現在の設計を基礎として `1.0.0` へ移行します。

        1.0 への移行条件は、機能を際限なく追加することではありません。現在の公開 API と概念モデルが、依存プロジェクトを支える安定した基盤として継続利用できると確認できることを重視します。
        """

        title @= "1.0 への移行"

    class DISTRIBUTION_NOTE:
        """
        Shikumi は PyPI と公開 GitHub リポジトリ `https://github.com/minoru-jp/shikumi` で公開しています。PyPI は Python package の配布先、GitHub は source、公開文書、issue、開発履歴の公開先として扱います。

        トップレベル README の主要文書、公式作例、LICENSE への参照には公開 GitHub repository の絶対 URL を使用し、GitHub 上だけでなく PyPI の README 表示からも同じ公開文書へ辿れるようにしています。package metadata でも Homepage / Repository / Documentation / Issues URL を公開します。

        GitHub Actions の hosted CI は `main` への push と pull request で実行します。quality job では Ruff と basedpyright による品質検査を行い、Ruff は lint と format check が clean、本体コードの basedpyright は error / warning が 0 の状態を品質ゲートとします。さらに `tests/typing` の consumer typing contract を専用の basedpyright 設定で検証し、公開型 API が意図した値を受理・拒否する契約も固定します。あわせて Python 3.11 から 3.14 のテスト、canonical document の drift 検査、wheel / sdist の build と distribution 内容検査を行います。

        PyPI への公開は通常の push とは分離します。`.github/workflows/release.yml` は GitHub Release が publish された場合だけ動作し、通常 CI と共通の reusable checks で Ruff、本体コードと consumer typing contract の basedpyright、canonical document drift、Python 3.11 から 3.14 の test suite を release tag の commit に対して再実行します。これらが成功し、release tag と `pyproject.toml` の version の一致も確認できた場合だけ distribution を build し、PyPI Trusted Publishing で公開します。GitHub の `pypi` environment と PyPI 側の Trusted Publisher は対応付け済みです。
        """

        title @= "配布とリポジトリ運用"
