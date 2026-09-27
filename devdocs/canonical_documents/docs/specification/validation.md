<!--
この文書は `shikumi-devdoc` で生成した日本語 canonical document です。
canonical source は `devdocs/canonical_sources/docs/specification/validation.py` です。
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

# Validation Semantics

SemanticView に対する validation の契約。

## VAL_001

ValidationRule は SemanticView を評価し、ゼロ件以上の Diagnostic を返す。validation は runtime state を自動補正してはならない。

title: Validation diagnoses without repair

level: MUST

## VAL_002

ValidationResult.is_valid は ERROR severity の diagnostic が一件もない場合にだけ true とする。warning と info は validation failure として扱わない。

title: Validity is determined by error diagnostics

level: MUST

## VAL_003

DescriptorUseRule は記述器使用対象の構造位置を評価し、allowed に不適合なら error、allowed には適合するが recommended に不適合なら warning を報告する。

title: Descriptor-use rule severity

level: MUST

related: [DESC_003](description.md#desc_003)

## VAL_004

構造検証は focus に対応する StructureSpecification の範囲について placement と StructuralKind の一致を評価する。

title: Structural validation compares the focused subtree

level: MUST

related: [STRUCT_004](structure.md#struct_004)

## VAL_005

Shikumi.validate() は view construction、descriptor-use check、任意の structure check、登録 ValidationRule の評価を一つの ValidationResult として集約する。

title: Shikumi validation aggregates semantic checks

level: MUST

## VAL_006

validation は Realizer.check() を暗黙に実行してはならない。realizer の実現可能性は規定への適合とは独立した判定である。

title: Validation does not imply realization checks

level: MUST NOT

## VAL_007

構造照合は選択された StructureSpecification の closed な規定範囲で、必要要素の欠落、kind 不一致、規定にない追加要素を error として報告する。LogicalStructureElement は解決された各 actual instance へ同じ closed fragment を適用し、unconstrained StructureFragment が明示された subtree だけは子孫の一致を要求しない。

title: Structure checking is closed unless explicitly unconstrained

level: MUST

related: [STRUCT_004](structure.md#struct_004), [STRUCT_009](structure.md#struct_009), [STRUCT_012](structure.md#struct_012)

## VAL_008

ValidationRule が subject=None の Diagnostic を返した場合、その規則へ渡された SemanticView の focus subject を diagnostic subject として補う。

title: Validation diagnostics default to the rule focus

level: MUST
