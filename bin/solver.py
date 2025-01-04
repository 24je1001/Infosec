#!/usr/bin/env python3

# Custom steganography: Hiding text in the LSB of an image
# Only uses built-in Python libraries

# Function to read an image as raw binary data

def read_image(file_path):
    with open(file_path, "rb") as f:
        return bytearray(f.read())

# Function to write modified binary data back to an image file
def write_image(file_path, data):
    with open(file_path, "wb") as f:
        f.write(data)

# Function to hide a message in the LSB of the image
def hide_message(image_data, message):
    message += "\0"  # Null terminator to mark end of the message
    binary_message = ''.join(f"{ord(c):08b}" for c in message)  # Convert message to binary

    if len(binary_message) > len(image_data):
        raise ValueError("Message is too large to hide in this image!")

    for i, bit in enumerate(binary_message):
        image_data[i] = (image_data[i] & ~1) | int(bit)  # Set the LSB to the message bit

    return image_data

# Function to extract a hidden message from the LSB of the image
def extract_message(image_data):
    binary_message = []

    for byte in image_data:
        binary_message.append(str(byte & 1))  # Get the LSB

        # Check for null terminator every 8 bits
        if len(binary_message) % 8 == 0 and ''.join(binary_message[-8:]) == "00000000":
            break

    # Convert binary to text
    message = ''.join(
        chr(int(''.join(binary_message[i:i+8]), 2))
        for i in range(0, len(binary_message) - 8, 8)
    )

    return message

# Main program
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: solver.py <hide/extract> <input_file> <output_file/message>")
        sys.exit(1)

    action, input_file = sys.argv[1], sys.argv[2]

    if action == "hide":
        if len(sys.argv) != 5:
            print("Usage: solver.py hide <input_file> <output_file> <message>")
            sys.exit(1)

        output_file, message = sys.argv[3], sys.argv[4]

        # Read image data
        image_data = read_image(input_file)

        # Hide message
        try:
            modified_data = hide_message(image_data, message)
            write_image(output_file, modified_data)
            print(f"Message hidden successfully in {output_file}.")
        except ValueError as e:
            print(f"Error: {e}")

    elif action == "extract":
        # Read image data
        image_data = read_image(input_file)

        # Extract message
        message = extract_message(image_data)
        print(f"Extracted message: {message}")

    else:
        print("Invalid action. Use 'hide' or 'extract'.")
        sys.exit(1)
