import argparse
import os
import io
import subprocess

from copy import deepcopy

from update_index import (
    prune_empty,
    parse_markdown_to_tree_start,
    recursive_do,
    update_link,
    walk_structure,
    path_to_key,
    make_markdown,
)


def update_filename(
    structure, obj, dst_path, pdfs_directory, papers_directory, dry_run=False
):
    substructure = list(filter(lambda x: x["filename"] == obj, structure))[0]

    src_basename_no_ext = os.path.splitext(os.path.basename(substructure["fullpath"]))[
        0
    ]
    dst_basename_no_ext = os.path.splitext(os.path.basename(dst_path))[0]

    # 1. Determine paths first
    existing_links_and_indices = list(
        filter(
            lambda t: os.path.basename(t[1]["fullpath"]) == src_basename_no_ext + ".md",
            enumerate(substructure["links"]),
        )
    )

    existing_link_index = existing_links_and_indices[0][0]
    existing_link = deepcopy(existing_links_and_indices[0][1])

    src_paper_path = os.path.join(
        papers_directory,
        os.path.relpath(
            os.path.splitext(substructure["linkpath"])[0] + ".md", pdfs_directory
        ),
    )
    dst_paper_path = os.path.join(
        papers_directory,
        os.path.relpath(os.path.splitext(dst_path)[0] + ".md", pdfs_directory),
    )

    # 2. Now make adjustments

    # Adjust link text if it is the same as the src filename
    if substructure["filename_link_text"] == src_basename_no_ext:
        substructure["filename_link_text"] = dst_basename_no_ext

    # Redirect the pdf link
    substructure["linkpath"] = dst_path
    substructure["fullpath"] = os.path.relpath(dst_path, pdfs_directory)
    substructure["filename"] = os.path.basename(dst_path)
    substructure["links"][existing_link_index]["fullpath"] = dst_paper_path
    substructure["content"] = update_link(
        substructure["content"],
        existing_link,
        substructure["links"][existing_link_index],
    )

    print(f"Move {src_paper_path} to {dst_paper_path}")
    if not dry_run:
        subprocess.run(["git", "mv", src_paper_path, dst_paper_path])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("dst")
    parser.add_argument("--index", type=str, default="index.md")
    parser.add_argument("--papers-directory", type=str, default="papers")
    parser.add_argument("--pdfs-directory", type=str, default="pdfs")
    parser.add_argument("--disable-index-check", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write anything, just say what would happen",
    )
    args = parser.parse_args()

    # Check git status first, we shouldn't make any changes to the index unless
    # we're all clear
    if not args.disable_index_check:
        git_status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            text=True,
            capture_output=True,
        ).stdout.splitlines(keepends=False)

        if any(
            [
                line.startswith(" M") or line.startswith("R ") or line.startswith("A")
                for line in git_status
            ]
        ):
            raise RuntimeError(
                "Only run this command with a clean index, commit or stash changes first"
            )

    with open(args.index, "r") as f:
        md_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

    key = [
        path_to_key(obj["fullpath"])
        for obj in walk_structure(md_structure)
        if obj["fullpath"] in args.src
    ][0]

    recursive_do(
        md_structure,
        key,
        update_filename,
        args.dst,
        args.pdfs_directory,
        args.papers_directory,
        dry_run=args.dry_run,
    )

    contents = io.StringIO()
    make_markdown(md_structure, level=1, file=contents)

    if not args.dry_run:
        print(f"Move file {args.src} to {args.dst}")
        if not args.dry_run:
            os.rename(args.src, args.dst)

        with open(args.index, "w") as f:
            f.write(contents.getvalue())

        subprocess.run(["git", "add", args.index])

        src_fullpath = os.path.relpath(args.src, args.pdfs_directory)
        dst_fullpath = os.path.relpath(args.dst, args.pdfs_directory)

        subprocess.run(
            ["git", "commit", "-m", f"papers: Move {src_fullpath} to {dst_fullpath}"]
        )


if __name__ == "__main__":
    main()
