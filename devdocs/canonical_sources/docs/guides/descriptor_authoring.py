"""Canonical Japanese guide for authoring Shikumi descriptors."""

from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title

from devdocs.canonical_sources.docs.vocabulary import TERMS

decorator_code = test_target_field("decorator example")
parameterized_code = test_target_field("parameterized decorator example")
binding_code = test_target_field("class binding example")
rule_code = test_target_field("descriptor rule example")


@summary("通常の Python を使って decorator や @= 記述器を定義する実装ガイド。")
@canonical_source(
    "記述器を定義する", filename="descriptor-authoring.md", order=20, heading="title"
)
class GUIDE:
    """{{TERM_1}} は具体的な{{TERM_15}} syntax を規定しない。規定体の著者は通常の Python で記述器を定義し、必要な runtime fact を明示的に記録する。"""

    merge @= TERMS.TERM_1
    merge @= TERMS.TERM_15

    class SECTION_001:
        """記述器使用と情報接続を明示的に行う decorator は、通常の Python method として実装できる。IDE の定義ジャンプ、docstring、型注釈も通常どおり利用できる。

        ```python
        {{decorator_code}}
        ```
        """

        title @= "引数を取らない decorator"

        decorator_code @= r"""
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
        """

    class SECTION_002:
        """decorator factory の引数や戻り値の作り方は記述器著者が所有する。{{TERM_1}} は signature から情報を推論しない。

        ```python
        {{parameterized_code}}
        ```
        """

        title @= "引数を取る decorator"

        merge @= TERMS.TERM_1

        parameterized_code @= r"""
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
        """

    class SECTION_003:
        """class body の評価時点では接続先 class がまだ成立していない。`class_binding()` は class body の実行完了後、かつ `__init_subclass__()` より前の class 作成処理中に callback を実行し、同じ binding name への繰り返し `@=` を記述順に再生する。現在の実装はこのタイミングを `__set_name__()` で実現するため、`__init_subclass__()` で追加される状態へ callback から依存してはならない。callback の例外は Shikumi が正規化せず Python runtime の class-creation semantics に従うため、Python 3.11 と 3.12 以降で外部から見える例外形状が異なる。

        `@=` は Shikumi Core が要求する syntax ではなく、独自{{TERM_15}}を作るために選択できる方法の一つである。通常の authoring flow では、外側の名前空間に保持された writer 自体は消費されず、各 class body の同名 name に一時 binding が置かれる。binding object 自体の aliasing や class 間での直接再利用は、公開された authoring contract には含めない。

        ```python
        {{binding_code}}
        ```
        """

        title @= "独自の @= 記述器"

        merge @= TERMS.TERM_15

        binding_code @= r"""
        from shikumi import (
            Cardinality,
            ClassBinding,
            InformationType,
            attach_information,
            class_binding,
            information_of,
            record_descriptor_use,
        )

        Tag = InformationType("tag", str, cardinality=Cardinality.MANY)

        class TagDescriptions:
            def __imatmul__(self, value: str) -> ClassBinding[str]:
                return class_binding(value, self._connect)

            def _connect(self, subject: type[object], value: str) -> None:
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
        """

    class SECTION_004:
        """記述器をどこで使用可能・推奨とするかは `DescriptorUseRule` と `StructureSelector` で記述できる。情報内容の validation とは別の責務である。

        ```python
        {{rule_code}}
        ```
        """

        title @= "記述器使用規則を組み合わせる"

        rule_code @= r"""
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
        """
