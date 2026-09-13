"""Shikumi API Reference の正本の記述体。

``TITLE_N`` の数値部分は Python 上で各見出しを識別するためだけに存在し、
順序、階層、見出し名その他の意味を一切表さない。
"""

from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs
from _internal.document_source.vocabulary import terms

@canonical
@vocabulary(terms)
@title('{{TERM_1}} API Reference')
class TITLE_1:
    r'''
    この文書は {{TERM_1}} の公開 API と、その意味上の契約を定義する。
    
    [`glossary.md`](./glossary.md) は概念の正規定義であり、この文書はその概念を Python API としてどのように公開するかを定める。概念上の意味に不一致がある場合は `glossary.md` を優先する。
    
    この文書に記載しないモジュール、クラス、関数、属性は内部実装として扱う。公開 API は `{{PROJECT.import_package}}` と `{{PROJECT.import_package}}.standard` から提供する。
    
    この API 仕様は実装に先行して定義されることがある。公開実装はこの文書へ適合させる。
    '''

    vocabulary_refs @= (
        terms.TERM_1,
    )


    @title('基本契約')
    class TITLE_2:
        r'''
        {{TERM_1}} は Python の実行後に成立した対象と{{TERM_13}}を扱う。Python source を AST として{{TERM_18}}して意味状態を再構成しない。
        
        {{TERM_13}}は {{TERM_1}} インスタンスに所有されない。{{TERM_2}}側は{{TERM_14}}を通じて Python の実行時対象へ{{TERM_13}}を接続し、{{TERM_1}} は自身が認識する{{TERM_12}}だけを{{TERM_19}}へ取り込む。
        
        {{TERM_15}}の具体的な形式は公開 API によって制限しない。デコレータ、`@=`、docstring、通常の関数呼び出し、その他の実行時処理を利用できる。{{TERM_16}}と{{TERM_14}}は別の実行時事実として扱い、{{TERM_2}}側は必要な場合だけ `record_descriptor_use()` で使用事実を記録し、`attach_information()` で{{TERM_13}}を接続する。
        
        {{TERM_21}}は{{TERM_19}}を対象とし、{{TERM_26}}は{{TERM_19}}から{{TERM_28}}を生成する。{{TERM_26}}は {{TERM_1}} に所有されない。
        
        ---
        '''

        vocabulary_refs @= (
            terms.TERM_1,
            terms.TERM_13,
            terms.TERM_18,
            terms.TERM_2,
            terms.TERM_14,
            terms.TERM_12,
            terms.TERM_19,
            terms.TERM_15,
            terms.TERM_16,
            terms.TERM_21,
            terms.TERM_26,
            terms.TERM_28,
        )


@title('Core API: `{{PROJECT.import_package}}`')
class TITLE_3:
    r'''
    '''

    vocabulary_refs @= (
    )

    @title('{{TERM_13}}')
    class TITLE_4:
        r'''
        '''

        vocabulary_refs @= (
            terms.TERM_13,
        )

        @title('`Cardinality`')
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

            vocabulary_refs @= (
                terms.TERM_12,
                terms.TERM_13,
                terms.TERM_14,
                terms.TERM_22,
            )

        @title('`InformationType`')
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

            vocabulary_refs @= (
                terms.TERM_12,
            )

            @title('属性')
            class TITLE_7:
                r'''
                ```python
                name: str
                value_type: type[T] | tuple[type[Any], ...]
                cardinality: Cardinality
                ```
                '''

            @title('`accepts(value)`')
            class TITLE_8:
                r'''
                ```python
                def accepts(self, value: object) -> bool
                ```
                
                `value` が `value_type` に適合するかを返す。これは値型の判定のみを行い、個数やその他の検証を行わない。
                
                {{TERM_12}}は、値が別の{{TERM_11}}、`module`、関数その他の Python オブジェクトである場合も特別扱いしない。{{TERM_1}} は参照解決や到達可能性の判定を行わず、その値をどのように利用するかは{{TERM_2}}側が定める。
                '''

                vocabulary_refs @= (
                    terms.TERM_12,
                    terms.TERM_11,
                    terms.TERM_1,
                    terms.TERM_2,
                )

        @title('`Information`')
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

            vocabulary_refs @= (
                terms.TERM_13,
                terms.TERM_15,
            )

        @title('`attach_information()`')
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
            
            {{TERM_13}} registry は `subject` の `__eq__` / `__hash__` を用いず、runtime identity で管理する。registry 内部の記録は `subject` を直接保持せず、`information_of()` の取得時に公開 `Information` を組み立てる。したがって registry 自体は `subject` を直接強参照しない。ただし、`Information.value` に相当する内部値や、その値から到達可能な Python object が `subject` を参照している場合、その参照によって `subject` の寿命が延びることがある。{{TERM_1}} は{{TERM_13}}値自身の参照関係を弱参照化したり切断したりしない。
            '''

            vocabulary_refs @= (
                terms.TERM_14,
                terms.TERM_13,
                terms.TERM_4,
                terms.TERM_2,
                terms.TERM_15,
                terms.TERM_21,
                terms.TERM_1,
                terms.TERM_12,
                terms.TERM_22,
            )

        @title('`information_of()`')
        class TITLE_11:
            r'''
            ```python
            def information_of(subject: object) -> tuple[Information[Any], ...]
            ```
            
            `subject` に直接接続された{{TERM_13}}を、接続順に返す。
            
            {{TERM_1}} による{{TERM_12}}の選別や{{TERM_10}}の{{TERM_18}}は行わない。
            '''

            vocabulary_refs @= (
                terms.TERM_13,
                terms.TERM_1,
                terms.TERM_12,
                terms.TERM_10,
                terms.TERM_18,
            )

        @title('`clear_information()`')
        class TITLE_12:
            r'''
            ```python
            def clear_information(subject: object) -> None
            ```
            
            `subject` に直接接続された{{TERM_13}}を削除する。
            
            主にテスト、対話的ツール、実行時ライフサイクルを明示的に管理する用途の API とする。通常の{{TERM_2}}・{{TERM_4}}では使用しない。
            '''

            vocabulary_refs @= (
                terms.TERM_13,
                terms.TERM_2,
                terms.TERM_4,
            )

    @title('{{TERM_16}}')
    class TITLE_13:
        r'''
        '''

        vocabulary_refs @= (
            terms.TERM_16,
        )

        @title('`DescriptorUse`')
        class TITLE_14:
            r'''
            ```python
            @dataclass(frozen=True)
            class DescriptorUse:
                descriptor: object
                subject: object
            ```
            
            ある{{TERM_15}}がある実行時対象に使用されたという事実を表す。{{TERM_14}}とは独立しており、一回の{{TERM_16}}がゼロ件、一件、複数件の{{TERM_14}}を行ってよい。
            '''

            vocabulary_refs @= (
                terms.TERM_15,
                terms.TERM_14,
                terms.TERM_16,
            )

        @title('`record_descriptor_use()`')
        class TITLE_15:
            r'''
            ```python
            def record_descriptor_use(
                subject: object,
                descriptor: object,
            ) -> DescriptorUse
            ```
            
            `descriptor` が `subject` に使用されたことを記録する低水準 API。{{TERM_15}}の import 元やソース上の名称は追跡せず、渡された Python object を実行時 identity として扱う。bound method は同じ instance と underlying function の組として照合されるため、`writer.describe` を属性アクセスし直しても同じ{{TERM_15}}として判定できる。
            '''

            vocabulary_refs @= (
                terms.TERM_15,
            )

        @title('`descriptor_uses_of()` / `clear_descriptor_uses()`')
        class TITLE_16:
            r'''
            ```python
            def descriptor_uses_of(subject: object) -> tuple[DescriptorUse, ...]
            def clear_descriptor_uses(subject: object) -> None
            ```
            
            対象へ直接記録された{{TERM_16}}を取得または削除する。`clear_descriptor_uses()` は主にテストや実行時ライフサイクル管理のための API である。
            
            {{TERM_16}} registry も{{TERM_13}} registry と同様に、対象の `__eq__` / `__hash__` ではなく runtime identity で管理する。内部記録は対象を直接保持せず、取得時に公開 `DescriptorUse` を組み立てるため、registry 自体は対象を直接強参照しない。ただし、記録された `descriptor` 自身、またはそこから到達可能な Python object が対象を参照している場合、その参照によって対象の寿命が延びることがある。たとえば instance の bound method は通常その instance を保持する。{{TERM_1}} は{{TERM_15}}自身の参照関係を弱参照化したり切断したりしない。
            '''

            vocabulary_refs @= (
                terms.TERM_16,
                terms.TERM_13,
                terms.TERM_1,
                terms.TERM_15,
            )

        @title('`StructureSelector`')
        class TITLE_17:
            r'''
            ```python
            StructureSelector(
                *,
                kind: StructuralKind | None = None,
                at: tuple[str, ...] | None = None,
                under: tuple[str, ...] | None = None,
            )
            ```
            
            {{TERM_17}}が対象とする{{TERM_7}}上の位置を選択する。`kind` は{{TERM_7}}種別、`at` は一つの有効 path との完全一致、`under` は指定 path 自身を含むその配下を表す。`at` と `under` は同時に指定できない。何も指定しない selector はすべての位置に一致する。複数の候補位置を許可する場合は `StructureSelector.one_of(a, b, ...)` または `a | b` で selector を OR 合成できる。
            '''

            vocabulary_refs @= (
                terms.TERM_17,
                terms.TERM_7,
            )

            @title('`one_of()` / `|`')
            class TITLE_18:
                r'''
                ```python
                @classmethod
                def one_of(
                    cls,
                    *selectors: StructureSelector,
                ) -> StructureSelector
                ```
                
                複数の selector のいずれかに一致する selector を返す。`a | b` は `StructureSelector.one_of(a, b)` と同じ意味を持つ。
                
                path は{{TERM_8}}と同じ{{TERM_2}}ルート基準で評価する。package 全体を{{TERM_20}}にした場合は package 自身をルート `()` とし、単独 module に `placement` を指定した場合はその予定配置を有効 path として用いる。
                '''

                vocabulary_refs @= (
                    terms.TERM_8,
                    terms.TERM_2,
                    terms.TERM_20,
                )

        @title('`DescriptorUseRule`')
        class TITLE_19:
            r'''
            ```python
            DescriptorUseRule(
                descriptor: object,
                allowed: StructureSelector,
                recommended: StructureSelector | None = None,
                name: str | None = None,
            )
            ```
            
            一つの{{TERM_15}}を{{TERM_7}}上のどこで使用可能または推奨とするかを定める。`allowed` に一致しない使用は error、`allowed` には一致するが `recommended` に一致しない使用は warning となる。`recommended=None` の場合、許可範囲内の位置をすべて同等に扱う。
            
            規則が存在しない{{TERM_15}}は、この仕組みによる{{TERM_7}}上の制約を受けない。{{TERM_12}}、{{TERM_13}}値、import 元などから暗黙の使用範囲を推論しない。
            '''

            vocabulary_refs @= (
                terms.TERM_15,
                terms.TERM_7,
                terms.TERM_12,
                terms.TERM_13,
            )

    @title('`@=` 用のクラス接続')
    class TITLE_20:
        r'''
        '''

        @title('`class_binding()`')
        class TITLE_21:
            r'''
            ```python
            def class_binding(
                value: T,
                connect: Callable[[type, T], None],
            ) -> object
            ```
            
            クラス本体の実行中にはまだ存在しないクラス{{TERM_11}}に対して、クラス成立後に処理を適用するための低水準 API。
            
            `@=` を用いる独自{{TERM_15}}の著者が利用する。{{TERM_1}} は `value` の型や意味を{{TERM_18}}せず、クラス成立後に `connect(subject, value)` を呼び出すことだけを保証する。
            
            返されたオブジェクトは、同じ名前に対する連続した `@=` を受け取れる。
            
            ```python
            class Tags:
                def __init__(self, information_type: InformationType) -> None:
                    self.information_type = information_type
            
                def __imatmul__(self, value: str):
                    return class_binding(value, self._connect)
            
                def _connect(self, subject: type, value: str) -> None:
                    record_descriptor_use(subject, self)
                    attach_information(
                        subject,
                        self.information_type,
                        value,
                    )
            
            
            tags = Tags(Tag)
            
            class Page:
                tags @= "python"
                tags @= "runtime"
            ```
            
            `class_binding()` はクラス成立後の処理タイミングを提供するだけであり、{{TERM_16}}の記録や{{TERM_14}}そのものを強制しない。{{TERM_1}} の{{TERM_15}}として利用する場合、必要に応じて `connect` から `record_descriptor_use()` と `attach_information()` をそれぞれ呼び出す。
            
            `class_binding()` の内部実装方法は公開契約に含めない。
            
            ---
            '''

            vocabulary_refs @= (
                terms.TERM_11,
                terms.TERM_15,
                terms.TERM_1,
                terms.TERM_18,
                terms.TERM_16,
                terms.TERM_14,
            )

    @title('{{TERM_7}}と{{TERM_20}}')
    class TITLE_22:
        r'''
        '''

        vocabulary_refs @= (
            terms.TERM_7,
            terms.TERM_20,
        )

        @title('`Focus`')
        class TITLE_23:
            r'''
            ```python
            @dataclass(frozen=True)
            class Focus:
                subject: object
                placement: tuple[str, ...] | None = None
            ```
            
            {{TERM_19}}を構成するときの{{TERM_20}}を表す。`placement` は、対象を{{TERM_7}}上のどこに配置したものとして{{TERM_18}}するかを明示するための任意の位置である。`None` は配置を指定していないことを表し、空 tuple `()` は{{TERM_8}}のルートを明示的に表す。
            
            通常は `{{TERM_1}}.view(subject)` / `{{TERM_1}}.validate(subject)` に実行時対象を直接渡せる。単独の module を{{TERM_21}}するときは配置を明示する必要がある。package 全体の{{TERM_21}}中に下位 module へ{{TERM_22}}を適用する場合、その配置は解決済み{{TERM_7}}から引き継がれる。
            '''

            vocabulary_refs @= (
                terms.TERM_19,
                terms.TERM_20,
                terms.TERM_7,
                terms.TERM_18,
                terms.TERM_8,
                terms.TERM_1,
                terms.TERM_21,
                terms.TERM_22,
            )

        @title('`StructuralKind`')
        class TITLE_24:
            r'''
            ```python
            class StructuralKind(str, Enum):
                PACKAGE = "package"
                MODULE = "module"
                ENTITY = "entity"
            ```
            
            Core が表現する{{TERM_7}}上の種別。
            '''

            vocabulary_refs @= (
                terms.TERM_7,
            )

        @title('`StructureNode`')
        class TITLE_25:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureNode:
                subject: object
                kind: StructuralKind
                name: str
                path: tuple[str, ...]
                parent: object | None = None
            ```
            
            {{TERM_10}}上の一位置を表す。
            
            `subject` は実行時対象、`path` は{{TERM_7}}上の位置を表す。`parent` は親となる実行時対象を持ち得る。
            '''

            vocabulary_refs @= (
                terms.TERM_10,
                terms.TERM_7,
            )

        @title('`ResolvedStructure`')
        class TITLE_26:
            r'''
            ```python
            @dataclass(frozen=True)
            class ResolvedStructure:
                focus: Focus
                nodes: tuple[StructureNode, ...]
            ```
            
            一つの{{TERM_20}}について解決された{{TERM_10}}。
            '''

            vocabulary_refs @= (
                terms.TERM_20,
                terms.TERM_10,
            )

            @title('`node_for(subject)`')
            class TITLE_27:
                r'''
                ```python
                def node_for(self, subject: object) -> StructureNode | None
                ```
                
                identity が一致する対象のノードを返す。
                
                `ResolvedStructure` は生成時に{{TERM_7}}の{{TERM_24}}を{{TERM_21}}する。少なくとも、{{TERM_20}}対象がちょうど一度だけ存在すること、`path` が一意であること、`subject` が identity で一意であること、すべてのノードが{{TERM_20}} root の配下にあること、{{TERM_20}}以外の各 path に{{TERM_7}}上の親 path が存在することを要求する。独自 `Structure` はこれらを満たさない `ResolvedStructure` を返せない。
                '''

                vocabulary_refs @= (
                    terms.TERM_7,
                    terms.TERM_24,
                    terms.TERM_21,
                    terms.TERM_20,
                )

        @title('`Structure`')
        class TITLE_28:
            r'''
            ```python
            class Structure(ABC):
                @abstractmethod
                def resolve(self, focus: Focus) -> ResolvedStructure:
                    ...
            ```
            
            {{TERM_7}}を{{TERM_18}}するための抽象基底。
            
            独自{{TERM_7}}は `resolve()` を実装し、{{TERM_20}}を含む `ResolvedStructure` を返す。
            '''

            vocabulary_refs @= (
                terms.TERM_7,
                terms.TERM_18,
                terms.TERM_20,
            )

        @title('`PythonStructure`')
        class TITLE_29:
            r'''
            ```python
            PythonStructure()
            ```
            
            Core が提供する最小の Python {{TERM_7}}。`PythonStructure`ではclassを`StructuralKind.ENTITY`として扱い、functionやmethodは{{TERM_11}}に含めない。
            
            - `class` を{{TERM_20}}にした場合、その{{TERM_11}}だけを{{TERM_18}}する。
            - `module` を{{TERM_20}}にした場合、その module と、その module で定義された class を{{TERM_18}}する。class の内部に字句上定義された入れ子 class も再帰的に{{TERM_11}}として含める。
            - `package` は package として識別するが、子 module を暗黙に import しない。
            - import された外部 class を、その module の{{TERM_11}}として扱わない。
            - 別の場所で定義された class を class 属性として代入しただけの alias は、入れ子{{TERM_11}}として扱わない。
            - `Focus.placement` が指定された場合、runtime object の identity は変えず、解決される{{TERM_7}}上の path をその位置へ再配置する。
            '''

            vocabulary_refs @= (
                terms.TERM_7,
                terms.TERM_11,
                terms.TERM_20,
                terms.TERM_18,
            )

        @title('`StructureElement`')
        class TITLE_30:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureElement:
                path: tuple[str, ...]
                kind: StructuralKind
            ```
            
            {{TERM_8}}において、ルートからの相対 path に要求される{{TERM_7}}上の種別を表す。ルート自身の path は `()` とする。
            '''

            vocabulary_refs @= (
                terms.TERM_8,
                terms.TERM_7,
            )

        @title('`StructureSpecification`')
        class TITLE_31:
            r'''
            ```python
            StructureSpecification(elements: Iterable[StructureElement])
            ```
            
            {{TERM_8}}を、ルート相対の `StructureElement` の集合として表す。要素 path は一意でなければならず、ルート要素 `()` と、各要素の親 path が存在しなければならない。

            現在の構造照合は完全一致であり、必要な要素の欠落だけでなく、規定にない追加要素もerrorとする。
            
            {{TERM_3}}は `StructureSpecification` を通常の Python object として明示的に公開できる。別の{{TERM_5}}から{{TERM_8}}を得る場合も、最終的には同じ `StructureSpecification` として表現する。{{TERM_1}} はこの二つの取得方法を自動で切り替えない。
            '''

            vocabulary_refs @= (
                terms.TERM_8,
                terms.TERM_3,
                terms.TERM_5,
                terms.TERM_1,
            )

            @title('`from_resolved()`')
            class TITLE_32:
                r'''
                ```python
                @classmethod
                def from_resolved(
                    cls,
                    structure: ResolvedStructure,
                ) -> StructureSpecification
                ```
                
                解決済み{{TERM_7}}から、その{{TERM_20}}をルート `()` とする{{TERM_8}}を導出する。
                '''

                vocabulary_refs @= (
                    terms.TERM_7,
                    terms.TERM_20,
                    terms.TERM_8,
                )

            @title('`element_at()` / `subtree()`')
            class TITLE_33:
                r'''
                ```python
                def element_at(self, path: tuple[str, ...]) -> StructureElement | None
                def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]
                ```
                
                指定位置の要素、または指定位置以下の部分{{TERM_7}}を返す。
                
                ---
                '''

                vocabulary_refs @= (
                    terms.TERM_7,
                )

    @title('{{TERM_19}}')
    class TITLE_34:
        r'''
        '''

        vocabulary_refs @= (
            terms.TERM_19,
        )

        @title('`ViewItem`')
        class TITLE_35:
            r'''
            ```python
            @dataclass(frozen=True)
            class ViewItem:
                node: StructureNode
                information: tuple[Information[Any], ...]
                descriptor_uses: tuple[DescriptorUse, ...] = ()
            ```
            
            {{TERM_19}}に含まれる一つの{{TERM_6}}を表す。
            '''

            vocabulary_refs @= (
                terms.TERM_19,
                terms.TERM_6,
            )

            @title('`subject`')
            class TITLE_36:
                r'''
                ```python
                @property
                def subject(self) -> object
                ```
                
                `node.subject` を返す。
                '''

            @title('`kind`')
            class TITLE_37:
                r'''
                ```python
                @property
                def kind(self) -> StructuralKind
                ```
                
                `node.kind` を返す。
                '''

            @title('`records(information_type)`')
            class TITLE_38:
                r'''
                ```python
                def records(
                    self,
                    information_type: InformationType[T],
                ) -> tuple[Information[T], ...]
                ```
                
                指定した{{TERM_12}}の{{TERM_13}}を identity によって選別して返す。
                '''

                vocabulary_refs @= (
                    terms.TERM_12,
                    terms.TERM_13,
                )

            @title('`values(information_type)`')
            class TITLE_39:
                r'''
                ```python
                def values(
                    self,
                    information_type: InformationType[T],
                ) -> tuple[T, ...]
                ```
                
                指定した{{TERM_12}}の値を接続順に返す。
                
                単一値の{{TERM_12}}であっても、{{TERM_21}}前には複数値が存在し得るため、常に tuple を返す。
                
                `InformationType[T]` の型変数は `records()` / `values()` まで伝播する。例えば `Title = InformationType("title", str)` を静的型検査器が `InformationType[str]` と解釈した場合、`item.values(Title)` は `tuple[str, ...]` になる。{{TERM_1}} は `py.typed` を配布し、この Core の{{TERM_12}}から取得までの型関係を公開契約に含める。
                
                複数の Python 型を `value_type=(str, int)` のように指定する場合は、現段階では型変数を精密な union として導出することを保証しない。また、Standard の `assignment()` / `decorator()` や任意の独自{{TERM_15}}へ `T` を完全に伝播させることも、この第一段階の契約には含めない。{{TERM_15}}の runtime 上の自由度を保ち、型付けのためだけに{{TERM_15}} API を複雑化しない。
                '''

                vocabulary_refs @= (
                    terms.TERM_12,
                    terms.TERM_21,
                    terms.TERM_1,
                    terms.TERM_15,
                )

            @title('`has(information_type)`')
            class TITLE_40:
                r'''
                ```python
                def has(self, information_type: InformationType[T]) -> bool
                ```
                
                指定した{{TERM_12}}の{{TERM_13}}を一件以上持つかを返す。
                '''

                vocabulary_refs @= (
                    terms.TERM_12,
                    terms.TERM_13,
                )

            @title('`uses(descriptor)`')
            class TITLE_41:
                r'''
                ```python
                def uses(self, descriptor: object) -> tuple[DescriptorUse, ...]
                ```
                
                この対象へ記録された、指定{{TERM_15}}による使用を返す。bound method は同じ bound instance と underlying function によって照合する。
                '''

                vocabulary_refs @= (
                    terms.TERM_15,
                )

        @title('`SemanticView`')
        class TITLE_42:
            r'''
            ```python
            @dataclass(frozen=True)
            class SemanticView:
                focus: Focus
                structure: ResolvedStructure
                items: tuple[ViewItem, ...]
            ```
            
            一つの{{TERM_20}}について構成された{{TERM_19}}。
            '''

            vocabulary_refs @= (
                terms.TERM_20,
                terms.TERM_19,
            )

            @title('`focused`')
            class TITLE_43:
                r'''
                ```python
                @property
                def focused(self) -> ViewItem
                ```
                
                {{TERM_20}}そのものに対応する `ViewItem` を返す。
                '''

                vocabulary_refs @= (
                    terms.TERM_20,
                )

            @title('`entities`')
            class TITLE_44:
                r'''
                ```python
                @property
                def entities(self) -> tuple[ViewItem, ...]
                ```
                
                {{TERM_11}}に対応する項目を返す。
                '''

                vocabulary_refs @= (
                    terms.TERM_11,
                )

            @title('`modules`')
            class TITLE_45:
                r'''
                ```python
                @property
                def modules(self) -> tuple[ViewItem, ...]
                ```
                
                module に対応する項目を返す。
                '''

            @title('`packages`')
            class TITLE_46:
                r'''
                ```python
                @property
                def packages(self) -> tuple[ViewItem, ...]
                ```
                
                package に対応する項目を返す。
                '''

            @title('`item(subject)`')
            class TITLE_47:
                r'''
                ```python
                def item(self, subject: object) -> ViewItem
                ```
                
                identity が一致する対象の `ViewItem` を返す。{{TERM_19}}に存在しない場合は `UnknownViewSubjectError` を送出する。
                '''

                vocabulary_refs @= (
                    terms.TERM_19,
                )

            @title('`subview(subject)`')
            class TITLE_48:
                r'''
                ```python
                def subview(self, subject: object) -> SemanticView
                ```
                
                この{{TERM_19}}にすでに含まれている対象を新しい{{TERM_20}}とし、その{{TERM_7}}上の subtree から部分{{TERM_19}}を返す。元の `ResolvedStructure`、{{TERM_13}}、{{TERM_16}}を再利用し、Python runtime を再{{TERM_18}}しない。元の{{TERM_20}}自身を指定した場合は同じ `SemanticView` を返す。{{TERM_19}}に存在しない対象では `UnknownViewSubjectError` を送出する。
                
                `SemanticView` は iterable であり、`items` の順序で `ViewItem` を反復する。
                
                ---
                '''

                vocabulary_refs @= (
                    terms.TERM_19,
                    terms.TERM_20,
                    terms.TERM_7,
                    terms.TERM_13,
                    terms.TERM_16,
                    terms.TERM_18,
                )

    @title('{{TERM_1}}')
    class TITLE_49:
        r'''
        '''

        vocabulary_refs @= (
            terms.TERM_1,
        )

        @title('`{{TERM_1}}`')
        class TITLE_50:
            r'''
            ```python
            {{TERM_1}}(
                *,
                structure: Structure | None = None,
                information_types: Iterable[InformationType[Any]] = (),
                validators: Iterable[ValidationRule] = (),
                descriptor_rules: Iterable[DescriptorUseRule] = (),
            )
            ```
            
            {{TERM_7}}、認識する{{TERM_12}}、{{TERM_22}}、{{TERM_17}}を一つの意味体系として構成する。
            
            `structure=None` の場合は `PythonStructure()` を使用する。明示的に指定する場合は `Structure` のインスタンスでなければならない。独自の{{TERM_7}}{{TERM_18}}は `Structure` を継承して実装できる。
            
            `information_types`、`validators`、`descriptor_rules` の各要素は、それぞれ `InformationType`、`ValidationRule`、`DescriptorUseRule` でなければならない。同一のオブジェクトを同じ {{TERM_1}} に重複登録してはならない。種類が異なる構成要素は constructor で `TypeError` とし、重複は `ValueError` とする。
            
            constructor が保証するのは、構成要素の種類と局所的な登録{{TERM_24}}までである。`Structure.resolve()` を試行したり、{{TERM_22}}同士の意味的整合性、{{TERM_17}}が実際の{{TERM_7}}で到達可能かといった意味的妥当性を事前評価したりはしない。これらは各構成要素の実行時の責務であり、独自拡張の表現力を constructor 検証のために狭めない。
            '''

            vocabulary_refs @= (
                terms.TERM_1,
                terms.TERM_7,
                terms.TERM_12,
                terms.TERM_22,
                terms.TERM_17,
                terms.TERM_18,
                terms.TERM_24,
            )

        @title('`recognizes()`')
        class TITLE_51:
            r'''
            ```python
            def recognizes(self, information_type: InformationType[Any]) -> bool
            ```
            
            その{{TERM_12}}を identity によって認識するかを返す。
            '''

            vocabulary_refs @= (
                terms.TERM_12,
            )

        @title('`view()`')
        class TITLE_52:
            r'''
            ```python
            def view(
                self,
                subject: object | Focus,
                *,
                placement: tuple[str, ...] | None = None,
            ) -> SemanticView
            ```
            
            対象を{{TERM_20}}として{{TERM_18}}し、{{TERM_19}}を返す。`placement` を指定すると、その位置を{{TERM_20}}の{{TERM_7}}上の配置として使用する。`Focus` 自体に配置が含まれる場合、method 引数として重ねて指定してはならない。
            
            {{TERM_19}}に取り込む{{TERM_13}}は、その {{TERM_1}} が `information_types` として認識するものだけである。対象へ接続されている未認識の{{TERM_13}}は削除されず、単にその{{TERM_19}}には現れない。{{TERM_16}}は{{TERM_12}}とは独立して{{TERM_19}}へ取り込まれ、`descriptor_rules` が必要な使用だけを{{TERM_7}}との関係で{{TERM_21}}する。
            '''

            vocabulary_refs @= (
                terms.TERM_20,
                terms.TERM_18,
                terms.TERM_19,
                terms.TERM_7,
                terms.TERM_13,
                terms.TERM_1,
                terms.TERM_16,
                terms.TERM_12,
                terms.TERM_21,
            )

        @title('`derive_structure_specification()`')
        class TITLE_53:
            r'''
            ```python
            def derive_structure_specification(
                self,
                subject: object | Focus,
                *,
                placement: tuple[str, ...] | None = None,
            ) -> StructureSpecification
            ```
            
            {{TERM_5}}をこの {{TERM_1}} の `Structure` で{{TERM_18}}し、その{{TERM_20}}をルートとする{{TERM_8}}を導出する。これは明示的な{{TERM_8}}を探索する method ではなく、呼び出し側が「{{TERM_5}}から導出する」ことを選択した場合に使用する。
            '''

            vocabulary_refs @= (
                terms.TERM_5,
                terms.TERM_1,
                terms.TERM_18,
                terms.TERM_20,
                terms.TERM_8,
            )

        @title('`validate()`')
        class TITLE_54:
            r'''
            ```python
            def validate(
                self,
                subject: object | Focus,
                *,
                placement: tuple[str, ...] | None = None,
                structure_specification: StructureSpecification | None = None,
            ) -> ValidationResult
            ```
            
            対象を{{TERM_20}}として{{TERM_19}}を構成し、適用可能な{{TERM_22}}と `descriptor_rules` を評価する。`structure_specification` が指定された場合は、同じ{{TERM_21}}操作の中で{{TERM_8}}への適合も確認する。
            
            単独の module を `validate()` する場合は `placement` が必須である。現在の import path を予定配置として暗黙採用しない。package 全体の{{TERM_21}}中に下位 module へ{{TERM_22}}を適用する場合は、解決済み{{TERM_7}}の位置を配置として自動的に引き継ぐ。
            
            ルートとなる{{TERM_20}}だけでなく、その{{TERM_19}}に含まれる各{{TERM_7}}要素について、その `StructuralKind` を要求する{{TERM_22}}を適用する。下位要素に規則を適用するときは、最初に構成した{{TERM_19}}から `SemanticView.subview()` で部分{{TERM_19}}を切り出して渡す。一回の `validate()` の途中で `Structure.resolve()` や{{TERM_13}}・{{TERM_16}}の取得を繰り返さず、一回{{TERM_18}}した runtime 状態を{{TERM_21}}操作全体で共有する。
            
            {{TERM_8}}の照合では、{{TERM_20}}に配置が指定されている場合、その位置以下の部分{{TERM_7}}だけを厳密に照合する。これにより、module 単体の{{TERM_21}}では外側の兄弟 module 等を観測したかのようには扱わない。
            
            ---
            '''

            vocabulary_refs @= (
                terms.TERM_20,
                terms.TERM_19,
                terms.TERM_22,
                terms.TERM_21,
                terms.TERM_8,
                terms.TERM_7,
                terms.TERM_13,
                terms.TERM_16,
                terms.TERM_18,
            )

    @title('{{TERM_21}}')
    class TITLE_55:
        r'''
        '''

        vocabulary_refs @= (
            terms.TERM_21,
        )

        @title('`DiagnosticSeverity`')
        class TITLE_56:
            r'''
            ```python
            class DiagnosticSeverity(str, Enum):
                ERROR = "error"
                WARNING = "warning"
                INFO = "info"
            ```
            
            {{TERM_23}}の重大度。
            '''

            vocabulary_refs @= (
                terms.TERM_23,
            )

        @title('`Diagnostic`')
        class TITLE_57:
            r'''
            ```python
            Diagnostic(
                message: str,
                code: str | None = None,
                severity: DiagnosticSeverity = DiagnosticSeverity.ERROR,
                subject: object | None = None,
            )
            ```
            
            一件の{{TERM_23}}。`message` と `code`、`severity` は生成時に型を検証し、`severity` は `DiagnosticSeverity` そのものを要求する。文字列 `"error"` 等を暗黙変換しない。
            
            {{TERM_22}}が `subject=None` の{{TERM_23}}を返した場合、その規則へ渡された{{TERM_19}}の{{TERM_20}}が自動的に `subject` として設定される。
            '''

            vocabulary_refs @= (
                terms.TERM_23,
                terms.TERM_22,
                terms.TERM_19,
                terms.TERM_20,
            )

        @title('`ValidationRule`')
        class TITLE_58:
            r'''
            ```python
            ValidationRule(
                focus_kind: StructuralKind,
                check: Callable[[SemanticView], ValidationOutput],
                name: str,
            )
            ```
            
            一つの{{TERM_22}}。
            
            `ValidationRule` は identity によって区別する。生成時に `focus_kind` が `StructuralKind`、`check` が callable、`name` が空でない `str` であることを検証する。
            
            呼び出し時には `focus_kind` と一致する{{TERM_20}}の{{TERM_19}}を要求し、{{TERM_23}}の tuple を返す。
            '''

            vocabulary_refs @= (
                terms.TERM_22,
                terms.TERM_20,
                terms.TERM_19,
                terms.TERM_23,
            )

        @title('`validator()`')
        class TITLE_59:
            r'''
            ```python
            def validator(
                *,
                focus: StructuralKind,
                name: str | None = None,
            ) -> Callable[[ValidationFunction], ValidationRule]
            ```
            
            通常の Python 関数から `ValidationRule` を定義するための補助デコレータ。
            
            {{TERM_21}}関数は `SemanticView` を受け取り、次のいずれかを返せる。
            
            ```python
            None
            Diagnostic
            Iterable[Diagnostic]
            ```
            
            例:
            
            ```python
            @validator(focus=StructuralKind.ENTITY)
            def require_title(view):
                if not view.focused.has(Title):
                    yield Diagnostic(
                        "title is required",
                        code="title.required",
                    )
            ```
            '''

            vocabulary_refs @= (
                terms.TERM_21,
            )

        @title('`check_descriptor_uses()`')
        class TITLE_60:
            r'''
            ```python
            def check_descriptor_uses(
                view: SemanticView,
                rules: Iterable[DescriptorUseRule],
            ) -> tuple[Diagnostic, ...]
            ```
            
            {{TERM_19}}に記録された{{TERM_16}}を、{{TERM_17}}と照合して{{TERM_23}}を返す。`{{TERM_1}}.validate()` は登録された `descriptor_rules` に対してこの検査を自動的に行う。
            '''

            vocabulary_refs @= (
                terms.TERM_19,
                terms.TERM_16,
                terms.TERM_17,
                terms.TERM_23,
                terms.TERM_1,
            )

        @title('`StructureCheck` / `check_structure()`')
        class TITLE_61:
            r'''
            ```python
            @dataclass(frozen=True)
            class StructureCheck:
                specification: StructureSpecification
                placement: tuple[str, ...]
                diagnostics: tuple[Diagnostic, ...]
            
            
            def check_structure(
                structure: ResolvedStructure,
                specification: StructureSpecification,
            ) -> StructureCheck
            ```
            
            解決済み{{TERM_7}}を{{TERM_8}}と照合した結果を表す。{{TERM_20}}の `placement` が指定されている場合はその部分{{TERM_7}}を、指定されていない場合は{{TERM_8}}のルートを照合する。
            
            `StructureCheck.is_valid` は error 診断がない場合に `True`。
            '''

            vocabulary_refs @= (
                terms.TERM_7,
                terms.TERM_8,
                terms.TERM_20,
            )

        @title('`ValidationResult`')
        class TITLE_62:
            r'''
            ```python
            @dataclass(frozen=True)
            class ValidationResult:
                view: SemanticView
                diagnostics: tuple[Diagnostic, ...]
                structure_check: StructureCheck | None = None
            ```
            
            一回の{{TERM_21}}結果。{{TERM_8}}を指定した場合、その照合結果を `structure_check` に保持し、{{TERM_7}}上の{{TERM_23}}も `diagnostics` に含める。
            '''

            vocabulary_refs @= (
                terms.TERM_21,
                terms.TERM_8,
                terms.TERM_7,
                terms.TERM_23,
            )

            @title('`is_valid`')
            class TITLE_63:
                r'''
                ```python
                @property
                def is_valid(self) -> bool
                ```
                
                `ERROR` の{{TERM_23}}が一件もない場合に `True`。
                
                `bool(result)` は `result.is_valid` と同じ意味を持つ。
                
                ---
                '''

                vocabulary_refs @= (
                    terms.TERM_23,
                )

    @title('{{TERM_25}}')
    class TITLE_64:
        r'''
        '''

        vocabulary_refs @= (
            terms.TERM_25,
        )

        @title('`RealizationCheck`')
        class TITLE_65:
            r'''
            ```python
            @dataclass(frozen=True)
            class RealizationCheck:
                view: SemanticView
                diagnostics: tuple[Diagnostic, ...] = ()
            ```
            
            {{TERM_28}}を生成せずに、特定の{{TERM_26}}が{{TERM_19}}を{{TERM_25}}可能か問い合わせた結果。`is_realizable` は error 診断がない場合に `True`。{{TERM_2}}への適合性とは独立している。
            '''

            vocabulary_refs @= (
                terms.TERM_28,
                terms.TERM_26,
                terms.TERM_19,
                terms.TERM_25,
                terms.TERM_2,
            )

        @title('`Realizer`')
        class TITLE_66:
            r'''
            ```python
            class Realizer(ABC, Generic[ArtifactT]):
                def check(self, view: SemanticView) -> RealizationCheck:
                    ...
            
                @abstractmethod
                def realize(self, view: SemanticView) -> ArtifactT:
                    ...
            ```
            
            {{TERM_19}}から{{TERM_28}}を生成するための抽象基底。`check()` は{{TERM_28}}を生成せず、与えられた{{TERM_19}}を{{TERM_25}}可能か問い合わせる。{{TERM_25}}条件を持つ{{TERM_26}}は `check()` を override し、満たされない条件を `Diagnostic` として返す。既定実装は追加の{{TERM_25}}条件なしとして扱う。
            
            {{TERM_26}}は {{TERM_1}} を所有せず、{{TERM_1}} からも所有されない。同じ{{TERM_19}}に複数の{{TERM_26}}を適用できる。
            
            ```python
            view = docs.view(source)
            
            markdown = MarkdownRealizer().realize(view)
            json_data = JsonRealizer().realize(view)
            ```
            
            {{TERM_28}}の型は {{TERM_1}} によって制限しない。
            
            ---
            '''

            vocabulary_refs @= (
                terms.TERM_19,
                terms.TERM_28,
                terms.TERM_25,
                terms.TERM_26,
                terms.TERM_1,
            )

    @title('例外')
    class TITLE_67:
        r'''
        '''

        @title('`{{TERM_1}}Error`')
        class TITLE_68:
            r'''
            {{TERM_1}} が定義する例外の基底。
            '''

            vocabulary_refs @= (
                terms.TERM_1,
            )

        @title('`UnsupportedFocusError`')
        class TITLE_69:
            r'''
            ```python
            class UnsupportedFocusError({{TERM_1}}Error, TypeError):
                ...
            ```
            
            {{TERM_7}}が与えられた{{TERM_20}}を{{TERM_18}}できない場合に送出する。
            '''

            vocabulary_refs @= (
                terms.TERM_1,
                terms.TERM_7,
                terms.TERM_20,
                terms.TERM_18,
            )

        @title('`UnknownViewSubjectError`')
        class TITLE_70:
            r'''
            ```python
            class UnknownViewSubjectError({{TERM_1}}Error, LookupError):
                ...
            ```
            
            {{TERM_19}}に存在しない対象を `SemanticView.item()` で取得しようとした場合に送出する。
            
            ---
            '''

            vocabulary_refs @= (
                terms.TERM_1,
                terms.TERM_19,
            )


@title('{{TERM_15}}を定義する')
class TITLE_71:
    r'''
    {{TERM_1}} は具体的な{{TERM_15}}の形を規定しない。{{TERM_3}}の著者は通常の Python を使って{{TERM_15}}を定義し、その中から{{TERM_14}}を行う。
    '''

    vocabulary_refs @= (
        terms.TERM_15,
        terms.TERM_1,
        terms.TERM_3,
        terms.TERM_14,
    )

    @title('引数を取らないデコレータ')
    class TITLE_72:
        r'''
        ```python
        Kind = InformationType(
            "kind",
            str,
            cardinality=Cardinality.MANY,
        )
        
        
        class KindDescriptions:
            def attr(self, subject):
                """属性として扱われる{{TERM_11}}。"""
                record_descriptor_use(subject, self.attr)
                attach_information(
                    subject,
                    Kind,
                    "attr",
                )
                return subject
        
            def service(self, subject):
                """サービスとして扱われる{{TERM_11}}。"""
                record_descriptor_use(subject, self.service)
                attach_information(
                    subject,
                    Kind,
                    "service",
                )
                return subject
        
        
        kind = KindDescriptions()
        ```
        
        {{TERM_5}}では通常の Python デコレータとして使用する。
        
        ```python
        @kind.attr
        class Owner:
            pass
        
        
        @kind.service
        class UserService:
            pass
        ```
        
        `attr` や `service` は通常の Python method として存在するため、IDE の定義ジャンプ、docstring 表示、型注釈などを通常どおり利用できる。
        '''

        vocabulary_refs @= (
            terms.TERM_11,
            terms.TERM_5,
        )

    @title('引数を取るデコレータ')
    class TITLE_73:
        r'''
        ```python
        Uses = InformationType(
            "uses",
            type,
            cardinality=Cardinality.MANY,
        )
        
        
        class RelationDescriptions:
            def uses(self, target: type):
                """対象の{{TERM_11}}を利用する関係。"""
        
                def decorate(subject):
                    record_descriptor_use(subject, self.uses)
                    attach_information(
                        subject,
                        Uses,
                        target,
                    )
                    return subject
        
                return decorate
        
        
        relation = RelationDescriptions()
        ```
        
        ```python
        @relation.uses(UserRepository)
        class UserService:
            pass
        ```
        
        引数、戻り値、デコレータの生成方法は{{TERM_15}}の著者の責務である。{{TERM_1}} はそれらをラップしたり、signature から{{TERM_13}}を推測したりしない。
        '''

        vocabulary_refs @= (
            terms.TERM_11,
            terms.TERM_15,
            terms.TERM_1,
            terms.TERM_13,
        )

    @title('独自の `@=` {{TERM_15}}')
    class TITLE_74:
        r'''
        `@=` の評価時点では、{{TERM_4}}先となる class はまだ成立していない。このため `class_binding()` を用いて、class 成立後に{{TERM_14}}を行う。
        
        ```python
        Tag = InformationType(
            "tag",
            str,
            cardinality=Cardinality.MANY,
        )
        
        
        class TagDescriptions:
            def __imatmul__(self, value: str):
                return class_binding(value, self._connect)
        
            def _connect(self, subject: type, value: str) -> None:
                record_descriptor_use(subject, self)
                attach_information(
                    subject,
                    Tag,
                    value,
                )
        
        
        tag = TagDescriptions()
        ```
        
        ```python
        class UserService:
            tag @= "application"
            tag @= "users"
        ```
        
        {{TERM_1}} は `value` の型や構造を解釈しない。`@=` にどのような型を受け付け、その値をどの{{TERM_12}}として接続するかは{{TERM_15}}の著者が決める。
        '''

        vocabulary_refs @= (
            terms.TERM_15,
            terms.TERM_4,
            terms.TERM_14,
            terms.TERM_1,
            terms.TERM_12,
        )

        @title('{{TERM_17}}の例')
        class TITLE_75:
            r'''
            ```python
            endpoint_rule = DescriptorUseRule(
                descriptor=kind.service,
                allowed=StructureSelector(kind=StructuralKind.ENTITY),
                recommended=StructureSelector(
                    kind=StructuralKind.ENTITY,
                    under=("api",),
                ),
                name="kind.service",
            )
            
            system = {{TERM_1}}(
                information_types=[Kind],
                descriptor_rules=[endpoint_rule],
            )
            ```
            
            この規則は `kind.service` を entity でのみ許可し、{{TERM_2}}ルートの `api` 以下での使用を推奨する。`api` 外の entity での使用は warning、entity 以外での使用は error になる。
            
            ---
            '''

            vocabulary_refs @= (
                terms.TERM_17,
                terms.TERM_1,
                terms.TERM_2,
            )


@title('Standard API: `{{PROJECT.import_package}}.standard`')
class TITLE_76:
    r'''
    Standard は Core の公開 API を組み合わせた再利用可能な具体機能を提供する。Standard は新しい意味モデルを導入しない。
    '''

    vocabulary_refs @= (
    )

    @title('`assignment()`')
    class TITLE_77:
        r'''
        ```python
        def assignment(information_type: InformationType)
        ```
        
        与えられた値をそのまま指定{{TERM_12}}として{{TERM_14}}する、標準的な `@=` {{TERM_15}}を返す。使用時には{{TERM_16}}も記録する。
        
        ```python
        Title = InformationType("title", str)
        title = assignment(Title)
        
        class Page:
            title @= "Overview"
        ```
        
        同じ名前に対する連続した `@=` を許可する。
        '''

        vocabulary_refs @= (
            terms.TERM_12,
            terms.TERM_14,
            terms.TERM_15,
            terms.TERM_16,
        )

    @title('`decorator()`')
    class TITLE_78:
        r'''
        ```python
        def decorator(information_type: InformationType)
        ```
        
        与えられた値をそのまま指定{{TERM_12}}として{{TERM_14}}する、単純なデコレータ生成{{TERM_15}}を返す。適用時には{{TERM_16}}も記録する。
        
        ```python
        Kind = InformationType("kind", str)
        kind = decorator(Kind)
        
        @kind("service")
        class Service:
            pass
        ```
        
        語彙名そのものを IDE から追跡可能にしたい場合や、引数に独自の意味を持たせたい場合は、この便利機能ではなく通常の Python デコレータを{{TERM_3}}で定義する。
        '''

        vocabulary_refs @= (
            terms.TERM_12,
            terms.TERM_14,
            terms.TERM_15,
            terms.TERM_16,
            terms.TERM_3,
        )

    @title('`DocstringWriter` / `docstring()`')
    class TITLE_79:
        r'''
        ```python
        DocstringWriter(
            information_type: InformationType,
            *,
            clean: bool = True,
            required: bool = False,
        )
        ```
        
        ```python
        def docstring(
            information_type: InformationType,
            *,
            clean: bool = True,
            required: bool = False,
        ) -> DocstringWriter
        ```
        
        明示的に適用された対象の `__doc__` を{{TERM_13}}として接続する標準{{TERM_15}}。適用時には{{TERM_16}}を記録し、docstring が存在しない場合でも「{{TERM_15}}が使用された」という事実は残る。
        
        ```python
        Content = content_type()
        content = docstring(Content)
        
        @content
        class Overview:
            """Overview document."""
        ```
        
        `clean=True` の場合は Python の docstring 整形規則に従って余分なインデントを除去する。
        
        `required=False` で docstring が存在しない場合は何も接続しない。{{TERM_13}}の必須性は通常、{{TERM_22}}で表現することを推奨する。
        '''

        vocabulary_refs @= (
            terms.TERM_13,
            terms.TERM_15,
            terms.TERM_16,
            terms.TERM_22,
        )

    @title('`content_type()`')
    class TITLE_80:
        r'''
        ```python
        def content_type(
            name: str = "content",
            *,
            value_type: type | tuple[type, ...] = str,
        ) -> InformationType
        ```
        
        主要内容を表す単一値の{{TERM_12}}を生成する便利関数。
        '''

        vocabulary_refs @= (
            terms.TERM_12,
        )

    @title('`PackageTreeStructure`')
    class TITLE_81:
        r'''
        ```python
        PackageTreeStructure()
        ```
        
        import 済み package を{{TERM_20}}としたとき、その物理 package tree を探索し、子 package / module を Python の通常の import 機構で読み込んで{{TERM_10}}を構成する。
        
        module または{{TERM_11}}を{{TERM_20}}とした場合は `PythonStructure` と同等の局所{{TERM_18}}を行う。各 module では、module 直下の class に加えて字句上の入れ子 class も{{TERM_11}}として{{TERM_10}}へ含める。
        
        この{{TERM_7}}は Python import の実行結果を意味状態の正とする。source を AST として解析しない。
        '''

        vocabulary_refs @= (
            terms.TERM_20,
            terms.TERM_10,
            terms.TERM_11,
            terms.TERM_18,
            terms.TERM_7,
        )

    @title('`information_type_rule()`')
    class TITLE_82:
        r'''
        ```python
        def information_type_rule(
            information_type: InformationType,
            *,
            focus: StructuralKind = StructuralKind.ENTITY,
        ) -> ValidationRule
        ```
        
        一つの{{TERM_12}}について、次を{{TERM_21}}する標準{{TERM_22}}を生成する。
        
        - `Cardinality.ONE` に対する複数値
        - `value_type` に適合しない値
        
        {{TERM_13}}の存在必須性や、値に{{TERM_2}}固有の意味を与える{{TERM_21}}は行わない。
        
        ---
        '''

        vocabulary_refs @= (
            terms.TERM_12,
            terms.TERM_21,
            terms.TERM_22,
            terms.TERM_13,
            terms.TERM_2,
        )


@title('公開 API の層分け')
class TITLE_83:
    r'''
    Core と Standard の境界は次のように扱う。
    
    ```text
    Core (`{{PROJECT.import_package}}`)
    ├─ {{TERM_12}}・{{TERM_13}}
    ├─ {{TERM_14}}
    ├─ class 成立後への低水準接続
    ├─ {{TERM_7}}・{{TERM_20}}・{{TERM_19}}
    ├─ {{TERM_1}}
    ├─ {{TERM_21}}
    └─ {{TERM_25}}
    
    Standard (`{{PROJECT.import_package}}.standard`)
    ├─ 汎用 `@=` {{TERM_15}}
    ├─ 汎用デコレータ{{TERM_15}}
    ├─ docstring {{TERM_15}}
    ├─ 標準{{TERM_12}}生成補助
    ├─ package tree {{TERM_7}}
    └─ 標準{{TERM_22}}
    ```
    
    `kind`、`attr`、`rel` など特定用途の語彙は Standard の責務としない。{{TERM_3}}が必要な語彙を通常の Python 定義として{{TERM_4}}する。
    
    ---
    '''

    vocabulary_refs @= (
        terms.TERM_12,
        terms.TERM_13,
        terms.TERM_14,
        terms.TERM_7,
        terms.TERM_20,
        terms.TERM_19,
        terms.TERM_1,
        terms.TERM_21,
        terms.TERM_25,
        terms.TERM_15,
        terms.TERM_22,
        terms.TERM_3,
        terms.TERM_4,
    )


@title('動作保証の境界')
class TITLE_84:
    r'''
    {{TERM_1}} は通常の Python class 作成と import / execution の振る舞いを前提とする。
    
    利用者または{{TERM_3}}が独自のデコレータ、metaclass、base class、mixin などを使用した場合、それらとの相互作用に対して {{TERM_1}} は互換処理を提供しない。組み合わせによって Python 標準の class 作成過程や{{TERM_15}}の実行順序が変化する場合、その動作は保証しない。
    
    {{TERM_1}} は次を行わない。
    
    - Python source の AST 解析による意味復元
    - {{TERM_15}}関数の signature や戻り値からの自動的な{{TERM_13}}推論
    - 特定語彙の自動登録
    - 未認識{{TERM_13}}の自動削除
    - {{TERM_21}}前の不正状態の自動補正
    - {{TERM_26}}の {{TERM_1}} への登録や所有
    
    この境界により、{{TERM_3}}の著者は通常の Python を使って{{TERM_4}}方法を自由に定義し、{{TERM_1}} は{{TERM_14}}以降の意味{{TERM_18}}に集中する。
    
    ---
    '''

    vocabulary_refs @= (
        terms.TERM_1,
        terms.TERM_3,
        terms.TERM_15,
        terms.TERM_13,
        terms.TERM_21,
        terms.TERM_26,
        terms.TERM_4,
        terms.TERM_14,
        terms.TERM_18,
    )


@title('CLI: `{{PROJECT.cli_entry_point}}`')
class TITLE_85:
    r'''
    {{TERM_1}} は、{{TERM_3}}が公開する `{{TERM_1}}`、{{TERM_5}}となる Python object、独立した{{TERM_26}}を実行時に結線する薄い CLI を提供する。
    
    CLI は{{TERM_3}}、{{TERM_5}}、{{TERM_26}}の登録・探索・所有関係を管理しない。指定された Python 参照を通常の import によって読み込み、その場で処理する。
    
    Python 参照は次の形式を用いる。
    
    ```text
    module
    module:object
    module:outer.inner
    ```
    
    `--shikumi` と `--realizer` は `module:object` を要求する。`--body` は module/package 自体を指定する場合は `module`、{{TERM_11}}を{{TERM_20}}にする場合は `module:object` を使用できる。
    '''

    vocabulary_refs @= (
        terms.TERM_1,
        terms.TERM_3,
        terms.TERM_5,
        terms.TERM_26,
        terms.TERM_11,
        terms.TERM_20,
    )

    @title('`validate`')
    class TITLE_86:
        r'''
        ```bash
        {{PROJECT.cli_entry_point}} validate \
          --shikumi SPEC_MODULE:SHIKUMI \
          --body DESCRIPTION_MODULE[:OBJECT] \
          [--at PLACEMENT] \
          [--structure-spec SPEC_MODULE:STRUCTURE | --structure-from DESCRIPTION_MODULE[:OBJECT]] \
          [--realizer REALIZER_MODULE:REALIZER] \
          [--format text|json]
        ```
        
        指定した{{TERM_5}}または{{TERM_11}}を `{{TERM_1}}.validate()` で{{TERM_21}}する。
        
        単独の module を `--body` に指定する場合、`--at` は必須である。値は `api.users` のような{{TERM_7}}上の予定配置を dotted path で表し、`.` は{{TERM_8}}のルートを表す。package 全体を指定した場合は配置を省略できる。
        
        {{TERM_8}}を利用する場合は、次のどちらか一方を利用者が明示的に選ぶ。
        
        - `--structure-spec MODULE:OBJECT`: {{TERM_3}}などが Python object として公開した `StructureSpecification` をそのまま使用する。指定 object が存在しない、または型が異なる場合は CLI 設定エラーとし、{{TERM_5}}からの導出へフォールバックしない。
        - `--structure-from MODULE[:OBJECT]`: 指定した{{TERM_5}}を現在の {{TERM_1}} で{{TERM_18}}し、その{{TERM_7}}から `StructureSpecification` を導出する。
        
        `--realizer` を指定すると、通常の{{TERM_21}}に加えて `Realizer.check()` を呼び、{{TERM_28}}を生成せずに{{TERM_27}}を問い合わせる。{{TERM_2}}への適合と{{TERM_27}}は別結果として JSON 応答に保持する。どちらかに error があれば command 全体の `ok` は `false` となる。
        
        {{TERM_21}}と、指定されている場合の{{TERM_27}}検査の双方に error がなければ exit code `0`、一件以上あれば `1` を返す。warning / info のみの場合は `0` とする。
        
        `validate` は{{TERM_28}}を生成しない。
        '''

        vocabulary_refs @= (
            terms.TERM_5,
            terms.TERM_11,
            terms.TERM_1,
            terms.TERM_21,
            terms.TERM_7,
            terms.TERM_8,
            terms.TERM_3,
            terms.TERM_18,
            terms.TERM_28,
            terms.TERM_27,
            terms.TERM_2,
        )

    @title('`realize`')
    class TITLE_87:
        r'''
        ```bash
        {{PROJECT.cli_entry_point}} realize \
          --shikumi SPEC_MODULE:SHIKUMI \
          --body DESCRIPTION_MODULE[:OBJECT] \
          [--at PLACEMENT] \
          --realizer REALIZER_MODULE:REALIZER \
          --output PATH \
          [--format text|json]
        ```
        
        指定した{{TERM_5}}から{{TERM_19}}を構成し、指定した `Realizer` へ渡して{{TERM_28}}を生成する。`--at` を指定した場合、その{{TERM_7}}上の配置を{{TERM_19}}へ反映する。
        
        `realize` は暗黙に validation も `Realizer.check()` も実行しない。{{TERM_2}}への適合、{{TERM_27}}の問い合わせ、実際の{{TERM_25}}は独立した操作として扱う。必要であれば先に `validate --realizer ...` を実行する。
        
        CLI からファイルへ書き出せる{{TERM_28}}は次のいずれかとする。
        
        - `str`: UTF-8 text として書き出す
        - `bytes` / bytes-like: binary として書き出す
        - JSON serialization 可能な Python 値: UTF-8 JSON として書き出す
        
        それ以外の{{TERM_28}}を返す{{TERM_26}}は、CLI の標準出力契約では直接利用できない。
        '''

        vocabulary_refs @= (
            terms.TERM_5,
            terms.TERM_19,
            terms.TERM_28,
            terms.TERM_7,
            terms.TERM_2,
            terms.TERM_27,
            terms.TERM_25,
            terms.TERM_26,
        )

    @title('`--format`')
    class TITLE_88:
        r'''
        ```text
        text
        json
        ```
        
        既定値は `text`。
        
        `--format` は **CLI 自身の応答形式**を決める。{{TERM_26}}が生成する{{TERM_28}}の形式を決めるものではない。
        
        `text` は端末で読むために整形されたテキストを出力する。
        
        `json` は LLM、CI、その他のツールから扱うための構造化応答を stdout に出力する。JSON 応答には `format_version` を含める。現在の version は `1`。
        
        例:
        
        ```json
        {
          "format_version": 1,
          "command": "validate",
          "ok": false,
          "shikumi": "api_spec:api",
          "body": "my_api",
          "focus_kind": "package",
          "placement": null,
          "diagnostic_counts": {
            "error": 1,
            "warning": 0,
            "info": 0
          },
          "diagnostics": [
            {
              "severity": "error",
              "code": "endpoint.path.required",
              "message": "endpoint path is required",
              "subject": "my_api.users.GetUser"
            }
          ],
          "structure": null,
          "realization": null
        }
        ```
        
        {{TERM_25}}時に `--output` を指定した場合、{{TERM_28}}はそのファイルへ書き出し、stdout には CLI 応答だけを出力する。この分離により、{{TERM_28}}自体が JSON であっても `--format json` の CLI 応答と混在しない。
        
        CLI が処理できる import、{{TERM_18}}、{{TERM_21}}、{{TERM_25}}、{{TERM_28}}書き出しの失敗は、`json` 形式では `ok: false` と `error.type` / `error.message` を持つ構造化応答として報告する。
        '''

        vocabulary_refs @= (
            terms.TERM_26,
            terms.TERM_28,
            terms.TERM_25,
            terms.TERM_18,
            terms.TERM_21,
        )
