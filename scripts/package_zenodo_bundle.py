#!/usr/bin/env python3
"""
Package the Werracle Zenodo Open Science Replication Bundle
Creates zenodo_bundle_werracle_v1.0.zip containing clean repository artifacts,
re-compiled paper PDF, contracts, tests, and metadata.
"""

import os
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ZIP = os.path.join(BASE_DIR, "zenodo_bundle_werracle_v1.0.zip")

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".cache",
    ".playwright"
}

EXCLUDED_EXTS = {
    ".pyc",
    ".log",
    ".zip"
}

def create_bundle():
    print(f"Creating Zenodo replication bundle at: {OUTPUT_ZIP}")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(BASE_DIR):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".")]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in EXCLUDED_EXTS:
                    continue
                if file.startswith(".env") or file == "zenodo_bundle_werracle_v1.0.zip":
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                # Store with forward slashes for cross-platform compatibility
                archive_name = rel_path.replace("\\", "/")
                z.write(full_path, archive_name)
                print(f"  + {archive_name}")

    file_size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"\n[SUCCESS] Zenodo Bundle Created: {OUTPUT_ZIP} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    create_bundle()
