"""CLI semantic specification."""

from shikumi_devdoc.fields.specification import MUST, MUST_NOT, detail, level, condition, related
from shikumi_devdoc.norms.common import canonical_source, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.docs.specification.public_api import SPECIFICATION_PART as PUBLIC_API
from devdocs.canonical_sources.docs.specification.structure import SPECIFICATION_PART as STRUCTURE
from devdocs.canonical_sources.docs.specification.validation import SPECIFICATION_PART as VALIDATION
from devdocs.canonical_sources.docs.specification.realization import SPECIFICATION_PART as REALIZATION


@summary("validate / realize command、Python reference、exit code、JSON 応答の契約。")
@canonical_source("CLI Semantics", filename="cli.md", order=60, heading="identity")
class SPECIFICATION_PART:
    """`shikumi` CLI が runtime object を結線して処理する契約。"""

    class CLI_001:
        """CLI は規定体、記述体、Realizer の registry や discovery mechanism を所有せず、指定された Python reference を通常の import で解決する。"""

        title @= "CLI is a thin runtime wiring layer"
        level @= MUST
        related @= PUBLIC_API.API_001

    class CLI_002:
        """`--shikumi` と `--realizer` は `module:object` を要求し、`--body` は module/package または `module:object` を受理する。"""

        title @= "Python reference forms"
        level @= MUST

    class CLI_003:
        """単独 module を `--body` として validation する場合、`--at` に予定 placement を明示しなければならない。"""

        title @= "Module validation requires placement"
        level @= MUST
        related @= STRUCTURE.STRUCT_003

    class CLI_004:
        """`--structure-spec` と `--structure-from` は利用者が明示的に選択する排他的な structure source とし、一方の解決失敗から他方へフォールバックしてはならない。"""

        title @= "Explicit structure source"
        level @= MUST_NOT
        related @= STRUCTURE.STRUCT_006

    class CLI_005:
        """`validate` は Shikumi.validate() を実行し、`--realizer` が指定された場合だけ追加で Realizer.check() を実行する。成果物を生成してはならない。"""

        title @= "Validate does not realize"
        level @= MUST_NOT
        related @= VALIDATION.VAL_006
        related @= REALIZATION.REAL_002

    class CLI_006:
        """`validate` は validation と任意 realization check の双方に ERROR がない場合 exit code 0、一件以上ある場合 1 を返す。warning と info だけなら 0 とする。"""

        title @= "Validate exit status"
        level @= MUST

    class CLI_007:
        """`realize` は SemanticView を指定 Realizer へ渡して成果物を生成するが、validation または Realizer.check() を暗黙に実行してはならない。"""

        title @= "Realize is independent from checks"
        level @= MUST_NOT
        related @= REALIZATION.REAL_001

    class CLI_008:
        """CLI が file output として直接扱える成果物は text、bytes-like、または JSON serialization 可能な値とする。"""

        title @= "CLI artifact serialization"
        level @= MUST

    class CLI_009:
        """`--format` は CLI 自身の response format を選択し、Realizer が生成する成果物形式を変更してはならない。"""

        title @= "Response format and artifact format are separate"
        level @= MUST

    class CLI_010:
        """JSON response は `format_version` を含み、現在の format version は `1` とする。output file を指定した場合、成果物は file へ、CLI response は stdout へ分離する。"""

        title @= "Structured CLI response"
        level @= MUST
        condition @= "`--format json` を使用する場合。"
