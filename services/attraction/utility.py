# Provide utility functions for attraction service
from PIL import Image
def resize_to_marker(img, size = 150):

    # find out the center and crop size
    crop_size = min(img.size[0], img.size[1])/2
    center_width = img.size[0] / 2
    center_height = img.size[1] / 2

    # crop the center of image
    img = img.crop(
        (
            center_width - crop_size,
            center_height - crop_size,
            center_width + crop_size,
            center_height + crop_size
        )
    )
    img.thumbnail([size, size],Image.ANTIALIAS)

    return img