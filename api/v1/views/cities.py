#!/usr/bin/python3
"""Towns"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.town import Town
from models.village import Village
from datetime import datetime
import uuid


@app_views.route('/villages/<village_id>/towns', methods=['GET'])
@app_views.route('/villages/<village_id>/towns/', methods=['GET'])
def list_towns_of_village(village_id):
    '''Retrieves a list of all Town objects'''
    all_villages = storage.all("Village").values()
    village_obj = [obj.to_dict() for obj in all_villages if obj.id == village_id]
    if village_obj == []:
        abort(404)
    list_towns = [obj.to_dict() for obj in storage.all("Town").values()
                   if village_id == obj.village_id]
    return jsonify(list_towns)


@app_views.route('/villages/<village_id>/towns', methods=['POST'])
@app_views.route('/villages/<village_id>/towns/', methods=['POST'])
def create_town(village_id):
    '''Creates a Town'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_villages = storage.all("Village").values()
    village_obj = [obj.to_dict() for obj in all_villages if obj.id == village_id]
    if village_obj == []:
        abort(404)
    towns = []
    new_town = Town(name=request.json['name'], village_id=village_id)
    storage.new(new_town)
    storage.save()
    towns.append(new_town.to_dict())
    return jsonify(towns[0]), 201


@app_views.route('/towns/<town_id>', methods=['GET'])
def get_town(town_id):
    '''Retrieves a Town object'''
    all_towns = storage.all("Town").values()
    town_obj = [obj.to_dict() for obj in all_towns if obj.id == town_id]
    if town_obj == []:
        abort(404)
    return jsonify(town_obj[0])


@app_views.route('/towns/<town_id>', methods=['DELETE'])
def delete_town(town_id):
    '''Deletes a Town object'''
    all_towns = storage.all("Town").values()
    town_obj = [obj.to_dict() for obj in all_towns if obj.id == town_id]
    if town_obj == []:
        abort(404)
    town_obj.remove(town_obj[0])
    for obj in all_towns:
        if obj.id == town_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/towns/<town_id>', methods=['PUT'])
def update_town(town_id):
    '''Updates a Town object'''
    all_towns = storage.all("Town").values()
    town_obj = [obj.to_dict() for obj in all_towns if obj.id == town_id]
    if town_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    town_obj[0]['name'] = request.json['name']
    for obj in all_towns:
        if obj.id == town_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(town_obj[0]), 200
