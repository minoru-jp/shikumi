<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/specification/core.py` です。
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

# Core Semantics

Shikumi の意味モデル全体に共通する契約。

## CORE_001

Shikumi は Python の実行後に成立した runtime object、情報、記述器使用を解釈対象とする。

title: Runtime state is the source of interpretation

level: MUST

## CORE_002

Shikumi は Python source を AST として解析し、source text から意味状態を再構成してはならない。

title: No AST-based semantic reconstruction

level: MUST NOT

## CORE_003

情報と記述器使用は Shikumi instance に所有されず、runtime object に対して成立する独立した実行時事実として扱う。

title: Runtime semantic state is independent of Shikumi instances

level: MUST

detail: 複数の Shikumi instance が同じ runtime object を、それぞれが認識する情報型や規則に従って解釈できる。

## CORE_004

Shikumi が構成する意味像には、その Shikumi が認識する情報だけを取り込む。未認識情報を runtime object から削除してはならない。

title: Interpret recognized information without mutating unknown information

level: MUST

## CORE_005

検証は意味像を入力とする意味上の判定であり、実現は意味像から成果物を生成する別操作として扱う。

title: Validation and realization are separate operations

level: MUST

## CORE_006

Realizer は Shikumi に登録・所有される構成要素ではない。同じ意味像へ複数の Realizer を独立して適用できる。

title: Realizers are independent consumers

level: MUST

## CORE_007

Shikumi は情報や記述器の意味を自動推論せず、規定側が明示した情報型、記述器使用規則、検証規則、構造を組み合わせて意味体系を構成する。

title: Meaning is author-defined

level: INFORMATIVE

## CORE_008

一つの SemanticView は一回の構造解決と runtime fact 取得から構成し、その subview や同一 validation 内の下位規則評価では、既に取り込んだ node、情報、記述器使用を再利用する。

title: Semantic views preserve one interpreted runtime snapshot

level: MUST
