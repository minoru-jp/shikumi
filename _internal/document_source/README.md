# `_internal/document_source/`

このディレクトリには、Shikumi の公開文書・リポジトリ専用文書の canonical source と、中間文書生成に必要な運用情報を配置する。

- `*/canonical.py`: 各文書の意味的な正本。
- `changelog/released.py`: 公開済み release を保持する物理分割 part。
- `vocabulary/canonical.py`: 文書体系で使用する Vocabulary の正本。
- `vocabulary/terms.py`: Vocabulary から `shikumi-devdoc` で生成する IDE 参照用モジュール。
- `notice.toml`: `_internal/document_build/ja/` の中間文書へ埋め込む注意事項。

`shikumi-devdoc` は Shikumi リポジトリの開発時だけ使用する。`shikumi` distribution の実行時依存ではなく、wheel / sdist にも含めない。

中間文書は `_internal/document_build/ja/` に生成し、リポジトリへ commit する。生成には次を使用する。

```bash
python scripts/render_canonical_docs.py
```

commit 済みの中間文書と正本の整合性だけを確認する場合は次を使用する。

```bash
python scripts/render_canonical_docs.py --check
```

プロジェクト名、version、`requires-python`、公開 import package 名、CLI entry point、distribution 名は `pyproject.toml` から実現時の context として構築する。これらを canonical source に重複して固定値として保持しない。
