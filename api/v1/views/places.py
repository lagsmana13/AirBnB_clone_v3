#!/usr/bin/python3
"""locations"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.district import District
from models.property import Property
from datetime import datetime
import uuid


@app_views.route('/districts/<district_id>/properties', methods=['GET'])
@app_views.route('/districts/<district_id>/properties/', methods=['GET'])
def list_properties_of_district(district_id):
    '''Retrieves a list of all Property objects in the district'''
    all_districts = storage.all("District").values()
    district_obj = [obj.to_dict() for obj in all_districts if obj.id == district_id]
    if district_obj == []:
        abort(404)
    list_properties = [obj.to_dict() for obj in storage.all("Property").values()
                   if district_id == obj.district_id]
    return jsonify(list_properties)


@app_views.route('/properties/<property_id>', methods=['GET'])
def get_property(property_id):
    '''Retrieves a Property object'''
    all_properties = storage.all("Property").values()
    property_obj = [obj.to_dict() for obj in all_properties if obj.id == property_id]
    if property_obj == []:
        abort(404)
    return jsonify(property_obj[0])


@app_views.route('/properties/<property_id>', methods=['DELETE'])
def delete_property(property_id):
    '''Deletes a Property object'''
    all_properties = storage.all("Property").values()
    property_obj = [obj.to_dict() for obj in all_properties
                 if obj.id == property_id]
    if property_obj == []:
        abort(404)
    property_obj.remove(property_obj[0])
    for obj in all_properties:
        if obj.id == property_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/districts/<district_id>/properties', methods=['POST'])
def create_property(district_id):
    '''Creates a Property'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_districts = storage.all("District").values()
    district_obj = [obj.to_dict() for obj in all_districts
                if obj.id == district_id]
    if district_obj == []:
        abort(404)
    properties = []
    new_property = Property(name=request.json['name'],
                      user_id=request.json['user_id'], district_id=district_id)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == new_property.user_id]
    if user_obj == []:
        abort(404)
    storage.new(new_property)
    storage.save()
    properties.append(new_property.to_dict())
    return jsonify(properties[0]), 201


@app_views.route('/properties/<property_id>', methods=['PUT'])
def update_property(property_id):
    '''Updates a Property object'''
    all_properties = storage.all("Property").values()
    property_obj = [obj.to_dict() for obj in all_properties if obj.id == property_id]
    if property_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' in request.get_json():
        property_obj[0]['name'] = request.json['name']
    if 'description' in request.get_json():
        property_obj[0]['description'] = request.json['description']
    if 'number_rooms' in request.get_json():
        property_obj[0]['number_rooms'] = request.json['number_rooms']
    if 'number_bathrooms' in request.get_json():
        property_obj[0]['number_bathrooms'] = request.json['number_bathrooms']
    if 'max_guest' in request.get_json():
        property_obj[0]['max_guest'] = request.json['max_guest']
    if 'price_per_night' in request.get_json():
        property_obj[0]['price_per_night'] = request.json['price_per_night']
    if 'latitude' in request.get_json():
        property_obj[0]['latitude'] = request.json['latitude']
    if 'longitude' in request.get_json():
        property_obj[0]['longitude'] = request.json['longitude']
    for obj in all_properties:
        if obj.id == property_id:
            if 'name' in request.get_json():
                obj.name = request.json['name']
            if 'description' in request.get_json():
                obj.description = request.json['description']
            if 'number_rooms' in request.get_json():
                obj.number_rooms = request.json['number_rooms']
            if 'number_bathrooms' in request.get_json():
                obj
