"""Web API example README canonical source."""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("Web API DSL")
class TITLE_1:
    '''
    この例は、独自の{{TERM_12}}と{{TERM_15}}を組み合わせて小さなWeb API DSLを作り、{{TERM_21}}とMarkdown{{TERM_25}}まで一周する総合例です。

    endpoint classにはmethod、path、tag、本文、関連endpointを{{TERM_13}}として記述します。
    {{TERM_22}}はentity、module、packageの複数の{{TERM_20}}で適用され、routeの形式や重複を確認します。
    '''

    vocabulary_refs @= (
        terms.TERM_12,
        terms.TERM_15,
        terms.TERM_21,
        terms.TERM_25,
        terms.TERM_13,
        terms.TERM_22,
        terms.TERM_20,
    )

    @title("試す")
    class TITLE_2:
        '''
        repository checkoutでは`examples/`をPython pathに置き、通常のPythonコードとして{{TERM_21}}とMarkdown{{TERM_25}}を試せます。

        ```python
        from web_api import api
        from web_api.shikumi_lib.norms import web_api, web_api_structure
        from web_api.shikumi_lib.realizers.markdown import markdown

        result = web_api.validate(api, structure_specification=web_api_structure)
        assert result.is_valid
        output = markdown.realize(result.view)
        ```

        作例自体は参考ソースとして配布され、公開import packageやCLI entry pointにはしません。
        '''

        vocabulary_refs @= (
            terms.TERM_21,
            terms.TERM_25,
        )

    @title("見るべき点")
    class TITLE_3:
        '''
        - `@=`、docstring、class参照を同じDSLの中で組み合わせています。
        - {{TERM_17}}により、各{{TERM_15}}をentityで使うことを明示しています。
        - package全体の{{TERM_19}}を{{TERM_26}}へ渡し、複数moduleの情報を一つの{{TERM_28}}へまとめています。
        '''

        vocabulary_refs @= (
            terms.TERM_17,
            terms.TERM_15,
            terms.TERM_19,
            terms.TERM_26,
            terms.TERM_28,
        )
