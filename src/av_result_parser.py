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
#from config_loader import config
import config_loader

config =config_loader.Config()

class av_result_parser_class:

    def av_parse(self, addressvalidation_result):
        #print(addressvalidation_result)
        """_summary_

        Args:
            addressvalidation_result (_type_): _description_

        Returns:
            _type_: _description_
        """        

        run_mode = config.run_mode

        parsedResult = dict()
        # Check to see if Response object contains top level result component
        if "result" in addressvalidation_result:
            # Check to see if result component contains verdict. Verdict contains the overall quality indicators, and should always be stored
            if "verdict" in addressvalidation_result["result"]:
                for k in addressvalidation_result["result"]["verdict"].keys():
                    parsedResult[k] = addressvalidation_result["result"]["verdict"][k]

            #    
            # If running in test mode, allow the application to store some data to understand Address Validation API response     
            # 
            if run_mode == 1:
                if "address" in addressvalidation_result["result"]:
                    if "formattedAddress" in addressvalidation_result["result"]["address"]:
                        parsedResult["formattedAddress"] = addressvalidation_result["result"]["address"]["formattedAddress"]

                    if "postalAddress" in addressvalidation_result["result"]["address"]:
                        for k in addressvalidation_result["result"]["address"]["postalAddress"]:
                            if k == "addressLines":
                                addressLineCounter = 1
                                for al in addressvalidation_result["result"]["address"]["postalAddress"][k]:
                                    parsedResult["addressLine" + str(addressLineCounter)] = al
                                    addressLineCounter += 1
                                continue
                            parsedResult[k] = addressvalidation_result["result"]["address"]["postalAddress"][k]
                if "geocode" in addressvalidation_result["result"]:
                    # Always store the Place ID
                    if "placeId" in addressvalidation_result["result"]["geocode"]:
                        parsedResult["placeId"] = addressvalidation_result["result"]["geocode"]["placeId"]
                    
                    if run_mode == 1:
                        # Only store the lat/lng if running in test mode 
                        if "location" in addressvalidation_result["result"]["geocode"]:
                            if "latitude" in addressvalidation_result["result"]["geocode"]["location"]:
                                parsedResult["latitude"] = addressvalidation_result["result"]["geocode"]["location"]["latitude"]
                            if "longitude" in addressvalidation_result["result"]["geocode"]["location"]:
                                parsedResult["longitude"] = addressvalidation_result["result"]["geocode"]["location"]["longitude"]
                # [USA Only] Store additional addresss metadata
                if "metadata" in addressvalidation_result["result"]:
                    for k in addressvalidation_result["result"]["metadata"].keys():
                        parsedResult[k] = addressvalidation_result["result"]["metadata"][k]
                # [USA Only] Check to see if uspsData componant exists
                if "uspsData" in addressvalidation_result["result"]:
                    for k in addressvalidation_result["result"]["uspsData"].keys():
                    # [USA Only] Store the postal service standardized address
                        if k == "standardizedAddress":
                            for sa in addressvalidation_result["result"]["uspsData"]["standardizedAddress"].keys():
                                parsedResult[sa] = addressvalidation_result["result"]["uspsData"]["standardizedAddress"][sa]
                            continue
                        # [USA Only] Store the USPS data
                        parsedResult[k] = addressvalidation_result["result"]["uspsData"][k]

            #    
            # If running in Production mode -NoUsers, allow the application to ONLY store formatted address, Place ID, verdict
            # 
            if run_mode == 2:
                if "address" in addressvalidation_result["result"]:
                    if "formattedAddress" in addressvalidation_result["result"]["address"]:
                        parsedResult["formattedAddress"] = addressvalidation_result["result"]["address"]["formattedAddress"]

                    if "postalAddress" in addressvalidation_result["result"]["address"]:
                        for k in addressvalidation_result["result"]["address"]["postalAddress"]:
                            if k == "addressLines":
                                addressLineCounter = 1
                                for al in addressvalidation_result["result"]["address"]["postalAddress"][k]:
                                    parsedResult["addressLine" + str(addressLineCounter)] = al
                                    addressLineCounter += 1
                                continue
                            parsedResult[k] = addressvalidation_result["result"]["address"]["postalAddress"][k]
                if "geocode" in addressvalidation_result["result"]:
                    # Always store the Place ID
                    if "placeId" in addressvalidation_result["result"]["geocode"]:
                        parsedResult["placeId"] = addressvalidation_result["result"]["geocode"]["placeId"]
                    
                    if run_mode == 2:
                        # Only store the lat/lng if running in test mode 
                        if "location" in addressvalidation_result["result"]["geocode"]:
                            if "latitude" in addressvalidation_result["result"]["geocode"]["location"]:
                                parsedResult["latitude"] = addressvalidation_result["result"]["geocode"]["location"]["latitude"]
                            if "longitude" in addressvalidation_result["result"]["geocode"]["location"]:
                                parsedResult["longitude"] = addressvalidation_result["result"]["geocode"]["location"]["longitude"]
                # [USA Only] Store additional addresss metadata
                if "metadata" in addressvalidation_result["result"]:
                    for k in addressvalidation_result["result"]["metadata"].keys():
                        parsedResult[k] = addressvalidation_result["result"]["metadata"][k]
                # [USA Only] Check to see if uspsData componant exists
                if "uspsData" in addressvalidation_result["result"]:
                    for k in addressvalidation_result["result"]["uspsData"].keys():
                    # [USA Only] Store the postal service standardized address
                        if k == "standardizedAddress":
                            for sa in addressvalidation_result["result"]["uspsData"]["standardizedAddress"].keys():
                                parsedResult[sa] = addressvalidation_result["result"]["uspsData"]["standardizedAddress"][sa]
                            continue
                        # [USA Only] Store the USPS data
                        parsedResult[k] = addressvalidation_result["result"]["uspsData"][k]


            #    
            # If running in Production mode -Users, allow the application to store formatted address, Place ID, verdict, address components spell correction
            # 
            if run_mode == 3:
                if "address" in addressvalidation_result["result"]:
                    if "formattedAddress" in addressvalidation_result["result"]["address"]:
                        parsedResult["formattedAddress"] = addressvalidation_result["result"]["address"]["formattedAddress"]

                    # Spell correction flag
                    if "addressComponents" in addressvalidation_result["result"]["address"]:
                        for x in addressvalidation_result["result"]["address"]["addressComponents"]:
                            for sc in x:
                                # print(sc)
                                if sc == "spellCorrected":
                                    # print("####################################addressComponents")
                                    parsedResult["spellCorrected"] = x[sc]
                            #         print("spellCorrected")

                    if "postalAddress" in addressvalidation_result["result"]["address"]:
                        for k in addressvalidation_result["result"]["address"]["postalAddress"]:
                            if k == "addressLines":
                                addressLineCounter = 1
                                for al in addressvalidation_result["result"]["address"]["postalAddress"][k]:
                                    parsedResult["addressLine" + str(addressLineCounter)] = al
                                    addressLineCounter += 1
                                continue
                            parsedResult[k] = addressvalidation_result["result"]["address"]["postalAddress"][k]
                if "geocode" in addressvalidation_result["result"]:
                    # Always store the Place ID
                    if "placeId" in addressvalidation_result["result"]["geocode"]:
                        parsedResult["placeId"] = addressvalidation_result["result"]["geocode"]["placeId"]
                    
                    if run_mode == 3:
                        # Only store the lat/lng if running in test mode 
                        if "location" in addressvalidation_result["result"]["geocode"]:
                            if "latitude" in addressvalidation_result["result"]["geocode"]["location"]:
                                parsedResult["latitude"] = addressvalidation_result["result"]["geocode"]["location"]["latitude"]
                            if "longitude" in addressvalidation_result["result"]["geocode"]["location"]:
                                parsedResult["longitude"] = addressvalidation_result["result"]["geocode"]["location"]["longitude"]
                # [USA Only] Store additional addresss metadata
                if "metadata" in addressvalidation_result["result"]:
                    for k in addressvalidation_result["result"]["metadata"].keys():
                        parsedResult[k] = addressvalidation_result["result"]["metadata"][k]
                # [USA Only] Check to see if uspsData componant exists
                if "uspsData" in addressvalidation_result["result"]:
                    for k in addressvalidation_result["result"]["uspsData"].keys():
                    # [USA Only] Store the postal service standardized address
                        if k == "standardizedAddress":
                            for sa in addressvalidation_result["result"]["uspsData"]["standardizedAddress"].keys():
                                parsedResult[sa] = addressvalidation_result["result"]["uspsData"]["standardizedAddress"][sa]
                            continue
                        # [USA Only] Store the USPS data
                        parsedResult[k] = addressvalidation_result["result"]["uspsData"][k]

        print("The dict with all the extracted elemnts is ready")
        print(parsedResult)
        return parsedResult