"""CLI for the substrate — what /reindex (and cold tests) invoke.

  python -m substrate index  <vault> [--store DIR] [--adapter stub|local|api] [--canon DIR] [--rebuild]
  python -m substrate search <vault> --query TEXT --candidates id1,id2,... [--store DIR] [--adapter ...]
  python -m substrate dedup  <vault> --threshold FLOAT [--store DIR] [--adapter ...]

The default adapter is `stub` so the shell runs cold (no model, no key) — that is how the
fixture corpus and the contract tests exercise the pipeline. `local`/`api` are the S19
adapters and raise NotConfigured until set up. The store defaults to `.claude/substrate/store`
under the vault; it is INSTANCE data (gitignored), never committed (MODEL-RETRIEVAL.md §5).
"""

import os
import sys

from . import (
    ApiAdapter,
    LocalAdapter,
    NotConfigured,
    StubEmbedder,
    index_pages,
    read_canon_pages,
    rerank,
    semantic_duplicates,
)

DEFAULT_STORE = os.path.join(".claude", "substrate", "store")
DEFAULT_CANON = "canon"


def build_adapter(name):
    """Construct the requested adapter. `stub` is dependency-free and cold-runnable; the
    others are the S19 adapters (placeholder pins / key env var — they raise until set up)."""
    if name == "stub":
        return StubEmbedder()
    if name == "local":
        # Pins are placeholders in the engine; real model id + checksum are set at S19.
        return LocalAdapter(model_id="<local-embedding-model>", expected_sha256="<sha256>")
    if name == "api":
        return ApiAdapter(key_env_var="PULSE_EMBEDDING_API_KEY", model_id="<api-embedding-model>")
    raise ValueError(f"unknown adapter: {name} (expected stub|local|api)")


def _parse(argv):
    if len(argv) < 3:
        raise ValueError("usage: python -m substrate <index|search|dedup> <vault> [options]")
    command, vault = argv[1], argv[2]
    options = {"--store": None, "--adapter": "stub", "--canon": None,
               "--query": None, "--candidates": None, "--threshold": None, "--rebuild": False}
    flags = {"--rebuild"}
    i = 3
    while i < len(argv):
        token = argv[i]
        if token in flags:
            options[token] = True
            i += 1
        elif token in options:
            options[token] = argv[i + 1]
            i += 2
        else:
            raise ValueError(f"unexpected argument: {token}")
    return command, vault, options


def main():
    try:
        command, vault, options = _parse(sys.argv)
    except (ValueError, IndexError) as error:
        print(f"substrate: {error}", file=sys.stderr)
        return 2
    if not os.path.isdir(vault):
        print(f"substrate: not a directory: {vault}", file=sys.stderr)
        return 2

    store_dir = options["--store"] or os.path.join(vault, DEFAULT_STORE)
    canon_dir = options["--canon"] or os.path.join(vault, DEFAULT_CANON)
    if not os.path.isdir(canon_dir):
        print(f"substrate: no canon dir: {canon_dir}", file=sys.stderr)
        return 2

    try:
        adapter = build_adapter(options["--adapter"])
        pages = read_canon_pages(canon_dir)

        if command == "index":
            summary = index_pages(store_dir, pages, adapter, full_rebuild=options["--rebuild"])
            mode = "rebuilt" if summary["rebuilt"] else "incremental"
            print(f"indexed {len(summary['indexed'])}, skipped {len(summary['skipped'])}, "
                  f"removed {len(summary['removed'])} (model: {summary['model']}, {mode})")
            for page_id in summary["indexed"]:
                print(f"  + {page_id}")
            return 0

        if command == "search":
            if not options["--query"] or options["--candidates"] is None:
                print("substrate: search needs --query and --candidates", file=sys.stderr)
                return 2
            candidate_ids = [c for c in options["--candidates"].split(",") if c]
            order = rerank(store_dir, options["--query"], candidate_ids, pages, adapter)
            for rank, page_id in enumerate(order, 1):
                print(f"  {rank}. {page_id}")
            return 0

        if command == "dedup":
            if options["--threshold"] is None:
                print("substrate: dedup needs --threshold (calibrated at S19)", file=sys.stderr)
                return 2
            pairs = semantic_duplicates(store_dir, pages, float(options["--threshold"]))
            print(f"duplicate candidates: {len(pairs)}")
            for id_a, id_b, score in pairs:
                print(f"  {score:.4f}  {id_a}  ~  {id_b}")
            return 0

        print(f"substrate: unknown command: {command}", file=sys.stderr)
        return 2
    except NotConfigured as error:
        print(f"substrate: {error}", file=sys.stderr)
        return 3
    except (ValueError, OSError) as error:
        # OSError covers a bad --store (e.g. a path that is a file) — clean exit 2, not a
        # raw traceback.
        print(f"substrate: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
