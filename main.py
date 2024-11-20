import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathlib import Path
import os  
import csv 

csvFolder = Path("input CSV folder")
files = list(csvFolder.glob("*.csv"))
if files:
    csv_file_path = files[0]
    print(f"Opening file: {csv_file_path}")
else:
    print("No CSV files found in the directory.")
    quit()

with open(csv_file_path, mode='r', encoding='utf-8') as inputFile:
    content = inputFile.read()  

updated_content = content.replace(';', ',') #we can remaster this codes

with open("tmp.csv", 'w', encoding='utf-8') as updatedFile:
    updatedFile.write(updated_content)

    
with open("tmp.csv", 'r', encoding='utf-8') as updatedFile:
    csv_reader = csv.DictReader(updatedFile)
    data_list = []
    for row in csv_reader:
        data_list.append(row)
for data in data_list:
    print(data["Product ID"])        
    # print(data["نام"])  !!!!!!!!!!      

if os.path.exists("tmp.csv"):  
    os.remove("tmp.csv")  
