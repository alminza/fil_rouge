#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:35:58 2021

@author: Malcor
"""

# Python program to convert text 
# file to JSON 
import os
import base64
import boto3
from flask import Flask, request
import PIL
import json 
import os
import csv
#client = boto3.client('s3')
client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)
os.remove(
                    "./static/jason"
                            )  # On enlève le fichier qui n'est plus utile

UPLOAD_FOLDER = './static/jason/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def upload_files(file_name, bucket, object_name= None, args= None):
    if object_name is None:
        object_name = file_name
    response = client.upload_file(file_name, bucket, object_name, ExtraArgs = args)
    
@app.route("/depot", methods=['GET', 'POST'])
def txt_to_json():
    
    if not os.path.isdir(app.config['UPLOAD_FOLDER']): 

        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    # the file to be converted 
    path_origin = request.files['file']
    noms_du_fichier = request.files['file'].filename
    print(noms_du_fichier)
    # resultant dictionary 
    dict1 = {} 
    L=[]

    path_origin.save(os.path.join(app.config['UPLOAD_FOLDER'], noms_du_fichier))
    
    prepa_extension = os.path.splitext(noms_du_fichier)
    extension = prepa_extension[1]
    
    if extension == ".jpg":
        
        data = {}
        with open('./static/jason/' + noms_du_fichier, mode='rb') as file:
            img = file.read()
        pouet = './photo_test.jpg'    
        extension = os.path.splitext(pouet)

        print(extension[-1])
        data['file.filename'] = base64.encodebytes(img).decode('utf-8')
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        out_file = open('./static/jason/' + nom_du_fichier_propre + ".json", "w") 
        json.dump(data, out_file, indent = 4) 
        out_file.close()
        upload_files('./static/jason/' + nom_du_fichier_propre + ".json", 'fil-rouge-storage', nom_du_fichier_propre + ".json")
        return ('Conversion réussie !')

        
    if extension == '.txt':

        with open('./static/jason/' + noms_du_fichier) as fh:
            # count variable for employee id creation
            l=0
            for m, line in enumerate(fh):
                if m == 0:
                    L = list(line.strip().split())
                 
                else :
                    fields=len(L)
                    # reading line by line from the text file 
                    description = list( line.strip().split()) 
                    # for output see below 
                    print(description) 
            		
            		# for automatic creation of id for each employee 
                    sno ='key_No'+str(l) 
            	
            		# loop variable 
                    i = 0
            		# intermediate dictionary
                    dict2 = {} 
                    while i<fields: 
            			
            				# creating dictionary for each employee 
                            dict2[str(L[i])]= description[i] 
                            i = i + 1
            				
            		# appending the record of each employee to 
            		# the main dictionary 
                    dict1[sno]= dict2
                    l = l + 1
        
        
        # creating json file		 
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        out_file = open('./static/jason/' + nom_du_fichier_propre + ".json", "w") 
        json.dump(dict1, out_file, indent = 4) 
        out_file.close()
        upload_files('./static/jason/' + nom_du_fichier_propre + ".json", 'fil-rouge-storage', nom_du_fichier_propre + ".json")
        return ('Conversion réussie !')

    if extension == '.csv':
                make_json('./static/jason/' + noms_du_fichier, './static/jason/' + nom_du_fichier_propre + ".json")
                upload_files('./static/jason/' + nom_du_fichier_propre + ".json", 'fil-rouge-storage', nom_du_fichier_propre + ".json")
                return ('Conversion réussie !')


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
# In[3]:

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
