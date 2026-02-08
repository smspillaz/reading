import argparse
import fnmatch
import json
from json.decoder import JSONDecodeError
import os
import re
import unicodedata
import urllib.request
import urllib.parse
import time


_SYNC_VERSION = 4
_RE_NUMBER_ONLY = re.compile("[0-9]+")

PROVIDERS = ["dblp", "openalex", "semanticscholar"]


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def normalize_title(title):
    return re.sub(r"\s+", "", re.sub("[^\w\s]", "", title)).lower()


def title_distance(a, b):
    return levenshtein(normalize_title(a), normalize_title(b))


def choose_best_candidate(title, candidates):
    if not candidates:
        return None

    distances = [title_distance(title, c["title"]) for c in candidates]
    best_index = min(range(len(candidates)), key=lambda i: distances[i])

    if distances[best_index] > max(10, len(title) // 3):
        return None

    return candidates[best_index]


def filter_author_text(text):
    return " ".join(
        [t for t in re.split(r"\s+", text) if not _RE_NUMBER_ONLY.match(t)]
    )


# ---------------------------------------------------------------------
# Frontmatter handling
# ---------------------------------------------------------------------

def parse_frontmatter(filename):
    frontmatter = {}
    parsing = False

    with open(filename, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    for line in lines:
        if line == "---":
            if parsing:
                return frontmatter
            parsing = True
            continue

        if parsing and ":" in line:
            key, value = line.split(":", maxsplit=1)
            value = value.strip()
            try:
                value = json.loads(value)
            except:
                pass
            frontmatter[key] = value

    return frontmatter


def format_item(value):
    return json.dumps(value)


def format_frontmatter(frontmatter):
    return "\n".join(
        [f"{k}: {format_item(v)}" for k, v in frontmatter.items()]
    )


def get_start_read_from(lines):
    frontmatter_count = 0
    for i, line in enumerate(lines):
        if line == "---":
            frontmatter_count += 1
        if frontmatter_count == 2:
            return i + 1
    return 0


def rewrite_frontmatter_section(filename, frontmatter):
    with open(filename, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    start_from = get_start_read_from(lines)
    contents = "\n".join(lines[start_from:])

    total_contents = "\n".join(["---", frontmatter, "---", contents])

    with open(filename, "w") as f:
        f.write(total_contents)


# ---------------------------------------------------------------------
# Metadata Providers
# ---------------------------------------------------------------------

def query_dblp(title, delay=None):
    encoded = urllib.parse.quote(title)
    url = f"https://dblp.org/search/publ/api?query={encoded}&format=json&h=20"

    if delay:
        time.sleep(delay)

    try:
        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read())
    except Exception:
        return None

    hits = data.get("result", {}).get("hits", {}).get("hit", [])
    results = []

    for h in hits:
        info = h["info"]

        authors_meta = info.get("authors", {}).get("author", [])
        if isinstance(authors_meta, dict):
            authors_meta = [authors_meta]

        authors = [filter_author_text(a["text"]) for a in authors_meta]

        results.append({
            "title": info.get("title"),
            "authors": authors,
            "year": info.get("year"),
            "venue": info.get("venue"),
            "key": info.get("key"),
            "url": info.get("url"),
            "_source": "dblp",
        })

    return choose_best_candidate(title, results)


def query_openalex(title, delay=None):
    encoded = urllib.parse.quote(title)
    url = f"https://api.openalex.org/works?search={encoded}&per-page=10"

    if delay:
        time.sleep(delay)

    try:
        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read())
    except Exception:
        return None

    results = []

    for work in data.get("results", []):
        authors = [
            a["author"]["display_name"]
            for a in work.get("authorships", [])
            if "author" in a
        ]

        results.append({
            "title": work.get("display_name"),
            "authors": authors,
            "year": str(work.get("publication_year")),
            "venue": (work.get("host_venue") or {}).get("display_name"),
            "doi": work.get("doi"),
            "url": work.get("id"),
            "_source": "openalex",
        })

    return choose_best_candidate(title, results)


def query_semanticscholar(title, delay=None):
    encoded = urllib.parse.quote(title)
    url = (
        "https://api.semanticscholar.org/graph/v1/paper/search"
        f"?query={encoded}"
        "&limit=10"
        "&fields=title,authors,year,venue,doi,abstract,url"
    )

    if delay:
        time.sleep(delay)

    try:
        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read())
    except Exception:
        return None

    results = []

    for paper in data.get("data", []):
        authors = [a["name"] for a in paper.get("authors", [])]

        results.append({
            "title": paper.get("title"),
            "authors": authors,
            "year": str(paper.get("year")),
            "venue": paper.get("venue"),
            "doi": paper.get("doi"),
            "abstract": paper.get("abstract"),
            "url": paper.get("url"),
            "_source": "semanticscholar",
        })

    return choose_best_candidate(title, results)


def retrieve_metadata(title, delay=None):
    for provider in PROVIDERS:
        if provider == "dblp":
            result = query_dblp(title, delay)
        elif provider == "openalex":
            result = query_openalex(title, delay)
        else:
            result = query_semanticscholar(title, delay)

        if result:
            print(f"Matched via {provider}")
            return result

    return None


# ---------------------------------------------------------------------
# Frontmatter update logic
# ---------------------------------------------------------------------

def make_cite_key(frontmatter_content):
    cite_key = frontmatter_content.get("key")
    if not cite_key:
        return None

    if "corr/" in cite_key:
        cite_key = "/".join(
            [
                cite_key,
                unicodedata.normalize(
                    "NFD",
                    frontmatter_content["authors"][0].split()[-1],
                ).encode("ascii", "ignore").decode(),
                frontmatter_content["year"],
            ]
        )

    return cite_key


def get_updated_frontmatter(filename, no_download=True, delay=None):
    frontmatter = parse_frontmatter(filename)

    if "title" not in frontmatter:
        return frontmatter, False

    if frontmatter.get("sync_version", 0) >= _SYNC_VERSION:
        return frontmatter, False

    print(f"Process {filename}")

    if no_download:
        return frontmatter, False

    retrieved = retrieve_metadata(frontmatter["title"], delay)
    if not retrieved:
        return frontmatter, False

    # conservative merge
    for k, v in retrieved.items():
        if v and k not in frontmatter:
            frontmatter[k] = v

    if retrieved.get("_source") == "dblp":
        cite_key = make_cite_key(retrieved)
        if cite_key:
            frontmatter["cite_key"] = cite_key

    frontmatter["sync_version"] = _SYNC_VERSION

    return frontmatter, True


def update_frontmatter(filename, dry_run=True, no_download=True, delay=None):
    updated_frontmatter, updated = get_updated_frontmatter(
        filename, no_download=no_download, delay=delay
    )

    if not updated_frontmatter:
        return

    formatted_frontmatter = format_frontmatter(updated_frontmatter)

    if dry_run:
        print(f"Frontmatter for {filename}")
        print(formatted_frontmatter)
    else:
        if updated:
            print(f"Rewrote frontmatter for {filename}")
        rewrite_frontmatter_section(filename, formatted_frontmatter)


def walk_and_process_notes(notes_directory, dry_run=False, no_download=False, delay=None):
    for root, _, filenames in os.walk(notes_directory):
        for filename in fnmatch.filter(filenames, "*.md"):
            update_frontmatter(
                os.path.join(root, filename),
                dry_run=dry_run,
                no_download=no_download,
                delay=delay,
            )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notes_directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--delay", type=int)

    args = parser.parse_args()

    walk_and_process_notes(
        args.notes_directory,
        dry_run=args.dry_run,
        no_download=args.no_download,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()