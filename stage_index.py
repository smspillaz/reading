import subprocess


def main():
    if " M index.md" not in subprocess.run(
        ["git", "status", "--porcelain"], text=True, capture_output=True
    ).stdout.splitlines(keepends=False):
        print("Nothing to stage")
        return

    print("Staging index")
    subprocess.run(["python", "filter_index_adds.py", "index.md", "index.stage"])


if __name__ == "__main__":
    main()
