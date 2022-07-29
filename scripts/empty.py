import argparse
import fnmatch
import os

from update_note_frontmatters import parse_frontmatter
from update_index import prune_empty, parse_markdown_to_tree_start, walk_structure


def parse_content(filename):
    count = 0

    with open(filename, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]

    content_lines = []

    for line in lines:
        if count < 2 and line == "---":
            count += 1
            continue

        if count == 0 or count == 2:
            content_lines.append(line)

    return content_lines


def walk_and_process_notes(notes_directory):
    for root, dirnames, filenames in os.walk(notes_directory):
        for filename in fnmatch.filter(filenames, "*.md"):
            path = os.path.join(root, filename)
            frontmatter = parse_frontmatter(path)

            if "cite_key" in frontmatter:
                if parse_content(path):
                    continue
                print(f"{path} has a cite_key but no content")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("index", help="Where the index.md file is stored")
    parser.add_argument("papers", help="Where the papers information is stored")
    args = parser.parse_args()

    walk_and_process_notes(args.papers)

    print("---")

    with open(args.index, "r") as f:
        md_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

        for obj in walk_structure(md_structure):
            if "keys" in obj and obj["keys"]:
                if obj["content"].startswith("."):
                    print(
                        f"{obj['links'][0]['fullpath']} has keys in index but no content"
                    )


if __name__ == "__main__":
    main()
