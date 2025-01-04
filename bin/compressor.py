#!/usr/bin/env python3

import argparse

def compress_file(input_path, output_path):
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        data = f_in.read()
        compressed_data = ''
        i = 0
        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i] == data[i + 1]:
                i += 1
                count += 1
            compressed_data += data[i] + str(count)
            i += 1
        f_out.write(compressed_data)

def decompress_file(input_path, output_path):
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        data = f_in.read()
        decompressed_data = ''
        i = 0
        while i < len(data):
            char = data[i]
            i += 1
            count = ''
            while i < len(data) and data[i].isdigit():
                count += data[i]
                i += 1
            decompressed_data += char * int(count)
        f_out.write(decompressed_data)

def main():
    parser = argparse.ArgumentParser(description="File Compression/Decompression Tool")
    parser.add_argument("operation", choices=["compress", "decompress"], help="Choose the operation to perform: compress or decompress")
    parser.add_argument("input_path", help="Path to the input file")
    parser.add_argument("output_path", help="Path to the output file")

    args = parser.parse_args()

    if args.operation == "compress":
        try:
            compress_file(args.input_path, args.output_path)
            print(f"File successfully compressed to {args.output_path}")
        except Exception as e:
            print(f"An error occurred during compression: {e}")

    elif args.operation == "decompress":
        try:
            decompress_file(args.input_path, args.output_path)
            print(f"File successfully decompressed to {args.output_path}")
        except Exception as e:
            print(f"An error occurred during decompression: {e}")

if __name__ == "__main__":
    main()
