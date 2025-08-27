import os
from PIL import Image

# --- Configuration ---
# Set the directory where your PNG images are located.
# Use '.' to specify the same directory where you run the script.
TARGET_DIRECTORY = "."

# Set the desired quality for the output JPEG images (1-100).
# 95 is considered very high quality.
JPEG_QUALITY = 95


def convert_png_to_jpeg(directory, quality):
    """
    Finds all PNG files in a given directory, converts them to JPEG format
    with a white background, and saves them with the same base name.
    """
    # 1. Check if the target directory exists
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    print(f"Scanning for PNG images in '{os.path.abspath(directory)}'...")

    # 2. Loop through all files in the specified directory
    for filename in os.listdir(directory):
        # Check for .png extension (case-insensitive)
        if filename.lower().endswith(".png"):

            # Construct the full path for the input file
            png_path = os.path.join(directory, filename)

            # Determine the output filename by replacing the extension
            base_name = os.path.splitext(filename)[0]
            jpeg_filename = f"{base_name}.jpeg"
            jpeg_path = os.path.join("../gallery", jpeg_filename)

            try:
                # 3. Open the PNG image using a 'with' block
                with Image.open(png_path) as img:
                    print(f"Converting '{filename}' -> '{jpeg_filename}'...")

                    # 4. Handle transparency (PNGs can have an alpha channel, JPEGs cannot)
                    # We check if the image mode is RGBA or LA (Luminance with Alpha)
                    if img.mode in ("RGBA", "LA"):
                        # Create a new image with a solid white background
                        background = Image.new("RGB", img.size, (255, 255, 255))

                        # Paste the original image onto the background.
                        # The original image's alpha channel is used as a mask.
                        background.paste(img, (0, 0), img)
                        img_to_save = background
                    else:
                        # If the image has no alpha channel, just ensure it's in RGB mode
                        img_to_save = img.convert("RGB")

                    # 5. Save the final image as a JPEG with the specified quality
                    img_to_save.save(jpeg_path, "jpeg", quality=quality)

            except Exception as e:
                print(f"  -> Failed to convert '{filename}'. Reason: {e}")

    print("\nConversion process finished.")


# --- Main execution block ---
if __name__ == "__main__":
    convert_png_to_jpeg(TARGET_DIRECTORY, JPEG_QUALITY)
