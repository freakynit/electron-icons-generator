# Electron Icons Generator

A Python script to generate icons for macOS (ICNS), Windows (ICO), and Linux (PNG) from a single input image.

## Features
- Generates macOS ICNS icons in multiple sizes (16, 32, 48, 64, 128, 256) and generates composite `icns` file
- Creates a 256x256 ICO file for Windows
- Produces PNG files for Linux in the same sizes

## Requirements
- Python 3.x
- Pillow (`pip install Pillow`)
- Input image of high quality (preferably `1024x1024` and square dimensions)

## Usage
```bash
python icon_generator.py <input_image> <output_directory>
```
Example:
```bash
python icon_generator.py my_image.png ./icons
```

## Output Structure
```
<output_directory>/
├── icon.icns      # macOS icon
├── icon.ico       # Windows icon (256x256)
└── linux/         # Linux PNGs
    ├── icon_16x16.png
    ├── icon_32x32.png
    ├── icon_48x48.png
    ├── icon_64x64.png
    ├── icon_128x128.png
    └── icon_256x256.png
```

## Notes
- Input image should preferably be PNG with transparency
- Temporary files are cleaned up automatically
- Requires ImageMagick installed for ICNS generation (`brew install imagemagick` on macOS)


## Contributing

Contributions, feedback, and feature requests are welcome! Feel free to fork the repository, submit pull requests, or open issues to help the project improve.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
