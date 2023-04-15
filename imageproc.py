#!/usr/bin/env python3

import os
import cv2
import numpy as np


def increase_contrast(image, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def blur_image(image, kernel_size=(5, 5)):
    return cv2.GaussianBlur(image, kernel_size, 0)


def sharpen_image(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)


def perspective_transform(image, src_points, dst_points):
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    return cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))


def on_alpha_trackbar(val):
    global alpha
    alpha = val / 100


def on_beta_trackbar(val):
    global beta
    beta = val


def on_threshold_trackbar(val):
    global threshold
    threshold = val


leaway = 10
width = 160
height = 65


def process_image(image, alpha, beta, threshold):
    x1, y1 = (218 - leaway, 277 - leaway)
    x2, y2 = (393 + leaway, 273 - leaway)
    x3, y3 = (219 - leaway, 345 + leaway)
    x4, y4 = (393 + leaway, 335 + leaway)

    # Define source and destination points for perspective transform
    src_points = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])  # Replace these with the actual coordinates
    dst_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Apply perspective transform
    transformed_image = perspective_transform(image, src_points, dst_points)

    # Denoise using Non-Local Means Denoising
    denoised_image = cv2.fastNlMeansDenoising(transformed_image, None, h=threshold, templateWindowSize=15,
                                              searchWindowSize=15)

    # Threshold
    # _, threshold_image = cv2.threshold(denoised_image, threshold, 255, cv2.THRESH_TOZERO)

    # Increase contrast[0:height, 0:width+20]
    # contrast_image = increase_contrast(denoised_image, alpha, beta)

    clahe = cv2.createCLAHE(clipLimit=alpha, tileGridSize=(beta, beta))
    clahe_image = clahe.apply(denoised_image)

    # Apply Gaussian blur
    sharpened_image = sharpen_image(clahe_image)

    return sharpened_image


def generate_image(filepath):
    global alpha, beta, threshold
    alpha, beta, threshold = 2.5, 16, 3

    # Read the input image
    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

    directory, filename = os.path.split(filepath)
    new_filename = f"postproc-{filename.lstrip('preproc-')}"  # noqa
    new_filepath = os.path.join(directory, new_filename)

    print(f"Processing image at {filepath}")
    cv2.imwrite(f'{new_filepath}',
                process_image(image, alpha, beta, threshold)[0:height + leaway * 2, 0:width + 2 * leaway])
    print("Image processed!")


if __name__ == '__main__':
    generate_image("/var/www/power_monitoring/images/latest.jpg")
