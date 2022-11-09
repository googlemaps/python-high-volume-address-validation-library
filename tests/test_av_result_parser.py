"""Tests for the addressvalidation module."""

#import responses

import os
import sys
import unittest
import json
from os import path

#Append source directory of the class to be tested
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))
from av_result_parser import av_result_parser_class

NYC_GOOGLE_OFFICE_RESPONSE='google_ny_response_test_data.json'

# Opening JSON file
class Testing(unittest.TestCase):

    def parse_response():
        with open(os.path.join(sys.path[0],NYC_GOOGLE_OFFICE_RESPONSE)) as json_file:
            av_response_data = json.load(json_file)
 
        # Print the type of data variable
        print("Type:", type(av_response_data))
        av_result_parser_load=av_result_parser_class()

        parsed_response=av_result_parser_load.parse_av_response(av_response_data)
        print('The final response after parsing from the test class is::')
        print(parsed_response['output_place_ID'])
        return parsed_response

    def test_check(self):
        parsed_response=Testing.parse_response()
        #These are the hard coded values we are testing against
        expected_place_ID='ChIJz1X15L5ZwokR3HHMKxQ7Gtk'
        expected_locality='CONFIRMED|inferred'
        #Checking if place_id and locality string matches exactly
        self.assertEqual(parsed_response['output_place_ID'], expected_place_ID)
        self.assertEqual(parsed_response['output_address_components']['locality'], expected_locality)


if __name__ == '__main__':
    unittest.main()