import argparse
import fnmatch
import os

from update_note_frontmatters import parse_frontmatter, rewrite_frontmatter_section, format_frontmatter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notes_directory", help="The papers directory")
    parser.add_argument("--papers", nargs="+", help="Papers to add tag to")
    parser.add_argument("--tags", nargs="+", help="The tags to add")
    parser.add_argument("--dry-run", action="store_true", help="Just print what would happen, don't tag")
    args = parser.parse_args()

    tagged_ids = set([os.path.splitext(os.path.basename(path))[0] for path in args.papers])

    for root, dirname, filenames in os.walk(args.notes_directory):
        for filename in fnmatch.filter(filenames, "*.md"):
            filename_id = os.path.splitext(os.path.basename(filename))[0]

            if filename_id in tagged_ids:
                path = os.path.join(root, filename)
                frontmatter = parse_frontmatter(path)
                frontmatter["tags"] = list(set(frontmatter.get("tags", [])) | set(args.tags))
                formatted_frontmatter = format_frontmatter(frontmatter)

                print(f"Added tags for {path} -> {frontmatter['tags']}")

                if not args.dry_run:
                    rewrite_frontmatter_section(path, formatted_frontmatter)


if __name__ == "__main__":
    main()


