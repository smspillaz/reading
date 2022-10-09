import argparse
import bibtexparser
import itertools
import re

_RE_CITE = r"\\cite[a-z]?\{(?P<citation>.+?)\}"


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("output_file", type=str)
    parser.add_argument("--fields", type=str, nargs="+")
    parser.add_argument(
        "--filter-only-ref-inputs",
        nargs="*",
        type=str,
        help="Filter out stuff not referred to in these LaTeX files",
    )
    args = parser.parse_args()

    contents = "".join(
        itertools.chain.from_iterable(map(read_file, args.filter_only_ref_inputs))
    )

    citations = list(
        itertools.chain.from_iterable(
            [
                map(lambda s: s.strip(), m.group("citation").split(","))
                for m in re.finditer(_RE_CITE, contents)
            ]
        )
    )
    print(citations)

    import pdb

    pdb.set_trace()

    with open(args.input_file, "r") as f:
        db = bibtexparser.load(f)

    fields = args.fields + ["ENTRYTYPE", "ID"]

    db.comments = []
    db.entries = [
        {k: v for k, v in db_entry.items() if k in fields}
        for db_entry in db.entries
        if not citations or (db_entry["ID"] in citations)
    ]

    with open(args.output_file, "w") as f:
        bibtexparser.dump(db, f)


if __name__ == "__main__":
    main()
