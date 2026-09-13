"""Architecture example README canonical source."""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("アーキテクチャ検証")
class TITLE_1:
    '''
    この例は、{{TERM_1}}を使って用途固有のアーキテクチャ規則を定義し、Python上の{{TERM_4}}を{{TERM_21}}する最小例です。

    `domain`、`application`、`infrastructure`という層を{{TERM_12}}として定義し、class間の依存関係を別の{{TERM_12}}として記述します。
    {{TERM_1}}自身はこれらの層や依存規則を知りません。どの依存方向を許可するかは、この例の{{TERM_3}}が定めています。

    この例が{{TERM_21}}するのは`DependsOn`として明示された依存です。実際のPython importやcall graphを自動検出する例ではありません。
    '''

    vocabulary_refs @= (
        terms.TERM_1,
        terms.TERM_4,
        terms.TERM_21,
        terms.TERM_12,
        terms.TERM_3,
    )

    @title("試す")
    class TITLE_2:
        '''
        repository checkoutでは`examples/`をPython pathに置けば、通常のPythonコードとして試せます。

        ```python
        from architecture import body
        from architecture.shikumi_lib.norms import architecture

        result = architecture.validate(body)
        assert result.is_valid
        ```

        `domain`のclassから`application`のclassへ依存するように{{TERM_4}}を変更すると、{{TERM_22}}が依存方向の違反を報告します。
        '''

        vocabulary_refs @= (
            terms.TERM_4,
            terms.TERM_22,
        )

    @title("見るべき点")
    class TITLE_3:
        '''
        - `Layer`と`DependsOn`はこの例が定義した{{TERM_12}}です。
        - `@layer(...)`と`depends_on @= ...`は、この例の意味をPython上へ書くための{{TERM_15}}です。
        - 依存方向の判定はpackageを{{TERM_20}}とする{{TERM_22}}として実装されています。
        - classは{{TERM_1}}のbase classやmetaclassを必要としません。
        '''

        vocabulary_refs @= (
            terms.TERM_12,
            terms.TERM_15,
            terms.TERM_20,
            terms.TERM_22,
            terms.TERM_1,
        )
