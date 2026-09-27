"""Structure showcase README canonical source."""

from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import list_field, test_target_field, title


try_code = test_target_field("try code")
patterns = list_field("patterns", str)


@canonical_source("構造ショーケース", filename="README.md", heading="title")
class EXAMPLE:
    '''
    この作例は特定の用途ドメインを模倣せず、Shikumi の構造規定が表現できる一般的なパターンを一つの実行可能な fixture 集として示します。

    規定本体は [`specification.py`](./specification.py) にあり、`valid/` は受理される構造、`invalid/` は意図的に規定へ違反する構造です。各 fixture は通常の Python package なので、`PackageTreeStructure` が実際の package tree を解決して検証します。
    '''

    class PATTERNS:
        '''{{patterns}}'''
        title @= '含まれる構造パターン'

        patterns @= "required / optional な具体名称の要素"
        patterns @= "自由名称および列挙名称を持つ logical element と cardinality"
        patterns @= "同じ parent に置く kind 別の任意名 package / module"
        patterns @= "StructureFragment による部分構造の再利用と unconstrained subtree"
        patterns @= "StructureFragment.recursive() による任意深度の再帰構造"
        patterns @= "StructureGroup による異種 exact sibling の集合 cardinality"
        patterns @= "明示 exact element が logical element より優先される override"

    class LAYOUT:
        '''
        `valid/minimal/` は required element だけを持つ最小構造です。`valid/combined/` は上記のパターンを一つの package tree にまとめています。

        `invalid/` には missing required element、空の logical collection、列挙外名称、group cardinality 違反、closed subtree への余分な要素をそれぞれ分離して置いています。invalid fixture は「失敗する作例」であり、その診断コードもテストで固定します。
        '''
        title @= 'fixture の構成'

    class TRY:
        '''
        repository checkout では `examples/` を Python path に置いて実行できます。

        ```python
        {{try_code}}
        ```
        '''
        title @= '試す'

        try_code @= r'''
        from structure_showcase.invalid import group_both
        from structure_showcase.specification import showcase, showcase_structure
        from structure_showcase.valid import combined

        valid_result = showcase.validate(
            combined,
            placement=(),
            structure_specification=showcase_structure,
        )
        assert valid_result.is_valid
        assert valid_result.structure_check is not None
        assert {binding.logical_element.logical_name for binding in valid_result.structure_check.bindings} >= {
            "entry",
            "variant",
            "package_child",
            "module_child",
            "branch",
            "module_leaf",
            "ordinary",
        }

        invalid_result = showcase.validate(
            group_both,
            placement=(),
            structure_specification=showcase_structure,
        )
        assert not invalid_result.is_valid
        assert {diagnostic.code for diagnostic in invalid_result.diagnostics} == {
            "structure.group.maximum",
        }
        '''
