# Icons resizer

A Python tool to automatically resize icon images. The tool detects the source resolution directly from the image files and resizes them to multiple target sizes (default: 1024x1024, 512x512, and 100x100). Non-square images are automatically skipped with an error message.

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

The tool automatically processes all image files in a directory, detecting their resolution and creating resized versions.

### Basic Usage

Simply run the tool in a directory containing your icon images:

```bash
python main.py
```

This will:
- Find all image files in the current directory (PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF, ICO, etc.)
- Detect the resolution directly from each image file
- Check if images are square (width == height) and skip non-square images with an error message
- **Keep original files unchanged** - only creates new resized files
- Convert non-PNG images to PNG format temporarily for processing (original files remain untouched)
- Create resized versions for each specified target resolution (default: 1024x1024, 512x512, and 100x100)
- Save all resized files to the `out` directory (created automatically if it doesn't exist)
- Skip files that already have a numeric suffix (generated files, e.g., `_512.png`, `_100.png`)
- Skip creating resized files if they already exist
- Preserve transparency for images that support it (RGBA)

### Custom Options

Specify a different input directory:

```bash
python main.py --dir /path/to/icons
```

Specify a different output directory:

```bash
python main.py --out-dir /path/to/output
```

Specify custom target resolutions:

```bash
python main.py --resolutions 1024 512 256
```

Combine all options:

```bash
python main.py --dir /path/to/icons --out-dir /path/to/output --resolutions 1024 512 256
```

### Output

For each source image file, the tool creates resized versions in the `out` directory (default) with the format:
- `out/{base_name}_{resolution}.png` (e.g., `out/icon_1024.png`, `out/icon_512.png`, `out/icon_100.png`)

The source resolution is automatically detected, so if you have a 2048x2048 image named `icon.png`, it will create `out/icon_1024.png`, `out/icon_512.png`, and `out/icon_100.png` (assuming default resolutions).

The `out` directory is created automatically if it doesn't exist.

### Generating Icons with [ChatGPT](https://chatgpt.com)

You can generate icons using ChatGPT with the following prompt. Replace `XXXXXX` with your desired icon description:

```text
Generate a XXXXXX, icon with a transparent background with this JSON style:
{
"icon_style": {
"perspective": "isometric",
"geometry": {
"proportions": "1:1 ratio canvas, with objects fitting comfortably within margins",
"element_arrangement": "central dominant object, with supporting elements symmetrically or diagonally placed"
},
"composition": {
"element_count": "2–4 main objects",
"spatial_depth": "layered to create sense of dimension and slight elevation",
"scale_consistency": "uniform object scale across icon set",
"scene_density": "minimal to moderate, maintaining clarity and visual focus"
},
"lighting": {
"type": "soft ambient light",
"light_source": "subtle top-right or front-top direction",
"shadow": "gentle drop shadows below and behind objects",
"highlighting": "mild edge illumination to define forms"
},
"textures": {
"material_finish": "semi-matte to satin surfaces",
"surface_treatment": "smooth with light tactile variation (e.g., wood grain, soft textures)",
"texture_realism": "stylized naturalism without hyper-realistic noise"
},
"render_quality": {
"resolution": "high-resolution octane 3D rendering",
"edge_definition": "crisp, no outlines; separation achieved via lighting and depth",
"visual_clarity": "clean, readable shapes with minimal clutter"
},
"color_palette": {
"tone": "naturalistic with slight saturation boost",
"range": "harmonious muted tones with gentle contrast",
"usage": "distinct colors per object to improve identification and readability",
"main_color": "#0f1237"
},
"background": {
"color": "transparent",
"style": "pure transparent, flat",
"texture": "none"
},
"stylistic_tone": "premium, friendly, clean with lifestyle or service-oriented appeal",
"icon_behavior": {
"branding_alignment": "neutral enough for broad applications",
"scalability": "legible at small and medium sizes",
"interchangeability": "part of a cohesive icon system with interchangeable subject matter"
}
}
}
```

After generating the icon, save it as a PNG file, then use this tool to resize it to the required dimensions. The tool will automatically detect the resolution from the file.

### Examples

**Basic example:**

You have image files: `icon1.png` (1024x1024), `icon2.jpg` (2048x2048), `my_icon.gif` (512x512)

Run the tool:

```bash
python main.py
```

This will:
- Detect the resolution from each file automatically
- Convert `icon2.jpg` and `my_icon.gif` to PNG temporarily for processing
- Create the `out` directory if it doesn't exist
- Create resized versions from each source file in the `out` directory:
  - `out/icon1_1024.png`, `out/icon1_512.png`, `out/icon1_100.png` (from 1024x1024 source)
  - `out/icon2_1024.png`, `out/icon2_512.png`, `out/icon2_100.png` (from 2048x2048 source)
  - `out/my_icon_1024.png`, `out/my_icon_512.png`, `out/my_icon_100.png` (from 512x512 source)
- Original files remain unchanged (temporary conversion files are cleaned up)

**Non-square image handling:**

If you have a non-square image (e.g., `banner.png` at 1920x1080), the tool will skip it with an error:

```bash
python main.py
# Output: Skipping banner.png: Image is not square (1920x1080)
```

**Custom resolutions example:**

To generate icons with custom resolutions:

```bash
python main.py --resolutions 1024 512 256 128 64
```

For a file `app_icon.png` at 2048x2048, this will create in the `out` directory:

- `out/app_icon_1024.png` (1024x1024)
- `out/app_icon_512.png` (512x512)
- `out/app_icon_256.png` (256x256)
- `out/app_icon_128.png` (128x128)
- `out/app_icon_64.png` (64x64)

## Notes

- The script uses high-quality LANCZOS resampling for better image quality
- **Original files are never modified, renamed, or deleted** - they remain exactly as they are
- All resized files are saved to the `out` directory (default, can be changed with `--out-dir`)
- The output directory is created automatically if it doesn't exist
- Only new resized files are created (e.g., `out/icon_1024.png`, `out/icon_512.png`, `out/icon_100.png` from `icon.png`)
- Temporary conversion files (for non-PNG images) are automatically cleaned up
- The source resolution is automatically detected from each image file
- Non-square images (width ≠ height) are automatically skipped with an error message
- Only square images are processed
- Generated files (with numeric suffix like `_512.png`, `_100.png`) are automatically skipped
- If a resized file already exists, it will be skipped (not overwritten)
- The tool supports multiple image formats (PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF, ICO) and converts them to PNG for processing
