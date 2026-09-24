#!/usr/bin/env python3
"""
Package Werracle arXiv submission into .tar.gz and .zip archives.
Archive root must contain:
- main.tex
- main.bbl
- references.bib
- figures/fig1_werracle_architecture.png
- figures/fig2_benchmarks_comparison.png
"""

import os
import tarfile
import zipfile

ARXIV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "arxiv"))
TAR_GZ_OUT = os.path.join(ARXIV_DIR, "werracle_arxiv_package.tar.gz")
ZIP_OUT = os.path.join(ARXIV_DIR, "werracle_arxiv_package.zip")

FILES_TO_PACK = [
    ("main.tex", "main.tex"),
    ("main.bbl", "main.bbl"),
    ("references.bib", "references.bib"),
    (os.path.join("figures", "fig1_werracle_architecture.png"), "figures/fig1_werracle_architecture.png"),
    (os.path.join("figures", "fig2_benchmarks_comparison.png"), "figures/fig2_benchmarks_comparison.png"),
]

def build_archives():
    print(f"Packaging files from: {ARXIV_DIR}")
    
    # 1. Build .tar.gz
    with tarfile.open(TAR_GZ_OUT, "w:gz") as tar:
        for local_rel, arcname in FILES_TO_PACK:
            full_path = os.path.join(ARXIV_DIR, local_rel)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Missing file: {full_path}")
            tar.add(full_path, arcname=arcname)
            print(f"  [tar.gz] Added: {arcname} ({os.path.getsize(full_path)} bytes)")
    print(f"Created: {TAR_GZ_OUT} ({os.path.getsize(TAR_GZ_OUT)} bytes)")

    # 2. Build .zip
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as zipf:
        for local_rel, arcname in FILES_TO_PACK:
            full_path = os.path.join(ARXIV_DIR, local_rel)
            zipf.write(full_path, arcname=arcname)
            print(f"  [zip]    Added: {arcname} ({os.path.getsize(full_path)} bytes)")
    print(f"Created: {ZIP_OUT} ({os.path.getsize(ZIP_OUT)} bytes)")

if __name__ == "__main__":
    build_archives()
