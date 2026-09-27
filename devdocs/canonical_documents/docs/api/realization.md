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
canonical source は `devdocs/canonical_sources/docs/api/realization.py` です。
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

# Realization API

SemanticView から成果物を生成する独立 Realizer の公開 API。

related: [Realization Semantics](../specification/realization.md)

## 実現

        

### `RealizationCheck`

```python
@dataclass(frozen=True)
class RealizationCheck:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...] = ()
```

成果物を生成せずに、特定の実現器が意味像を実現可能か問い合わせた結果。`is_realizable` は error 診断がない場合に `True`。規定への適合性とは独立している。

related: [REAL_003](../specification/realization.md#real_003), [REAL_006](../specification/realization.md#real_006)

name: RealizationCheck

kind: Type

#### `is_realizable`

```python
@property
def is_realizable(self) -> bool
```

`ERROR` severity の `Diagnostic` が一件もない場合に `True`。`bool(check)` は `check.is_realizable` と同じ意味を持つ。

related: [REAL_003](../specification/realization.md#real_003)

name: is_realizable

kind: Value

### `Realizer`

```python
class Realizer(ABC, Generic[ArtifactT]):
    def check(self, view: SemanticView) -> RealizationCheck:
        ...

    @abstractmethod
    def realize(self, view: SemanticView) -> ArtifactT:
        ...
```

意味像から成果物を生成するための抽象基底。`check()` は成果物を生成せず、与えられた意味像を実現可能か問い合わせる。実現条件を持つ実現器は `check()` を override し、満たされない条件を `Diagnostic` として返す。既定実装は追加の実現条件なしとして扱う。

実現器は Shikumi を所有せず、Shikumi からも所有されない。同じ意味像に複数の実現器を適用できる。

```python
from shikumi import InformationType, Realizer, Shikumi, attach_information

Title = InformationType("title", str)

class MarkdownTitle(Realizer[str]):
    def realize(self, view):
        return f"# {view.focused.values(Title)[0]}\n"

class DictTitle(Realizer[dict[str, str]]):
    def realize(self, view):
        return {"title": view.focused.values(Title)[0]}

class Page:
    pass

attach_information(Page, Title, "Overview")
view = Shikumi(information_types=[Title]).view(Page)

markdown = MarkdownTitle()
data = DictTitle()
assert markdown.check(view).is_realizable
assert markdown.realize(view) == "# Overview\n"
assert data.realize(view) == {"title": "Overview"}
```
成果物の型は Shikumi によって制限しない。

---

related: [REAL_001](../specification/realization.md#real_001), [REAL_002](../specification/realization.md#real_002), [REAL_004](../specification/realization.md#real_004)

name: Realizer

kind: Type
