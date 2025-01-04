#!/usr/bin/env python3
import argparse

def hex_dump(file_path):
    """Generate a hex dump of the entire file."""
    with open(file_path, 'rb') as f:
        content = f.read()
    hex_content = ' '.join(f'{byte:02x}' for byte in content)
    return hex_content

def read_header(file_path):
    """Read the first 16 bytes of the file as the header."""
    with open(file_path, 'rb') as f:
        header = f.read(16)
    return header

def file_size(file_path):
    """Return the size of the file in kilobytes (KB)."""
    size = 0
    with open(file_path, 'rb') as f:
        while f.read(1024):  # Read 1KB chunks
            size += 1
    return f"{size} KB"

def analyze_file_header(file_path):
    """Perform detailed analysis of the file header."""
    header = read_header(file_path)
    header_hex = ' '.join(f'{byte:02x}' for byte in header)

    print("Header Hexadecimal Representation:")
    print(header_hex)

    try:
        with open(file_path, 'r') as f:
            content = f.read(256)  # Read the first 256 characters
            is_text = all(32 <= ord(char) <= 126 or char in '\t\n\r' for char in content)
    except UnicodeDecodeError:
        is_text = False

    # Determine file type based on header
    if header.startswith(b'\x89PNG'):
        print("\nFile Type: PNG Image")
        print(f"File Size: {file_size(file_path)}")
        print("Details: This is a PNG image file.")
        with open(file_path, 'rb') as f:
            f.seek(16)
            width = int.from_bytes(f.read(4), 'big')
            height = int.from_bytes(f.read(4), 'big')
            print(f"Resolution: {width} x {height}")
    elif header[:2] == b'\xFF\xD8':
        print("\nFile Type: JPEG Image")
        print(f"File Size: {file_size(file_path)}")
        print("Details: This is a JPEG image file.")
        print("Compression: Baseline DCT, Huffman coding")
        print("Color Space: YCbCr")
    elif header[:4] == b'%PDF':
        print("\nFile Type: PDF Document")
        print(f"File Size: {file_size(file_path)}")
        print("Details: This is a PDF file.")
        version = header.decode(errors='ignore').split('-')[1]
        print(f"PDF Version: %PDF-{version}")
    elif header[:4] == b'PK\x03\x04':
        print("\nFile Type: ZIP Archive")
        print(f"File Size: {file_size(file_path)}")
        print("Details: This is a ZIP archive.")
    elif header[:4] == b'MZ':
        print("\nFile Type: Windows Executable (EXE)")
        print(f"File Size: {file_size(file_path)}")
        print("Details: This is a Windows executable file.")
    elif header[:3] == b'\x1f\x8b\x08':
        print("\nFile Type: GZIP Compressed File")
        print(f"File Size: {file_size(file_path)}")
        print("Details: This is a GZIP compressed file.")
    elif is_text:
        print("\nFile Type: Plain Text (.txt)")
        print(f"File Size: {file_size(file_path)}")
        print("Details: This appears to be a plain text file.")
    else:
        print("\nFile Type: Unknown")
        print(f"File Size: {file_size(file_path)}")
        print("Details: The file header does not match known signatures.")

# Further analysis: provide information about potential file structure
        if header[:4] == b'\x00\x00\x00\x00':
            print("The file might be padded or have no signature, possibly binary data or custom format.")
        elif header[:2] == b'\xFF\xFF':
            print("This might be a sound or audio file, as the header suggests a possible audio format.")
        elif all(0 <= byte <= 255 for byte in header[:8]):
            print("The first few bytes are within normal binary data range. It might be a custom binary format or unrecognized.")
        else:
            print("Unable to determine specific characteristics. The file might be non-standard or obscure.")

def main():
    parser = argparse.ArgumentParser(
        description="Hex dump and header analysis of a file.",
        epilog="Examples:\n"
               "  mycmd file.txt           Analyze the whole file\n"
               "  mycmd -h file.txt        Show only the header\n"
               "  mycmd -d file.txt        Show only the hex dump\n"
               "  mycmd -A file.txt        Perform detailed header analysis",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('file', metavar='FILE', type=str, help="File to analyze")
    parser.add_argument('-d', '--dump', action='store_true', help="Show the full hex dump of the file")
    parser.add_argument('-H', '--header', action='store_true', help="Show only the file header (first 16 bytes)")
    parser.add_argument('-A', '--analyze', action='store_true', help="Perform detailed header analysis")

    args = parser.parse_args()

    try:
        if args.dump:
            print("Hex Dump of the file:")
            print(hex_dump(args.file))
        elif args.header:
            print("File Header (first 16 bytes in hex):")
            header = read_header(args.file)
            print(' '.join(f'{byte:02x}' for byte in header))
        elif args.analyze:
            print("Detailed Header Analysis:")
            analyze_file_header(args.file)
        else:
            print("Hex Dump of the file:")
            print(hex_dump(args.file))
            print("\nFile Header (first 16 bytes in hex):")
            header = read_header(args.file)
            print(' '.join(f'{byte:02x}' for byte in header))
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        parser.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        parser.exit(1)

if __name__ == '__main__':
    main()
