# File: scripts/merge_test_code.py
"""
Script to consolidate all test Python files under tests/ into one annotated text file.
This output is saved to: scripts/merged_sources/tests_code_merged.txt
"""

from pathlib import Path

OUTPUT_DIR = Path("scripts/merged_sources")
OUTPUT_FILE = OUTPUT_DIR / "tests_code_merged.txt"
SOURCE_DIR = Path("tests")


def should_ignore(path):
    return "__pycache__" in path.parts or path.suffix == ".pyc"


def merge_test_files():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("# Consolidated Test Code from `tests/`\n\n")

        for filepath in sorted(SOURCE_DIR.rglob("*.py")):
            if should_ignore(filepath):
                continue
            try:
                rel_path = filepath.relative_to(Path.cwd())
            except ValueError:
                rel_path = str(filepath)
            outfile.write(f"\n\n{'-' * 80}\n")
            outfile.write(f"# This is the {rel_path}:\n")
            outfile.write(f"{'-' * 80}\n\n")
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(infile.read().rstrip() + "\n")

    print(f"[✅] Merged test/ code written to {OUTPUT_FILE}")


if __name__ == "__main__":
    merge_test_files()
