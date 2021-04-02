# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:16:47 2021

@author: Malcor
"""

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
import PyPDF2
import os
import csv
client = boto3.client('s3')

UPLOAD_FOLDER = './static/jason/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def pdf_json(path, noms_du_fichier):  # Transforme un fichier PDF en JSON

    fichier = open(path, "rb")
    # On ouvre le fichier comme un PDF
    read_pdf = PyPDF2.PdfFileReader(path)
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
    metadata["Nom du fichier"] = noms_du_fichier    
    for p in range(number_of_pages):  # Permet de gérer plusieurs pages
        page = read_pdf.getPage(p)
        page_content = page.extractText()
        contenu = texte + page_content + str(metadata)

    json_pdf = json.dumps(contenu)
    content = (json_pdf, metadata)
    
    return(content)

def upload_files(file_name, bucket, object_name= None, args= None):
    if object_name is None:
        object_name = file_name
    response = client.upload_file(file_name, bucket, object_name, ExtraArgs = args)
    print(response)

def csv_json(csvFilePath, jsonFilePath, noms_du_fichier):
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
            
            metadata = {}
            metadata["nombre de colonne"] = ncol
            metadata["nombre de ligne"] = nrow
            metadata["header"] = data[0]
            metadata["Le nom du fichier est"] = noms_du_fichier
            
            json_csv = json.dumps(data)
            content = (json_csv, metadata)
            return(content)

def detect_labels_rekognition(path,):  # Cette fonction permet de demandé à AWS de faire de la reconnaissance d'image
    with open(path, "rb") as f:
        Image_bytes = f.read()
        session = boto3.Session()
        s3_client = session.client("rekognition")
        response = s3_client.detect_labels( Image={"Bytes": Image_bytes}, MaxLabels=5, MinConfidence=90)  #on garde maximum 5 label et seulement s'ils ont une confiance de plus de 90 %
        return response

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
    
    if extension == '.jpg' or '.png':
        meta_data = {}
        data = {}
        with open('./static/jason/' + noms_du_fichier, mode='rb') as file:
            img = file.read()
        meta_data ={}
        image = Image.open('./static/jason/' + noms_du_fichier,)
        meta_data["Width"] = image.size[0]
        meta_data["Height"] = image.size[1]
        meta_data["Format"] = image.format  # Certaine metadatas
        meta_data["Nom fichier"] = noms_du_fichier

        labels = detect_labels_rekognition('./static/jason/' + noms_du_fichier)  # Reconnaissance d'image par AWS, si l'image à été récupéré par PIL alors il est possible de la lire avec AWS et qu'elle fait moins de 5MB
        Labels_dictionary = {}
        for k in range(len(labels["Labels"])):
            Labels_dictionary[labels["Labels"][k]["Name"]] = "Confiance de" + str(labels["Labels"][k]["Confidence"])
            meta_data["Labels detected"] = Labels_dictionary
        
        data["contenu"] = base64.encodebytes(img).decode('utf-8')
        json_jpg = json.dumps(data)
        content = (json_jpg, meta_data)
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        upload_files('./static/jason/' + noms_du_fichier, 'fil-rouge-storage', noms_du_fichier)
        return (content)

        
    if extension == '.txt':

        with open('./static/jason/' + noms_du_fichier) as fh:
            # count variable for employee id creation
            caractere =0
            dict2 = {}
            ligne = 0 
            contenu = ""
            poid = os.path.getsize
            for line in fh:
                ligne +=1
                caractere += len(line)
                contenu = contenu + line
        metadata = {
            "taille": poid,
            "MIME": "txt",
            "Nombre de ligne": ligne,
            "Nombre de caractère": caractere,
                }
        json_txt = json.dumps(contenu)
        content = (json_txt, metadata)
        # creating json file		 
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        upload_files('./static/jason/' + noms_du_fichier, 'fil-rouge-storage', noms_du_fichier)
        return (content)

    if extension == '.csv':
                content = csv_json('./static/jason/' + noms_du_fichier, './static/jason/' + nom_du_fichier_propre + ".json", noms_du_fichier)
                upload_files('./static/jason/' + noms_du_fichier, 'fil-rouge-storage', noms_du_fichier)
                return (content)
    if extension == '.pdf':
        nom_du_fichier_propre = os.path.splitext(noms_du_fichier)[0]
        content = pdf_json('./static/jason/' + noms_du_fichier, noms_du_fichier)
        upload_files('./static/jason/' + noms_du_fichier, 'fil-rouge-storage', noms_du_fichier)
        return (content)
        
        

        


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
