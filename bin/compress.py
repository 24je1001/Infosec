#!/usr/bin/env python3

import argparse

def compress_file(input_path, output_path):
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        data = f_in.read()
        compressed_data = bytearray()
        i = 0
        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i] == data[i + 1] and count < 255:
                i += 1
                count += 1
            compressed_data.append(data[i])
            compressed_data.append(count)
            i += 1
        f_out.write(compressed_data)

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        data = f_in.read()
        decompressed_data = bytearray()
        i = 0
        while i < len(data):
            char = data[i]
            count = data[i + 1]
            decompressed_data.extend([char] * count)
            i += 2
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
