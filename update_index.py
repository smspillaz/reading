import argparse
import io
import json
import os
import sys
import re
from collections import defaultdict

_RE_HEADING = re.compile(r"^(?P<hashes>#+)\s+(?P<content>.+)$")
_RE_LINK = re.compile(r"\[\[(?P<link>[^\|]+)\|?(?P<desc>.+)\]\]")
_RE_BULLET = re.compile(r"\s-\s(?P<content>.+)$")


def lookup_to_node(tree, dirpath):
    node = tree
    split = dirpath.split(os.path.sep)
    for s in split:
        node = node["children"][s]

    return node


def defaultdict_of_defaultdict():
    return defaultdict(defaultdict_of_defaultdict)


def walk_fs_to_tree(root, exclude):
    tree = defaultdict_of_defaultdict()
    abs_root = os.path.abspath(root)

    for dirpath, dirnames, filenames in os.walk(abs_root):
        if any([p.startswith(".") for p in dirpath.split(os.path.sep)]):
            continue

        if any([p in exclude for p in dirpath.split(os.path.sep)]):
            continue

        if dirpath == abs_root:
            node = tree
        else:
            node = lookup_to_node(tree, dirpath[len(abs_root) + 1 :])

        node["objects"] = [
            {
                "filename": filename,
                "fullpath": os.path.relpath(os.path.join(dirpath, filename), abs_root),
                "filename_link_text": os.path.splitext(filename)[0],
            }
            for filename in filenames
            if os.path.splitext(filename)[1] == ".pdf"
        ]

    return tree


def parse_bullet(bullet_content):
    metadata = {}
    link_matches = list(_RE_LINK.finditer(bullet_content))

    assert len(link_matches) > 0

    # First link is a link to the filepath
    first_link, other_links = link_matches[0], link_matches[1:]
    metadata["fullpath"] = first_link.group("link")
    metadata["filename"] = os.path.basename(metadata["fullpath"])
    metadata["filename_link_text"] = first_link.group("desc")

    return metadata


def parse_markdown_to_tree(tree, markdown_lines, index, heading_level, depth):
    while index < len(markdown_lines):
        heading_match = _RE_HEADING.match(markdown_lines[index])

        if heading_match is not None:
            parsed_heading_level = len(heading_match.group("hashes"))
            heading_content = heading_match.group("content")

            # Get out of parsing this heading and go to the parent context
            if parsed_heading_level <= heading_level:
                return index

            tree["children"][heading_content] = defaultdict_of_defaultdict()
            index = parse_markdown_to_tree(
                tree["children"][heading_content],
                markdown_lines,
                index + 1,
                parsed_heading_level,
                depth + 1,
            )
            continue

        bullet_match = _RE_BULLET.match(markdown_lines[index])

        if bullet_match is not None:
            if "objects" not in tree:
                tree["objects"] = []
            tree["objects"].append(parse_bullet(bullet_match.group("content")))

        index += 1

    return index


def parse_markdown_to_tree_start(markdown_lines):
    tree = defaultdict_of_defaultdict()
    parse_markdown_to_tree(tree, markdown_lines, 0, 0, 0)

    return tree


def prune_empty(dictionary):
    # Recurse first and then check for emptiness in both children
    # and objects
    empty_child_keys = []

    for k in dictionary.get("children", {}):
        prune_empty(dictionary["children"][k])
        if (
            not dictionary["children"][k]["objects"]
            and not dictionary["children"][k]["children"]
        ):
            empty_child_keys.append(k)

    for k in empty_child_keys:
        del dictionary["children"][k]

    return dictionary


def make_markdown(structure, level=1, file=None):
    for object in structure["objects"]:
        print(
            f" - [[{object['fullpath']}|{object['filename_link_text']}]]:",
            file=file or sys.stdout,
        )

    for child in structure["children"]:
        print("#" * level, child, file=file or sys.stdout)
        make_markdown(structure["children"][child], level=level + 1, file=file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--papers-directory",
        default=".",
        help="The directory containing all the papers",
    )
    parser.add_argument(
        "--exclude", nargs="*", default=["journal", ".git"], help="What to exclude"
    )
    parser.add_argument("index", help="Index filename to update")
    args = parser.parse_args()

    fs_structure = prune_empty(
        walk_fs_to_tree(args.papers_directory, set(args.exclude))
    )
    with open(args.index, "r") as f:
        md_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

    print(json.dumps(md_structure, indent=2))

    contents = io.StringIO()
    make_markdown(md_structure, level=1, file=contents)

    with open(args.index, "w") as f:
        f.write(contents.getvalue())


if __name__ == "__main__":
    main()
