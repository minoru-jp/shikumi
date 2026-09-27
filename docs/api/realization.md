# Realization API

Public APIs for independent Realizers and realization checks.

related: [Realization Semantics](../specification/realization.md)

## Realization

### `RealizationCheck`

```python
@dataclass(frozen=True)
class RealizationCheck:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...] = ()
```

The result of asking whether a particular Realizer can realize a Semantic View without generating an Artifact. `is_realizable` is `True` when there are no error Diagnostics. This is independent of conformance to the specification.

related: [REAL_003](../specification/realization.md#real_003), [REAL_006](../specification/realization.md#real_006)

name: RealizationCheck

kind: Type


#### `is_realizable`

```python
@property
def is_realizable(self) -> bool
```

`True` when there are no `Diagnostic`s with `ERROR` severity. `bool(check)` has the same meaning as `check.is_realizable`.

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

Abstract base class for generating an Artifact from a Semantic View. `check()` asks whether the supplied Semantic View is realizable without generating an Artifact. A Realizer with realization requirements overrides `check()` and returns unmet requirements as `Diagnostic`s. The default implementation treats the view as having no additional realization requirements.

A Realizer does not own a Shikumi and is not owned by a Shikumi. Multiple Realizers may be applied to the same Semantic View.

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

Shikumi does not restrict the Artifact type.


related: [REAL_001](../specification/realization.md#real_001), [REAL_002](../specification/realization.md#real_002), [REAL_004](../specification/realization.md#real_004)

name: Realizer

kind: Type

---
