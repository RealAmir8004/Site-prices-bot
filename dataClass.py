import os  
import csv 
from pathlib import Path
from scraping import scrap , Site
from constants import RESULTS

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
        self.sites : list[Site] = None
        self.chosen_site = None

    def update(self):
        for site in sites[:RESULTS-1]:
                self.sites = sites[:RESULTS]
            self.sites= sites[:RESULTS-1]
        #tst
        self.sites = [
            Site(shop_name=f"Shop A ({self.name[0:3]})", price=self.price, badged=len(self.name) % 2 == 0),
            Site(shop_name=f"Shop B ({self.name[1:4]})", price=self.price * 0.95, badged=self.price > 100000),
            Site(shop_name=f"Shop C ({self.name[2:5]})", price=self.price * 1.2, badged=self.active),
            Site(shop_name=f"Shop D ({self.name[-4:]})", price=self.price * 1.1, badged=self.number > 10),
            Site(shop_name=f"Shop E ({self.name[-3:]})", price=self.price * 1.5, badged=self.price_tax > 5000),
        ]

    def chose_site (self , ch : Site) :
        self.chosen_site = ch

class CsvData :
    """
        creat one object of this class for getting a Data list from csv and use it\n
        class contains a list[Data] \n
        or\n 
        use .next function to return a object(Data)
    """
    _instance = None
    __index = -1
    __list_data : list[Data]= []
    def __init__(self) :

        csvFolder = Path("input CSV folder")

        files = list(csvFolder.glob("*.csv"))
        if files:
            csv_file_path = files[0]


        # reading csv file
        with open(csv_file_path, 'r' , encoding='utf-8') as csvfile:

            csvreader = csv.reader(csvfile , delimiter=';')
            next(csvreader)
            for line in csvreader:
                self.__list_data.append(Data(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]))

    def current(self)-> Data :
            return self.__list_data[self.__index]


    def showData(self , is_next : bool) -> Data:
        """This will go forward in the list and return the next Data object."""
        try:
            if is_next :
                self.__index += 1
            else :    
                self.__index -= 1
            curr = self.current()
            if curr.sites is None:
                curr.update()
            print(f"showing Data object: {curr.id}")
            return curr
        except IndexError:
            print("No more data available.")
            return None  # Return None if the list is exhausted
     