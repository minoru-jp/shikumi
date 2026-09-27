# Error API

Public exception types.

related: [Public API Boundary](../specification/public-api.md)

## Exceptions

### `ShikumiError`

Base class for exceptions defined by Shikumi.

name: ShikumiError

kind: Type


### `UnsupportedFocusError`

```python
class UnsupportedFocusError(ShikumiError, TypeError):
    ...
```

Raised when a Structure cannot interpret the supplied Focus.

name: UnsupportedFocusError

kind: Type


### `UnknownViewSubjectError`

```python
class UnknownViewSubjectError(ShikumiError, LookupError):
    ...
```

Raised when `SemanticView.item()` is asked for a subject that is not present in the Semantic View.


name: UnknownViewSubjectError

kind: Type

---
