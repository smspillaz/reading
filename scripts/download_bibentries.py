import argparse
import fnmatch
import os
import urllib.request
import urllib.parse
from collections import defaultdict
import re

from update_note_frontmatters import parse_frontmatter


def filter_content(bibtex_entry, frontmatter):
    lines = bibtex_entry.splitlines()
    lines[0] = re.sub(r"(.*\{)(.*)$", f"\\1{frontmatter['cite_key']},", lines[0])

    return "\n".join(lines)


def download_bibentry_from_file(
    filename, dry_run=False, redownload=False, rewrite=False
):
    frontmatter = parse_frontmatter(filename)

    if not "cite_key" in frontmatter:
        # Silently
        return None

    if not "url" in frontmatter:
        print(f"Not generating bibentry for {filename}, missing url")
        return None

    url = frontmatter["url"]
    bib_url, html_ext = os.path.splitext(url)
    bib_url = bib_url + ".bib"

    bib_filename, filename_ext = os.path.splitext(filename)
    bib_filename = bib_filename + ".bib"

    if os.path.exists(bib_filename):
        if not redownload:
            if rewrite:
                # Open the file if it exists and rewrite it
                print(f"Opening {bib_filename} to rewrite it")
                try:
                    with open(bib_filename, "r") as f:
                        contents = filter_content(f.read(), frontmatter)

                    if not dry_run:
                        with open(bib_filename, "w") as f:
                            f.write(contents)
                except IOError as e:
                    print(f"Skipped re-writing {bib_filename}: {e}")
                return

            print(f"Skipping {bib_filename} as it already exists")
            return
        print(f"Re-downloading {bib_filename}")

    print(f"Downloading from {bib_url}")

    if not dry_run:
        try:
            with urllib.request.urlopen(bib_url) as remote:
                with open(bib_filename, "w") as f:
                    f.write(filter_content(remote.read().decode(), frontmatter))
        except urllib.error.HTTPError as e:
            print(f"Skipping {bib_filename} because of error {e}")
            return None

    print(f"Downloaded {bib_filename} for {frontmatter['cite_key']}")
    return None


def walk_and_process_notes(
    notes_directory, dry_run=False, redownload=False, rewrite=False
):
    for root, dirnames, filenames in os.walk(notes_directory):
        for filename in fnmatch.filter(filenames, "*.md"):
            download_bibentry_from_file(
                os.path.join(root, filename),
                dry_run=dry_run,
                redownload=redownload,
                rewrite=rewrite,
            )


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notes_directory", type=str, help="Path to the notes")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write anything, just say what would happen",
    )
    parser.add_argument(
        "--redownload",
        action="store_true",
        help="Forcibly re-download from the server",
    )
    parser.add_argument(
        "--rewrite",
        action="store_true",
        help="Forcibly re-write based on any updated rulesr",
    )
    args = parser.parse_args()

    print(f"Process {args.notes_directory}")
    walk_and_process_notes(
        args.notes_directory, args.dry_run, args.redownload, args.rewrite
    )


if __name__ == "__main__":
    main()
