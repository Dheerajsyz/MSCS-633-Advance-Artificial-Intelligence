# QR Code Generator for Biox Systems

A Python application that generates QR codes from URL input, developed as part of MSCS-633 Assignment 2.

## Features

- **GUI Mode**: User-friendly graphical interface with tkinter
- **Command-line Mode**: Terminal-based operation for automation
- **Save Functionality**: Export QR codes as PNG images
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

1. **Clone or download this project**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **For macOS users (if GUI doesn't work):**
   ```bash
   brew install python-tk
   ```

## Usage

### GUI Mode (Default)
```bash
python qr_generator.py
```

### Command-line Mode
```bash
# Interactive mode
python qr_generator.py --cli

# Direct URL input
python qr_generator.py --cli --url "https://example.com"

# Specify output file
python qr_generator.py --cli --url "https://example.com" --output "my_qr.png"
```

## Files

- `qr_generator.py` - Main QR code generator with GUI and CLI modes
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `bioxsystems_qr_final.png` - Generated QR code for Biox Systems

## Requirements

- Python 3.7+
- qrcode library
- Pillow (PIL)
- tkinter (for GUI mode)

## Output

The application generates QR codes that match the specified layout requirements, displaying them in a window with a clean, professional interface similar to the reference image provided.

<img width="1090" height="1334" alt="CleanShot 2025-09-03 at 22 16 43@2x" src="https://github.com/user-attachments/assets/c65fd06e-8369-4d9b-a207-f2c4f0530690" />

