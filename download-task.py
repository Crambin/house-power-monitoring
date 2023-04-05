#!/usr/bin/env python3

import os
import requests
from datetime import datetime
from imageproc import generate_image


images_dir = "/var/www/power_monitoring/images/"
latest_image_link = "/var/www/power_monitoring/images/latest.jpg"


def download_image():
    camera_ip = os.environ.get('CAMERA_IP', "192.168.1.164")
    url = f"http://{camera_ip}/capture"
    response = requests.get(url)
    if response.status_code != 200:  # noqa
        print(f"Failed to get image. Status code: {response.status_code}")
        return

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"preproc-{timestamp}.jpg"
    filepath = os.path.join(images_dir, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    # Create a symbolic link to the latest image file
    if os.path.exists(latest_image_link):
        os.unlink(latest_image_link)
    os.symlink(filepath, latest_image_link)

    print("Image saved successfully!")
    return filepath


filepath = download_image()
generate_image(filepath)
