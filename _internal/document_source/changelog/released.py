"""Released Shikumi changelog entries kept as a physical changelog part."""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.changelog import ADDED, change, changelog_part, release, released_on, vocabulary_refs


@changelog_part(order=10)
class CHANGELOG_PART:
    @release("0.1.0")
    class RELEASE_1:
        """初回公開リリースです。"""

        released_on @= "2026-09-12"

        @change(ADDED)
        class CHANGE_1:
            """{{TERM_13}}、{{TERM_16}}、{{TERM_7}}、{{TERM_19}}を分離したCoreの意味モデルを追加しました。"""

            vocabulary_refs @= (
                terms.TERM_13,
                terms.TERM_16,
                terms.TERM_7,
                terms.TERM_19,
            )

        @change(ADDED)
        class CHANGE_2:
            """実体・module・packageを同じ仕組みで扱う{{TERM_21}}と、独立した{{TERM_26}}による{{TERM_25}}を追加しました。"""

            vocabulary_refs @= (
                terms.TERM_21,
                terms.TERM_26,
                terms.TERM_25,
            )

        @change(ADDED)
        class CHANGE_3:
            """デコレータ、`@=`、docstring、package treeなど、再利用可能なStandardの{{TERM_15}}と{{TERM_7}}実装を追加しました。"""

            vocabulary_refs @= (
                terms.TERM_15,
                terms.TERM_7,
            )

        @change(ADDED)
        class CHANGE_4:
            """{{TERM_3}}、{{TERM_5}}、{{TERM_26}}を通常のPython参照として結線するCLIを追加しました。"""

            vocabulary_refs @= (
                terms.TERM_3,
                terms.TERM_5,
                terms.TERM_26,
            )

        @change(ADDED)
        class CHANGE_5:
            """README、Glossary、API Reference、Distribution Guideからなる英語の公開文書体系を追加しました。公開文書は日本語のcanonical document sourceを正本として生成・翻訳します。"""

        @change(ADDED)
        class CHANGE_6:
            """architecture、structured docs、Web API、`structure-from`の4方向を示す公式作例を追加しました。"""
