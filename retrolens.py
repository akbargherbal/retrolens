#!/usr/bin/env python3
"""
RetroLens CLI
─────────────
Browse and retrieve promptlets. No API calls — just copy and use.

Commands:
  python retrolens.py list                      List all promptlets
  python retrolens.py list --category <cat>     Filter by category
  python retrolens.py get  <alias>              Print promptlet text
  python retrolens.py get  <alias> --save       Save promptlet to <alias>.txt

Cheat sheet:
  # Browse
  python retrolens.py list
  python retrolens.py list --category diagnostic

  # Inspect a promptlet before using it
  python retrolens.py get d1-thinking-loop

  # Get and save to file — paste into any UI, CLI agent, or API call
  python retrolens.py get d1-thinking-loop --save
  python retrolens.py get e1-session-conclusion --save
"""

import argparse
import json
import sys
from pathlib import Path

DIR        = Path(__file__).parent
PROMPTLETS = DIR / "retrolens_promptlets.json"


def load_promptlets() -> list[dict]:
    if not PROMPTLETS.exists():
        sys.exit(f"Error: {PROMPTLETS} not found.")
    with PROMPTLETS.open() as f:
        return json.load(f)


def find_promptlet(alias: str, promptlets: list[dict]) -> dict:
    match = next((p for p in promptlets if p["alias"] == alias), None)
    if not match:
        available = ", ".join(p["alias"] for p in promptlets)
        sys.exit(f"Error: '{alias}' not found.\nAvailable: {available}")
    return match


def cmd_list(args):
    promptlets = load_promptlets()

    if args.category:
        promptlets = [p for p in promptlets if p["category"] == args.category]
        if not promptlets:
            sys.exit(f"No promptlets found for category '{args.category}'.")

    grouped: dict[str, list] = {}
    for p in promptlets:
        grouped.setdefault(p["category"], []).append(p)

    for category, items in grouped.items():
        print(f"\n  {category.upper()}")
        print(f"  {'─' * 52}")
        for p in items:
            print(f"  {p['alias']:<28} {p['description']}")
    print()


def cmd_get(args):
    promptlets = load_promptlets()
    p = find_promptlet(args.alias, promptlets)

    output = (
        f"# {p['name']}\n"
        f"# alias: {p['alias']} | category: {p['category']}\n\n"
        f"{p['promptlet']}\n"
    )

    print(f"\n{'─' * 60}")
    print(output)
    print(f"{'─' * 60}\n")

    if args.save:
        out_file = DIR / f"{p['alias']}.txt"
        out_file.write_text(output, encoding="utf-8")
        print(f"  Saved to: {out_file}\n")


def main():
    parser = argparse.ArgumentParser(
        description="RetroLens CLI — browse and retrieve promptlets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="command")

    p_list = sub.add_parser("list", help="List available promptlets")
    p_list.add_argument("--category", metavar="CAT",
                        help="diagnostic | extraction | optimization | comparative | archival")

    p_get = sub.add_parser("get", help="Print a promptlet ready to copy")
    p_get.add_argument("alias", help="e.g.  d1-thinking-loop")
    p_get.add_argument("--save", action="store_true",
                       help="Also save to <alias>.txt in the same directory")

    args = parser.parse_args()

    if   args.command == "list": cmd_list(args)
    elif args.command == "get":  cmd_get(args)
    else:                        parser.print_help()


if __name__ == "__main__":
    main()
