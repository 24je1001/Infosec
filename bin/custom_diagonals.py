#!/usr/bin/env python3

from PIL import Image

# Function to read an image and extract pixel data
def read_image(file_path):
    with Image.open(file_path) as img:
        return img.convert('RGB'), img.size

# Function to save the modified image
def save_image(file_path, img):
    img.save(file_path)

# Function to calculate diagonal pixel indices in the image
def calculate_diagonal_indices(width, height):
    indices = []
    for i in range(min(width, height)):
        indices.append(i * (width + 1))  # Diagonal index formula for linearized array
    return indices

# Function to hide a message in the diagonal pixels of the image
def hide_message_diagonal(img, message, width, height):
    message += "\0"  # Null terminator to mark end of the message
    binary_message = ''.join(f"{ord(c):08b}" for c in message)  # Convert message to binary

    diagonal_indices = calculate_diagonal_indices(width, height)

    if len(binary_message) > len(diagonal_indices):
        raise ValueError("Message is too large to hide in the diagonal pixels of this image!")

    pixels = img.load()  # Access image pixel data
    for i, bit in enumerate(binary_message):
        x, y = divmod(diagonal_indices[i], width)  # Convert the linear index to 2D coordinates
        r, g, b = pixels[x, y]
        new_pixel = (r & ~1 | int(bit), g, b)  # Modify only the LSB of the red channel
        pixels[x, y] = new_pixel  # Update the pixel

    return img

# Function to extract a hidden message from the diagonal pixels of the image
def extract_message_diagonal(img, width, height):
    diagonal_indices = calculate_diagonal_indices(width, height)
    binary_message = []

    pixels = img.load()  # Access image pixel data
    for index in diagonal_indices:
        x, y = divmod(index, width)  # Convert the linear index to 2D coordinates
        r, g, b = pixels[x, y]
        binary_message.append(str(r & 1))  # Get the LSB from the red channel

        # Check for null terminator every 8 bits
        if len(binary_message) >= 8 and ''.join(binary_message[-8:]) == "00000000":
            break

    print('Binary message:', ''.join(binary_message))  # This will print the raw binary message

    # Convert binary to text
    message = ''
    byte_str = ''.join(binary_message)
    for i in range(0, len(byte_str), 8):
        byte = byte_str[i:i+8]
        if len(byte) < 8:  # In case of leftover bits
            break
        # Check for null terminator
        if byte == "00000000":
            break
        message += chr(int(byte, 2))

    return message

# Main program
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: custom_diagonals.py <hide/extract> <input_file> <output_file/message>")
        sys.exit(1)

    action, input_file = sys.argv[1], sys.argv[2]
    output_file_or_message = sys.argv[3]

    # Read image data
    img, (width, height) = read_image(input_file)

    if action == "hide":
        if len(sys.argv) != 5:
            print("Usage: custom_diagonals.py hide <input_file> <output_file> <message>")
            sys.exit(1)

        output_file = sys.argv[3]
        message = sys.argv[4]

        # Hide message in image
        try:
            modified_img = hide_message_diagonal(img, message, width, height)
            save_image(output_file, modified_img)
            print(f"Message hidden successfully in {output_file}.")
        except ValueError as e:
            print(f"Error: {e}")

    elif action == "extract":
        # Extract hidden message from image
        message = extract_message_diagonal(img, width, height)
        print(f"Extracted message: {message}")

    else:
        print("Invalid action. Use 'hide' or 'extract'.")
        sys.exit(1)
