# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 17:21:38 2021

@author: Malcor
"""
import boto3
import csv

import json
client = boto3.client('s3')
def upload_files(file_name, bucket, object_name= None, args= None):
    if object_name is None:
        object_name = file_name
        response = client.upload_file(file_name, bucket, object_name, ExtraArgs = args)
        print(response)

def make_json(csvFilePath, jsonFilePath):
            i = 0
            # create a dictionary
            data = {}

            # Open a csv reader called DictReader
            with open(csvFilePath) as csvf:
                csvReader = csv.DictReader(csvf)

                # Convert each row into a dictionary
                # and add it to data
                for rows in csvReader:

                    # Assuming a column named 'No' to
                    # be the primary key

                    data[i] = rows
                    i += 1
                    #print(i)

            # Open a json writer, and use the json.dumps()
            # function to dump data
#            with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                csvf.write(json.dumps(data, indent=4))