import os
import argparse
import logging
from PIL import Image

DEFAULT_RESOLUTIONS = [1024, 512, 100]
DEFAULT_DIRECTORY = '.'
DEFAULT_OUTPUT_DIR = 'out'
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.ico'}
TRANSPARENT_MODES = ('RGBA', 'LA', 'P')

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

def process_images(input_dir, resolutions, output_dir):
    """Process images: convert to PNG if needed, detect resolution, and resize to specified resolutions."""
    # Ensure the input directory exists
    if not os.path.exists(input_dir):
        logger.error(f"Directory {input_dir} does not exist.")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")

    processed_count = 0
    resized_count = 0
    
    # Iterate through all files in the directory
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Get file extension
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Check if it's an image file
        is_image = file_ext in IMAGE_EXTENSIONS
        
        # Skip if not an image
        if not is_image:
            continue
        
        # Check if it's a generated file (has numeric suffix pattern)
        base_name = os.path.splitext(filename)[0]
        if '_' in base_name:
            parts = base_name.rsplit('_', 1)
            if len(parts) == 2 and parts[1].isdigit():
                # This is a generated file (has numeric suffix), skip it
                continue
        
        try:
            # Open the image to check its size and validity
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Check if image is square
                if width != height:
                    logger.error(f"Skipping {filename}: Image is not square ({width}x{height})")
                    continue
                
                source_resolution = width
                
                # Load the image data (convert if needed) before closing the context
                if img.mode in TRANSPARENT_MODES:
                    img_data = img.convert('RGBA')
                else:
                    img_data = img.convert('RGB')
            
            # Now process the image data (context is closed, but we have the data)
            # If it's not PNG, we need to convert it first
            if file_ext != '.png':
                # Create a temporary PNG path for processing
                temp_png_path = os.path.join(input_dir, f"{base_name}_temp.png")
                img_data.save(temp_png_path, 'PNG')
                logger.info(f"Converted {filename} to PNG for processing")
                processed_count += 1
                
                # Use the temp file for resizing
                source_base_name = base_name
            else:
                # Already PNG, use it directly
                source_base_name = base_name
            
            # Resize to each specified resolution
            for resolution in resolutions:
                output_path = os.path.join(output_dir, f"{source_base_name}_{resolution}.png")
                
                # Skip if output file already exists
                if os.path.exists(output_path):
                    logger.warning(f"Skipping {output_path}: File already exists")
                    continue
                
                resized_img = img_data.resize((resolution, resolution), Image.Resampling.LANCZOS)
                resized_img.save(output_path, 'PNG')
                logger.info(f"Saved {output_path}")
                resized_count += 1
            
            # Clean up temporary PNG file if we created one
            if file_ext != '.png':
                temp_png_path = os.path.join(input_dir, f"{base_name}_temp.png")
                if os.path.exists(temp_png_path):
                    os.remove(temp_png_path)
                    
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            continue
    
    if processed_count == 0 and resized_count == 0:
        logger.info(f"No image files found to process. All files are generated files or non-square images.")
    else:
        if processed_count > 0:
            logger.info(f"Converted {processed_count} file(s) to PNG for processing.")
        if resized_count > 0:
            logger.info(f"Created {resized_count} resized image(s).")

def main():
    parser = argparse.ArgumentParser(
        description='Icon resizer tool - automatically detect resolution and resize icon images'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set the logging level (default: INFO)'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default=DEFAULT_DIRECTORY,
        help='Directory containing image files (default: current directory)'
    )
    parser.add_argument(
        '--out-dir',
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help='Directory to save resized images (default: out)'
    )
    parser.add_argument(
        '--resolutions',
        type=int,
        nargs='+',
        default=DEFAULT_RESOLUTIONS,
        help='List of resolutions to convert to (default: 1024 512 100)'
    )
    
    args = parser.parse_args()
    
    log_level = getattr(args, 'log_level', 'INFO')
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    process_images(args.dir, args.resolutions, args.out_dir)

if __name__ == "__main__":
    main()

