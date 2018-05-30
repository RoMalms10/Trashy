#!/usr/bin/python3
"""
Flask App that handles API requests and redirects
"""
from flask import Flask, render_template, url_for
from flask import jsonify
from models import storage

# Flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'

@app.route('/')
def landing_page():
    """
    Render the landing page
    """
    return render_template('index.html')

@app.route('/map')
def render_map_page():
    """
    Serve the map webpage
    """
    return render_template('map.html')

@app.route('/api/bins')
def get_bins():
    """
    Gets all of the bin info from csv file
    """
    from models import storage

    trash_list = []
    obj_dict = storage.all()
    for key, value in obj_dict.items():
        trash_list.append(value.to_dict())
    return jsonify(trash_list)

if __name__ == "__main__":
    app.run(host=host, port=port)
