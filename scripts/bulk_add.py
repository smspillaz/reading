import argparse
import subprocess
import fnmatch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("papers", type=str, help="Path to papers directory")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Just print what would happen but don't do anything",
    )
    args = parser.parse_args()

    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        text=True,
        capture_output=True,
    ).stdout.splitlines(keepends=False)
    update_files = list(
        fnmatch.filter(
            [
                line[3:]
                for line in status
                if (line.startswith(" M") or line.startswith("??"))
            ],
            f"{args.papers}/**/*.md",
        )
    )

    print(
        "Creating commits for the following files:\n"
        + "\n".join(map(lambda x: f"- {x}", update_files))
    )

    for filename in update_files:
        add_args = (
            ["python", "scripts/add.py", "--section", "papers", "--update-index"]
            + (["--dry-run"] if args.dry_run else [])
            + [filename]
        )
        print(" ".join(add_args))
        subprocess.run(add_args)


if __name__ == "__main__":
    main()
