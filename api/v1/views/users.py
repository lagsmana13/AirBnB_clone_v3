#!/usr/bin/python3
"""members"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.member import Member
from datetime import datetime
import uuid


@app_views.route('/members/', methods=['GET'])
@app_views.route('/members', methods=['GET'])
def list_members():
    '''Retrieves a list of all Member objects'''
    list_members = [obj.to_dict() for obj in storage.all("Member").values()]
    return jsonify(list_members)


@app_views.route('/members/<member_id>', methods=['GET'])
def get_member(member_id):
    '''Retrieves a Member object'''
    all_members = storage.all("Member").values()
    member_obj = [obj.to_dict() for obj in all_members if obj.id == member_id]
    if member_obj == []:
        abort(404)
    return jsonify(member_obj[0])


@app_views.route('/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    '''Deletes a Member object'''
    all_members = storage.all("Member").values()
    member_obj = [obj.to_dict() for obj in all_members if obj.id == member_id]
    if member_obj == []:
        abort(404)
    member_obj.remove(member_obj[0])
    for obj in all_members:
        if obj.id == member_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/members/', methods=['POST'])
def create_member():
    '''Creates a Member'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    members = []
    new_member = Member(email=request.json['email'],
                        password=request.json['password'])
    storage.new(new_member)
    storage.save()
    members.append(new_member.to_dict())
    return jsonify(members[0]), 201


@app_views.route('/members/<member_id>', methods=['PUT'])
def updates_member(member_id):
    '''Updates a Member object'''
    all_members = storage.all("Member").values()
    member_obj = [obj.to_dict() for obj in all_members if obj.id == member_id]
    if member_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        member_obj[0]['first_name'] = request.json['first_name']
    except:
        pass
    try:
        member_obj[0]['last_name'] = request.json['last_name']
    except:
        pass
    for obj in all_members:
        if obj.id == member_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except:
                pass
    storage.save()
    return jsonify(member_obj[0]), 200
