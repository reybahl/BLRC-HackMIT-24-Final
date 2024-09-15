import io
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

from flask import Blueprint, request, jsonify, send_file
from util.files import CloudflareR2

imgsegbp = Blueprint('imgseg', __name__)
r2_client = CloudflareR2()

plt.switch_backend('Agg')

UPLOAD_FOLDER = './upload'

@imgsegbp.route('/imgseg', methods=['POST'])
def imgseg():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if not len(request.files):
            return 'No file part'
        # print(request.files.keys())
        file = request.files['']
        file.save("frame.png")
    color_mapping = generate_seg_img("frame.png") # maybe need to correct file extension here?
    output_img = Image.open("output.png")
    image_bytes = io.BytesIO()
    output_img.save(image_bytes, format="PNG")
    object_key = f'{random.randint(0, 1000000)}.png'
    image_bytes.seek(0)

    # presigned_url = r2_client.generate_presigned_url('hackmit2024', object_key)
    # print(f"Presigned URL for uploading: {presigned_url}")

    r2_client.upload_object(object_key, image_bytes)
    
    print(f"Uploaded object '{object_key}'")

    return_dict = {
        "img_url" : f"https://hackmit2024.lilbillbiscuit.com/{object_key}",
        "color_mapping" : color_mapping
    }
    return jsonify(return_dict)
    
    #upload_img = CloudflareR2()
    


def combine_images(images, relevant_categories):

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

    color_to_label_mapping = {

    }

    # # Process each pixel
    for x in range(output_image.width):
        for y in range(output_image.height):
            # Check each image to see if any have a white pixel at (x, y)
            which_imgs = [img.getpixel((x, y)) == 255 for img in images]
            for i, img_data in enumerate(which_imgs):
                if img_data:
                    color = possible_colors[i]
                    color_to_label_mapping[str(color)] = relevant_categories[i]
                    output_image.putpixel((x, y), color)  # Set pixel to that color
                    break

    return output_image, color_to_label_mapping

def generate_seg_img(img_path):
    img = Image.open(img_path)
    semantic_segmentation = pipeline("image-segmentation", "nvidia/segformer-b0-finetuned-ade-512-512")
    results = semantic_segmentation(img)
    print(results)

    fig, ax = plt.subplots()

    ax.set_axis_off()
    # ax.imshow(img, aspect='auto')
    total_objects = [x['label'] for x in results]
    relevant_categories = get_relevant_objects(total_objects)
    imgs_to_combine = []
    for x in results:
        if x["label"] in relevant_categories:
            imgs_to_combine.append(x["mask"])
    
    new_img, mapping = combine_images(imgs_to_combine, relevant_categories)
    ax.imshow(new_img, alpha=0.5, aspect='auto')

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
    plt.savefig('output.png')
    plt.axis('off')  # Hide the axis

    return mapping

# generate_seg_img("first_frame.png")
