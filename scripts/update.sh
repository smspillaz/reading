#!/bin/bash

rm index.stage
python scripts/update_index.py index.md
python scripts/scrape_titles.py index.md
python scripts/update_index.py index.md
python scripts/update_note_frontmatters.py papers
python scripts/update_index.py index.md
python scripts/download_bibentries.py papers
bash scripts/move_untracked_images.sh
python scripts/stage_index.py
python scripts/bulk_add.py papers --suffix md bib
