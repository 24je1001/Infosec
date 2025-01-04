#!/usr/bin/env python3

def extract_strings(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        return ''.join([chr(c) for c in content if 32 <= c <= 126 or c == 10]).strip()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = extract_strings(file_path)
        print(result)
    else:
        print("No file path provided.")
