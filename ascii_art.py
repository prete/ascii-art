import shutil
from PIL import Image
import argparse

def ascii_art(options):
    # Read image
    img = Image.open(options.image_path)

    # Get image's size 
    width, height = img.size

    # Resize to fit to terminal
    terminal_size = shutil.get_terminal_size()

    if width > terminal_size.columns:
        shrink_ratio = (terminal_size.columns-1)/width
        new_width = int(width*shrink_ratio)
        new_height = int(height*shrink_ratio)
        img = img.resize( (new_width, new_height), Image.ANTIALIAS )
        img.save("fit_img.jpg")
        height = new_height
        width = new_width

    # Get pixel data
    img_contents = img.convert("RGB").getdata()

    # Build a 2-dimensional array of pixels
    rgb_matrix = []

    for row in range(height):
        pixel_row = []
        for col in range(width):
            pixel = img_contents[col + width*row]
            pixel_row.append(pixel)
        rgb_matrix.append(pixel_row)

    # Convert the RGB tuples into single brightness numbers
    brightness_matrix = []
    for row in range(height):
        brightness_row = []
        for col in range(width):
            R, G, B = rgb_matrix[row][col]
            if options.brightness == "avg":
                average = (R + G + B) / 3
                brightness_row.append(average)
            if options.brightness == "light":
                lightness = ( max(R, G, B) + min(R, G, B) )/ 2
                brightness_row.append(lightness)
            if options.brightness == "lum":
                luminosity = (0.21 * R) + (0.72 * G) + (0.07 * B)
                brightness_row.append(luminosity)
        brightness_matrix.append(brightness_row)

    # Convert brightness numbers to ASCII characters
    character_map = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    character_matrix = []
    delta = (len(character_map)-1)/255

    for row in range(height):
        character_row = []
        for col in range(width):
            brightness = brightness_matrix[row][col]
            character = character_map[int(brightness * delta)]
            character_row.append(character)
        character_matrix.append(character_row)

    for row in range(height):
        for col in range(width):
            print(character_matrix[row][col], end='')
        print()

    print(options)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert image into ASCII-art.')
    parser.set_defaults(brightness="avg")
    parser.set_defaults(colourful=False)
    parser.add_argument("-i", "--image", help="Input image path", type=str, required=True, dest="image_path")
    parser.add_argument("-b", "--brightness", help="Brightnes mode: average, lightness or luminosity", dest="brightness", type=str, choices=["avg", "light", "lum"], required=False)
    parser.add_argument("-c", "--color", help="Use colourful output", dest="colourful", required=False, action='store_true')
    args = parser.parse_args()
    ascii_art(args)
