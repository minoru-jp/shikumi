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
正本は `_internal/document_source/documentation_workflow/canonical.py` です。
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

# 文書運用

このリポジトリでは、公開文書およびリポジトリ専用文書の内容を、`_internal/document_source/` 以下の canonical document source で管理する。

文書の公開版・配置版は正本ではない。文書の変更は canonical document source から開始し、`shikumi-devdoc` による検証・実現、翻訳、配置という一方向の工程を通して反映する。

## 依存関係

`shikumi-devdoc` は、このリポジトリの文書生成に使用する開発時ツールである。`shikumi` package の実行時依存ではない。

package としては `shikumi-devdoc` が `shikumi` を利用する。一方、このリポジトリは開発工程で `shikumi-devdoc` を利用し、生成済み Markdown を distribution に含める。したがって `shikumi` の `[project.dependencies]` から `shikumi-devdoc` へ依存させない。

文書生成時には checkout 中の `src/shikumi` を import 可能にし、`shikumi-devdoc` が現在開発中の Shikumi を使って canonical source を解釈する。

## 正本と生成物

文書内容の正本は `_internal/document_source/**/canonical.py` に置く。Vocabulary から生成する `_internal/document_source/vocabulary/terms.py` も生成物であり、正本ではない。

`_internal/document_build/ja/` の日本語 Markdown は、正本を `shikumi-devdoc` で実現した**コミット済み中間文書**である。人間が差分を確認できるようリポジトリに保持するが、直接編集しない。

英語の Markdown 文書は、中間文書を翻訳して配置した公開版またはリポジトリ専用版である。正本、中間文書、英語版の内容に差異がある場合は canonical document source を基準とする。

文書が説明する Python 実装そのものはこの規則の対象外であり、通常どおり各 package/module 側を正本とする。

## 基本フロー

文書の作成・更新は次の流れで行う。

```text
canonical.py
    ↓ shikumi-devdoc validation / realization
_internal/document_build/ja/ の日本語 Markdown
    ↓ translation
English Markdown
    ↓ placement
repository / distribution
```

1. canonical document source を作成または更新する。
2. `python scripts/render_canonical_docs.py` を実行し、Vocabulary の用語参照体と日本語中間文書を再生成する。
3. 中間文書の差分を確認する。
4. 中間文書を英語へ翻訳する。
5. 翻訳結果を、その文書に定められた位置へ配置する。
6. `python scripts/render_canonical_docs.py --check`、関連テスト、リンク、公開名、distribution 配置を確認する。

## 中間文書

`_internal/document_build/ja/` の中間文書は翻訳入力であり、正本からの実現結果をレビューするための成果物でもある。

- 中間文書をリポジトリへ commit する。
- 中間文書を wheel / sdist へ含めない。
- 中間文書を文書の正本として直接編集しない。
- 修正が必要な場合は canonical source を変更して再生成する。
- 生成時には `notice.toml` の注意事項と翻訳向けメタデータを埋め込む。

この配置により、canonical source の変更、実現結果の変更、英語翻訳の変更を別々の段階としてレビューできる。

## 外部情報

プロジェクト名、version、`requires-python`、公開 import package 名、CLI entry point、distribution 名など、既に `pyproject.toml` に正本を持つ値は canonical source に重複して固定しない。

`scripts/render_canonical_docs.py` が実現時点の値から `shikumi-devdoc` の context を構築し、`PROJECT.version` などの context 参照へ与える。

## 既存文書を更新する

既存文書を変更するときは、配置済みの英語 Markdown や中間文書から編集を始めない。

1. 対応する `canonical.py` を変更する。
2. 用語を変更した場合は `terms.py` を含めて中間成果物を再生成する。
3. 日本語中間文書の差分を確認する。
4. 中間文書を英語へ翻訳する。
5. 既存の英語文書を翻訳結果で置き換える。
6. 生成整合性と関連テストを確認する。

英語版だけに問題を見つけた場合も、最終的には canonical source へ修正を反映してから再生成する。

## 新しい文書を追加する

新しい文書を追加するときは、まずその文書の意味構造に `shikumi-devdoc` が提供する document、Vocabulary、CHANGELOG の規定体を再利用できるか判断する。

新規文書では、少なくとも次を決める。

- canonical source の配置
- 使用する `shikumi-devdoc` の規定体と実現器
- `_internal/document_build/ja/` 内の中間文書配置
- 英語版の配置先
- canonical source の検証テスト
- リポジトリ専用か、wheel / sdist にも含めるか

新しい生成対象は `scripts/render_canonical_docs.py` の一覧へ追加する。配布物へ含める場合だけ、`pyproject.toml` と配布物検査も更新する。

## 翻訳

配置版は英語で提供する。翻訳では、中間文書が持つ意味、章構造、コード例、公開 API 名、Python 名、CLI 名、パスなどを保つ。

`shikumi-devdoc` の translation-source metadata で表記維持対象となった用語は、その表記を変更しない。中間文書先頭の自動生成 notice と translation metadata は公開文書へ含めない。

翻訳の過程で、中間文書に存在しない仕様や説明を追加しない。原文に曖昧さや不足を見つけた場合は canonical source を修正し、中間文書の生成からやり直す。

## 配置と配布

README、公開リファレンス、公式作例の README、CHANGELOG などは distribution に含めることができる。一方、保守・運用だけを目的とする文書はリポジトリ専用にできる。

`_internal/document_source/`、`_internal/document_build/`、`shikumi-devdoc` 自体は Shikumi の wheel / sdist に含めない。

`DOCUMENTATION_WORKFLOW.md` 自身はリポジトリ専用文書とし、wheel / sdist には含めない。

## 確認

文書を配置した後は、少なくとも次を確認する。

- canonical source が対応する規定を満たすこと
- `python scripts/render_canonical_docs.py --check` が成功し、commit 済みの `terms.py` と日本語中間文書が正本から再現できること
- 中間文書に未解決の Vocabulary / context プレースホルダーが残っていないこと
- 英語版のコード例、リンク、公開名が壊れていないこと
- distribution 対象文書では、配布物検査が期待する配置と一致すること

CI でも中間文書の drift を検査する。
