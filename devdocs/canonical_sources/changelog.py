"""Canonical Japanese changelog source for Shikumi."""

from shikumi_devdoc.fields.changelog import added, changed, released_on, version
from shikumi_devdoc.norms.common import canonical_source, merge

from devdocs.canonical_sources.docs.vocabulary import TERMS


@canonical_source("Shikumi 変更履歴", filename="CHANGELOG.md", heading="title")
class CHANGELOG:
    """{{TERM_1}} の公開リリースごとの主な変更を記録する。"""

    merge @= TERMS.TERM_1

    class UNRELEASED:
        """次の公開リリースへ向けた変更。"""

    class V0_2_4:
        """独自 `@=` 記述器の公開型契約を runtime 能力と一致させた型互換性修正リリース。"""

        version @= "0.2.4"
        released_on @= "2026-10-03"

        class TYPING:
            """`class_binding()` の value type を反復 `@=` まで保持し、利用者側の独自記述器を静的型検査できるようにした。runtime の binding 動作は変更していない。"""

            added @= "`class_binding()` が返す一時値の公開静的契約として `ClassBinding[T]` を追加した。具体的な runtime binding 実装は引き続き非公開とする。"
            changed @= "`class_binding()` の戻り値型を `object` から `ClassBinding[T]` へ修正し、同じ binding name への繰り返し `@=` で最初の value type を保持するようにした。"
            changed @= "`tests/typing` の consumer typing contract に `class_binding()` を使う独自 `@=` 記述器を追加し、正しい反復記述を受理し異なる value type を拒否することを CI / release checks で固定した。"
            changed @= "Descriptor Authoring Guide と Descriptor API Reference を新しい公開型契約へ合わせ、`ClassBinding[T]` と型付きの独自 `@=` 記述器例を記載した。"
            changed @= "`class_binding()` の callback 契約を class body 実行後かつ `__init_subclass__()` より前という観測可能な順序として明確化し、現在の `__set_name__()` 利用は内部実装として説明した。callback 例外を Shikumi が正規化せず Python runtime の class-creation semantics に従うことも文書化した。"
            changed @= "`@=` は Shikumi Core が強制する syntax ではなく `shikumi.standard` が提供する標準的な選択肢であること、通常の authoring flow では外側の writer を消費せず各 class body 側へ一時 binding を置くこと、低水準 `ClassBinding[T]` と Standard writer の `Self` 契約が異なる抽象度を表すことを文書化した。"

    class V0_2_3:
        """静的解析と CI 品質ゲートを整備した内部品質改善リリース。"""

        version @= "0.2.3"
        released_on @= "2026-10-03"

        class INTERNAL:
            """Ruff と basedpyright を開発時および CI の品質ゲートへ追加し、既存コードを両チェックで clean な状態へ整備した。公開 API と CLI の契約は変更していない。"""

            changed @= "CLI JSON の `diagnostic_counts` について、型定義と実際の payload のキー集合が `DiagnosticSeverity` と同期することを回帰テストで固定した。"
            changed @= "通常 CI と release workflow が同じ reusable quality / test checks を利用するよう整理し、release tag の commit が Ruff、basedpyright、canonical document drift、Python 3.11 から 3.14 の test suite を通過した後だけ build / publish へ進むようにした。"
            changed @= "従来 mypy の unused-ignore を前提としていた `tests/typing` の consumer typing contract を basedpyright 専用設定と rule 指定付き `pyright: ignore` へ移行し、通常 CI と release checks の双方で検証するようにした。"
            changed @= "Ruff formatter を開発・CI の品質ゲートへ追加し、実装・テスト・canonical source などの編集対象を統一フォーマットへ揃えた。canonical / published document などの生成物は正本生成フローを優先し、formatter の直接編集対象から除外した。"
            changed @= "`shikumi-devdoc` の version 制約を `[dependency-groups].docs` に一元化し、test group と CI は dependency group を通じて同じ制約を利用するよう整理した。"

    class V0_2_2:
        """PyPI から公開文書へ辿れるよう README と package metadata の公開リンクを整備。"""

        version @= "0.2.2"
        released_on @= "2026-09-29"
        changed @= "README の Guides、Glossary、API Reference、Specification、STATUS、CHANGELOG、公式作例、LICENSE への参照を公開 GitHub repository の絶対 URL に変更し、PyPI の README 表示からも正しく辿れるようにした。"
        changed @= "package metadata に Homepage、Repository、Documentation、Issues の project URL を追加し、PyPI から公開 repository と文書へ直接移動できるようにした。"

    class V0_2_1:
        """配布物の役割を整理し、sdist を完全な release source として再構成。"""

        version @= "0.2.1"
        released_on @= "2026-09-27"
        changed @= "wheel は実装、公開文書、公式作例を含む利用者向け distribution とする方針を維持した。"
        changed @= "sdist を release の再構成・検証・理解に必要な完全な source distribution とし、`src/`、公開文書、`examples/` に加えて `tests/`、`devdocs/`、`scripts/` を含めるよう変更した。"
        changed @= "sdist の対象を個別列挙する方式をやめ、project を原則収録し、`.github/` などの repository operation 設定、VCS metadata、仮想環境、cache、build output など release source ではないものだけを除外する方針へ変更した。"

    class V0_2_0:
        """文書体系の再構成、構造規定の再利用・論理要素、Beta移行。"""

        version @= "0.2.0"
        released_on @= "2026-09-27"
        added @= "StructureFragment / StructureMount による部分構造の再利用と、LogicalStructureElement による自由名称・列挙名称・出現数を持つ論理構造要素を追加した。明示的 StructureElement は論理要素より優先される。"
        added @= "StructureFragment.unconstrained() により、構造要素自体は規定しつつ子孫の topology へ制約を課さない規定を明示できるようにした。"
        added @= "StructureElement(required=False) により、具体名称を持つ区分を optional にし、存在した場合だけその subtree の規定を有効化できるようにした。optional exact element も LogicalStructureElement より優先される。"
        added @= "LogicalStructureElement を StructuralKind ごとに同一 parent へ共存できるよう拡張し、名称ではなく観測された kind により任意名 package / module などの規定を一意に選択できるようにした。"
        added @= "StructureFragment.recursive() により、同じ fragment 規定を任意深度の recursive child へ遅延再適用できるようにした。"
        added @= "StructureGroup により、異なる exact sibling 規定へ at-least-one / exactly-one などの集合 cardinality を追加できるようにした。"
        added @= "StructureCheck.bindings / StructureBinding により、論理構造要素と実際の path の対応を照合結果として取得できるようにした。"
        changed @= "Development Status を Alpha から Beta へ移行した。既存の StructureElement / StructureSpecification.elements / element_at() / subtree() / from_resolved() / Focus.placement / ResolvedStructure の exact / actual path semantics は維持した。"
        changed @= "Python 3.14 を正式サポート対象として PyPI classifier に追加した。"
        changed @= "公開 GitHub リポジトリをまだ持たないため `.github/workflows/` の CI / release workflow を削除した。現時点の検証と PyPI 公開はローカルで行い、GitHub 公開時に hosted CI と release automation を新たに構成する。"
        changed @= "公式作例をトップレベルの `shikumi_examples` import package から `examples/` の参考ソースへ移し、wheel では `shikumi/_examples/` に同梱するよう変更した。作例の `python -m` 実行入口を削除し、利用者コードが依存する公開面から分離した。"
        added @= "トップレベルに STATUS.md を追加し、0.2.x Beta の互換性方針、1.0 への移行基準、PyPI のみで公開していることに起因する文書リンク上の既知制約を明文化した。"
        changed @= "用途別の4つの公式作例を廃止し、一般的な構造規定を valid / invalid fixture で示す `examples/structure_showcase` へ再編した。単機能の利用例は Guides / API Reference の検証済みコードへ集約した。"
        changed @= "文書体系を shikumi-devdoc 0.3.0 の collection / field model に合わせて再構成し、API Reference を領域別 collection に分割、意味上の契約を Specification collection として独立させ、検証価値のある記述器作例を test_target_field とテストへ分離した。"
        changed @= "README を入口と最小例へ絞り、Guides を Getting Started / Descriptor Authoring / Project Layout and CLI の collection として再編した。旧 Distribution Guide は Project Layout guide へ統合し、公開例と CLI 例の検証可能な test_target_field を拡充した。"
        changed @= "リポジトリ専用の文書運用ガイドをトップレベルの DOCUMENTATION_WORKFLOW.md から devdocs/README.md へ移し、文書開発 workspace 自身の入口として配置した。"
        changed @= "API Reference の実行可能な使用例を監査し、情報接続、class binding、構造解決、Semantic View、Shikumi composition、validation、structure check、realization の例を test_target_field と実行テストへ昇格した。signature や型形状などの非実行スニペットは通常の fence として区別した。"
        changed @= "Specification / API Reference をレビューし、公開 subject を一対一の API node へ整理、`shikumi.standard` を独立 API page へ分離した。API field の型・引数・関連 specification の不一致を修正し、SemanticView snapshot、exact structure check、diagnostic subject 補完の契約を Specification に明文化した。canonical / published 間の見出しと semantic field 構造も回帰テストで検査するようにした。"
        changed @= "shikumi-devdoc の更新に追従し、nested node の見出し情報を `title @= ...` へ統一して Vocabulary reference を利用可能にし、canonical source の heading policy を明示化した。検証対象のコード・command は presentation 非依存の `test_target_field` へ移行し、Glossary 公開は既定値を利用して冗長な `glossary @= True` を削除した。"

    class V0_1_0:
        """初回公開リリース。"""

        version @= "0.1.0"
        released_on @= "2026-09-12"
        added @= (
            "情報、記述器使用、構造、意味像を分離した Core の意味モデルを追加した。"
        )
        added @= "実体・module・packageを同じ仕組みで扱う検証と、独立した実現器による実現を追加した。"
        added @= "デコレータ、`@=`、docstring、package treeなど、再利用可能な Standard の記述器と構造実装を追加した。"
        added @= (
            "規定体、記述体、実現器を通常の Python 参照として結線する CLI を追加した。"
        )
        added @= "README、Glossary、API Reference、Distribution Guide からなる英語の公開文書体系を追加した。公開文書は日本語の canonical source を正本として生成・翻訳する。"
        added @= "architecture、structured docs、Web API、`structure-from` の4方向を示す公式作例を追加した。"

        merge @= TERMS.TERM_13
        merge @= TERMS.TERM_16
        merge @= TERMS.TERM_7
        merge @= TERMS.TERM_19
        merge @= TERMS.TERM_21
        merge @= TERMS.TERM_26
        merge @= TERMS.TERM_25
        merge @= TERMS.TERM_15
        merge @= TERMS.TERM_3
        merge @= TERMS.TERM_5
