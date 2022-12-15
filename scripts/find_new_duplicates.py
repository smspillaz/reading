import argparse
from collections import defaultdict
from datetime import datetime, timezone
import fnmatch
import itertools
import os
import stat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdfs", type=str, help="Path to pdfs")
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args()

    local_paths = list(
        itertools.chain.from_iterable(
            [
                [
                    os.path.relpath(os.path.join(root, fname), args.pdfs)
                    for fname in fnmatch.filter(fnames, "*.pdf")
                ]
                for root, dirnames, fnames in os.walk(args.pdfs)
            ]
        )
    )
    local_paths_with_mtimes = [
        (
            p,
            datetime.fromtimestamp(
                os.stat(os.path.join(args.pdfs, p))[stat.ST_MTIME], tz=timezone.utc
            ),
        )
        for p in local_paths
    ]

    objects_by_unique_key = defaultdict(list)
    for path, mtime in local_paths_with_mtimes:
        key = os.path.basename(path)
        objects_by_unique_key[key].append((path, mtime))

    objects_by_unique_key = {
        key: sorted(values, key=lambda v: v[1])
        for key, values in objects_by_unique_key.items()
    }

    duplicates = {
        values[0][0]: values[1:]
        for values in objects_by_unique_key.values()
        if len(values) > 1
    }

    for key, dupes in duplicates.items():
        print(f" - {key}")
        print("\n".join([f"   - {dupe} {mtime.isoformat()}" for dupe, mtime in dupes]))

        if args.delete:
            for dupe, mtime in dupes:
                os.remove(os.path.join(args.pdfs, dupe))


if __name__ == "__main__":
    main()
