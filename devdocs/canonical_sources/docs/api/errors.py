"""Canonical Japanese API reference source for Error API."""

from devdocs.canonical_sources.docs.vocabulary import TERMS
from shikumi_devdoc.fields.api_reference import (
    NAMESPACE, OPERATION, OTHER, TYPE, VALUE,
    input, kind, name, output, related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.docs.specification.public_api import SPECIFICATION_PART as PUBLIC_API_SPEC

@summary('公開例外型。')
@canonical_source('Error API', filename='errors.md', order=80, heading="title")
class API_REFERENCE_PART:
    """公開 API が明示的に利用者へ伝える例外型。"""

    related @= PUBLIC_API_SPEC

    class TITLE_67:
        r'''
        '''
        title @= '例外'

        class TITLE_68:
            r'''
            {{TERM_1}} が定義する例外の基底。
            '''
            title @= '`ShikumiError`'
            name @= 'ShikumiError'
            kind @= TYPE


            merge @= TERMS.TERM_1

        class TITLE_69:
            r'''
            ```python
            class UnsupportedFocusError({{TERM_1}}Error, TypeError):
                ...
            ```

            {{TERM_7}}が与えられた{{TERM_20}}を{{TERM_18}}できない場合に送出する。
            '''
            title @= '`UnsupportedFocusError`'
            name @= 'UnsupportedFocusError'
            kind @= TYPE


            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_7
            merge @= TERMS.TERM_20
            merge @= TERMS.TERM_18

        class TITLE_70:
            r'''
            ```python
            class UnknownViewSubjectError({{TERM_1}}Error, LookupError):
                ...
            ```

            {{TERM_19}}に存在しない対象を `SemanticView.item()` で取得しようとした場合に送出する。

            ---
            '''
            title @= '`UnknownViewSubjectError`'
            name @= 'UnknownViewSubjectError'
            kind @= TYPE


            merge @= TERMS.TERM_1
            merge @= TERMS.TERM_19

