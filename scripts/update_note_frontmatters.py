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
import unicodedata
import urllib.request
import urllib.parse
from collections import defaultdict


_SYNC_VERSION = 3
_RE_NUMBER_ONLY = re.compile("[0-9]+")


def levenshtein(s1, s2):
    """Implementation of levensthein distance from WikiBooks."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row
            # are one character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def parse_frontmatter(filename):
    frontmatter = {}
    parsing = False

    with open(filename, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    for line in lines:
        if line == "---":
            if parsing:
                return frontmatter
            parsing = True

        if parsing:
            if ":" in line:
                key, value = line.split(":", maxsplit=1)
                frontmatter[key] = value.lstrip().rstrip()

    return frontmatter


def retrieve_metadata(title, no_download=True):
    encoded_title = urllib.parse.quote(title)
    url = f"https://dblp.org/search/publ/api?query={encoded_title}&format=json&h=50"

    print(f"Get {url}")

    if no_download:
        return None

    try:
        with urllib.request.urlopen(url) as f:
            content = f.read()
    except urllib.error.URLError as error:
        print(f"Error: {error}")
        return None

    try:
        json_content = json.loads(content)
    except JSONDecodeError as error:
        print(f"JSON Decode Error: {error}")
        return None

    return json_content


def find_best_hit(title, metadata):
    if not int(metadata["result"]["hits"]["@total"]):
        print(f"Error: no hits found for {metadata['result']['query']}")
        return None

    hits = metadata["result"]["hits"]["hit"]
    distances = [levenshtein(title, h["info"]["title"]) for h in hits]
    conference_factor = [0 if h["info"]["key"].startswith("conf") else 1 for h in hits]
    scores = [-int(h["@score"]) for h in hits]
    weights = list(zip(distances, conference_factor, scores))

    best_index = min(range(len(hits)), key=lambda x: weights[x])

    return hits[best_index]


def filter_author_text(text):
    return " ".join([t for t in re.split("\s+", text) if not _RE_NUMBER_ONLY.match(t)])


def metadata_to_frontmatter_content(hit):
    authors_metadata = hit["info"]["authors"]["author"]
    authors_metadata_list = (
        [authors_metadata] if isinstance(authors_metadata, dict) else authors_metadata
    )
    authors = [filter_author_text(a["text"]) for a in authors_metadata_list]

    hit_info = {k: v for k, v in hit["info"].items() if isinstance(v, str)}
    hit_info["authors"] = authors

    return hit_info


def make_cite_key(frontmatter_content):
    cite_key = frontmatter_content["key"]

    if "corr/" in cite_key:
        cite_key = "/".join(
            [
                cite_key,
                unicodedata.normalize(
                    "NFD", frontmatter_content["authors"][0].split()[-1]
                )
                .encode("ascii", "ignore")
                .decode(),
                frontmatter_content["year"],
            ]
        )

    return cite_key


def get_updated_frontmatter(filename, no_download=True):
    frontmatter = parse_frontmatter(filename)

    # Skip these two without warning to reduce noise
    if "title" not in frontmatter:
        return None

    if "sync_version" in frontmatter:
        if int(frontmatter["sync_version"]) >= _SYNC_VERSION:
            return None

    print(f"Process {filename}")
    metadata = retrieve_metadata(frontmatter["title"], no_download=no_download)

    if not metadata:
        return None

    best_hit = find_best_hit(frontmatter["title"], metadata)

    if not best_hit:
        return None

    retrieved_content = metadata_to_frontmatter_content(best_hit)

    if not retrieved_content:
        return None

    frontmatter = {
        **frontmatter,
        **retrieved_content,
        "sync_version": _SYNC_VERSION,
        "cite_key": make_cite_key(retrieved_content),
    }

    return frontmatter


def format_item(value):
    if isinstance(value, str):
        return value

    return json.dumps(value)


def format_frontmatter(frontmatter):
    return "\n".join([f"{k}: {format_item(v)}" for k, v in frontmatter.items()])


def get_start_read_from(filename_lines):
    frontmatter_count = 0
    start_from = 0

    for i, line in enumerate(filename_lines):
        if line == "---":
            frontmatter_count += 1

        if frontmatter_count == 2:
            start_from = i + 1
            break

    return start_from


def rewrite_frontmatter_section(filename, frontmatter):
    # Read the file and exclude the frontmatter section if
    # there is one
    with open(filename, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    start_from = get_start_read_from(lines)
    contents = "\n".join(lines[start_from:])

    total_contents = "\n".join(["---", frontmatter, "---", contents])

    with open(filename, "w") as f:
        f.write(total_contents)


def update_frontmatter(filename, dry_run=True, no_download=True):
    updated_frontmatter = get_updated_frontmatter(filename, no_download=no_download)

    if not updated_frontmatter:
        return

    formatted_frontmatter = format_frontmatter(updated_frontmatter)

    if dry_run:
        print(f"Frontmatter for {filename}")
        print(formatted_frontmatter)
    else:
        print(f"Rewrote frontmatter for {filename}")
        rewrite_frontmatter_section(filename, formatted_frontmatter)


def walk_and_process_notes(notes_directory, dry_run=False, no_download=False):
    for root, dirnames, filenames in os.walk(notes_directory):
        for filename in fnmatch.filter(filenames, "*.md"):
            update_frontmatter(
                os.path.join(root, filename), dry_run=dry_run, no_download=no_download
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notes_directory", type=str, help="Path to the notes")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write anything, just say what would happen",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Don't download anything, just say what would happen",
    )
    args = parser.parse_args()

    walk_and_process_notes(
        args.notes_directory, dry_run=args.dry_run, no_download=args.no_download
    )


if __name__ == "__main__":
    main()
