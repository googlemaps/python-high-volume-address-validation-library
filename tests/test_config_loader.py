# This Python file uses the following encoding: utf-8
#
# Copyright 2022 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Tests for the addressvalidation module."""

#import responses

import googlemaps
#from . import TestCase
import unittest
import sys
# sys.path.append('../tests')

from test_config_loader import config

class ConfigLoaderTest(unittest.TestCase):
    def setUp(self):
        self.key = 'YOUR_API_KEY'
        self.client = googlemaps.Client(self.key)

   
    def test_yaml_loader(self):
        default_address_file = "./addresses.csv"
        self.assertEqual(config.address_file, default_address_file)
        print("assert is equalled")