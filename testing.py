#!/usr/bin/env python3
import os
import secrets
import datetime
import subprocess
from pathlib import Path

DOMAIN_KEYWORD = "rocloud.id"
REPO_DIR = Path("osint-trufflehog-lab")
BRANCH_NAME = "test/leak-simulation"
FILE_NAME = "config/dev.env"
README_NAME = "README.md"
# Fake secrets for safe simulation:
API_KEY="OnlyTestingJW91B5wBv80Vme2KuXVag5xwRSEGdr"
JWT_SECRET="OnlyTestingJW91B5wBv80Vme2KuXVag5xwRSEGdr"
DB_PASSWORD="OnlyTestingJW91B5wBv80Vme2KuXVag5xwRSEGdr"

def run(cmd, cwd=None):
    subprocess.check_call(cmd, cwd=cwd)

def fake_secret(label: str, length: int = 32) -> str:
    # Fake-looking token, guaranteed not a real provider key
    return f"FAKE_{label}_{secrets.token_urlsafe(length)}"

def main():
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    REPO_DIR.mkdir(parents=True, exist_ok=True)

    # init git
    if not (REPO_DIR / ".git").exists():
        run(["git", "init"], cwd=REPO_DIR)
        run(["git", "config", "user.name", "osint-lab"], cwd=REPO_DIR)
        run(["git", "config", "user.email", "osint-lab@localhost"], cwd=REPO_DIR)

    # create files
    (REPO_DIR / "config").mkdir(exist_ok=True)
    leak_file = REPO_DIR / FILE_NAME
    readme = REPO_DIR / README_NAME

    leak_content = f"""# LAB ONLY - DO NOT USE REAL SECRETS
# Keyword anchor for OSINT discovery:
DOMAIN={DOMAIN_KEYWORD}

# Fake secrets for safe simulation:
API_KEY={fake_secret("APIKEY", 24)}
JWT_SECRET={fake_secret("JWT", 24)}
DB_PASSWORD={fake_secret("DBPASS", 24)}

# Marker for search:
OSSINT_LAB_MARKER={DOMAIN_KEYWORD}_{ts}
"""
    leak_file.write_text(leak_content, encoding="utf-8")

    readme.write_text(
        f"""# OSINT + TruffleHog Lab (SAFE)

This repo is for **safe simulation** only.
- Contains keyword: `{DOMAIN_KEYWORD}`
- Contains **FAKE** secrets (non-functional)

Marker: `{DOMAIN_KEYWORD}_{ts}`
""",
        encoding="utf-8"
    )

    # commit on a branch (for PR)
    run(["git", "checkout", "-B", BRANCH_NAME], cwd=REPO_DIR)
    run(["git", "add", "."], cwd=REPO_DIR)
    run(["git", "commit", "-m", f"lab: add safe fake secrets marker {DOMAIN_KEYWORD}_{ts}"], cwd=REPO_DIR)

    print("\n[OK] Repo lab created:")
    print(f"- Path   : {REPO_DIR.resolve()}")
    print(f"- Branch : {BRANCH_NAME}")
    print("\nNext steps (manual):")
    print("1) Create a NEW public GitHub repo (empty) e.g. osint-trufflehog-lab")
    print("2) Add remote and push:")
    print("   cd osint-trufflehog-lab")
    print("   git remote add origin https://github.com/<USER>/<REPO>.git")
    print(f"   git push -u origin {BRANCH_NAME}")
    print("3) Open PR on GitHub from this branch to main")

if __name__ == "__main__":
    main()
