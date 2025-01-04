#!/usr/bin/env python3

import os
import argparse

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"File renamed successfully from '{old_name}' to '{new_name}'.")
    except FileNotFoundError:
        print(f"Error: The file '{old_name}' does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to rename '{old_name}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rename a file.")
    parser.add_argument('old_name', type=str, help="The current file name (including extension).")
    parser.add_argument('new_name', type=str, help="The new file name (including extension).")
    args = parser.parse_args()

    rename_file(args.old_name, args.new_name)

if __name__ == "__main__":
    main()
