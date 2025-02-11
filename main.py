import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathlib import Path
import os  
import csv 
from typing import Literal


if os.path.exists("A.txt"):  # tst
    os.remove("A.txt")  

csvFolder = Path("input CSV folder")
files = list(csvFolder.glob("*.csv"))
if files:
    csv_file_path = files[0]
    print(f"successful Opening file: {csv_file_path}")
else:
    print("No CSV files found in the directory.")
    quit()

with open(csv_file_path, mode='r', encoding='utf-8') as inputFile:
    lines = inputFile.readlines()  

class Data :
    def __init__(self,id,picture,name,code,group,price,price_tax,number,active) : 
        self.id = int(id)
        self.picture = picture #(href)        
        self.name = str(name)       
        self.name = self.name[1:-1]  # remove " from start and end of string for better search in google      
        self.code = code 
        self.group = group
        self.price = float(price)    
        self.price_tax = int(price_tax)           
        self.number =int(number)          
        self.active =bool(int(active))    


data = []
for line in lines[1:]:
    values = line.split(';')    
    data.append(Data(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8]))

with open("A.txt" , "w" , encoding='utf-8')as f: # tst
    temp = 0
    for d in data:
        if  d.active : # tst
            f.write(str(d.id))
            f.write('\n')
            temp+=1
    print(temp)    


# problems :
# csv(number of Data ) =  site (number of mahsols)  = 1050
# csv(kamine=1 ) =  site (number>0)  = 181
# csv(not active  ) =  site (number>0)  = 181 ???