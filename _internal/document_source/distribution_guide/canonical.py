"""Distribution Guide の正本の記述体。

``TITLE_N`` の数値部分は Python 上で各見出しを識別するためだけに存在し、
順序、階層、見出し名その他の意味を一切表さない。
"""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title('{{TERM_3}}・{{TERM_5}}・{{TERM_26}}の配置')
class TITLE_1:
    r'''
    この文書は、{{TERM_3}}、{{TERM_5}}、{{TERM_26}}を、最終的に CLI から通常の Python import で参照できる形へ分かりやすく配置するための指針を示す。

    {{TERM_1}} は専用の配布形式や登録機構を要求しない。重要なのは、利用する Python object が import 可能であり、CLI からその参照を指定できることである。
    '''

    vocabulary_refs @= (
        terms.TERM_3,
        terms.TERM_5,
        terms.TERM_26,
        terms.TERM_1,
    )


    @title('目的')
    class TITLE_2:
        r'''
        CLI は、{{TERM_3}}が公開する `{{TERM_1}}`、{{TERM_5}}、{{TERM_26}}などを `MODULE:OBJECT` 形式の Python 参照として受け取る。

        したがって配置の目的は、これらを特別な Shikumi 用形式へ変換することではなく、通常の Python module/package として import 可能にし、どの object がどの役割を担うかを分かりやすく保つことである。

        {{TERM_3}}、{{TERM_5}}、{{TERM_26}}は物理形式ではなく役割であり、同じ module/package や distribution に同梱してもよい。
        '''

        vocabulary_refs @= (
            terms.TERM_3,
            terms.TERM_1,
            terms.TERM_5,
            terms.TERM_26,
        )

    @title('推奨配置')
    class TITLE_3:
        r'''
        プロジェクト固有の Shikumi 関連コードは、公式の作例では `{{TERM_33}}` package にまとめ、その中を `{{TERM_34}}` と `{{TERM_35}}` に分ける。

        ```text
        project/
        ├─ {{TERM_33}}/
        │  ├─ __init__.py
        │  ├─ {{TERM_34}}/
        │  │  ├─ __init__.py
        │  │  └─ ...
        │  └─ {{TERM_35}}/
        │     ├─ __init__.py
        │     └─ ...
        └─ application/
           └─ ...
        ```

        `{{TERM_34}}` には、{{TERM_3}}として利用する{{TERM_12}}、{{TERM_15}}、{{TERM_7}}、{{TERM_22}}、`{{TERM_1}}` インスタンスなどを置く。`{{TERM_35}}` には、{{TERM_19}}から{{TERM_28}}を生成する{{TERM_26}}を置く。

        {{TERM_5}}は、検証や実現の対象となる通常の Python module/package そのものであり、`{{TERM_33}}` の下へ移す必要はない。

        `{{TERM_33}}` という名前は、本体の import package `{{PROJECT.import_package}}` との衝突を避けつつ、そのプロジェクト固有の Shikumi 関連コードであることを一目で示すための作例である。
        '''

        vocabulary_refs @= (
            terms.TERM_33,
            terms.TERM_34,
            terms.TERM_35,
            terms.TERM_3,
            terms.TERM_12,
            terms.TERM_15,
            terms.TERM_7,
            terms.TERM_22,
            terms.TERM_1,
            terms.TERM_19,
            terms.TERM_28,
            terms.TERM_26,
            terms.TERM_5,
        )

    @title('CLI から参照する')
    class TITLE_4:
        r'''
        たとえば、次のような配置を想定する。

        ```text
        myproject/
        ├─ {{TERM_33}}/
        │  ├─ {{TERM_34}}/
        │  └─ {{TERM_35}}/
        └─ application/
        ```

        {{TERM_21}}では、{{TERM_3}}と{{TERM_5}}を通常の import path で指定する。

        ```bash
        {{PROJECT.cli_entry_point}} validate \
          --shikumi myproject.{{TERM_33}}.{{TERM_34}}:app \
          --body myproject.application \
          --structure-spec myproject.{{TERM_33}}.{{TERM_34}}:structure \
          --format text
        ```

        {{TERM_25}}では、さらに{{TERM_26}}を指定する。

        ```bash
        {{PROJECT.cli_entry_point}} realize \
          --shikumi myproject.{{TERM_33}}.{{TERM_34}}:app \
          --body myproject.application \
          --realizer myproject.{{TERM_33}}.{{TERM_35}}.markdown:markdown \
          --output OUTPUT.md \
          --format json
        ```

        CLI から参照できることが確認できれば、配置上の目的は達成されている。
        '''

        vocabulary_refs @= (
            terms.TERM_33,
            terms.TERM_34,
            terms.TERM_35,
            terms.TERM_21,
            terms.TERM_3,
            terms.TERM_5,
            terms.TERM_25,
            terms.TERM_26,
        )

    @title('配置と配布の自由')
    class TITLE_5:
        r'''
        `{{TERM_33}}/{{TERM_34}}` と `{{TERM_33}}/{{TERM_35}}` は、役割を分かりやすくするための推奨作例であり、{{TERM_1}} の要求ではない。

        小さな構成では単一 module にまとめてもよい。複数の役割を同じ distribution に同梱しても、別々のライブラリとして配布してもよい。名前や分割方法も、通常の Python ライブラリ設計として変更できる。

        {{TERM_3}}や{{TERM_26}}は {{TERM_1}} 本体とは独立した Python コードとして配布でき、独立して作成したコードには作者が任意のライセンスを設定できる。ただし、取り込んだ第三者コードにはそのライセンスが適用される。

        公式作例は参考ソースとして本体distributionに同梱する。ただし、作例そのものは公開import packageやCLI entry pointではない。repositoryでは`examples/`、wheelでは`shikumi/_examples/`に配置し、利用者コードが依存する公開面から分離する。

        実際の利用者プロジェクトでは、必要な object が通常の Python import で取得でき、利用時に明示的に参照できればよい。
        '''

        vocabulary_refs @= (
            terms.TERM_33,
            terms.TERM_34,
            terms.TERM_35,
            terms.TERM_1,
            terms.TERM_3,
            terms.TERM_26,
        )
