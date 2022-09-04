import argparse

from duplicates import handle_duplicates
from find_new import find_new
from rename import rename_files
from settings import SETTINGS_FILEPATH, Settings


def main():
    parser = argparse.ArgumentParser(
        description="A script that helps you organize your pictures."
    )
    parser.add_argument(
        "-a",
        "--action",
        choices=["rename", "duplicates", "find-new"],
        required=True,
        help="The action to execute.",
    )

    args = parser.parse_args()
    settings = Settings.from_file(SETTINGS_FILEPATH)

    if args.action == "rename":
        rename_files()
    elif args.action == "duplicates":
        result = handle_duplicates(settings.pic_paths)
        print(f"Found {len(result)} duplicates.")
    elif args.action == "find-new":
        result = find_new(settings.pic_paths)
        print(f"Found {len(result)} new files that was copied to ./new_images.")


if __name__ == "__main__":
    main()
