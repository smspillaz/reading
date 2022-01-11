import argparse
import os
import subprocess
import re

_RE_PARSE_LINK = re.compile(r"\[\[(?P<link>[\w_\.\/\-]+)\]\]")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", required=True)
    parser.add_argument("filename")
    args = parser.parse_args()

    img_list = os.listdir("img")

    subprocess.run(["git", "add", args.filename])

    with open(args.filename) as f:
        contents = f.read()
        for match in _RE_PARSE_LINK.finditer(contents):
            link = match.group("link")
            if link is not None:
                print("link:", link)

                if link.startswith("pdf/"):
                    print("skipping:", link)

                if link in img_list:
                    subprocess.call(["git", "add", "img/" + link])
                    print("Added img", link)
                elif "/" in link:
                    ret = subprocess.run(["git", "add", link]).retcode
                    if ret != 0:
                        print("Failed to add", link)

                else:
                    print("Ignoring", link)

    subprocess.run(
        ["git", "commit", "-m", "'{}: Add {}".format(args.section, args.filename)]
    )


if __name__ == "__main__":
    main()
