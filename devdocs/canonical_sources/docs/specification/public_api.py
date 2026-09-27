"""Public API boundary specification."""

from shikumi_devdoc.fields.specification import INFORMATIVE, MUST, MUST_NOT, detail, level, related
from shikumi_devdoc.norms.common import canonical_source, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.docs.specification.core import SPECIFICATION_PART as CORE


@summary("Core、Standard、内部実装の公開境界。")
@canonical_source("Public API Boundary", filename="public-api.md", order=50, heading="identity")
class SPECIFICATION_PART:
    """Shikumi distribution が利用者へ約束する import surface。"""

    class API_001:
        """公開 Python API は `shikumi` と `shikumi.standard` が明示的に export する名前から構成する。文書化されない内部 module の import path は公開契約に含めない。"""

        title @= "Documented exports define the public surface"
        level @= MUST

    class API_002:
        """Core (`shikumi`) は情報、runtime binding、構造、意味像、Shikumi、validation、realization の抽象契約を提供する。"""

        title @= "Core owns the semantic primitives"
        level @= INFORMATIVE

    class API_003:
        """Standard (`shikumi.standard`) は Core を組み合わせた再利用可能な記述器、標準構造、標準 validation rule を提供し、新しい意味モデルを導入しない。"""

        title @= "Standard builds on Core"
        level @= MUST

    class API_004:
        """`kind`、`attr`、`rel` のような用途固有語彙を Standard が暗黙に定義または登録してはならない。用途固有語彙は規定体が通常の Python 定義として所有する。"""

        title @= "Domain vocabulary belongs to the specification author"
        level @= MUST_NOT
        related @= CORE.CORE_007

    class API_005:
        """独自 decorator、metaclass、base class、mixin が Python 標準の class creation や記述器実行順序を変更する組合せについて、Shikumi は互換処理を保証しない。"""

        title @= "Python class-creation interactions are outside compatibility guarantees"
        level @= INFORMATIVE
