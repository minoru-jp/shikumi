"""Realization semantics specification."""

from shikumi_devdoc.fields.specification import MAY, MUST, level, related
from shikumi_devdoc.norms.common import canonical_source, summary
from shikumi_devdoc.norms.document import title

from devdocs.canonical_sources.docs.specification.core import SPECIFICATION_PART as CORE


@summary("SemanticView を成果物へ変換する Realizer の独立性と check 契約。")
@canonical_source(
    "Realization Semantics", filename="realization.md", order=40, heading="identity"
)
class SPECIFICATION_PART:
    """Realizer と realization check の意味上の契約。"""

    class REAL_001:
        """Realizer.realize() は SemanticView を受け取り、成果物を返す。成果物の Python type は Shikumi core が制限しない。"""

        title @= "Realizer consumes a semantic view"
        level @= MUST
        related @= CORE.CORE_005

    class REAL_002:
        """Realizer.check() は成果物を生成せず、その Realizer 固有の実現可能性を RealizationCheck として返す。"""

        title @= "Check does not realize"
        level @= MUST

    class REAL_003:
        """RealizationCheck.is_realizable は ERROR severity の diagnostic がない場合に true とする。"""

        title @= "Realizability is determined by error diagnostics"
        level @= MUST

    class REAL_004:
        """Realizer は Shikumi instance に登録または所有される必要がなく、同じ SemanticView に複数の Realizer を適用できる。"""

        title @= "Realizers remain independent"
        level @= MUST
        related @= CORE.CORE_006

    class REAL_005:
        """Realizer は必要であれば check() に独自条件を実装してよいが、core validation の代替として暗黙に扱ってはならない。"""

        title @= "Realizer checks may add output-specific conditions"
        level @= MAY

    class REAL_006:
        """RealizationCheck に subject=None の Diagnostic が渡された場合、check 対象 SemanticView の focus subject を diagnostic subject として補う。"""

        title @= "Realization diagnostics default to the view focus"
        level @= MUST
