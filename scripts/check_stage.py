import argparse
from operator import index

from update_index import prune_empty, parse_markdown_to_tree_start, walk_structure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("index")
    parser.add_argument("stage")

    args = parser.parse_args()

    with open(args.index, "r") as f:
        index_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

    with open(args.stage, "r") as f:
        stage_structure = prune_empty(parse_markdown_to_tree_start(f.readlines()))

    index_filename_to_descriptions = {
        obj["filename"]: obj for obj in walk_structure(index_structure)
    }
    stage_filename_to_descriptions = {
        obj["filename"]: obj for obj in walk_structure(stage_structure)
    }

    for stage_filename in stage_filename_to_descriptions:
        if stage_filename not in index_filename_to_descriptions:
            print(f" - {stage_filename} not in {args.index}")
            continue

        if (
            index_filename_to_descriptions[stage_filename]["content"]
            != stage_filename_to_descriptions[stage_filename]["content"]
        ):
            print(f" - content differs on {stage_filename}")
            print(stage_filename_to_descriptions[stage_filename]["content"])


if __name__ == "__main__":
    main()
