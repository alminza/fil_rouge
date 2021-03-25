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
from PIL import Image
from PIL.ExifTags import TAGS
import base64
import boto3
from flask import Flask, request
import json 
import os
import csv
client = boto3.client('s3')
#client = boto3.client(
#    's3',
#    aws_access_key_id=ACCESS_KEY,
#    aws_secret_access_key=SECRET_KEY,
#    aws_session_token=SESSION_TOKEN
#)

UPLOAD_FOLDER = './static/jason/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def pdf_json(path):  # Transforme un fichier PDF en JSON

    fichier = open(path, "rb")
    try:  # On ouvre le fichier comme un PDF
        read_pdf = PyPDF2.PdfFileReader(fichier)
    except:
        return "Erreur lors de la transformation, etes vous sur que le fichier soit un PDF?"  # Si on arrive pas à l'ouvrir ce n'est pas un PDF
    Docinfo = read_pdf.getDocumentInfo()  # Extraction des metadonnées du PDF
    metadata = {
        "Auteur": Docinfo.author,
        "Createur": Docinfo.creator,
        "Sujet": Docinfo.subject,
        "Titre": Docinfo.title,
        "MIME": "pdf",
        "taille": os.path.getsize(path),
    }
    number_of_pages = read_pdf.getNumPages()
    texte = ""

    for p in range(number_of_pages):  # Permet de gérer plusieurs pages
        page = read_pdf.getPage(p)
        page_content = page.extractText()
        content = texte + page_content + str(metadata)


    
    return(content)

def upload_files(file_name, bucket, object_name= None, args= None):
    if object_name is None:
        object_name = file_name
    response = client.upload_file(file_name, bucket, object_name, ExtraArgs = args)
    print(response)

def csv_json(csvFilePath, jsonFilePath):
            i = 0 
            # create a dictionary
            data = {}
             
            # Open a csv reader called DictReader
            with open(csvFilePath, "r+") as csvf:
                csvReader = csv.DictReader(csvf)
                 
                # Convert each row into a dictionary 
                # and add it to data
                for rows in csvReader:
                     
                    # Assuming a column named 'No' to
                    # be the primary key
                    
                    data[i] = rows
                    i += 1
                    #print(i)
            with open (csvFilePath) as f:
                reader = csv.reader(f)
                headers = next(reader)        # The header row is now consumed
                ncol = len(headers)
                nrow = sum(1 for _ in reader) # What remains are the data rows
                
                content = reader + headers + ncol + nrow + str(data)
            # Open a json writer, and use the json.dumps() 
            # function to dump data
            with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                jsonf.write(json.dumps(content, indent=4))



@app.route('/depot', methods=['GET', 'POST'])
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
    nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
    path_origin.save(os.path.join(app.config['UPLOAD_FOLDER'], noms_du_fichier))
    
    prepa_extension = os.path.splitext(noms_du_fichier)
    extension = prepa_extension[1]
    
    if extension == '.jpg':
        meta_data = {}
        data = {}
        with open('./static/jason/' + noms_du_fichier, mode='rb') as file:
            img = file.read()
        chemin = './static/jason/' + noms_du_fichier
        # open the image
        with Image.open(chemin, 'r') as mario:
          
        # extracting the exif metadata
            exifdata = mario.getexif()
        # looping through all the tags present in exifdata
        for tagid in exifdata:
              
            # getting the tag name instead of tag id
            tagname = TAGS.get(tagid, tagid)
          
            # passing the tagid to get its respective value
            value = exifdata.get(tagid)
            
            meta_data[tagname] = value
            
        
        
        print(extension[-1])
        data['file.filename'] = base64.encodebytes(img).decode('utf-8')
        content = str(data) + str(meta_data)
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        out_file = open('./static/jason/' + nom_du_fichier_propre + ".json", "w") 
        json.dump(content, out_file, indent = 4) 
        out_file.close()
        upload_files('./static/jason/' + nom_du_fichier_propre + ".json", 'fil-rouge-storage', nom_du_fichier_propre + ".json")
        return ('Conversion réussie !')

        
    if extension == '.txt':

        with open('./static/jason/' + noms_du_fichier) as fh:
            # count variable for employee id creation
            l=0
            for line in fh:
                    fields=len(L)
                    # reading line by line from the text file 
                    sno ='key_No'+str(l) 
                    i = 0
                    dict2 = {} 
                    while i<fields: 
                            dict2[sno]= description[i] 
                            i = i + 1
        
        
        # creating json file		 
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        out_file = open('./static/jason/' + nom_du_fichier_propre + ".json", "w") 
        json.dump(dict2, out_file, indent = 4) 
        out_file.close()
        upload_files('./static/jason/' + nom_du_fichier_propre + ".json", 'fil-rouge-storage', nom_du_fichier_propre + ".json")
        return ('Conversion réussie !')

    if extension == '.csv':
                csv_json('./static/jason/' + noms_du_fichier, './static/jason/' + nom_du_fichier_propre + ".json")
                upload_files('./static/jason/' + nom_du_fichier_propre + ".json", 'fil-rouge-storage', nom_du_fichier_propre + ".json")
                return ('Conversion réussie !')
    if extension == '.pdf':
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        content = pdf_json('./static/jason/' + noms_du_fichier)
        out_file = open('./static/jason/' + nom_du_fichier_propre + ".json", "w")
        json.dump(content, out_file, indent = 4)
        upload_files('./static/jason/' + nom_du_fichier_propre + ".json", 'fil-rouge-storage', nom_du_fichier_propre + ".json")
        return ('Conversion réussie !')
        
        

        


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
