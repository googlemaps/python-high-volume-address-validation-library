"""Tests for the addressvalidation module."""

#import responses

import os
import sys
import googlemaps
import unittest
#from . import TestCase
# importing the module
import json

from av_result_parser import av_result_parser_class
import config_loader
 
# Opening JSON file
with open(os.path.join(sys.path[0],'tests/google_ny_response_test_data.json')) as json_file:
    av_response_data = json.load(json_file)
 
    # Print the type of data variable
    print("Type:", type(av_response_data))

config =config_loader.Config()
#Create a client of the googleMaps client library

#gmaps = googlemaps.Client(key=config.api_key)

av_result_parser_load=av_result_parser_class()

parsed_response=av_result_parser_load.parse_av_response(av_response_data)
print('::::::::::::::::::::::::::;;')
print('The final response after parsing from the test class is::')
print(parsed_response)