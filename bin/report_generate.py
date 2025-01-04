#!/usr/bin/env python3
import argparse

# Function from file_type_detection.py
def identify_file_type(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(8)  # Read the first 8 bytes of the file

    file_signatures = {
        b'\x89PNG\r\n\x1a\n': 'PNG Image',
        b'\xff\xd8\xff\xe0': 'JPEG Image',
        b'PK\x03\x04': 'ZIP Archive',
        b'%PDF-': 'PDF Document',
        b'\x1f\x8b\x08': 'GZIP Compressed'
    }

    for sig, filetype in file_signatures.items():
        if header.startswith(sig):
            return filetype

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return 'Text File'
    except UnicodeDecodeError:
        pass

    if any(byte > 127 for byte in header):
        return 'Binary File'

    if all(c in b'0123456789abcdefABCDEF \n' for c in header):
        return 'Hex Dump'

    return 'Unknown'

# Function from extract.py
def extract_strings(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        return ''.join([chr(c) for c in content if 32 <= c <= 126 or c == 10]).strip()

# Function from text_extraction.py
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

# Functions from hex_use.py
def read_header(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(16)
    return header

def file_size(file_path):
    size = 0
    with open(file_path, 'rb') as f:
        while f.read(1024):
            size += 1
    return f"{size} KB"

def analyze_file_header(file_path):
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
        description="Generate a comprehensive report on the given file, including file type detection, text extraction, and header analysis."
    )
    parser.add_argument("file_path", help="Path to the file to analyze.")

    args = parser.parse_args()

    try:
        file_type = identify_file_type(args.file_path)
        print(f"File Type: {file_type}\n")

        extracted_text = extract_text(args.file_path)
        print(f"Extracted Text:\n{extracted_text}\n")

        analyze_file_header(args.file_path)
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
