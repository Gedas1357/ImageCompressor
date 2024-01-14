import os
import time
from PIL import Image
import imageio

def compress_and_save(input_path, output_folder, format, compression=None):
    start_time = time.time()

    with open(input_path, 'rb') as raw_file:
        width, height = get_image_dimensions(raw_file)
        raw_data = raw_file.read()

    image = Image.frombytes('RGB', (width, height), raw_data)

    if format.lower() == 'jpeg2000':
        output_path = os.path.join(output_folder, f"output.{format}")
        image.save(output_path, format='JPEG2000', quality_layers=[compression])
    else:
        output_path = os.path.join(output_folder, f"output.{format}")
        imageio.imwrite(output_path, image, format=format.upper())

    end_time = time.time()
    conversion_time = end_time - start_time
    print(f"Conversion to {format.upper()} completed in {conversion_time:.10f} seconds.")

def get_image_dimensions(file):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    width = height = int((file_size / 3) ** 0.5)
    file.seek(0)
    return width, height

if __name__ == "__main__":
    input_path = r"input"
    output_folder = r"output"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    formats = ['png', 'gif', 'tiff', 'bmp', 'jpeg', 'webp', 'jpeg2000', 'heif']
    compression_values = [3, None, 'tiff_lzw', None, 75, 75, 75, None]

    for format, compression in zip(formats, compression_values):
        compress_and_save(input_path, output_folder, format, compression)
