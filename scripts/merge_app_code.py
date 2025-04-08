# File: scripts/merge_app_code.py
"""
Script to consolidate all Python source files under app/ (excluding __pycache__)
and selected root-level files (e.g., run.py) into one annotated text file.
This output is saved to: scripts/merged_sources/app_code_merged.txt
"""

from pathlib import Path

OUTPUT_DIR = Path("scripts/merged_sources")
OUTPUT_FILE = OUTPUT_DIR / "app_code_merged.txt"
SOURCE_DIR = Path("app")
ROOT_FILES = [Path("run.py")]  # Add any other root-level .py files here


def should_ignore(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix == ".pyc"


def merge_python_files():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("# Consolidated Source Code from `app/` and root-level Python files\n\n")

        # Include all Python files from app/
        for filepath in sorted(SOURCE_DIR.rglob("*.py")):
            if should_ignore(filepath):
                continue
            try:
                rel_path = filepath.relative_to(Path.cwd())
            except ValueError:
                rel_path = filepath
            outfile.write(f"\n{'-' * 80}\n")
            outfile.write(f"# This is the {rel_path}:\n")
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(infile.read().rstrip() + "\n")

        # Include root-level Python files (like run.py)
        # outfile.write("\n\n" + "=" * 80 + "\n")
        # outfile.write("# Additional Root-Level Files\n")
        # outfile.write("=" * 80 + "\n\n")

        for root_file in ROOT_FILES:
            if root_file.exists():
                outfile.write(f"\n{'-' * 80}\n")
                outfile.write(f"# This is the {root_file}:\n")
                with open(root_file, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read().rstrip() + "\n")

    print(f"[✅] Merged app/ + root files written to {OUTPUT_FILE}")


if __name__ == "__main__":
    merge_python_files()
