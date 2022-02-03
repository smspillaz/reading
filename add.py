import argparse
import os
import subprocess
import re

_RE_PARSE_LINK = re.compile(r"\[\[(?P<link>[\w_\.\/\-]+)\]\]")


def run(args, dry_run=False, **kwargs):
    print(" ".join(args))

    if not dry_run:
        return subprocess.run(args, **kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", required=True)
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't run, just print commands"
    )
    parser.add_argument("filename")
    args = parser.parse_args()

    img_list = os.listdir("img")

    run(["git", "add", args.filename], dry_run=args.dry_run)

    with open(args.filename) as f:
        contents = f.read()
        for match in _RE_PARSE_LINK.finditer(contents):
            link = match.group("link")
            if link is not None:
                print("link:", link)

                if link.startswith("pdf/"):
                    print("skipping:", link)

                if link in img_list:
                    run(["git", "add", "img/" + link], dry_run=args.dry_run)
                    print("Added img", link)
                elif "/" in link:
                    proc = run(["git", "add", link], dry_run=args.dry_run)
                    if proc and proc.returncode != 0:
                        print("Failed to add", link)

                else:
                    print("Ignoring", link)

    run(
        ["git", "commit", "-m", "{}: Update {}".format(args.section, args.filename)],
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
