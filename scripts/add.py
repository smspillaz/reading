import argparse
import os
import subprocess
import re

_RE_PARSE_LINK = re.compile(r"\[\[(?P<link>[\w_\.\/\-]+)\]\]")


def run(args, dry_run=False, **kwargs):
    print(" ".join(args))

    if not dry_run:
        return subprocess.run(args, **kwargs)


def update_index(filename, dry_run=False):
    basename = os.path.splitext(os.path.basename(filename))[0]
    run(
        [
            "python",
            "scripts/update_index.py",
            "index.md",
            "--filter-changes",
            basename,
            "--pull-descriptions",
            "index.stage",
        ],
        dry_run=dry_run,
    )
    add_index_proc = run(["git", "add", "index.md"], dry_run=dry_run)

    if add_index_proc is None or add_index_proc.returncode == 0:
        run(
            ["git", "commit", "-m", f"index: Update index for '{basename}'"],
            dry_run=dry_run,
        )


def add_linked_content(filename, dry_run=False):
    img_list = os.listdir("img")

    with open(filename) as f:
        contents = f.read()
        for match in _RE_PARSE_LINK.finditer(contents):
            link = match.group("link")
            if link is not None:
                print("link:", link)

                if link.startswith("pdf/"):
                    print("skipping:", link)

                if link in img_list:
                    run(["git", "add", "img/" + link], dry_run=dry_run)
                    print("Added img", link)
                elif "/" in link:
                    proc = run(["git", "add", link], dry_run=dry_run)
                    if proc and proc.returncode != 0:
                        print("Failed to add", link)

                else:
                    print("Ignoring", link)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", required=True)
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't run, just print commands"
    )
    parser.add_argument(
        "--update-index", action="store_true", help="Also update the index"
    )
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    for filename in args.filenames:
        run(["git", "add", filename], dry_run=args.dry_run)

        if os.path.splitext(filename)[1] == ".md":
            add_linked_content(filename, dry_run=args.dry_run)

        run(
            ["git", "commit", "-m", "{}: Update {}".format(args.section, filename)],
            dry_run=args.dry_run,
        )

        if args.update_index:
            if not os.path.exists("index.stage"):
                print("index.stage does not exist, cannot update an index")
            else:
                update_index(filename, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
