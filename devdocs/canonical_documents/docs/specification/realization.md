<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/specification/realization.py` です。
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

# Realization Semantics

Realizer と realization check の意味上の契約。

## REAL_001

Realizer.realize() は SemanticView を受け取り、成果物を返す。成果物の Python type は Shikumi core が制限しない。

title: Realizer consumes a semantic view

level: MUST

related: [CORE_005](core.md#core_005)

## REAL_002

Realizer.check() は成果物を生成せず、その Realizer 固有の実現可能性を RealizationCheck として返す。

title: Check does not realize

level: MUST

## REAL_003

RealizationCheck.is_realizable は ERROR severity の diagnostic がない場合に true とする。

title: Realizability is determined by error diagnostics

level: MUST

## REAL_004

Realizer は Shikumi instance に登録または所有される必要がなく、同じ SemanticView に複数の Realizer を適用できる。

title: Realizers remain independent

level: MUST

related: [CORE_006](core.md#core_006)

## REAL_005

Realizer は必要であれば check() に独自条件を実装してよいが、core validation の代替として暗黙に扱ってはならない。

title: Realizer checks may add output-specific conditions

level: MAY

## REAL_006

RealizationCheck に subject=None の Diagnostic が渡された場合、check 対象 SemanticView の focus subject を diagnostic subject として補う。

title: Realization diagnostics default to the view focus

level: MUST
