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
    # age khasti "for" ro ezafe koni "def func" ha ro biyar biron !!!!!!!!!!!!!!! 
    # for d in data:
    #     if d.active and d.number>0 : 

    d = data[8] #tst
    d = data[13] #tst
    d = data[22] #tst
    d.active = True # fix me : after fixing (ایرادات)
# "بلندگو پایونیر Pioneer TS-G1020F - اصلی"G
    
    def search_google (d : Data):
        print("searching google for ", d.id, ":")
        from googlesearch import search
        import re
        query = d.name
        num_results = 10
        targets = []
        target_pattern = r"https://torob.com/"
        with open("searchResult_ME.txt","w") as file:
            for result in search(query , num_results):
                file.write(f"\n{result}\n")
                if re.match(target_pattern,result):
                    targets.append( result)
        
        print("prinring all search results (first url will be used) :")
        print(targets)
        return targets

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
    

    class Site :
        def __init__(self , shop_name  ,  warranty_badged  , price , last_price_change ):
            self.name = shop_name
            self.badged = warranty_badged
            self.price = price 
            self.last_change = last_price_change


    import json # tst 
    from json import loads
    def get_all_sites (soup : BeautifulSoup) -> list[Site] :

        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        
        json_data = loads(script_tag.string)  

        with open("test_data.json", "w", encoding="utf-8") as j: #tst
            json.dump(json_data, j, ensure_ascii=False, indent=4)
        
        products = json_data["props"]["pageProps"]["baseProduct"]["products_info"]["result"]

        sites: list[Site] = []
        with open("other_sites.txt" , "w" , encoding='utf-8')as f : #tst (not all of down)
            for product in products:
                if product['availability'] :
                    sites.append(Site(product['shop_name'] , product['is_filtered_by_warranty']  , product['price_text'] , product['last_price_change_date']))
                    f.write(f"------{product['shop_name']} ----------- {product['price_text']}  \n") # tst
                else :
                    f.write(f"{product['shop_name'] } ----------- {product['price_text']} \n") # tst
        return sites


    def calc_price (soup : BeautifulSoup): 
        from bs4.element import Tag        
        
        buy_box : Tag= soup.find('div', class_='Showcase_buy_box__q4cpD') # class = Showcase_buy_box__q4cpD # badge =.Showcase_guarantee_badge_text__Kz3AW
        
        get_all_sites(soup)
        
        result : list[Tag] = buy_box.find_all('div' , class_='Showcase_buy_box_text__otYW_ Showcase_ellipsis__FxqVh')  #result[0] = site_name   result[1] = site_price 
        if "اسپارک" in result[0].get_text(strip=True):
            return False

        price_txt = result[1].get_text(strip=True)
        price = int(''.join(filter(str.isdigit, price_txt)))
        print(f"buy box = {price}", end=" ")


        if buy_box.find('div' , class_="Showcase_buy_box_badge__Tc_1w Showcase_guarantee_badge__U90n2") is None : # ckeck if guarantee_badge 
            print("is Not badged", end=" ")
            new_price = (price *105 ) / 100 
            mod = new_price % 10_000
            print (f" (tst : price={price} <> mod={mod} ) " , end="")
            if mod >= 9000 or price<200_000  :
                return new_price
            else:
                return  new_price - (mod + 1000)  
        
        else : # is badged 
            print("issss  badged", end=" ")
            mod = price % 10_000
            return  price - (mod + 1000)  # fix me : we can upgrade to new versions later (price_reduce->from after-csv-faze1 (commit) )
    


    results = search_google(d)
    print("searching torob :")
    response = get_html(results[0]) # targets[0] = first torob result(url)

    soup = BeautifulSoup(response.content , "html5lib")    
    
    with  open("TorobResult3.html" , "w" , encoding='utf-8') as file  : #tst
        file.write(soup.prettify())

    new_price = calc_price(soup)
    
    if new_price == False : # fix me (for tst ) : bayad "continue" kone bjaye "return" -> for loop
        print("buy box was already spark")
        return 
    else:
        print(f"Converted to :{new_price}")
        return new_price


# main.py :

data = get_data_from_csv()
scrap_data(data)


# printed result :
# suggestion : (if spark is first => start from row 2 ---> kolan spark ro har ja bod skip kon )
# 1- 1465156 calced with first site 
# 2- 155416 calced with second site 
# ...    
# sites :
# 31561
# 6541651 = spark 
# 524516 = (red = warranty)
# 54546
# 5466666654 = (red = warranty) 
# 58464