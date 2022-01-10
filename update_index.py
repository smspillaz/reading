import argparse
import io
import itertools
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
        # No hidden files
        if any([p.startswith(".") for p in dirpath.split(os.path.sep)]):
            continue

        # No files in the exclude list
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

    # First link is a link to the fullpath
    first_link, other_links = link_matches[0], link_matches[1:]
    metadata["fullpath"] = first_link.group("link")
    metadata["filename"] = os.path.basename(metadata["fullpath"])
    metadata["filename_link_text"] = first_link.group("desc")
    metadata["content"] = bullet_content[first_link.end():].lstrip(": ")

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


def walk_structure(structure):
    yield from structure["objects"]

    for key in structure.get("children", {}):
        yield from walk_structure(structure["children"][key])


def path_to_key(path):
    # Don't want the last "children" and the second last "children"
    # becomes "objects"
    key = list(
        itertools.chain.from_iterable(
            zip(itertools.repeat("children"), path.split(os.path.sep))
        )
    )
    obj = key.pop(-1)

    assert key[-1] == "children"
    key[-1] = "objects"

    return (key, obj)


def get_by_filename(structure, obj, *args, **kwargs):
    return list(filter(lambda x: x["filename"] == obj, structure))[0]


def append_by_filename(structure, obj, substructure, *args, **kwargs):
    if obj not in structure:
        structure[obj] = []

    structure[obj].append(substructure)


def del_by_filename(structure, obj, *args, **kwargs):
    matching_indexes = [idx for idx, s in enumerate(structure) if s["filename"] == obj]

    assert len(matching_indexes) == 1
    structure.pop(matching_indexes[0])


def recursive_do(structure, key, func, *args, **kwargs):
    node = structure
    path, obj = key
    for part in path:
        node = node[part]

    return func(node, obj, *args, **kwargs)


def report_paths_to_update(paths_to_update):
    for src_path, dst_path in paths_to_update:
        print(f"Moving {src_path} -> {dst_path}")


def reconcile_moves(structure_src, structure_to_update):
    src_filename_to_fullpath = {
        obj["filename"]: obj["fullpath"] for obj in walk_structure(structure_src)
    }
    to_update_filename_to_fullpath = {
        obj["filename"]: obj["fullpath"] for obj in walk_structure(structure_to_update)
    }

    # Detect moves as those where we have a key in both
    # but in a different location - the src_filename_to_fullpath
    # is the source of truth in this case
    paths_to_update = [
        (to_update_filename_to_fullpath[filename], src_filename_to_fullpath[filename])
        for filename in to_update_filename_to_fullpath
        if filename in src_filename_to_fullpath
        and to_update_filename_to_fullpath[filename]
        != src_filename_to_fullpath[filename]
    ]

    report_paths_to_update(paths_to_update)

    keys_to_update = [
        (path_to_key(src), path_to_key(dst)) for src, dst in paths_to_update
    ]
    reassigns = [
        # We're reassigning to "objects", so pop last from the key
        (
            (dst_key[0][:-1], dst_key[0][-1]),
            recursive_do(structure_to_update, src_key, get_by_filename),
        )
        for src_key, dst_key in keys_to_update
    ]
    # Update structures in reassigns to account for new path
    reassigns = [
        (key, {**obj, "fullpath": src_filename_to_fullpath[obj["filename"]]})
        for key, obj in reassigns
    ]
    deletes = [src_key for src_key, dst_key in keys_to_update]

    for dst_key, substructure in reassigns:
        recursive_do(structure_to_update, dst_key, append_by_filename, substructure)

    # Now we delete from the old structure
    for src_key in deletes:
        recursive_do(structure_to_update, src_key, del_by_filename)


def report_adds(paths):
    for path in paths:
        print(f"Add {path}")


def reconcile_adds(structure_src, structure_to_update):
    src_filename_to_fullpath = {
        obj["filename"]: obj["fullpath"] for obj in walk_structure(structure_src)
    }
    to_update_filenames = {
        obj["filename"] for obj in walk_structure(structure_to_update)
    }

    # Anything in structure_src not in structure_to_update will
    # need to be added
    paths_to_add = [
        src_filename_to_fullpath[filename]
        for filename in src_filename_to_fullpath
        if filename not in to_update_filenames
    ]

    report_adds(paths_to_add)

    keys_to_add = [path_to_key(path) for path in paths_to_add]
    assignments_to_make = [
        (
            (dst_key[0][:-1], dst_key[0][-1]),
            recursive_do(structure_src, dst_key, get_by_filename),
        )
        for dst_key in keys_to_add
    ]

    for dst_key, substructure in assignments_to_make:
        recursive_do(structure_to_update, dst_key, append_by_filename, substructure)


def reconcile_structures(structure_src, structure_to_update):
    reconcile_moves(structure_src, structure_to_update)
    reconcile_adds(structure_src, structure_to_update)


def make_markdown(structure, level=1, file=None):
    for object in structure["objects"]:
        print(
            f" - [[{object['fullpath']}|{object['filename_link_text']}]]: {object['content']}",
            file=file or sys.stdout,
        )

    for child in structure["children"]:
        print("#" * level, child, file=file or sys.stdout)
        make_markdown(structure["children"][child], level=level + 1, file=file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--papers-directory",
        default="pdfs",
        help="The directory containing all the papers",
    )
    parser.add_argument(
        "--exclude", nargs="*", default=["journal", ".git"], help="What to exclude"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write the index file, just show what would happen in json",
    )
    parser.add_argument(
        "--json-dump",
        action="store_true",
        help="Show the resulting markdown structure in json",
    )
    parser.add_argument("index", help="Index filename to update")
    args = parser.parse_args()

    fs_structure = prune_empty(
        walk_fs_to_tree(args.papers_directory, set(args.exclude))
    )
    with open(args.index, "r") as f:
        md_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

    # After this, md_structure is the most up to date
    reconcile_structures(fs_structure, md_structure)
    prune_empty(md_structure)

    if args.json_dump:
        print(json.dumps(md_structure, indent=2))

    contents = io.StringIO()
    make_markdown(md_structure, level=1, file=contents)

    if not args.dry_run:
        with open(args.index, "w") as f:
            f.write(contents.getvalue())


if __name__ == "__main__":
    main()
