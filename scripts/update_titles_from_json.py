import argparse
import json
import io


from update_index import (
    parse_markdown_to_tree_start,
    prune_empty,
    walk_structure,
    recursive_do,
    path_to_key,
    postprocess_structure,
    make_markdown,
)
from update_note_frontmatters import retrieve_metadata, find_best_hit, levenshtein


def update_title(structure, obj, update_titles, **kwargs):
    substructure = list(filter(lambda x: x["filename"] == obj, structure))[0]
    update_to = update_titles.get(substructure["filename_link_text"], None)

    if update_to is not None:
        print(
            f"Update content {substructure['filename_link_text']} to {update_to['title']}"
        )
        substructure["filename_link_text"] = update_to["title"]


def reconcile_notes(structure_to_update, update_titles, no_download=True):
    keys = [path_to_key(obj["fullpath"]) for obj in walk_structure(structure_to_update)]

    for dst_key in keys:
        recursive_do(structure_to_update, dst_key, update_title, update_titles)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("index", help="Index filename to update")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write anything, just say what would happen",
    )
    parser.add_argument(
        "--update-titles", type=str, help="JSON file to update the titles from"
    )
    args = parser.parse_args()

    with open(args.update_titles, "r") as f:
        update_titles = json.load(f)

    with open(args.index, "r") as f:
        md_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

    reconcile_notes(md_structure, update_titles)

    contents = io.StringIO()
    make_markdown(md_structure, level=1, file=contents)

    # Postprocessing (sorting, etc)
    postprocess_structure(md_structure)

    if not args.dry_run:
        with open(args.index, "w") as f:
            f.write(contents.getvalue())


if __name__ == "__main__":
    main()
