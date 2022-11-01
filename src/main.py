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


#
# This is the main class and where the program starts
# This class is first going to call the method to load the csv
# csv is then parsed and loaded into a shelve object
# then another class starts calling the address validation API
# get the responses from it and update the shelve object
# FInal output is generated from the shelve object
#

import glob
import googlemaps
import os
import sys
# sys.path.append('./src')
#from config_loader import config
import config_loader
import shelve
from pathlib import Path
import read_write_addresses
from read_write_addresses import read_write_addressess_class
from av_result_parser import av_result_parser_class
import csv
import json


config =config_loader.Config()
#Create a client of the googleMaps client library

gmaps = googlemaps.Client(key=config.api_key)

av_result_parser_load=av_result_parser_class()

class HighVolumeAVMain: 

    def readAndStoreAddresses():
    # Read the csv file, parse it, construct the addresses
    # Insert the addresses in the persistant shelve object
        try:
            with read_write_addressess_class() as read_write_addressess_load:
                read_write_addressess_load.read_csv_with_addresses()
                return True
        except IndexError as ie:
            print(ie)
            print('Bad row reading csv')
    

    #
    # This functions checks if the load in the shelve object is accurate or not
    # This functions checks if the load in the shelve object is accurate or not
    # read_write_addressess_load.test_datastore()
    #


    def callAVApi():
        #
        # Call addressvalidation API with the addresses from shelves to validate the addresses
        # After validation store the address back in the shelve store
        #

        with shelve.open(config.shelve_db, 'c') as address_datastore:
        
            for key in address_datastore:
                addressvalidation_result = gmaps.addressvalidation(key)
                parsed_response=av_result_parser_load.av_parse(addressvalidation_result)
                address_datastore[key] = parsed_response
        return True

    def createExportCSV():
        # 
        # open the file in the write mode
        # read the shelve file
        # store the content back as CSV
        #

        with open(config.output_csv, 'w') as outputCSV:
            csvWriter = csv.writer(outputCSV)
            # Get the output headers from the config file
            header = config.output_columns
    
            csvWriter.writerow(header)
            with shelve.open(config.shelve_db) as addressShelve:
                
                print("===================================================")
               # print(json.dumps(dict(addressShelve), indent =4 ))
                for address in addressShelve.keys():

                    print("The address going to be inserted in the csv is "+str(address))

                 #   print("The address going to be inserted in the csv is"+str(address))
                    #Create an empty array to write a line to the CSV file
                    data = []
                    #Grab the input address
                    data.append(str(address))

                    for h in header:
                        #We already have the input address
                        if h == 'inputAddress':
                            continue
                        #Check to see if the relevent data exists in the shelf file
                        if h in addressShelve[address]:
                            data.append(addressShelve[address][h])
                        else:
                        #If not, write a blank cell
                            data.append('')
                        

                    # write a row to the csv file
                    csvWriter.writerow(data)

    def createExportJSON():
        # 
        # open the file in the write mode
        # read the shelve file
        # store the content back as JSON
        #

        with open(config.output_csv, 'w') as outputCSV:
            csvWriter = csv.writer(outputCSV)

            #Write the CSV headers to the file
           # header = ['inputAddress', 'inputGranularity', 'validationGranularity', 'geocodeGranularity', 'addressComplete', 'hasUnconfirmedComponents', 'hasInferredComponents', 'hasReplacedComponents', 'placeId', 'spellCorrected']
           # csvWriter.writerow(header)
            with shelve.open(config.shelve_db) as addressShelve:
                
                print("===================================================")
                outputJson=json.dumps(dict(addressShelve), indent =4 )
                return outputJson
                #print (outputJson)   

    def printDuplication():
        with open('duplicationReport.csv', 'w') as f:
                    for key in read_write_addresses.globalDuplicateCounter.keys():
                        f.write("%s,%s\n"%(key,read_write_addresses.globalDuplicateCounter[key]))

       # for key, value in read_write_addresses.globalDuplicateCounter.items():
           # if read_write_addresses.globalDuplicateCounter[x] !=1:
          #  print(key, ' : ', value)
               

    #
    # Delete the shelve file after it is done
    # By not doing this it creates a bug if this program is run multiple times from same computer
    # without changing the shelve file name
    #

    def teardown():
   
        for dbFile in Path(config.directory).glob('*.db'):
            try:
                dbFile.unlink()
                print("Unlinking file "+str(dbFile))
            except OSError as e:
                print("Error while deleting db files: %s : %s" % (dbFile, e.strerror))


#
#  The flow of events:
#  First: Read the addresses and store it in a shelve object
#  Second: Call the address Validation API by reading the addresses from the shelve
#  Third: Create the CSV from data stored in shelve
#  Clean up the project and the files it created
#   

try:
    (HighVolumeAVMain.readAndStoreAddresses() and HighVolumeAVMain.callAVApi())
    if config.output_format== "csv":

        HighVolumeAVMain.createExportCSV()

    elif config.output_format== "json":
        HighVolumeAVMain.createExportJSON()
    
    HighVolumeAVMain.printDuplication()
    HighVolumeAVMain.teardown()

except Exception as er:
    print("Error happened when calling the main functions")
    print(er)