import argparse
import fnmatch
import io
import itertools
import json
from json.decoder import JSONDecodeError
import os
import sys
import subprocess
import re
import urllib.request
import urllib.parse
from collections import defaultdict

from update_note_frontmatters import parse_frontmatter


_REQUIRED_SECTIONS = {"title", "venue", "year", "key", "cite_key", "url", "authors"}


def format_author(author):
    parts = author.split()
    first = " ".join(parts[:-1])
    last = parts[-1]

    return f"{last}, {first}"


def format_authors(authors):
    return " and ".join(
        [
            format_author(author)
            for author in (
                json.loads(authors) if not isinstance(authors, list) else authors
            )
        ]
    )


def format_title(title):
    return re.sub("([A-Z])", "{\\1}", title)


def format_pages(pages):
    return "--".join(pages.split("-"))


def make_bibentry_from_frontmatter(filename):
    frontmatter = parse_frontmatter(filename)
    keys = set(list(frontmatter.keys()))

    if not "cite_key" in frontmatter:
        # Silently
        return None

    remaining_keys = _REQUIRED_SECTIONS - keys

    if remaining_keys:
        print(f"Not generating bibentry for {filename}, missing {remaining_keys}")
        print(keys)
        return None

    print(f"Generate from {filename}")
    return (
        f"@inproceedings{{{frontmatter['cite_key']},\n  "
        + "\n  ".join(
            list(
                filter(
                    lambda x: x,
                    [
                        f"author = {{{format_authors(frontmatter['authors'])}}},",
                        f"title = {{{format_title(frontmatter['title'])}}},",
                        f"booktitle = {{{frontmatter['venue']}}},",
                        f"volume = {{{frontmatter['volume']}}},"
                        if "volume" in frontmatter
                        else None,
                        f"number = {{{frontmatter['number']}}},"
                        if "number" in frontmatter
                        else None,
                        f"pages = {{{format_pages(frontmatter['pages'])}}},"
                        if "pages" in frontmatter
                        else None,
                        f"year = {{{frontmatter['year']}}},",
                        f"url = {{{frontmatter['ee']}}}" if "ee" in frontmatter else None
                    ],
                )
            )
        )
        + "\n}\n"
    )


def read_bibentry_from_correpsonding_bibfile(filename):
    filename, ext = os.path.splitext(filename)
    bib_filename = filename + ".bib"

    try:
        with open(bib_filename, "r") as f:
            print(f"Read from {bib_filename}")
            return f.read()
    except IOError:
        print(f"Could not open {bib_filename}")
        return None


def get_bibentry_for_filename(filename):
    bibentry = read_bibentry_from_correpsonding_bibfile(filename)

    if bibentry is not None:
        return bibentry

    return make_bibentry_from_frontmatter(filename)


def walk_and_process_notes(notes_directory):
    for root, dirnames, filenames in os.walk(notes_directory):
        if root != notes_directory:
            yield f"% {os.path.relpath(root, notes_directory)}"

        for filename in fnmatch.filter(filenames, "*.md"):
            bibentry = get_bibentry_for_filename(os.path.join(root, filename))

            if bibentry:
                yield f"% {filename}"
                yield bibentry


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notes_directory", type=str, help="Path to the notes")
    parser.add_argument(
        "bibliography",
        default="bibliography.bib",
        type=str,
        help="Path to the bibliography",
    )
    parser.add_argument(
        "--append",
        nargs="+",
        type=str,
        help="Append the content of these files to the bibliography",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write anything, just say what would happen",
    )
    args = parser.parse_args()

    entries = list(walk_and_process_notes(args.notes_directory))
    append_contents = [read_file(append_filename) for append_filename in args.append]

    contents = "\n".join(["\\UseRawInputEncoding", *entries, *append_contents])

    if not args.dry_run:
        with open(args.bibliography, "w") as f:
            f.write(contents)


if __name__ == "__main__":
    main()
