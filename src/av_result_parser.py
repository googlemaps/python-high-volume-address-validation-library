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
                
            # Check to see if result component contains verdict. Verdict contains the overall quality indicators, and should always be stored    
            # If running in test mode (run mode 1), allow the application to store some data to understand Address Validation API response     
            #  Test Mode: 1
            #  Production mode -Users: 2
            #  Production mode -NoUsers: 3

        if run_mode == 1:
                
            #Check to see if the address object is within the result 
            #Add the formatted address to the parsed result dict   
            #Check to see if the address lines are in the address objet
            parsed_result["output_verdict"]=av_result_parser_class.get_verdict(address_validation_result,parsed_result)
            parsed_result["output_formatted_address"]=av_result_parser_class.get_formatted_address(address_validation_result,parsed_result)
            parsed_result["output_spell_corrected"]=av_result_parser_class.get_spell_corrected(address_validation_result,parsed_result)
            parsed_result["output_postal_address"]=av_result_parser_class.get_postal_address(address_validation_result,parsed_result)
            parsed_result["output_place_ID"]=av_result_parser_class.get_place_ID(address_validation_result,parsed_result)
            parsed_result["output_latlong"]=av_result_parser_class.get_latlong(address_validation_result,parsed_result)
            parsed_result["output_usps_data"]=av_result_parser_class.get_usps_data(address_validation_result,parsed_result)

            #    
            # If running in Production mode -Users, allow the application to ONLY store formatted address, Place ID, verdict
            # address components, spell correction
            # 
           
        if run_mode == 2:

            parsed_result["output_verdict"]=av_result_parser_class.get_verdict(address_validation_result,parsed_result)
            parsed_result["output_formatted_address"]=av_result_parser_class.get_formatted_address(address_validation_result,parsed_result)
            parsed_result["output_spell_corrected"]=av_result_parser_class.get_spell_corrected(address_validation_result,parsed_result)
            parsed_result["output_postal_address"]=av_result_parser_class.get_postal_address(address_validation_result,parsed_result)
            parsed_result["output_place_ID"]=av_result_parser_class.get_place_ID(address_validation_result,parsed_result)
            parsed_result["output_latlong"]=av_result_parser_class.get_latlong(address_validation_result,parsed_result)
            
            #    
            # If running in Production mode -No Users, allow the application to store Place ID
            # 
        if run_mode == 3:

           parsed_result["output_place_ID"]=av_result_parser_class.get_place_ID(address_validation_result,parsed_result)

           


        print("The dict with all the extracted elemnts is ready")
        print(parsed_result)
        return parsed_result


    def get_place_ID(address_validation_result,parsed_result):
    #
    # Check if response have geocode and placeID and store it in the parsed_result
    # object
    #
        if "geocode" in address_validation_result["result"]:
            if "placeId" in address_validation_result["result"]["geocode"]:
                return address_validation_result["result"]["geocode"]["placeId"]

    def get_formatted_address(address_validation_result,parsed_result):
         
        if "address" in address_validation_result["result"]:
                   
                    #Add the formatted address to the parsed result dict
                    if "formattedAddress" in address_validation_result["result"]["address"]:
                        return address_validation_result["result"]["address"]["formattedAddress"]
        

    def get_verdict(address_validation_result,parsed_result):
        if "result" in address_validation_result:
            
            # Check to see if result component contains verdict. Verdict contains the overall quality indicators, and should always be stored
            if "verdict" in address_validation_result["result"]:
            
                #Loop through the result object and add componens to the parsed result dict 
                for key in address_validation_result["result"]["verdict"].keys():
                    return address_validation_result["result"]["verdict"][key]

    def get_latlong(address_validation_result,parsed_result):
        latlong_dict={}
        if "location" in address_validation_result["result"]["geocode"]:
                if "latitude" in address_validation_result["result"]["geocode"]["location"]:
                    latlong_dict["latitude"] = address_validation_result["result"]["geocode"]["location"]["latitude"]
                if "longitude" in address_validation_result["result"]["geocode"]["location"]:
                    latlong_dict["longitude"] = address_validation_result["result"]["geocode"]["location"]["longitude"]
        return latlong_dict

    def get_spell_corrected(address_validation_result,parsed_result):
        if "addressComponents" in address_validation_result["result"]["address"]:
                        for address_component in address_validation_result["result"]["address"]["addressComponents"]:
                            for spell_corrected in address_component:
                                if spell_corrected == "spellCorrected":
                                    return address_component[spell_corrected]
    
    def get_postal_address(address_validation_result,parsed_result):
       
        if "postalAddress" in address_validation_result["result"]["address"]:
                for k in address_validation_result["result"]["address"]["postalAddress"]:
                    if k == "addressLines":
                        addressLineCounter = 1
                        for al in address_validation_result["result"]["address"]["postalAddress"][k]:
                            parsed_result["addressLine" + str(addressLineCounter)] = al
                            addressLineCounter += 1
                            continue
                        return address_validation_result["result"]["address"]["postalAddress"][k]
    
    def get_usps_data(address_validation_result,parsed_result):
        
                """_summary_ : [USA Only] Store additional addresss metadata from 
                USPS dataset

        Args:
            address_validation_result (_type_): _description_
            parsed_result (_type_): _description_

        Returns:
            _type_: _description_
        """  

                if "metadata" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["metadata"].keys():
                        parsed_result[k] = address_validation_result["result"]["metadata"][k]
               
                # [USA Only] Check to see if uspsData component exists
                if "uspsData" in address_validation_result["result"]:
                    for k in address_validation_result["result"]["uspsData"].keys():
               
                    # [USA Only] Store the postal service standardized address
                        if k == "standardizedAddress":
                            for sa in address_validation_result["result"]["uspsData"]["standardizedAddress"].keys():
                                parsed_result[sa] = address_validation_result["result"]["uspsData"]["standardizedAddress"][sa]
                            continue
               
                        # [USA Only] Store the USPS data
                        return address_validation_result["result"]["uspsData"][k]
                #return parsed_result        