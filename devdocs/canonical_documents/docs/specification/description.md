<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/specification/description.py` です。
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

# Description Semantics

記述を runtime semantic state として成立させる契約。

## DESC_001

情報型は意味情報の種類、受理する Python value type、cardinality を定義し、その identity は InformationType object の identity による。

title: Information type identity

level: MUST

related: [CORE_003](core.md#core_003)

## DESC_002

情報接続は、対象、InformationType、値を一件の runtime information record として関連付ける。Cardinality.ONE であっても接続時点では複数値を禁止しない。

title: Attachment preserves observable runtime state

level: MUST

detail: Cardinality 違反は不正状態を保持したまま validation で診断できる。

## DESC_003

記述器使用と情報接続は別の実行時事実であり、一回の記述器使用がゼロ件、一件、複数件の情報接続を行ってよい。

title: Descriptor use and information attachment are distinct

level: MUST

## DESC_004

記述器の具体的な Python syntax は規定しない。decorator、@=、docstring、通常の関数呼び出しその他の実行時処理を利用できる。

title: Description syntax is open

level: MAY

## DESC_005

Shikumi は記述器関数の signature、戻り値、import 元、source 上の名称から情報や記述器使用規則を自動推論してはならない。

title: No descriptor inference

level: MUST NOT

related: [CORE_007](core.md#core_007)

## DESC_006

class body の @= 記述で接続先 class がまだ成立していない場合、class_binding は class 成立後まで値を保持し、指定 callback へ owner class と値を渡す低水準機構として振る舞う。

title: Class binding defers connection until class creation

level: MUST
