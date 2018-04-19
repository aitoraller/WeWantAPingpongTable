import cv2

def resize_image(image, max_size=640):
    image_resized = image.copy()
    height, width = image.shape[0:2]
    scale = 1
    if height > max_size or width > max_size:
        scale = float(max_size) / max([height, width])
        image_resized = cv2.resize(image, None, fx=scale, fy=scale)

    return image_resized, scale