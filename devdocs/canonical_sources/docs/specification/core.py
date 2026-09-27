"""Core semantic specification for Shikumi."""

from shikumi_devdoc.fields.specification import (
    INFORMATIVE,
    MUST,
    MUST_NOT,
    detail,
    level,
)
from shikumi_devdoc.norms.common import canonical_source, summary
from shikumi_devdoc.norms.document import title


@summary("実行後の Python 状態を意味像として解釈する Shikumi の中核契約。")
@canonical_source("Core Semantics", filename="core.md", order=0, heading="identity")
class SPECIFICATION_PART:
    """Shikumi の意味モデル全体に共通する契約。"""

    class CORE_001:
        """Shikumi は Python の実行後に成立した runtime object、情報、記述器使用を解釈対象とする。"""

        title @= "Runtime state is the source of interpretation"
        level @= MUST

    class CORE_002:
        """Shikumi は Python source を AST として解析し、source text から意味状態を再構成してはならない。"""

        title @= "No AST-based semantic reconstruction"
        level @= MUST_NOT

    class CORE_003:
        """情報と記述器使用は Shikumi instance に所有されず、runtime object に対して成立する独立した実行時事実として扱う。"""

        title @= "Runtime semantic state is independent of Shikumi instances"
        level @= MUST
        detail @= "複数の Shikumi instance が同じ runtime object を、それぞれが認識する情報型や規則に従って解釈できる。"

    class CORE_004:
        """Shikumi が構成する意味像には、その Shikumi が認識する情報だけを取り込む。未認識情報を runtime object から削除してはならない。"""

        title @= "Interpret recognized information without mutating unknown information"
        level @= MUST

    class CORE_005:
        """検証は意味像を入力とする意味上の判定であり、実現は意味像から成果物を生成する別操作として扱う。"""

        title @= "Validation and realization are separate operations"
        level @= MUST

    class CORE_006:
        """Realizer は Shikumi に登録・所有される構成要素ではない。同じ意味像へ複数の Realizer を独立して適用できる。"""

        title @= "Realizers are independent consumers"
        level @= MUST

    class CORE_007:
        """Shikumi は情報や記述器の意味を自動推論せず、規定側が明示した情報型、記述器使用規則、検証規則、構造を組み合わせて意味体系を構成する。"""

        title @= "Meaning is author-defined"
        level @= INFORMATIVE

    class CORE_008:
        """一つの SemanticView は一回の構造解決と runtime fact 取得から構成し、その subview や同一 validation 内の下位規則評価では、既に取り込んだ node、情報、記述器使用を再利用する。"""

        title @= "Semantic views preserve one interpreted runtime snapshot"
        level @= MUST
