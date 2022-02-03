import argparse
import fnmatch
import io
import itertools
import json
import os
import sys
import subprocess
import re
from collections import defaultdict

from update_note_frontmatters import (
    parse_frontmatter,
    format_frontmatter,
    rewrite_frontmatter_section,
)

_RE_HEADING = re.compile(r"^(?P<hashes>#+)\s+(?P<content>.+)$")
_RE_LINK = re.compile(r"\[\[(?P<text>.+?)\]\]")
_RE_LINK_INTERNAL = re.compile(r"(?P<link>[^\|]+)\|?(?P<desc>[^\]]*)")
_RE_BULLET = re.compile(r"\s-\s(?P<content>.+)$")
_RE_KEY = re.compile(r"\(cite:\s(?P<key>[^\s]+)?\)")


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
                "linkpath": os.path.relpath(
                    os.path.join(dirpath, filename), os.path.dirname(abs_root)
                ),
                "filename_link_text": os.path.splitext(filename)[0],
                "content": "",
            }
            for filename in filenames
            if os.path.splitext(filename)[1] in [".ps", ".pdf"]
        ]

    return tree


def process_link_matches(link_matches):
    for match in link_matches:
        yield _RE_LINK_INTERNAL.match(match.group("text"))


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def delete_ranges(content, ranges_to_delete):
    if not ranges_to_delete:
        return content

    return "".join(
        [content[: ranges_to_delete[0][0]]]
        + [content[e1:b2] for (b1, e1), (b2, e2) in pairwise(ranges_to_delete)]
        + [content[ranges_to_delete[-1][-1] :]]
    )


def parse_bullet(bullet_content, path_stack):
    metadata = {}
    link_matches = list(_RE_LINK.finditer(bullet_content))
    processed_link_matches = list(process_link_matches(link_matches))
    key_matches = list(_RE_KEY.finditer(bullet_content))

    assert len(link_matches) > 0
    assert len(key_matches) <= 1

    ranges_to_delete = [link_matches[0].span(), *[m.span() for m in key_matches]]

    keep_content = delete_ranges(bullet_content, ranges_to_delete).lstrip(": ")

    # First link is a link to the fullpath
    first_link, other_links = processed_link_matches[0], processed_link_matches[1:]
    metadata["linkpath"] = first_link.group("link")
    metadata["fullpath"] = os.path.sep.join(
        path_stack + [os.path.basename(metadata["linkpath"])]
    )
    metadata["filename"] = os.path.basename(metadata["fullpath"])
    metadata["filename_link_text"] = first_link.group("desc")
    # Note, link_matches[0] is different from first_link, since it contains
    # the position of the link in the original text
    metadata["content"] = keep_content
    metadata["links"] = [
        {
            "fullpath": l.group("link"),
            "filename_link_text": l.group("desc") or l.group("link"),
        }
        for l in other_links
    ]
    metadata["keys"] = [{"key": l.group("key")} for l in key_matches]

    return metadata


def parse_markdown_to_tree(
    tree, markdown_lines, index, heading_level, depth, path_stack
):
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
                path_stack + [heading_content],
            )
            continue

        bullet_match = _RE_BULLET.match(markdown_lines[index])

        if bullet_match is not None:
            if "objects" not in tree:
                tree["objects"] = []
            tree["objects"].append(
                parse_bullet(bullet_match.group("content"), path_stack)
            )

        index += 1

    return index


def parse_markdown_to_tree_start(markdown_lines):
    tree = defaultdict_of_defaultdict()
    parse_markdown_to_tree(tree, markdown_lines, 0, 0, 0, [])

    return tree


def prune_empty(dictionary):
    # Recurse first and then check for emptiness in both children
    # and objects
    empty_child_keys = []

    for k in dictionary.get("children", {}):
        prune_empty(dictionary["children"][k])
        if (
            # Checks both that objects is empty or None. We don't want
            # to do an access here as that will trigger the defaultdict
            # to create a dict entry for "objects"
            not dictionary["children"][k].get("objects", None)
            and not dictionary["children"][k]["children"]
        ):
            empty_child_keys.append(k)

    for k in empty_child_keys:
        del dictionary["children"][k]

    return dictionary


def walk_structure(structure):
    yield from structure.get("objects", [])

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


def matches_filter(filename, match_filter):
    if match_filter is not None:
        return match_filter.match(filename) is not None

    return True


def report_paths_to_update(paths_to_update):
    for src_path, dst_path in paths_to_update:
        print(f"Moving {src_path} -> {dst_path}")


def reconcile_moves(structure_src, structure_to_update):
    src_filename_to_fullpath = {
        obj["filename"]: obj["fullpath"] for obj in walk_structure(structure_src)
    }
    src_filename_to_linkpath = {
        obj["filename"]: obj["linkpath"] for obj in walk_structure(structure_src)
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
        (
            key,
            {
                **obj,
                "fullpath": src_filename_to_fullpath[obj["filename"]],
                "linkpath": src_filename_to_linkpath[obj["filename"]],
            },
        )
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


def report_unmatched_notes(unmatched_notes):
    print("\n".join([f"Unmatched note: {note}" for note in unmatched_notes]))


def format_link(link):
    return f"[[{link['fullpath']}|{link['filename_link_text']}]]"


def update_link(content, existing_link, new_link):
    link_matches = list(_RE_LINK_INTERNAL.finditer(content))

    for link in link_matches:
        if link.group("link") == existing_link["fullpath"]:
            content = (
                content[: link.start()] + format_link(new_link) + content[link.end() :]
            )
            return content


def add_link_if_not_exists(structure, obj, link_to_add, *args, **kwargs):
    substructure = list(filter(lambda x: x["filename"] == obj, structure))[0]

    if not "links" in substructure:
        substructure["links"] = []

    substructure["links_to_add"] = []
    substructure["links_to_update"] = []

    if not "content" in substructure:
        substructure["content"] = ""

    link_to_add_basename = os.path.basename(link_to_add["fullpath"])

    existing_links = list(
        filter(
            lambda link: os.path.basename(link["fullpath"]) == link_to_add_basename,
            substructure["links"],
        )
    )

    if not existing_links:
        print(f"Add link {link_to_add['fullpath']} to {substructure['fullpath']}")
        substructure["content"] = (
            substructure["content"].rstrip(".") + f". {format_link(link_to_add)}"
        )
    elif existing_links[0]["fullpath"] != link_to_add["fullpath"]:
        print(
            f"Update link {existing_links[0]['fullpath']} to {link_to_add['fullpath']}"
        )
        substructure["content"] = update_link(
            substructure["content"], existing_links[0], link_to_add
        )


def notes_paths(notes_directory):
    return {
        k: v
        for k, v in itertools.chain.from_iterable(
            [
                [
                    (os.path.splitext(filename)[0], os.path.join(root, filename))
                    for filename in fnmatch.filter(filenames, "*.md")
                ]
                for root, dirnames, filenames in os.walk(notes_directory)
            ]
        )
    }


def report_moves(notes_to_move):
    print(
        "\n".join(
            [f"Move {src_path} to {dst_path}" for src_path, dst_path in notes_to_move]
        )
    )


def report_creates(notes_to_create):
    print("\n".join([f"Create {path}" for path in notes_to_create]))


def move_vcs_file(src_path, dst_path):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    try:
        subprocess.check_call(["git", "mv", src_path, dst_path])
    except subprocess.CalledProcessError:
        os.rename(src_path, dst_path)


def sync_notes_locations(structure, notes_directory, dry_run=True):
    objects_to_fullpath = {
        os.path.splitext(obj["filename"])[0]: obj["fullpath"]
        for obj in walk_structure(structure)
    }
    notes = notes_paths(notes_directory)

    matched_notes = [
        (
            os.path.relpath(notes[key], notes_directory),
            os.path.splitext(objects_to_fullpath[key])[0] + ".md",
        )
        for key in notes
        if key in objects_to_fullpath
    ]
    notes_to_move = [
        (
            os.path.join(notes_directory, src_path),
            os.path.join(notes_directory, dst_path),
        )
        for src_path, dst_path in matched_notes
        if src_path != dst_path
    ]
    notes_to_create = [
        os.path.join(
            notes_directory, os.path.splitext(objects_to_fullpath[key])[0] + ".md"
        )
        for key in objects_to_fullpath
        if key not in notes
    ]

    report_moves(notes_to_move)
    report_creates(notes_to_create)

    if not dry_run:
        for src_path, dst_path in notes_to_move:
            move_vcs_file(src_path, dst_path)

        for path in notes_to_create:
            os.makedirs(os.path.dirname(path), exist_ok=True)

            assert not os.path.exists(path)
            with open(path, "w") as f:
                f.write("")


def sync_note_metadata(structure, obj, note_path, *args, **kwargs):
    dry_run = kwargs.get("dry_run", True)

    substructure = list(filter(lambda x: x["filename"] == obj, structure))[0]
    note_frontmatter = parse_frontmatter(note_path)
    changes_made = False

    if "title" not in note_frontmatter:
        if (
            substructure["filename_link_text"]
            != os.path.splitext(substructure["filename"])[0]
        ):
            # If there's no title, then pull it from the
            # the index (as long as its not just the same
            # as the filename basename, eg, it was edited by
            # the user).
            print(
                f"Sync title {substructure['filename_link_text']} to note {note_path} frontmatter"
            )
            note_frontmatter["title"] = substructure["filename_link_text"]
            changes_made = True

    else:
        # Pull the title from the note frontmatter and use it in the
        # index => the note frontmatter is the source of truth in this case.
        if substructure["filename_link_text"] != note_frontmatter["title"]:
            print(
                f"Pull title {note_frontmatter['title']} from note {note_path} frontmatter to index"
            )
        substructure["filename_link_text"] = note_frontmatter["title"]

    if "cite_key" not in note_frontmatter:
        if substructure.get("keys", []):
            # If there's no cite_key, then pull it from the
            # the index.
            print(
                f"Sync title {substructure['keys'][0]['key']} to note {note_path} frontmatter"
            )
            note_frontmatter["cite_key"] = substructure["keys"][0]["key"]
            changes_made = True

    else:
        # Pull the title from the note frontmatter and use it in the
        # index => the note frontmatter is the source of truth in this case.
        if (
            not substructure["keys"]
            or substructure["keys"][0]["key"] != note_frontmatter["cite_key"]
        ):
            print(
                f"Pull key {note_frontmatter['cite_key']} from note {note_path} frontmatter to index"
            )

        substructure["keys"] = [{"key": note_frontmatter["cite_key"]}]

    if changes_made and not dry_run:
        rewrite_frontmatter_section(note_path, format_frontmatter(note_frontmatter))


def reconcile_notes(structure_to_update, notes_directory, dry_run=True):
    objects_to_fullpath = {
        os.path.splitext(obj["filename"])[0]: obj["fullpath"]
        for obj in walk_structure(structure_to_update)
    }
    notes = notes_paths(notes_directory)

    matched_notes = [
        (notes[key], objects_to_fullpath[key])
        for key in notes
        if key in objects_to_fullpath
    ]
    unmatched_notes = [notes[key] for key in notes if key not in objects_to_fullpath]
    report_unmatched_notes(unmatched_notes)

    note_keys = [
        (note_path, path_to_key(object_path))
        for note_path, object_path in matched_notes
    ]

    for link_path, dst_key in note_keys:
        recursive_do(
            structure_to_update,
            dst_key,
            add_link_if_not_exists,
            {"fullpath": link_path, "filename_link_text": "Notes"},
        )
        recursive_do(
            structure_to_update, dst_key, sync_note_metadata, link_path, dry_run=dry_run
        )


def make_markdown(structure, level=1, file=None):
    for object in structure.get("objects", []):
        cite_key = "" if not object.get("keys", []) else f"(cite: {object['keys'][0]['key']}) "
        print(
            f" - [[{object['linkpath']}|{object['filename_link_text']}]]: {cite_key}{object['content']}",
            file=file or sys.stdout,
        )

    for child in structure["children"]:
        print("#" * level, child, file=file or sys.stdout)
        make_markdown(structure["children"][child], level=level + 1, file=file)


def postprocess_structure(structure):
    structure["objects"] = sorted(
        structure.get("objects", []), key=lambda obj: obj["filename_link_text"]
    )
    structure["children"] = {
        k: structure["children"][k] for k in sorted(list(structure["children"].keys()))
    }

    for substructure in structure["children"].values():
        postprocess_structure(substructure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--papers-directory",
        default="pdfs",
        help="The directory containing all the papers",
    )
    parser.add_argument(
        "--notes-directory",
        default="papers",
        help="Notes directory per-paper. If a note here has the same name as a paper the two will be linked",
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

    # Its important that we sync the note locations before we call
    # reconcile_notes, that way reconcile_notes will out links to the correct
    # directories as it walks the tree again
    #
    # Note that what --dry-run says will happen in this case will be a bit
    # wrong since sync_notes_locations won't move anything and therefore
    # the displayed link names will be wrong. That's difficult to fix
    # its left broken for now.
    sync_notes_locations(md_structure, args.notes_directory, args.dry_run)
    reconcile_notes(md_structure, args.notes_directory, args.dry_run)

    # Postprocessing (sorting, etc)
    postprocess_structure(md_structure)

    if args.json_dump:
        print(json.dumps(md_structure, indent=2))

    contents = io.StringIO()
    make_markdown(md_structure, level=1, file=contents)

    if not args.dry_run:
        with open(args.index, "w") as f:
            f.write(contents.getvalue())


if __name__ == "__main__":
    main()
