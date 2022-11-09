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

#read_write_addresses.py
import csv
import shelve

#from config_loader import config
import config_loader

global global_duplicate_counter
global_duplicate_counter={}

config =config_loader.Config()

class read_write_addressess_class:

#currentAddressCounter
    

    def __enter__(self):
        return self

    def __init__ (self):

        self.column_numbers = config.column_numbers
        self.address_file = config.address_file
        self.address_datastore = shelve.open(config.shelve_db, 'n')
        self.separator = config.separator
        self.address_datastore.clear()

#
# Get a row object
# Get the columns which constitute the address in the input csv
# Address can be in one column or split across multiple columns
# Concatinate those address with comma in between
# Return the string address
#

    def build_address_string(self,row):

        current_row=""
        for index,column in enumerate(self.column_numbers):
            
            # we want to ensure we are not putting the separator at the end of the string
            # So here we are checking if it is the last element of the row and if yes, do 
            # not add the separtor at the end

            if (index < len(self.column_numbers)-1):
               # print("len is "+str(len(self.column_numbers)))
                #print("index is "+str(index))
                current_row+=str(row[column])+self.separator
                #print("current row is "+str(current_row))
            
            else:  
                current_row+=str(row[column])
        
        return current_row

#
# read the csv file
# Iterate through the file and extract each row
# Read the address component from the file
#

    def read_csv_with_addresses(self):
       
        # reading csv file
        with open(self.address_file, 'r') as csvfile:
        # creating a csv reader object
         
            csvreader = csv.reader(csvfile)
      
            # extracting field names through first row
     
            # extracting each data row one by one
            for row in csvreader:
                if(config.supplied_primary_key is None):
                    final_address=self.build_address_string(row)
                else:
                    final_address=self.build_address_string(row)

               # print("Key getting inserted in db is ",final_address )
                self.insert_addresses_in_ds(final_address)
       
            # get total number of rows
            #print(rows)
            print("Total no. of rows: %d"%(csvreader.line_num))        
 
    #
    # We want to insert the address in a datastore
    # We choose to insert in a shelve  object since it has a persistant
    # storage mechanism
    #       

    def insert_addresses_in_ds(self,final_address):

        print("Inside insert_addresses_in_ds::::  ",final_address)
       
        #try:
       # print("Hereeeee")
        current_address_counter=int()
        
        if final_address in self.address_datastore:
            print("Insside first big IF ############### If ")
           
            if final_address in global_duplicate_counter:
                print("############### Address already exiss",final_address)
                current_address_counter = global_duplicate_counter[final_address]
                nextCounter=current_address_counter+1
                global_duplicate_counter[final_address] = nextCounter
                print("Counter for ",final_address," is ",nextCounter)
            else:
                global_duplicate_counter[final_address] = 1
                print("The counter for ", final_address,"is ::",current_address_counter)
            
        else:
            print("In else block inserting ",final_address,"to DS and to dict")
            global_duplicate_counter[final_address] = 1
            self.address_datastore[final_address]={"Nothing"}

    # 
    # Close the connection to the shelve datastore
    # Do it before the class is destroyed 
    #    

    def __exit__(self, exc_type, exc_value, traceback):
        #self.address_datastore.sync()
        self.address_datastore.close()

    def test_datastore(self):
        
        my_keys = list(self.address_datastore.keys())
        print("length of th my keys list is ",list(self.address_datastore.keys()))
        for lctno, element in enumerate(my_keys):
            print(1)    