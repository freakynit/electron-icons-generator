from PIL import Image
import os
import argparse

def generate_icons(input_image, output_path):
    # Default iconset name for macOS
    mac_iconset_path = os.path.join(output_path, "icon.iconset")
    # Path for Linux PNG files
    linux_path = os.path.join(output_path, "linux")

    # Create directories if they don't exist
    os.makedirs(mac_iconset_path, exist_ok=True)
    os.makedirs(linux_path, exist_ok=True)

    # List of sizes to generate
    sizes = [16, 32, 48, 64, 128, 256]

    # Process each size
    with Image.open(input_image) as img:
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        for size in sizes:
            # Calculate half size
            half = size // 2
            
            # Generate macOS icons
            # Full size
            full_size_img = img.resize((size, size), Image.Resampling.LANCZOS)
            full_size_path = os.path.join(mac_iconset_path, f"icon_{size}x{size}.png")
            full_size_img.save(full_size_path)
            
            # Half size
            half_size_img = img.resize((half, half), Image.Resampling.LANCZOS)
            half_size_path = os.path.join(mac_iconset_path, f"icon_{half}x{half}@2x.png")
            half_size_img.save(half_size_path)

            # Generate Linux PNG files
            linux_img = img.resize((size, size), Image.Resampling.LANCZOS)
            linux_path_file = os.path.join(linux_path, f"icon_{size}x{size}.png")
            linux_img.save(linux_path_file)

        # Generate Windows ICO file (256x256)
        ico_size_img = img.resize((256, 256), Image.Resampling.LANCZOS)
        ico_path = os.path.join(output_path, "icon.ico")
        ico_size_img.save(ico_path, format='ICO')

    # Generate macOS composite ICNS file
    os.system(f"iconutil -c icns {mac_iconset_path}")

    # Delete the temporary mac_iconset_path folder
    # for file_name in os.listdir(mac_iconset_path):
    #     file_path = os.path.join(mac_iconset_path, file_name)
    #     if os.path.isfile(file_path):
    #         os.remove(file_path)
    # os.rmdir(mac_iconset_path)

    print(f"All generated and saved at {output_path}");

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate icons for macOS (ICNS), Windows (ICO), and Linux (PNG) from an input image.')
    parser.add_argument('input_image', help='Path to the input image file (preferably PNG)')
    parser.add_argument('output_path', help='Path to the output directory where icons will be saved')

    args = parser.parse_args()

    generate_icons(args.input_image, args.output_path)

if __name__ == "__main__":
    main()
