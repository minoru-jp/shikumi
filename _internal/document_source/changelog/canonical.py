"""Shikumi CHANGELOG の正本となる記述体。"""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.changelog import (
    CHANGED,
    breaking,
    canonical,
    change,
    changelog,
    release,
    unreleased,
    vocabulary,
    vocabulary_refs,
)


@canonical
@vocabulary(terms)
@changelog("Changelog")
class CHANGELOG:
    """{{TERM_1}}の公開リリースごとの主な変更を記録します。"""

    vocabulary_refs @= (terms.TERM_1,)

    @release()
    class RELEASE_1:
        """次の公開リリースへ向けた変更です。"""

        unreleased @= True

        @change(CHANGED)
        class CHANGE_1:
            """公式作例をトップレベルの`shikumi_examples` import packageから`examples/`の参考ソースへ移し、wheelでは`shikumi/_examples/`に同梱するよう変更しました。作例の`python -m`実行入口を削除し、利用者コードが依存する公開面から分離しました。"""

            breaking @= True
