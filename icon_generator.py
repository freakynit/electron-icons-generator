from PIL import Image
import os
import argparse

def generate_icons(input_image, output_path, tray_threshold):
    # Default iconset name for macOS
    mac_iconset_path = os.path.join(output_path, "icon.iconset")
    # Path for Linux PNG files
    linux_path = os.path.join(output_path, "linux")

    # Create directories if they don't exist
    os.makedirs(mac_iconset_path, exist_ok=True)
    os.makedirs(linux_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)  # Ensure output_path exists for tray icons

    # List of sizes to generate for regular icons
    sizes = [16, 32, 48, 64, 128, 256]

    # Map tray_threshold (1-10) to actual pixel value (0-255)
    threshold_value = int((tray_threshold - 1) * (255 / 9))  # Scale 1-10 to 0-255

    # Process icons
    with Image.open(input_image) as img:
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Generate regular icons
        for size in sizes:
            # Calculate half size
            half = size // 2
            
            # Generate macOS icons
            full_size_img = img.resize((size, size), Image.Resampling.LANCZOS)
            full_size_path = os.path.join(mac_iconset_path, f"icon_{size}x{size}.png")
            full_size_img.save(full_size_path)
            
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

        # Generate macOS tray template icons (monochrome)
        # Convert to grayscale first, then to black and white with adjustable threshold
        tray_img = img.convert('L')  # Convert to grayscale
        tray_img = tray_img.point(lambda x: 0 if x < threshold_value else 255, '1')  # Adjustable threshold
        tray_img = tray_img.convert('RGBA')  # Convert back to RGBA to preserve transparency
        
        # Get original alpha channel
        alpha = img.split()[3]
        # Apply original alpha to the black/white image
        tray_img.putalpha(alpha)

        # Generate 16x16 tray icon
        tray_16 = tray_img.resize((16, 16), Image.Resampling.LANCZOS)
        tray_16_path = os.path.join(output_path, "tray_16x16.png")
        tray_16.save(tray_16_path)

        # Generate 32x32@2x tray icon (for retina displays)
        tray_32 = tray_img.resize((32, 32), Image.Resampling.LANCZOS)
        tray_32_path = os.path.join(output_path, "tray_16x16@2x.png")
        tray_32.save(tray_32_path)

    # Generate macOS composite ICNS file
    os.system(f"iconutil -c icns {mac_iconset_path}")

    # Delete the temporary mac_iconset_path folder
    for file_name in os.listdir(mac_iconset_path):
        file_path = os.path.join(mac_iconset_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(mac_iconset_path)

    print(f"All icons generated and saved at {output_path}")
    print(f"Tray icons generated with threshold value: {tray_threshold} (mapped to {threshold_value}/255)")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate icons for macOS (ICNS), Windows (ICO), Linux (PNG), and macOS tray templates from an input image.')
    parser.add_argument('input_image', help='Path to the input image file (preferably PNG)')
    parser.add_argument('output_path', help='Path to the output directory where icons will be saved')
    parser.add_argument('--tray-threshold', type=int, choices=range(1, 11), default=5,
                        help='Threshold for tray icon monochrome conversion (1-10, default: 5)')

    args = parser.parse_args()

    generate_icons(args.input_image, args.output_path, args.tray_threshold)

if __name__ == "__main__":
    main()
