"""Description and runtime information specification."""

from shikumi_devdoc.fields.specification import (
    MAY,
    MUST,
    MUST_NOT,
    detail,
    level,
    related,
)
from shikumi_devdoc.norms.common import canonical_source, summary
from shikumi_devdoc.norms.document import title

from devdocs.canonical_sources.docs.specification.core import SPECIFICATION_PART as CORE


@summary("情報接続、記述器使用、記述方法の責務境界。")
@canonical_source(
    "Description Semantics", filename="description.md", order=10, heading="identity"
)
class SPECIFICATION_PART:
    """記述を runtime semantic state として成立させる契約。"""

    class DESC_001:
        """情報型は意味情報の種類、受理する Python value type、cardinality を定義し、その identity は InformationType object の identity による。"""

        title @= "Information type identity"
        level @= MUST
        related @= CORE.CORE_003

    class DESC_002:
        """情報接続は、対象、InformationType、値を一件の runtime information record として関連付ける。Cardinality.ONE であっても接続時点では複数値を禁止しない。"""

        title @= "Attachment preserves observable runtime state"
        level @= MUST
        detail @= "Cardinality 違反は不正状態を保持したまま validation で診断できる。"

    class DESC_003:
        """記述器使用と情報接続は別の実行時事実であり、一回の記述器使用がゼロ件、一件、複数件の情報接続を行ってよい。"""

        title @= "Descriptor use and information attachment are distinct"
        level @= MUST

    class DESC_004:
        """記述器の具体的な Python syntax は規定しない。decorator、@=、docstring、通常の関数呼び出しその他の実行時処理を利用できる。"""

        title @= "Description syntax is open"
        level @= MAY

    class DESC_005:
        """Shikumi は記述器関数の signature、戻り値、import 元、source 上の名称から情報や記述器使用規則を自動推論してはならない。"""

        title @= "No descriptor inference"
        level @= MUST_NOT
        related @= CORE.CORE_007

    class DESC_006:
        """class body の @= 記述で接続先 class がまだ成立していない場合、class_binding は class 成立後まで値を保持し、指定 callback へ owner class と値を渡す低水準機構として振る舞う。"""

        title @= "Class binding defers connection until class creation"
        level @= MUST
