# Architecture validation

This is a minimal example of using Shikumi to define application-specific architecture rules and validate Python descriptions.

It defines the `domain`, `application`, and `infrastructure` layers as information types and describes class dependencies with another information type. Shikumi itself knows nothing about these layers or dependency rules. The regulation in this example decides which dependency directions are allowed.

This example validates dependencies explicitly described through `DependsOn`. It does not discover actual Python imports or call graphs.

## Try it

From a repository checkout, put `examples/` on the Python path and use the example as ordinary Python code.

```python
from architecture import body
from architecture.shikumi_lib.norms import architecture

result = architecture.validate(body)
assert result.is_valid
```

If you change the description so that a `domain` class depends on an `application` class, the validation rule reports the invalid dependency direction.

## What to look at

- `Layer` and `DependsOn` are information types defined by this example.
- `@layer(...)` and `depends_on @= ...` are descriptors for writing the example's meaning in Python.
- Dependency-direction checks are implemented as validation rules focused on the package.
- Classes do not need a Shikumi base class or metaclass.
