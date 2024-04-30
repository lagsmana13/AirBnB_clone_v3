#!/usr/bin/python3
"""home"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.customer import Customer
from models.property import Property
from models.region import Region
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"customers": "Customer", "properties": "Property", "regions": "Region",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    '''endpoint for status'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''retrieves the count of each object type'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
