import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathlib import Path
import os  
import csv 
from typing import Literal # ?


class Data :
    def __init__(self,id,picture,name,code,group,price,price_tax,number,active) : 
        self.id = int(id)
        self.picture = picture #(href)        
        self.name = name 
        self.code = code 
        self.group = group
        self.price = float(price)    
        self.price_tax = int(price_tax)           
        self.number =int(number)          
        self.active =bool(int(active))    


def get_data_from_csv() -> list[Data]:

    if os.path.exists("active.txt"):  # tst
        os.remove("active.txt")  

    if os.path.exists("All.txt"):  # tst
        os.remove("All.txt")  

    csvFolder = Path("input CSV folder")

    files = list(csvFolder.glob("*.csv"))
    if files:
        csv_file_path = files[0]
        print(f"successful Opening file: {csv_file_path}")
    else:
        print("No CSV files found in the directory.")
        quit()




    data = []
    # reading csv file
    with open(csv_file_path, 'r' , encoding='utf-8') as csvfile:

        csvreader = csv.reader(csvfile , delimiter=';')
        next(csvreader)
        for line in csvreader:
            data.append(Data(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]))



    with open("active.txt" , "w" , encoding='utf-8')as f: # tst
        temp = 0
        for d in data:
            if   d.number ==0 and d.active == True: 
                f.write(str(d.id))
                f.write('\n')
                temp+=1
        print("temp:", temp)

    with open("All.txt" , "w" , encoding='utf-8')as f: # tst
        for d in data:
            f.write(str(d.id))
            f.write(";")
            f.write(d.picture)
            f.write(";")
            f.write(d.name)
            f.write(";")
            f.write(d.code)
            f.write(";")
            f.write(d.group)
            f.write(";")
            f.write(str(d.price))
            f.write(";")
            f.write(str(d.price_tax))
            f.write(";")
            f.write(str(d.number))
            f.write(";")
            f.write(str(d.active))
            f.write('\n')

    return data
#                       csv              site

#  all :                951               951

#  number>0 :           135               135
#  number=0 :           816               816

#  actives :            135(false)        209
#  non active:          816(true)         742    

# actives & number>0:   135(false n>0)    127
# !actives & number>0:  0(true n>0)       8         127+8=135     


# ایرادات:
# تعداد محصول ناصفر در سایت تبدیل شده به محصولات فعال در سی اس وی 
#  اینکه محصولات فعال در سی اس وی = false


def scrap_data (data : list[Data]):
    
    # fix me : removed for (tst) 
    # for d in data:
    #     if d.active and d.number>0 : 

    d = data[8] #tst
    d.active = True # fix me : after fixing (ایرادات)
    print("searching google for ", d.id, ":")

    search_url = f"https://www.google.com/search?q={d.name}&num=10" # 10 = number of sites

    def get_html(url : str ) -> requests.Response:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        try:
            response = requests.get(url=url , headers=headers)
            response.raise_for_status()
        except HTTPError as err:
            print(f'HTTP error occurred: {err}')  
        except Exception as err:
            print(f'Other error occurred: {err}') 
        else:
            print('Success! no expection with url : ' ,response.url) 
            return response

    
    def find_torob_Link (response : requests.Response):
        links = []
        soup = BeautifulSoup(response.text , "html.parser")    

        with  open("soupPrettify.html" , "w" ,) as file  : # tst*
            file.write(soup.prettify())
        
        for g in soup.find_all('div', class_='tF2Cxc'):  # tF2Cxc = results class
            link = g.find('a')['href']
            if 'torob' in link :
                return link 
            
        return False
    

    print("searching google :")
    response = get_html(search_url) # tst*   

    with  open("searchResult.html" , "wb" ,) as file  : # tst*
        file.write(response.content)

    # find_torob_Link(get_html())      #  in khat bayad bshe bjaye in ( # tst* ) haye bala

    torobLink=find_torob_Link(response)
    if (torobLink==False) :
        print("torob url not founded ")
        quit()

    print("torob url founded : ", torobLink)

    # fix me : declare a function ? 

    print("searching torob :")
    response = get_html(torobLink) # fix me : response is overwrited (is it neccecery to change the name of the variable? )

    with  open("TorobResult.html" , "wb" ,) as file  :
        file.write(response.content)
    
    
# main.py :

data = get_data_from_csv()
scrap_data(data)

