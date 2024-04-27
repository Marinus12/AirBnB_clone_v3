#!/usr/bin/python3
"""Views for llinking Place objects and Amenity objects"""

from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves all Amenity objects linked to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = []
    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    elif storage.__class__.__name__ == 'FileStorage':
        amenities = []
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place_amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()

    return make_response({}, 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Link an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity_id in place_amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
