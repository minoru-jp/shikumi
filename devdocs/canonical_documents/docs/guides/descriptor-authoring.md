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
canonical source は `devdocs/canonical_sources/docs/guides/descriptor_authoring.py` です。
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

# 記述器を定義する

Shikumi は具体的な記述器 syntax を規定しない。規定体の著者は通常の Python で記述器を定義し、必要な runtime fact を明示的に記録する。

## 引数を取らない decorator

記述器使用と情報接続を明示的に行う decorator は、通常の Python method として実装できる。IDE の定義ジャンプ、docstring、型注釈も通常どおり利用できる。

```python
from shikumi import (
    Cardinality,
    InformationType,
    attach_information,
    descriptor_uses_of,
    information_of,
    record_descriptor_use,
)

Kind = InformationType("kind", str, cardinality=Cardinality.MANY)

class KindDescriptions:
    def attr(self, subject):
        record_descriptor_use(subject, self.attr)
        attach_information(subject, Kind, "attr")
        return subject

    def service(self, subject):
        record_descriptor_use(subject, self.service)
        attach_information(subject, Kind, "service")
        return subject

kind = KindDescriptions()

@kind.attr
class Owner:
    pass

@kind.service
class UserService:
    pass

assert [record.value for record in information_of(Owner)] == ["attr"]
assert descriptor_uses_of(UserService)[0].subject is UserService
```

## 引数を取る decorator

decorator factory の引数や戻り値の作り方は記述器著者が所有する。Shikumi は signature から情報を推論しない。

```python
from shikumi import (
    Cardinality,
    InformationType,
    attach_information,
    information_of,
    record_descriptor_use,
)

Uses = InformationType("uses", type, cardinality=Cardinality.MANY)

class RelationDescriptions:
    def uses(self, target: type):
        def decorate(subject):
            record_descriptor_use(subject, self.uses)
            attach_information(subject, Uses, target)
            return subject
        return decorate

relation = RelationDescriptions()

class UserRepository:
    pass

@relation.uses(UserRepository)
class UserService:
    pass

assert information_of(UserService)[0].value is UserRepository
```

## 独自の @= 記述器

class body の評価時点では接続先 class がまだ成立していない。`class_binding()` を使うと class 成立後に callback を実行でき、同じ binding name への繰り返し `@=` も記述順に再生される。

```python
from shikumi import (
    Cardinality,
    InformationType,
    attach_information,
    class_binding,
    information_of,
    record_descriptor_use,
)

Tag = InformationType("tag", str, cardinality=Cardinality.MANY)

class TagDescriptions:
    def __imatmul__(self, value: str):
        return class_binding(value, self._connect)

    def _connect(self, subject: type, value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(subject, Tag, value)

tag = TagDescriptions()

class UserService:
    tag @= "application"
    tag @= "users"

assert [record.value for record in information_of(UserService)] == [
    "application",
    "users",
]
```

## 記述器使用規則を組み合わせる

記述器をどこで使用可能・推奨とするかは `DescriptorUseRule` と `StructureSelector` で記述できる。情報内容の validation とは別の責務である。

```python
from shikumi import (
    DescriptorUseRule,
    InformationType,
    Shikumi,
    StructuralKind,
    StructureSelector,
)
from shikumi.standard import decorator

Kind = InformationType("kind", str)
service = decorator(Kind)

service_rule = DescriptorUseRule(
    descriptor=service,
    allowed=StructureSelector(kind=StructuralKind.ENTITY),
    recommended=StructureSelector(
        kind=StructuralKind.ENTITY,
        under=("api",),
    ),
    name="service",
)

system = Shikumi(
    information_types=[Kind],
    descriptor_rules=[service_rule],
)

@service("service")
class Endpoint:
    pass

result = system.validate(Endpoint)
assert result.is_valid
```
