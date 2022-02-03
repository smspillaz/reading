import argparse
import itertools
import subprocess
import sys
import re

from filter_diff import yield_filtered_hunks, yield_hunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=str, help="Name of index file to filter")
    parser.add_argument(
        "target", type=str, help="Where to put the filtered index entries"
    )
    args = parser.parse_args()

    added_hunks = list(
        filter(
            lambda x: x.startswith(" - "),
            map(
                lambda x: x[1:],
                itertools.chain.from_iterable(
                    yield_filtered_hunks(
                        yield_hunks(
                            subprocess.run(
                                ["git", "diff", args.index],
                                capture_output=True,
                                text=True,
                            ).stdout.splitlines(keepends=False)
                        ),
                        re_obj=None,
                        keep_adds=True,
                        keep_context=False,
                        keep_removes=False,
                    ),
                ),
            ),
        )
    )
    with open(args.target, "w") as f:
        f.write("\n".join(added_hunks))


if __name__ == "__main__":
    main()
