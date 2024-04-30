#!/usr/bin/python3
"""Interests"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.interest import Interest
from datetime import datetime
import uuid


@app_views.route('/interests/', methods=['GET'])
def list_interests():
    '''Retrieves a list of all Interest objects'''
    list_interests = [obj.to_dict() for obj in storage.all("Interest").values()]
    return jsonify(list_interests)


@app_views.route('/interests/<interest_id>', methods=['GET'])
def get_interest(interest_id):
    '''Retrieves an Interest object'''
    all_interests = storage.all("Interest").values()
    interest_obj = [obj.to_dict() for obj in all_interests
                   if obj.id == interest_id]
    if interest_obj == []:
        abort(404)
    return jsonify(interest_obj[0])


@app_views.route('/interests/<interest_id>', methods=['DELETE'])
def delete_interest(interest_id):
    '''Deletes an Interest object'''
    all_interests = storage.all("Interest").values()
    interest_obj = [obj.to_dict() for obj in all_interests
                   if obj.id == interest_id]
    if interest_obj == []:
        abort(404)
    interest_obj.remove(interest_obj[0])
    for obj in all_interests:
        if obj.id == interest_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/interests/', methods=['POST'])
def create_interest():
    '''Creates an Interest'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    interests = []
    new_interest = Interest(name=request.json['name'])
    storage.new(new_interest)
    storage.save()
    interests.append(new_interest.to_dict())
    return jsonify(interests[0]), 201


@app_views.route('/interests/<interest_id>', methods=['PUT'])
def update_interest(interest_id):
    '''Updates an Interest object'''
    all_interests = storage.all("Interest").values()
    interest_obj = [obj.to_dict() for obj in all_interests
                   if obj.id == interest_id]
    if interest_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    interest_obj[0]['name'] = request.json['name']
    for obj in all_interests:
        if obj.id == interest_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(interest_obj[0]), 200
