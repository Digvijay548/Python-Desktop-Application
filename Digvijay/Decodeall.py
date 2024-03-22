from PIL import Image, ImageDraw
import numpy as np
from pypylon import pylon
import pylibdmtx.pylibdmtx as dmtx
 
# Function to decode barcodes and draw rectangles
import time
import numpy as np
from PIL import Image, ImageDraw
import pylibdmtx.pylibdmtx as dmtx

import time
import numpy as np
from PIL import Image, ImageDraw
import pylibdmtx.pylibdmtx as dmtx

def decode_and_draw(image_data, num_barcodes_to_find, decoded_values, modified_image=None, timeout_ms=700):
    start_time = time.time()
    while True:
        # Check if timeout has occurred
        if (time.time() - start_time) * 1000 > timeout_ms:
            return None, decoded_values  # Return None as image and the decoded values so far

        # Convert image data to numpy array
        image_np = np.frombuffer(image_data, dtype=np.uint8)

        # If modified_image is None, load image from image_path, otherwise use modified_image
        if modified_image is None:
            image = Image.fromarray(image_np)
        else:
            image = modified_image

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Decode barcodes from the image
        codes = dmtx.decode(image_np)

        # Iterate over decoded values
        for code in codes:
            decoded_value = code.data.decode('utf-8')

            # If the decoded value is not in the external list, add it and draw a rectangle
            if decoded_value not in decoded_values:
                decoded_values.append(decoded_value)
                bbox = code.rect
                draw.rectangle([bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]], outline='red')

                # If the number of decoded values is equal to the desired number, return
                if len(decoded_values) == num_barcodes_to_find:
                    return image, decoded_values

        # If the number of decoded values is not equal to the desired number, repeat the process
        if len(decoded_values) < num_barcodes_to_find:
            continue

        break  # Exit the loop if the desired number of barcodes is found

    return image, decoded_values
