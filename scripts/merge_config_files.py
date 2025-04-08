# File: scripts/merge_config_files.py
"""
Script to collect all relevant config and setting files into one annotated text file.
Includes: pyproject.toml, requirements*.txt, .pre-commit-config.yaml, .env.example, Dockerfile, etc.
Output saved to: scripts/merged_sources/config_files_merged.txt
"""

from pathlib import Path

OUTPUT_DIR = Path("scripts/merged_sources")
OUTPUT_FILE = OUTPUT_DIR / "config_files_merged.txt"
CONFIG_FILES = [
    "pyproject.toml",
    "requirements.txt",
    "dev-requirements.txt",
    ".pre-commit-config.yaml",
    ".env.example",
    ".env",
    "Dockerfile",
    "docker-compose.yml",
    ".flake8",
    ".github/workflows/backend.yml",
]


def merge_config_files():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("# Consolidated Config & Setup Files\n\n")

        for file in CONFIG_FILES:
            path = Path(file)
            if not path.exists():
                continue
            outfile.write(f"\n\n{'-' * 80}\n")
            outfile.write(f"# This is the {file}:\n")
            outfile.write(f"{'-' * 80}\n\n")
            with open(path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read().rstrip() + "\n")

    print(f"[✅] Merged config files written to {OUTPUT_FILE}")


if __name__ == "__main__":
    merge_config_files()
