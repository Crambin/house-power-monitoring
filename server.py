#!/usr/bin/env python3

import os
from flask import Flask, abort, send_file


app = Flask(__name__)
latest_image_link = "/var/www/power_monitoring/images/latest.jpg"


@app.route('/image', methods=['GET'])
def get_image():
    if not os.path.exists(latest_image_link):
        return abort(404, "Latest image not found on this server.")

    send_file(latest_image_link, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
