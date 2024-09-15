import random
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from transformers import pipeline
import requests
import matplotlib.colors as mcolors
from io import BytesIO
from llm1 import get_relevant_objects
from util.files import CloudflareR2


# image_url = "https://as2.ftcdn.net/v2/jpg/00/66/26/87/1000_F_66268784_jccdcfdpf2vmq5X8raYA8JQT0sziZ1H9.jpg"
# response = requests.get(image_url)

# # Ensure the request was successful
# if response.status_code == 200:
    # img = Image.open(BytesIO(response.content))


def combine_images(images):

    # Ensure all images have the same size
    widths, heights = zip(*(i.size for i in images))
    if len(set(widths)) > 1 or len(set(heights)) > 1:
        raise ValueError("All images must have the same dimensions")

    # Initialize output image with all pixels set to black
    output_image = Image.new('RGB', images[0].size, color=(0, 0, 0))
    # up to 5
    possible_colors = [
        (103, 204, 247),
        (255, 64, 64),
        (103, 247, 113),
        (163, 52, 196),
        (255, 198, 97)
    ]

    # # Process each pixel
    for x in range(output_image.width):
        for y in range(output_image.height):
            # Check each image to see if any have a white pixel at (x, y)
            which_imgs = [img.getpixel((x, y)) == 255 for img in images]
            for i, img_data in enumerate(which_imgs):
                if img_data:
                    color = possible_colors[i]
                    output_image.putpixel((x, y), color)  # Set pixel to that color
                    break

    return output_image

def generate_seg_img(img_path):
    img = Image.open(img_path)
    semantic_segmentation = pipeline("image-segmentation", "nvidia/segformer-b0-finetuned-ade-512-512")
    results = semantic_segmentation(img)
    print(results)

    fig, ax = plt.subplots()

    ax.set_axis_off()
    ax.imshow(img, aspect='auto')
    total_objects = [x['label'] for x in results]
    relevant_categories = get_relevant_objects(total_objects)
    imgs_to_combine = []
    for x in results:
        if x["label"] in relevant_categories:
            imgs_to_combine.append(x["mask"])

    ax.imshow(combine_images(imgs_to_combine), alpha=0.5, aspect='auto')

    ret_str = ""
    for i, result in enumerate(results):
        mask = result['mask']
        
        # Convert mask to numpy array if it's not already
        mask_np = np.array(mask)
        
        # Get the coordinates of the mask (assuming mask is binary)
        y_indices, x_indices = np.nonzero(mask_np)
        
        if len(x_indices) > 0 and len(y_indices) > 0:
            # Compute the average (center) of the coordinates
            center_x = np.mean(x_indices)
            center_y = np.mean(y_indices)
            
            print(f"Center of Mask {i}: (x={center_x:.2f}, y={center_y:.2f})")
            ret_str += f"Center of Mask {i}: (x={center_x:.2f}, y={center_y:.2f})\n"

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)  # Close the figure

    # Get the byte string
    buffer.seek(0)  # Go to the start of the buffer
    image_bytes = buffer.getvalue()

    r2 = CloudflareR2()
    r2.upload_object("thing.png", image_bytes)
    # plt.savefig('thing.png')
    plt.axis('off')  # Hide the axis

    return ret_str

# generate_seg_img("first_frame.png")
