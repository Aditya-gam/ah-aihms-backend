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
    ".github/workflows/backend.yml",
    ".coveragerc",
    ".env",
    ".flaskenv",
    ".gitignore",
    "isort.cfg",
    ".pre-commit-config.yaml",
    "dev-requirements.txt",
    "docker-compose.yml",
    "Dockerfile",
    "pyproject.toml",
    "requirements.txt",
    "run.py",
]


def merge_config_files():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("# Consolidated Config & Setup Files\n\n")

        for file in CONFIG_FILES:
            path = Path(file)
            if not path.exists():
                continue
            outfile.write(f"\n{'-' * 80}\n")
            outfile.write(f"# This is the {file}:\n")
            # outfile.write(f"{'-' * 80}\n")
            with open(path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read().rstrip() + "\n")

    print(f"[✅] Merged config files written to {OUTPUT_FILE}")


if __name__ == "__main__":
    merge_config_files()
