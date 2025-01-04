#!/usr/bin/env python3

import os
import argparse

def list_hidden_files(directory):
    """Returns a list of hidden files in the given directory."""
    try:
        return [f for f in os.listdir(directory) if f.startswith('.')]
    except FileNotFoundError:
        return f"Error: The directory '{directory}' does not exist."
    except PermissionError:
        return f"Error: You do not have permission to access '{directory}'."

def main():
    """Interactive function to list hidden files in a user-specified directory."""
    parser = argparse.ArgumentParser(description="List hidden files in a specified directory.")
    parser.add_argument(
        "directory",
        nargs="?",
        default="./",
        help="The directory to scan for hidden files. Defaults to the current directory './'."
    )
    
    args = parser.parse_args()
    directory = args.directory

    hidden_files = list_hidden_files(directory)
    if isinstance(hidden_files, list):
        if hidden_files:
            print("Hidden files:")
            for file in hidden_files:
                print(f"- {file}")
        else:
            print("No hidden files found.")
    else:
        print(hidden_files)  # Display the error message

if __name__ == "__main__":
    main()
