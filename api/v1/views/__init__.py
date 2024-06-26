#!/usr/bin/python3
"""Blueprint creation"""
from flask import Blueprint

app_views = Blueprint('app_views', name, url_prefix='/api/v1')

if app_views is not None:
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.reviews import *
from api.v1.views.places_amenities import *
