"""Structured-documents example README canonical source."""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("構造化文書の実現")
class TITLE_1:
    '''
    この例は、Python上の{{TERM_4}}から{{TERM_19}}を構成し、独立した{{TERM_26}}でMarkdownへ{{TERM_25}}する例です。

    command名、category、docstringの本文をそれぞれ{{TERM_12}}として扱います。
    {{TERM_21}}は記述が規定を満たしているかを確認し、Markdown{{TERM_26}}は同じ{{TERM_19}}から公開用の一覧を生成します。
    '''

    vocabulary_refs @= (
        terms.TERM_4,
        terms.TERM_19,
        terms.TERM_26,
        terms.TERM_25,
        terms.TERM_12,
        terms.TERM_21,
    )

    @title("試す")
    class TITLE_2:
        '''
        repository checkoutでは`examples/`をPython pathに置き、通常のPythonコードとして{{TERM_21}}と{{TERM_25}}を試せます。

        ```python
        from structured_docs import body
        from structured_docs.shikumi_lib.norms import structured_docs
        from structured_docs.shikumi_lib.realizers.markdown import markdown

        result = structured_docs.validate(body)
        assert result.is_valid
        output = markdown.realize(result.view)
        ```

        `output`には`deploy`と`status`の説明を含むMarkdownが入ります。
        '''

        vocabulary_refs @= (
            terms.TERM_21,
            terms.TERM_25,
        )

    @title("見るべき点")
    class TITLE_3:
        '''
        - `@command(...)`、`category @= ...`、docstringという異なる記法が、それぞれ{{TERM_13}}として同じ{{TERM_19}}へ現れます。
        - {{TERM_26}}は{{TERM_1}}に登録されず、{{TERM_19}}を受け取る独立したコンポーネントです。
        - `check()`による{{TERM_27}}の判定と`realize()`による{{TERM_25}}は別の操作です。
        '''

        vocabulary_refs @= (
            terms.TERM_13,
            terms.TERM_19,
            terms.TERM_26,
            terms.TERM_1,
            terms.TERM_27,
            terms.TERM_25,
        )
