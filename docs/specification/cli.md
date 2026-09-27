# CLI Semantics

Contracts for the `shikumi` command-line interface.

## CLI_001
The CLI **MUST** act as a thin runtime wiring layer. It does not own a registry or discovery system for specification bodies, description bodies, or Realizers and resolves supplied Python references by ordinary import.

title: CLI is a thin runtime wiring layer

level: MUST

related: [API_001](public-api.md#api_001)

## CLI_002
`--shikumi` and `--realizer` **MUST** use `module:object`; `--body` may name a module/package or `module:object`.

title: Python reference forms

level: MUST

## CLI_003
Validating a standalone module through `--body` **MUST** also supply its intended placement through `--at`.

title: Module validation requires placement

level: MUST

related: [STRUCT_003](structure.md#struct_003)

## CLI_004
`--structure-spec` and `--structure-from` are explicit, mutually exclusive structure sources. Failure to resolve one **MUST NOT** fall back to the other.

title: Explicit structure source

level: MUST NOT

related: [STRUCT_006](structure.md#struct_006)

## CLI_005
`validate` **MUST** run `Shikumi.validate()` and, only when `--realizer` is supplied, additionally run `Realizer.check()`. It **MUST NOT** generate an artifact.

title: Validate does not realize

level: MUST NOT

related: [VAL_006](validation.md#val_006), [REAL_002](realization.md#real_002)

## CLI_006
`validate` **MUST** return exit status `0` when neither Validation nor an optional realization check contains an error, otherwise `1`. Warnings and informational Diagnostics alone return `0`.

title: Validate exit status

level: MUST

## CLI_007
`realize` **MUST** generate an artifact by passing a Semantic View to the selected Realizer and **MUST NOT** implicitly run Validation or `Realizer.check()`.

title: Realize is independent from checks

level: MUST NOT

related: [REAL_001](realization.md#real_001)

## CLI_008
Artifacts directly writable by the CLI **MUST** be text, bytes-like data, or JSON-serializable Python values.

title: CLI artifact serialization

level: MUST

## CLI_009
`--format` **MUST** select the CLI response format and **MUST NOT** alter the artifact format produced by the Realizer.

title: Response format and artifact format are separate

level: MUST

## CLI_010
A JSON response **MUST** include `format_version`; the current version is `1`. When an output file is requested, the artifact goes to the file and the CLI response remains on stdout.

title: Structured CLI response

level: MUST

condition: When `--format json` is used.
