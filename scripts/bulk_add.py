import argparse
import os
import itertools
import subprocess
import fnmatch

from update_index import prune_empty, parse_markdown_to_tree_start, walk_structure


def get_notes_link(structure):
    return [
        l["fullpath"] for l in structure["links"] if l["filename_link_text"] == "Notes"
    ][0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "papers", type=str, help="Path to papers directory", default="papers"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Just print what would happen but don't do anything",
    )
    parser.add_argument("--scripts-dir", default="scripts", type=str)
    parser.add_argument(
        "--suffix", type=str, nargs="+", help="File suffix to bulk-add", default=["md"]
    )
    parser.add_argument("--stage-file", default="index.stage", type=str)
    args = parser.parse_args()

    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        text=True,
        capture_output=True,
    ).stdout.splitlines(keepends=False)
    update_files = set(
        list(
            itertools.chain.from_iterable(
                [
                    fnmatch.filter(
                        [
                            line[3:]
                            for line in status
                            if (line.startswith(" M") or line.startswith("??"))
                        ],
                        f"**/*.{suffix}"
                        if args.papers == "."
                        else f"{args.papers}/**/*.{suffix}",
                    )
                    for suffix in args.suffix
                ]
            )
        )
    )

    if os.path.exists(args.stage_file):
        with open(args.stage_file, "r") as f:
            stage_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))
            stage_filenames = set(
                [get_notes_link(obj) for obj in walk_structure(stage_structure)]
            )
            update_files |= stage_filenames

    print(
        "Creating commits for the following files:\n"
        + "\n".join(map(lambda x: f"- {x}", update_files))
    )

    for filename in update_files:
        add_args = (
            [
                "python",
                f"{args.scripts_dir}/add.py",
                "--section",
                filename.split(os.path.sep)[0],
                "--update-index",
            ]
            + (["--dry-run"] if args.dry_run else [])
            + [filename]
        )
        print(" ".join(add_args))
        subprocess.run(add_args)


if __name__ == "__main__":
    main()
