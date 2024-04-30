#!/usr/bin/python3
"""amenities_places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    @app_views.route('/amenities/<amenity_id>/places', methods=['GET'])
    @app_views.route('/amenities/<amenity_id>/places/', methods=['GET'])
    def list_places_of_amenity(amenity_id):
        ''' Retrieves a list of all Place objects of an Amenity '''
        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)
        list_places = []
        for obj in all_amenities:
            if obj.id == amenity_id:
                for place in obj.places:
                    list_places.append(place.to_dict())
        return jsonify(list_places)

    @app_views.route('/amenities/<amenity_id>/places/<place_id>', methods=['POST'])
    def create_amenity_place(amenity_id, place_id):
        '''Creates a Place'''
        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        places = []
        for amenity in all_amenities:
            if amenity.id == amenity_id:
                for place in all_places:
                    if place.id == place_id:
                        amenity.places.append(place)
                        storage.save()
                        places.append(place.to_dict())
                        return jsonify(places[0]), 200
        return jsonify(places[0]), 201

    @app_views.route('/amenities/<amenity_id>/places/<place_id>', methods=['DELETE'])
    def delete_amenity_place(amenity_id, place_id):
        '''Deletes a Place object'''
        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)
        place_obj.remove(place_obj[0])

        for obj in all_amenities:
            if obj.id == amenity_id:
                if obj.places == []:
                    abort(404)
                for place in obj.places:
                    if place.id == place_id:
                        storage.delete(place)
                        storage.save()
        return jsonify({}), 200
else:
    @app_views.route('/amenities/<amenity_id>/places', methods=['GET'])
    @app_views.route('/amenities/<amenity_id>/places/', methods=['GET'])
    def list_places_of_amenity(amenity_id):
        ''' Retrieves a list of all Place objects of an Amenity '''
        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)
        list_places = []
        for obj in all_amenities:
            if obj.id == amenity_id:
                for place in obj.places:
                    list_places.append(place.to_dict())
        return jsonify(list_places)

    @app_views.route('/amenities/<amenity_id>/places/<place_id>', methods=['POST'])
    def create_amenity_place(amenity_id, place_id):
        '''Creates a Place'''
        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        places = []
        for amenity in all_amenities:
            if amenity.id == amenity_id:
                for place in all_places:
                    if place.id == place_id:
                        amenity.places.append(place)
                        storage.save()
                        places.append(place.to_dict())
                        return jsonify(places[0]), 200
        return jsonify(places[0]), 201

    @app_views.route('/amenities/<amenity_id>/places/<place_id>', methods=['DELETE'])
    def delete_amenity_place(amenity_id, place_id):
        '''Deletes a Place object'''
        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)
        place_obj.remove(place_obj[0])

        for obj in all_amenities:
            if obj.id == amenity_id:
                if obj.places == []:
                    abort(404)
                for place in obj.places:
                    if place.id == place_id:
                        storage.delete(place)
                        storage.save()
        return jsonify({}), 200

if __name__ == "__main__":
    pass
