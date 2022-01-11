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


_SYNC_VERSION = 0


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
    url = f"https://dblp.org/search/publ/api?query={encoded_title}&format=json&h=1"

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


def metadata_to_frontmatter_content(metadata):
    if not int(metadata["result"]["hits"]["@total"]):
        print(f"Error: no hits found for {metadata['result']['query']}")
        return None

    first_hit = metadata["result"]["hits"]["hit"][0]
    authors_metadata = first_hit["info"]["authors"]["author"]
    authors_metadata_list = (
        [authors_metadata] if isinstance(authors_metadata, dict) else authors_metadata
    )
    authors = [a["text"] for a in authors_metadata_list]

    first_hit_info = {k: v for k, v in first_hit["info"].items() if isinstance(v, str)}
    first_hit_info["authors"] = authors

    return first_hit_info


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

    retrieved_content = metadata_to_frontmatter_content(metadata)

    if not retrieved_content:
        return None

    frontmatter = {**frontmatter, **retrieved_content, "sync_version": _SYNC_VERSION}

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
