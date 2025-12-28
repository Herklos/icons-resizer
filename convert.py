import os
from PIL import Image

def resize_images(input_dir):
    # Ensure the input directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return

    # Iterate through all files in the directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            
            # Open the image to check its size
            with Image.open(input_path) as img:
                width, height = img.size
                
                # Prepare output filenames
                base_name = filename.replace('_1024.png', '')
                output_512 = os.path.join(input_dir, f"{base_name}_512.png")
                output_100 = os.path.join(input_dir, f"{base_name}_100.png")
                
                # Resize to 512x512
                img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
                img_512.save(output_512, 'PNG')
                print(f"Saved {output_512}")
                
                # Resize to 100x100
                img_100 = img.resize((100, 100), Image.Resampling.LANCZOS)
                img_100.save(output_100, 'PNG')
                print(f"Saved {output_100}")

if __name__ == "__main__":
    # Specify the directory containing PNG files
    input_directory = "."
    resize_images(input_directory)

