#!/usr/bin/env python3
"""Render pattern pieces without typing full module paths.

    python run.py                                     # render everything
    python run.py front                                # render every "front" (errors if ambiguous)
    python run.py aldrich_tailored_skirt/base/front.py  # render exactly this one
    python run.py front back --profile kaveri           # render multiple, with a profile
    python run.py --list                                # show every available target
"""

import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
EXCLUDED_DIRS = {"utils", "render", "generated", "__pycache__", ".git"}


def discover_targets() -> dict:
    """Map dotted module path -> file path for every renderable pattern script."""
    targets = {}
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [
            d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith(".")
        ]
        if dirpath == REPO_ROOT:
            continue  # top-level scripts (run.py etc.) aren't pattern targets
        for filename in filenames:
            if not filename.endswith(".py") or filename == "__init__.py":
                continue
            file_path = os.path.join(dirpath, filename)
            with open(file_path) as f:
                source = f.read()
            if "render_svg(" not in source:
                continue
            rel_path = os.path.relpath(file_path, REPO_ROOT)
            module = rel_path[: -len(".py")].replace(os.sep, ".")
            targets[module] = file_path
    return targets


def normalize(target: str) -> str:
    target = target.strip().replace("\\", "/")
    if target.endswith(".py"):
        target = target[: -len(".py")]
    return target.strip("/").replace("/", ".")


def resolve_target(target: str, targets: dict) -> str:
    lower = normalize(target).lower()

    for module in targets:
        if module.lower() == lower:
            return module

    suffix_matches = [m for m in targets if m.lower().endswith("." + lower)]
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    if len(suffix_matches) > 1:
        _fail_ambiguous(target, suffix_matches)

    contains_matches = [m for m in targets if lower in m.lower()]
    if len(contains_matches) == 1:
        return contains_matches[0]
    if len(contains_matches) > 1:
        _fail_ambiguous(target, contains_matches)

    print(
        f"No pattern target matches {target!r}. Run `python run.py --list` to see options.",
        file=sys.stderr,
    )
    sys.exit(1)


def _fail_ambiguous(target: str, matches: list) -> None:
    print(f"{target!r} matches multiple targets, be more specific:", file=sys.stderr)
    for module in sorted(matches):
        print(f"  {module.replace('.', '/')}.py", file=sys.stderr)
    sys.exit(1)


def run_module(module: str, env: dict) -> None:
    print(f"Running {module}...")
    subprocess.run([sys.executable, "-m", module], check=True, cwd=REPO_ROOT, env=env)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets",
        nargs="*",
        help="Pattern(s) to render (name, path, or dotted module). "
        "Omit to render everything.",
    )
    parser.add_argument(
        "--profile",
        default=os.environ.get("PATTERN_PROFILE", "default"),
        help="Measurement profile name (utils/profiles/<name>.json)",
    )
    parser.add_argument(
        "--list", action="store_true", help="List available targets and exit."
    )
    args = parser.parse_args()

    if REPO_ROOT not in sys.path:
        sys.path.insert(0, REPO_ROOT)

    all_targets = discover_targets()

    if args.list:
        for module in sorted(all_targets):
            print(module.replace(".", "/") + ".py")
        return 0

    modules = (
        [resolve_target(t, all_targets) for t in args.targets]
        if args.targets
        else sorted(all_targets)
    )

    env = os.environ.copy()
    env["PATTERN_PROFILE"] = args.profile

    for module in modules:
        run_module(module, env)

    print(f"Rendered {len(modules)} pattern(s) successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
