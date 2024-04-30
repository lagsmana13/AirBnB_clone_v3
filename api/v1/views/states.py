#!/usr/bin/python3
"""countries"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.country import Country
from datetime import datetime
import uuid


@app_views.route('/countries/', methods=['GET'])
def list_countries():
    '''Retrieves a list of all Country objects'''
    list_countries = [obj.to_dict() for obj in storage.all("Country").values()]
    return jsonify(list_countries)


@app_views.route('/countries/<country_id>', methods=['GET'])
def get_country(country_id):
    '''Retrieves a Country object'''
    all_countries = storage.all("Country").values()
    country_obj = [obj.to_dict() for obj in all_countries if obj.id == country_id]
    if country_obj == []:
        abort(404)
    return jsonify(country_obj[0])


@app_views.route('/countries/<country_id>', methods=['DELETE'])
def delete_country(country_id):
    '''Deletes a Country object'''
    all_countries = storage.all("Country").values()
    country_obj = [obj.to_dict() for obj in all_countries if obj.id == country_id]
    if country_obj == []:
        abort(404)
    country_obj.remove(country_obj[0])
    for obj in all_countries:
        if obj.id == country_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/countries/', methods=['POST'])
def create_country():
    '''Creates a Country'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    countries = []
    new_country = Country(name=request.json['name'])
    storage.new(new_country)
    storage.save()
    countries.append(new_country.to_dict())
    return jsonify(countries[0]), 201


@app_views.route('/countries/<country_id>', methods=['PUT'])
def updates_country(country_id):
    '''Updates a Country object'''
    all_countries = storage.all("Country").values()
    country_obj = [obj.to_dict() for obj in all_countries if obj.id == country_id]
    if country_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    country_obj[0]['name'] = request.json['name']
    for obj in all_countries:
        if obj.id == country_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(country_obj[0]), 200
