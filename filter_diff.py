import argparse
import itertools
import sys
import re

_RE_HUNK = re.compile("^@@.*")
_RE_LINE_ADDED = re.compile("^\+.*")
_RE_LINE_DEL = re.compile("^\-.*")
_RE_HEADING = re.compile("[\s\-\+]*#+")


def yield_hunks(lines):
    hunk = []
    collecting = False

    for line in lines:
        if _RE_HUNK.match(line):
            if collecting:
                yield hunk

            hunk = []
            collecting = True

        if collecting:
            hunk.append(line)

    if collecting and hunk:
        yield hunk


def filter_hunk(hunk, re_obj, keep_adds=True, keep_removes=True, keep_context=True):
    lines = []
    keep = False

    for line in hunk:
        # Only keep relevant lines that were added or removed
        added = _RE_LINE_ADDED.match(line)
        removed = _RE_LINE_DEL.match(line)
        if added or removed:
            if not re_obj or re_obj.match(line):
                keep = True
                if (added and keep_adds) or (removed and keep_removes):
                    lines.append(line)
            elif removed and keep_context:
                # If the line didn't match, keep the removed
                # line and convert it into a context line
                lines.append(f" {line[1:]}")

            if _RE_HEADING.match(line) and keep_context:
                # Keep any relevant headings from this hunk
                lines.append(line)
        elif keep_context:
            # Keep context and everything else
            lines.append(line)

    # Only return the lines if the hunk was relevant
    return lines if keep else None


def yield_filtered_hunks(
    hunks, re_obj, keep_adds=True, keep_removes=True, keep_context=True
):
    for hunk in hunks:
        matched_hunk = filter_hunk(
            hunk,
            re_obj,
            keep_adds=keep_adds,
            keep_removes=keep_removes,
            keep_context=keep_context,
        )

        if matched_hunk is not None:
            yield matched_hunk


def main():
    parser = argparse.ArgumentParser("Filter diffs for an expression")
    parser.add_argument(
        "filter_expr", help="Regular expression to filter a diff for", type=str
    )
    args = parser.parse_args()

    re_obj = re.compile(".*{}.*".format(args.filter_expr))

    # Print the first four lines
    for line in itertools.islice(sys.stdin, 4):
        print(line.rstrip())

    # The new lines are all hunks, so yield filtered hunks
    for hunk in yield_filtered_hunks(yield_hunks(sys.stdin), re_obj):
        for line in hunk:
            print(line.rstrip())


if __name__ == "__main__":
    main()
