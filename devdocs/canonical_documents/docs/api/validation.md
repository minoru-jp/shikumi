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
canonical source は `devdocs/canonical_sources/docs/api/validation.py` です。
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

# Validation API

ValidationRule、Diagnostic、ValidationResult など検証の公開 API。

related: [Validation Semantics](../specification/validation.md)

## 検証

        

### `DiagnosticSeverity`

```python
class DiagnosticSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
```

診断情報の重大度。

name: DiagnosticSeverity

kind: Type

### `Diagnostic`

```python
Diagnostic(
    message: str,
    code: str | None = None,
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR,
    subject: object | None = None,
)
```

一件の診断情報。`message` と `code`、`severity` は生成時に型を検証し、`severity` は `DiagnosticSeverity` そのものを要求する。文字列 `"error"` 等を暗黙変換しない。

検証規則が `subject=None` の診断情報を返した場合、その規則へ渡された意味像の焦点が自動的に `subject` として設定される。

related: [VAL_008](../specification/validation.md#val_008)

name: Diagnostic

kind: Type

### `ValidationRule`

```python
ValidationRule(
    focus_kind: StructuralKind,
    check: Callable[[SemanticView], ValidationOutput],
    name: str,
)
```

一つの検証規則。

`ValidationRule` は identity によって区別する。生成時に `focus_kind` が `StructuralKind`、`check` が callable、`name` が空でない `str` であることを検証する。

呼び出し時には `focus_kind` と一致する焦点の意味像を要求し、診断情報の tuple を返す。

name: ValidationRule

kind: Type

### `validator()`

```python
def validator(
    *,
    focus: StructuralKind,
    name: str | None = None,
) -> Callable[[ValidationFunction], ValidationRule]
```

通常の Python 関数から `ValidationRule` を定義するための補助デコレータ。

検証関数は `SemanticView` を受け取り、次のいずれかを返せる。

```python
None
Diagnostic
Iterable[Diagnostic]
```

例:

```python
from shikumi import (
    Diagnostic,
    InformationType,
    Shikumi,
    StructuralKind,
    attach_information,
    validator,
)

Title = InformationType("title", str)

@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic("title is required", code="title.required")

docs = Shikumi(information_types=[Title], validators=[require_title])

class MissingTitle:
    pass

invalid = docs.validate(MissingTitle)
assert not invalid.is_valid
assert invalid.diagnostics[0].code == "title.required"
assert invalid.diagnostics[0].subject is MissingTitle

class Titled:
    pass

attach_information(Titled, Title, "Overview")
assert docs.validate(Titled).is_valid
```

name: validator()

kind: Operation

input: function: Callable[[SemanticView], Diagnostic | Iterable[Diagnostic] | None]

output: ValidationRule

### `check_descriptor_uses()`

```python
def check_descriptor_uses(
    view: SemanticView,
    rules: Iterable[DescriptorUseRule],
) -> tuple[Diagnostic, ...]
```

意味像に記録された記述器使用を、記述器使用規則と照合して診断情報を返す。`Shikumi.validate()` は登録された `descriptor_rules` に対してこの検査を自動的に行う。

related: [VAL_003](../specification/validation.md#val_003)

name: check_descriptor_uses()

kind: Operation

input: view: SemanticView, rules: Iterable[DescriptorUseRule]

output: tuple[Diagnostic, ...]

### `StructureBinding`

```python
@dataclass(frozen=True)
class StructureBinding:
    logical_element: LogicalStructureElement
    actual_path: tuple[str, ...]
```

論理構造要素と、構造照合でその規定へ解決された具体 path の対応を表す。`ResolvedStructure` の actual path 自体は変更しない。

related: [STRUCT_013](../specification/structure.md#struct_013)

name: StructureBinding

kind: Type

### `StructureCheck`

```python
@dataclass(frozen=True)
class StructureCheck:
    specification: StructureSpecification
    placement: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    bindings: tuple[StructureBinding, ...] = ()
```

解決済み構造を構造規定と照合した結果を表す。`placement` は照合対象になった構造規定上の actual position を保持し、論理構造要素が解決された場合は `bindings` に logical-to-actual の対応を保持する。

related: [VAL_004](../specification/validation.md#val_004), [VAL_007](../specification/validation.md#val_007)

name: StructureCheck

kind: Type

#### `is_valid`

```python
@property
def is_valid(self) -> bool
```

`ERROR` の診断情報が一件もない場合に `True`。`bool(check)` は `check.is_valid` と同じ意味を持つ。

name: is_valid

kind: Value

### `check_structure()`

```python
def check_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
) -> StructureCheck
```

解決済み構造を構造規定と照合する。焦点の `placement` が指定されている場合はその subtree だけを、指定されていない場合は構造規定のルートを照合する。closed な exact / logical 規定では必要要素の欠落、kind 不一致、規定にない追加要素を error とする。unconstrained な構造断片では、その root より下の topology は検査しない。

```python
from shikumi import (
    Focus,
    PythonStructure,
    StructuralKind,
    StructureElement,
    StructureSpecification,
    check_structure,
)

class Page:
    pass

resolved = PythonStructure().resolve(Focus(Page))
expected = StructureSpecification(
    [StructureElement(path=(), kind=StructuralKind.ENTITY)]
)
assert check_structure(resolved, expected).is_valid

wrong = StructureSpecification(
    [StructureElement(path=(), kind=StructuralKind.MODULE)]
)
mismatch = check_structure(resolved, wrong)
assert not mismatch.is_valid
assert mismatch.diagnostics[0].code == "structure.kind.mismatch"
```

related: [VAL_004](../specification/validation.md#val_004), [VAL_007](../specification/validation.md#val_007)

name: check_structure()

kind: Operation

input: structure: ResolvedStructure, specification: StructureSpecification

output: StructureCheck

### `ValidationResult`

```python
@dataclass(frozen=True)
class ValidationResult:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...]
    structure_check: StructureCheck | None = None
```

一回の検証結果。構造規定を指定した場合、その照合結果を `structure_check` に保持し、構造上の診断情報も `diagnostics` に含める。

related: [VAL_002](../specification/validation.md#val_002)

name: ValidationResult

kind: Type

#### `is_valid`

```python
@property
def is_valid(self) -> bool
```

`ERROR` の診断情報が一件もない場合に `True`。

`bool(result)` は `result.is_valid` と同じ意味を持つ。

---

name: is_valid

kind: Value
