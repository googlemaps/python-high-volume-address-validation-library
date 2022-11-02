# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv

import config_loader

config =config_loader.Config()

class av_result_parser_class:

    def parse_av_response(self, address_validation_result):

        """_summary_

        Args:
            addressvalidation_result (_type_): _description_

        Returns:
            _type_: _description_
        """        

        run_mode = config.run_mode
        #Dict to store the parsed result
        parsed_result = dict()
        # Check to see if Response object contains top level result component
        if "result" in address_validation_result:
            # Check to see if result component contains verdict. Verdict contains the overall quality indicators, and should always be stored
            if "verdict" in address_validation_result["result"]:
                #Loop through the result object and add componens to the parsed result dict 
                for k in address_validation_result["result"]["verdict"].keys():
                    parsed_result[k] = address_validation_result["result"]["verdict"][k]

            #    
            # If running in test mode (run mode 1), allow the application to store some data to understand Address Validation API response     
            # 
            if run_mode == 1:
                #Check to see if the address ovject is within the result
                if "address" in address_validation_result["result"]:
                    #Add the formatted address to the parsed result dict
                    if "formattedAddress" in address_validation_result["result"]["address"]:
                        parsed_result["formattedAddress"] = address_validation_result["result"]["address"]["formattedAddress"]
                    #Check to see if the address lines are in the address objet
                    if "postalAddress" in address_validation_result["result"]["address"]:
                        #Loop through the address lines and add to the parsed result dict
                        for k in address_validation_result["result"]["address"]["postalAddress"]:
                            if k == "addressLines":
                                #There can be n number of address lines. Loop though adn add these to the parsed result dict
                                addressLineCounter = 1
                                for al in address_validation_result["result"]["address"]["postalAddress"][k]:
                                    parsed_result["addressLine" + str(addressLineCounter)] = al
                                    addressLineCounter += 1
                                continue
                            parsed_result[k] = address_validation_result["result"]["address"]["postalAddress"][k]
                if "geocode" in address_validation_result["result"]:
                    # Always store the Place ID
                    if "placeId" in address_validation_result["result"]["geocode"]:
                        parsed_result["placeId"] = address_validation_result["result"]["geocode"]["placeId"]
                    
                    if run_mode == 1:
                        # Only store the lat/lng if running in test mode (run mode 1)
                        if "location" in address_validation_result["result"]["geocode"]:
                            if "latitude" in address_validation_result["result"]["geocode"]["location"]:
                                parsed_result["latitude"] = address_validation_result["result"]["geocode"]["location"]["latitude"]
                            if "longitude" in address_validation_result["result"]["geocode"]["location"]:
                                parsed_result["longitude"] = address_validation_result["result"]["geocode"]["location"]["longitude"]
                # [USA Only] Store additional addresss metadata
                if "metadata" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["metadata"].keys():
                        parsed_result[k] = address_validation_result["result"]["metadata"][k]
                # [USA Only] Check to see if uspsData componant exists
                if "uspsData" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["uspsData"].keys():
                    # [USA Only] Store the postal service standardized address
                        if k == "standardizedAddress":
                            for sa in address_validation_result["result"]["uspsData"]["standardizedAddress"].keys():
                                parsed_result[sa] = address_validation_result["result"]["uspsData"]["standardizedAddress"][sa]
                            continue
                        # [USA Only] Store the USPS data
                        parsed_result[k] = address_validation_result["result"]["uspsData"][k]

            #    
            # If running in Production mode -NoUsers, allow the application to ONLY store formatted address, Place ID, verdict
            # 
            if run_mode == 2:
                if "address" in address_validation_result["result"]:
                    if "formattedAddress" in address_validation_result["result"]["address"]:
                        parsed_result["formattedAddress"] = address_validation_result["result"]["address"]["formattedAddress"]

                    if "postalAddress" in address_validation_result["result"]["address"]:
                        for k in address_validation_result["result"]["address"]["postalAddress"]:
                            if k == "addressLines":
                                addressLineCounter = 1
                                for al in address_validation_result["result"]["address"]["postalAddress"][k]:
                                    parsed_result["addressLine" + str(addressLineCounter)] = al
                                    addressLineCounter += 1
                                continue
                            parsed_result[k] = address_validation_result["result"]["address"]["postalAddress"][k]
                if "geocode" in address_validation_result["result"]:
                    # Always store the Place ID
                    if "placeId" in address_validation_result["result"]["geocode"]:
                        parsed_result["placeId"] = address_validation_result["result"]["geocode"]["placeId"]
                    
                    if run_mode == 2:
                        # Only store the lat/lng if running in test mode 
                        if "location" in address_validation_result["result"]["geocode"]:
                            if "latitude" in address_validation_result["result"]["geocode"]["location"]:
                                parsed_result["latitude"] = address_validation_result["result"]["geocode"]["location"]["latitude"]
                            if "longitude" in address_validation_result["result"]["geocode"]["location"]:
                                parsed_result["longitude"] = address_validation_result["result"]["geocode"]["location"]["longitude"]
                # [USA Only] Store additional addresss metadata
                if "metadata" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["metadata"].keys():
                        parsed_result[k] = address_validation_result["result"]["metadata"][k]
                # [USA Only] Check to see if uspsData componant exists
                if "uspsData" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["uspsData"].keys():
                    # [USA Only] Store the postal service standardized address
                        if k == "standardizedAddress":
                            for sa in address_validation_result["result"]["uspsData"]["standardizedAddress"].keys():
                                parsed_result[sa] = address_validation_result["result"]["uspsData"]["standardizedAddress"][sa]
                            continue
                        # [USA Only] Store the USPS data
                        parsed_result[k] = address_validation_result["result"]["uspsData"][k]


            #    
            # If running in Production mode -Users, allow the application to store formatted address, Place ID, verdict, address components spell correction
            # 
            if run_mode == 3:
                if "address" in address_validation_result["result"]:
                    if "formattedAddress" in address_validation_result["result"]["address"]:
                        parsed_result["formattedAddress"] = address_validation_result["result"]["address"]["formattedAddress"]

                    # Spell correction flag
                    if "addressComponents" in address_validation_result["result"]["address"]:
                        for x in address_validation_result["result"]["address"]["addressComponents"]:
                            for sc in x:
                                # print(sc)
                                if sc == "spellCorrected":
                                    # print("####################################addressComponents")
                                    parsed_result["spellCorrected"] = x[sc]
                            #         print("spellCorrected")

                    if "postalAddress" in address_validation_result["result"]["address"]:
                        for k in address_validation_result["result"]["address"]["postalAddress"]:
                            if k == "addressLines":
                                addressLineCounter = 1
                                for al in address_validation_result["result"]["address"]["postalAddress"][k]:
                                    parsed_result["addressLine" + str(addressLineCounter)] = al
                                    addressLineCounter += 1
                                continue
                            parsed_result[k] = address_validation_result["result"]["address"]["postalAddress"][k]
                if "geocode" in address_validation_result["result"]:
                    # Always store the Place ID
                    if "placeId" in address_validation_result["result"]["geocode"]:
                        parsed_result["placeId"] = address_validation_result["result"]["geocode"]["placeId"]
                    
                    if run_mode == 3:
                        # Only store the lat/lng if running in test mode 
                        if "location" in address_validation_result["result"]["geocode"]:
                            if "latitude" in address_validation_result["result"]["geocode"]["location"]:
                                parsed_result["latitude"] = address_validation_result["result"]["geocode"]["location"]["latitude"]
                            if "longitude" in address_validation_result["result"]["geocode"]["location"]:
                                parsed_result["longitude"] = address_validation_result["result"]["geocode"]["location"]["longitude"]
                # [USA Only] Store additional addresss metadata
                if "metadata" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["metadata"].keys():
                        parsed_result[k] = address_validation_result["result"]["metadata"][k]
                # [USA Only] Check to see if uspsData componant exists
                if "uspsData" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["uspsData"].keys():
                    # [USA Only] Store the postal service standardized address
                        if k == "standardizedAddress":
                            for sa in address_validation_result["result"]["uspsData"]["standardizedAddress"].keys():
                                parsed_result[sa] = address_validation_result["result"]["uspsData"]["standardizedAddress"][sa]
                            continue
                        # [USA Only] Store the USPS data
                        parsed_result[k] = address_validation_result["result"]["uspsData"][k]

        print("The dict with all the extracted elemnts is ready")
        print(parsed_result)
        return parsed_result