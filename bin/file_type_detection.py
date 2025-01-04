#!/usr/bin/env python3
import argparse

def identify_file_type(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(8)  # Read the first 8 bytes of the file

    # File signatures for known types
    file_signatures = {
        b'\x89PNG\r\n\x1a\n': 'PNG Image',
        b'\xff\xd8\xff\xe0': 'JPEG Image',
        b'PK\x03\x04': 'ZIP Archive',
	b'%PDF-': 'PDF Document',
	b'\x1f\x8b\x08': 'GZIP Compressed'
    }

    # Check against known file signatures
    for sig, filetype in file_signatures.items():
        if header.startswith(sig):
            return filetype

    # Detect text files by checking if the file can be decoded as UTF-8
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()  # Try reading the file as text
        return 'Text File'
    except UnicodeDecodeError:
        pass  # Not a text file if decoding fails

    # Detect binary files by checking for high-entropy content
    if any(byte > 127 for byte in header):
        return 'Binary File'

    # Detect hex dump by specific patterns (e.g., ASCII-represented hex bytes)
    if all(c in b'0123456789abcdefABCDEF \n' for c in header):
        return 'Hex Dump'

    return 'Unknown'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Identify the type of a file based on its signature.")
    parser.add_argument("file_path", help="Path to the file to check.")
    args = parser.parse_args()

    try:
        print(identify_file_type(args.file_path))
    except FileNotFoundError:
        print("File not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

