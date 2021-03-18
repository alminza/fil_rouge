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
from jsonlib import *
import os
import base64
import boto3
from flask import Flask, request
import PIL
import json 
import os
import csv
#session = boto3.Session(aws_access_key_id = ASIAT546GKVAGH5KTB5B, aws_secret_access_key = 1aASGO2J77MDa8Ke/QhIz7SqfnoMI2yVN9n6BmO4)

os.environ['AWS_PROFILE'] = "csloginstudent"
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
client = boto3.client('s3')

UPLOAD_FOLDER = './static/jason/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/depot", methods=['POST'])
def txt_to_json():
    
    if not os.path.isdir(app.config['UPLOAD_FOLDER']): 

        os.makedirs(app.config['UPLOAD_FOLDER'])
    if request.method == "POST":    
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
    
    
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
