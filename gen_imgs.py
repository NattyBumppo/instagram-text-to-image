from PIL import Image, ImageDraw, ImageFont
import random
import textwrap

# Function to generate a pastel color
def get_random_pastel_color():
    r = random.randint(190, 255)
    g = random.randint(190, 255)
    b = random.randint(190, 255)
    return (r, g, b)

# Function to find the optimal font size
def find_optimal_font_size(draw, text, font_path, max_width, max_height):
    font_size = 1
    font = ImageFont.truetype(font_path, font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    
    while text_bbox[2] < max_width and text_bbox[3] < max_height:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)
        text_bbox = draw.textbbox((0, 0), text, font=font)
    
    return font_size - 1

# Function to add text to an image
def add_text_to_image(text, increment_text, title_text, filename_base, bg_color):

    img_size = (1080, 1080)
    margin = 0.1
    text_color = (0, 0, 0)
    max_line_length = 40

    # Create a new image with the given background color
    img = Image.new('RGB', img_size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Define the font path
    font_path = 'C:/Windows/Fonts/calibri.ttf'
    font_path_ital = 'C:/Windows/Fonts/calibrii.ttf'
    
    # Break into multiple lines and wrap each line
    wrapped_lines = ['\n'.join(textwrap.wrap(line, width=max_line_length)) for line in text.split('\n')]

    # Recombine text for printing
    wrapped_text = '\n'.join(wrapped_lines)

    # Calculate the maximum width and height for the text
    max_width = img_size[0] * (1 - 2 * margin)
    max_height = img_size[1] * (1 - 2 * margin)
    
    # Find the optimal font size
    optimal_font_size = find_optimal_font_size(draw, wrapped_text, font_path, max_width, max_height)
    font = ImageFont.truetype(font_path, optimal_font_size)
    
    # Calculate the text position
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (img_size[0] - text_width) / 2
    text_y = (img_size[1] - text_height) / 2
    
    # Add increment text
    increment_font_size = 50
    increment_font = ImageFont.truetype(font_path, increment_font_size)
    increment_x = margin * img_size[0]
    increment_y = margin * img_size[1]
    
    # Draw the increment text
    draw.text((increment_x, increment_y), increment_text, font=increment_font, fill=text_color)
    
    # Add title text
    title_font_size = 30
    title_font = ImageFont.truetype(font_path_ital, title_font_size)

    # Calculate text width and height
    title_width = draw.textlength(title_text, font=title_font)

    # Calculate positions
    title_x = (img_size[0] - title_width) / 2  # Center the text
    title_y = img_size[1] - (margin * img_size[1] / 2)  # Position at bottom with margin

    # Draw the title text
    draw.text((title_x, title_y), title_text, font=title_font, fill=text_color, align='center')

    # Draw the main text
    draw.text((text_x, text_y), wrapped_text, font=font, fill=text_color, spacing=20, align='left')
    
    # Save the image
    img.save(f'imgs/{filename_base}.png')

# Read text chunks from a file
def read_chunks_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        full_text = file.read()
        chunks = full_text.split('-----')
    return [chunk.strip() for chunk in chunks if len(chunk.strip()) > 0]

# Main function to generate images from text file
def generate_images_from_file(filename):
    text_lines = read_chunks_from_file(filename)
    
    title_text = ''

    for i, text in enumerate(text_lines):
        # Only set the title text for the third image and later
        if i >= 2:
            title_text = '"The Two Government Officials" by Kenji Miyazawa'

        # Set new background color on every 10th image
        if i % 10 == 0:
            bg_color = get_random_pastel_color()

        increment_text = f'{i + 1}/{len(text_lines)}'

        print(f'Adding text for {i+1} / {len(text_lines)}')
        add_text_to_image(text, increment_text, title_text, i+1, bg_color)

# Specify the filename containing the text lines
filename = 'text.txt'
generate_images_from_file(filename)