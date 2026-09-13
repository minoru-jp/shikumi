"""Structure-from-body example README canonical source."""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("記述体から構造規定を導出する")
class TITLE_1:
    '''
    この例は、ある{{TERM_5}}を{{TERM_7}}として{{TERM_18}}した結果から{{TERM_8}}を導出し、別の{{TERM_5}}がその{{TERM_7}}に適合するかを{{TERM_21}}します。

    最初の{{TERM_5}}は、別の{{TERM_5}}に対して{{TERM_8}}を与える材料として使われます。
    これは特別なファイル形式ではなく、通常のPython packageです。
    '''

    vocabulary_refs @= (
        terms.TERM_5,
        terms.TERM_7,
        terms.TERM_18,
        terms.TERM_8,
        terms.TERM_21,
    )

    @title("試す")
    class TITLE_2:
        '''
        repository checkoutでは`examples/`をPython pathに置き、通常のPythonコードとして試せます。

        ```python
        from structure_from_body import candidate, reference
        from structure_from_body.shikumi_lib.norms import structure_only

        specification = structure_only.derive_structure_specification(reference)
        result = structure_only.validate(candidate, structure_specification=specification)
        assert result.is_valid
        ```

        `reference` packageから{{TERM_8}}を導出し、`candidate` packageをそれに対して{{TERM_21}}します。両者は同じmodule/class配置を持つため、{{TERM_21}}は成功します。
        '''

        vocabulary_refs @= (
            terms.TERM_8,
            terms.TERM_21,
        )

    @title("何を検証しないか")
    class TITLE_3:
        '''
        この仕組みが{{TERM_21}}するのは{{TERM_8}}への適合性です。二つの{{TERM_5}}の内容や意味が一致することは、{{TERM_1}}自身からは{{TERM_21}}されません。

        この例では意図的に、`reference.catalog.ITEM_1`と`candidate.catalog.ITEM_1`のdocstringを全く別の内容にしています。それでも{{TERM_7}}が一致しているため、構造{{TERM_21}}は成功します。

        典型的な応用として、原文の文書構造から{{TERM_8}}を導出し、翻訳版に同じ見出し構造が存在することを確認できます。しかし、翻訳内容の意味的一致まで必要なら、その条件は用途側の{{TERM_12}}や{{TERM_22}}として別途定義する必要があります。
        内容を意図的に異ならせた二つの{{TERM_5}}へ同じ{{TERM_8}}を適用することも問題ありません。
        '''

        vocabulary_refs @= (
            terms.TERM_21,
            terms.TERM_8,
            terms.TERM_5,
            terms.TERM_1,
            terms.TERM_7,
            terms.TERM_12,
            terms.TERM_22,
        )
