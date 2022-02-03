import argparse
import os
import subprocess
import fnmatch


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
        "--suffix", type=str, help="File suffix to bulk-add", default="md"
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
            f"**/*.{args.suffix}"
            if args.papers == "."
            else f"{args.papers}/**/*.{args.suffix}",
        )
    )

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
