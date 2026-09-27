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
canonical source は `devdocs/canonical_sources/changelog.py` です。
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

# Shikumi 変更履歴

Shikumi の公開リリースごとの主な変更を記録する。

## UNRELEASED

次の公開リリースへ向けた変更。

## V0_2_0

文書体系の再構成、構造規定の再利用・論理要素、Beta移行。

version: 0.2.0

released on: 2026-09-27

Added:

- StructureFragment / StructureMount による部分構造の再利用と、LogicalStructureElement による自由名称・列挙名称・出現数を持つ論理構造要素を追加した。明示的 StructureElement は論理要素より優先される。
- StructureFragment.unconstrained() により、構造要素自体は規定しつつ子孫の topology へ制約を課さない規定を明示できるようにした。
- StructureElement(required=False) により、具体名称を持つ区分を optional にし、存在した場合だけその subtree の規定を有効化できるようにした。optional exact element も LogicalStructureElement より優先される。
- LogicalStructureElement を StructuralKind ごとに同一 parent へ共存できるよう拡張し、名称ではなく観測された kind により任意名 package / module などの規定を一意に選択できるようにした。
- StructureFragment.recursive() により、同じ fragment 規定を任意深度の recursive child へ遅延再適用できるようにした。
- StructureGroup により、異なる exact sibling 規定へ at-least-one / exactly-one などの集合 cardinality を追加できるようにした。
- StructureCheck.bindings / StructureBinding により、論理構造要素と実際の path の対応を照合結果として取得できるようにした。
- トップレベルに STATUS.md を追加し、0.2.x Beta の互換性方針、1.0 への移行基準、PyPI のみで公開していることに起因する文書リンク上の既知制約を明文化した。

Changed:

- Development Status を Alpha から Beta へ移行した。既存の StructureElement / StructureSpecification.elements / element_at() / subtree() / from_resolved() / Focus.placement / ResolvedStructure の exact / actual path semantics は維持した。
- Python 3.14 を正式サポート対象として PyPI classifier に追加した。
- 公開 GitHub リポジトリをまだ持たないため `.github/workflows/` の CI / release workflow を削除した。現時点の検証と PyPI 公開はローカルで行い、GitHub 公開時に hosted CI と release automation を新たに構成する。
- 公式作例をトップレベルの `shikumi_examples` import package から `examples/` の参考ソースへ移し、wheel では `shikumi/_examples/` に同梱するよう変更した。作例の `python -m` 実行入口を削除し、利用者コードが依存する公開面から分離した。
- 用途別の4つの公式作例を廃止し、一般的な構造規定を valid / invalid fixture で示す `examples/structure_showcase` へ再編した。単機能の利用例は Guides / API Reference の検証済みコードへ集約した。
- 文書体系を shikumi-devdoc 0.3.0 の collection / field model に合わせて再構成し、API Reference を領域別 collection に分割、意味上の契約を Specification collection として独立させ、検証価値のある記述器作例を test_target_field とテストへ分離した。
- README を入口と最小例へ絞り、Guides を Getting Started / Descriptor Authoring / Project Layout and CLI の collection として再編した。旧 Distribution Guide は Project Layout guide へ統合し、公開例と CLI 例の検証可能な test_target_field を拡充した。
- リポジトリ専用の文書運用ガイドをトップレベルの DOCUMENTATION_WORKFLOW.md から devdocs/README.md へ移し、文書開発 workspace 自身の入口として配置した。
- API Reference の実行可能な使用例を監査し、情報接続、class binding、構造解決、Semantic View、Shikumi composition、validation、structure check、realization の例を test_target_field と実行テストへ昇格した。signature や型形状などの非実行スニペットは通常の fence として区別した。
- Specification / API Reference をレビューし、公開 subject を一対一の API node へ整理、`shikumi.standard` を独立 API page へ分離した。API field の型・引数・関連 specification の不一致を修正し、SemanticView snapshot、exact structure check、diagnostic subject 補完の契約を Specification に明文化した。canonical / published 間の見出しと semantic field 構造も回帰テストで検査するようにした。
- shikumi-devdoc の更新に追従し、nested node の見出し情報を `title @= ...` へ統一して Vocabulary reference を利用可能にし、canonical source の heading policy を明示化した。検証対象のコード・command は presentation 非依存の `test_target_field` へ移行し、Glossary 公開は既定値を利用して冗長な `glossary @= True` を削除した。

## V0_1_0

初回公開リリース。

version: 0.1.0

released on: 2026-09-12

Added:

- 情報、記述器使用、構造、意味像を分離した Core の意味モデルを追加した。
- 実体・module・packageを同じ仕組みで扱う検証と、独立した実現器による実現を追加した。
- デコレータ、`@=`、docstring、package treeなど、再利用可能な Standard の記述器と構造実装を追加した。
- 規定体、記述体、実現器を通常の Python 参照として結線する CLI を追加した。
- README、Glossary、API Reference、Distribution Guide からなる英語の公開文書体系を追加した。公開文書は日本語の canonical source を正本として生成・翻訳する。
- architecture、structured docs、Web API、`structure-from` の4方向を示す公式作例を追加した。
