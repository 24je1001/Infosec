#!/usr/bin/env python3
import argparse

def extract_text(file_path):
    readable_text = ''
    try:
        with open(file_path, 'rb') as f:
            byte = f.read(1)
            while byte:
                if 32 <= ord(byte) <= 126 or byte in (b'\n', b'\r'):
                    readable_text += byte.decode('ascii', errors='ignore')
                byte = f.read(1)
    except FileNotFoundError:
        return "Error: File not found. Please check the file path."
    except Exception as e:
        return f"Error: {e}"
    return readable_text

if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(
        description="Extract human-readable text from a binary file."
    )
    # Add arguments
    parser.add_argument(
        "file_path",
        help="The path to the binary file you want to extract text from."
    )
    # Parse arguments
    args = parser.parse_args()
    # Extract text and print the result
    result = extract_text(args.file_path)
    print("\nExtracted Text:\n")
    print(result)
