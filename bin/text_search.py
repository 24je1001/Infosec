#!/usr/bin/env python3

import argparse

def search_pattern(file_path, pattern):
    matches = []
    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, start=1):
                if pattern.lower() in line.lower():  # Case-insensitive substring search
                    matches.append((line_num, line.strip()))
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return matches

def main():
    parser = argparse.ArgumentParser(description="Search for a term or pattern in a file (case-insensitive).")
    parser.add_argument("file_path", help="The path to the file to search.")
    parser.add_argument("pattern", help="The term or pattern to search for.")
    
    args = parser.parse_args()

    matches = search_pattern(args.file_path, args.pattern)
    
    if matches:
        print("Matches found:")
        for line_num, line in matches:
            print(f"Line {line_num}: {line}")
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()

