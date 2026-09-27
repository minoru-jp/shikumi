"""Canonical Japanese API reference source for Information API."""

from devdocs.canonical_sources.docs.vocabulary import TERMS
from shikumi_devdoc.fields.api_reference import (
    NAMESPACE, OPERATION, OTHER, TYPE, VALUE,
    input, kind, name, output, related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title
from devdocs.canonical_sources.docs.specification.description import SPECIFICATION_PART as DESCRIPTION_SPEC


attachment_example = test_target_field("attachment example")
@summary('情報型と実行時情報接続の公開 API。')
@canonical_source('Information API', filename='information.md', order=0, heading="title")
class API_REFERENCE_PART:
    """InformationType と runtime information attachment の公開 API。"""

    related @= DESCRIPTION_SPEC

    class TITLE_4:
        r'''
        '''
        title @= "{{TERM_13}}"

        merge @= TERMS.TERM_13

        class TITLE_5:
            r'''
            ```python
            class Cardinality(str, Enum):
                ONE = "one"
                MANY = "many"
            ```

            {{TERM_12}}に許される{{TERM_13}}の個数を表す。

            `ONE` は意味上の単一値を表すが、{{TERM_14}}そのものは不正状態を禁止しない。複数値が接続された状態を保持したうえで、{{TERM_22}}が不適合として診断できる。
            '''
            title @= '`Cardinality`'
            name @= 'Cardinality'
            kind @= TYPE


            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_14
            merge @= TERMS.TERM_22

        class TITLE_6:
            r'''
            ```python
            class InformationType(Generic[T]):
                name: str
                value_type: type[T] | tuple[type[Any], ...]
                cardinality: Cardinality
            ```

            {{TERM_12}}を定義する。単一の `value_type` を指定した場合、その Python 型を型変数 `T` として静的型情報にも伝える。

            {{TERM_12}}の同一性はオブジェクト identity による。同じ `name` を持つ二つの `InformationType` は別の{{TERM_12}}である。

            コンストラクタは `name` が空でない `str`、`value_type` が `type` または空でない `tuple[type, ...]` で、かつ `isinstance()` の第2引数として利用可能であること、`cardinality` が `Cardinality` であることを検証する。不正な型を後段の `accepts()` まで持ち越さない。
            '''
            title @= '`InformationType`'
            related @= DESCRIPTION_SPEC.DESC_001

            name @= 'InformationType'
            kind @= TYPE


            merge @= TERMS.TERM_12

            class TITLE_7:
                r'''
                ```python
                name: str
                value_type: type[T] | tuple[type[Any], ...]
                cardinality: Cardinality
                ```
                '''
                title @= '属性'

            class TITLE_8:
                r'''
                ```python
                def accepts(self, value: object) -> bool
                ```

                `value` が `value_type` に適合するかを返す。これは値型の判定のみを行い、個数やその他の検証を行わない。

                {{TERM_12}}は、値が別の{{TERM_11}}、`module`、関数その他の Python オブジェクトである場合も特別扱いしない。{{TERM_1}} は参照解決や到達可能性の判定を行わず、その値をどのように利用するかは{{TERM_2}}側が定める。
                '''
                title @= '`accepts(value)`'
                name @= 'accepts(value)'
                kind @= OPERATION
                input @= 'value: object'
                output @= 'bool'


                merge @= TERMS.TERM_12
                merge @= TERMS.TERM_11
                merge @= TERMS.TERM_1
                merge @= TERMS.TERM_2

        class TITLE_9:
            r'''
            ```python
            @dataclass(frozen=True)
            class Information(Generic[T]):
                type: InformationType[T]
                value: T
                subject: object
            ```

            実行時対象へ接続された一件の{{TERM_13}}を表す。{{TERM_15}}が使用された事実は `Information` に埋め込まず、`DescriptorUse` として独立して記録する。
            '''
            title @= '`Information`'
            name @= 'Information'
            kind @= TYPE


            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_15

        class TITLE_10:
            r'''
            ```python
            def attach_information(
                subject: object,
                information_type: InformationType[T],
                value: T,
            ) -> Information[T]
            ```

            **{{TERM_14}}の標準導線。**

            `value` を `information_type` の{{TERM_13}}として `subject` へ接続し、生成した `Information` を返す。

            この関数は{{TERM_4}}構文ではない。{{TERM_2}}側が独自の{{TERM_15}}を定義するときに利用する低水準 API である。

            `attach_information()` 自体は次を{{TERM_21}}しない。

            - `value_type` への適合
            - `cardinality` への適合
            - {{TERM_1}} がその{{TERM_12}}を認識しているか

            これらは意味状態を保持した後、必要な{{TERM_22}}によって{{TERM_21}}する。

            `subject` は弱参照可能な実行時対象でなければならない。接続不能な対象に対しては `TypeError` を送出する。

            例:

            ```python
            {{attachment_example}}
            ```
            {{TERM_13}} registry は `subject` の `__eq__` / `__hash__` を用いず、runtime identity で管理する。registry 内部の記録は `subject` を直接保持せず、`information_of()` の取得時に公開 `Information` を組み立てる。したがって registry 自体は `subject` を直接強参照しない。ただし、`Information.value` に相当する内部値や、その値から到達可能な Python object が `subject` を参照している場合、その参照によって `subject` の寿命が延びることがある。{{TERM_1}} は{{TERM_13}}値自身の参照関係を弱参照化したり切断したりしない。
            '''
            title @= '`attach_information()`'
            attachment_example @= r"""
            from shikumi import (
                InformationType,
                attach_information,
                clear_information,
                information_of,
            )

            Title = InformationType("title", str)

            class Page:
                pass

            assert Title.accepts("Overview")
            assert not Title.accepts(42)

            record = attach_information(Page, Title, "Overview")
            assert record.subject is Page
            assert tuple(item.value for item in information_of(Page)) == ("Overview",)

            clear_information(Page)
            assert information_of(Page) == ()
            """

            related @= DESCRIPTION_SPEC.DESC_002

            name @= 'attach_information()'
            kind @= OPERATION
            input @= 'subject: object'
            input @= 'information_type: InformationType[T]'
            input @= 'value: T'
            output @= 'Information[T]'


            merge @= TERMS.TERM_14
            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_4
            merge @= TERMS.TERM_2
            merge @= TERMS.TERM_15
            merge @= TERMS.TERM_21
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_22

        class TITLE_11:
            r'''
            ```python
            def information_of(subject: object) -> tuple[Information[Any], ...]
            ```

            `subject` に直接接続された{{TERM_13}}を、接続順に返す。

            {{TERM_1}} による{{TERM_12}}の選別や{{TERM_10}}の{{TERM_18}}は行わない。
            '''
            title @= '`information_of()`'
            name @= 'information_of()'
            kind @= OPERATION
            input @= 'subject: object'
            output @= 'tuple[Information[Any], ...]'


            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_12
            merge @= TERMS.TERM_10
            merge @= TERMS.TERM_18

        class TITLE_12:
            r'''
            ```python
            def clear_information(subject: object) -> None
            ```

            `subject` に直接接続された{{TERM_13}}を削除する。

            主にテスト、対話的ツール、実行時ライフサイクルを明示的に管理する用途の API とする。通常の{{TERM_2}}・{{TERM_4}}では使用しない。
            '''
            title @= '`clear_information()`'
            name @= 'clear_information()'
            kind @= OPERATION
            input @= 'subject: object'
            output @= 'None'


            merge @= TERMS.TERM_13
            merge @= TERMS.TERM_2
            merge @= TERMS.TERM_4

