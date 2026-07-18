#!/usr/bin/env python3
"""Run all top-level pattern generation modules."""

import os
import subprocess
import sys

MODULES = [
    "aldrich_close_fitting_bodice.main",
    "aldrich_close_fitting_bodice.one_dart_front",
    "aldrich_close_fitting_bodice.two_dart_front",
    "aldrich_close_fitting_bodice.base.front",
    "aldrich_close_fitting_bodice.base.back",
    "aldrich_close_fitting_bodice.designs.shoulder_dart_front",
    "aldrich_close_fitting_bodice.designs.v_side_front",
    "aldrich_tailored_skirt.main",
    "aldrich_tailored_skirt.base.front",
    "aldrich_tailored_skirt.base.back",
    "aldrich_tailored_trousers.base.front",
    "aldrich_tailored_trousers.base.back",
    "aldrich_tailored_trousers.designs.no_dart_flare_shorts.front",
    "aldrich_tailored_trousers.designs.no_dart_flare_shorts.back",
]


def run_module(module: str) -> None:
    print(f"Running {module}...")
    subprocess.run([sys.executable, "-m", module], check=True)
    print()


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    for module in MODULES:
        run_module(module)

    print("All pattern modules executed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
