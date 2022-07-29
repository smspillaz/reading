import argparse
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


def scrape_title_by_name(name, no_download=True):
    metadata = retrieve_metadata(name, no_download=no_download)

    if not metadata:
        return None

    best_hit = find_best_hit(name, metadata)

    if not best_hit:
        return None

    return best_hit["info"]["title"]


def scrape_and_update_title(structure, obj, *args, **kwargs):
    substructure = list(filter(lambda x: x["filename"] == obj, structure))[0]

    if substructure["filename_link_text"] in substructure["linkpath"]:
        search_term = substructure["filename_link_text"].replace("_", " ")
        possible_title = scrape_title_by_name(
            search_term, kwargs.get("no_download", True)
        )

        if not possible_title:
            return

        # A few sanity checks - we should expect a very large degree of overlap by
        # levenshtein distance
        distance = levenshtein(search_term, possible_title)
        normalized_distance = distance / len(search_term)

        if normalized_distance > 0.3:
            print(
                f"Skipping update of {substructure['filename_link_text']} to {possible_title} as the edit distance ({normalized_distance}) is too long"
            )
            return

        print(
            f"Update content {substructure['filename_link_text']} to {possible_title}"
        )
        substructure["filename_link_text"] = possible_title
        return


def reconcile_notes(structure_to_update, no_download=True):
    keys = [path_to_key(obj["fullpath"]) for obj in walk_structure(structure_to_update)]

    for dst_key in keys:
        recursive_do(
            structure_to_update,
            dst_key,
            scrape_and_update_title,
            no_download=no_download,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("index", help="Index filename to update")
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

    with open(args.index, "r") as f:
        md_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

    reconcile_notes(md_structure, no_download=args.no_download)

    contents = io.StringIO()
    make_markdown(md_structure, level=1, file=contents)

    # Postprocessing (sorting, etc)
    postprocess_structure(md_structure)

    if not args.dry_run:
        with open(args.index, "w") as f:
            f.write(contents.getvalue())


if __name__ == "__main__":
    main()
