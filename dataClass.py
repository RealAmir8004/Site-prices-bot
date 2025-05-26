import os  
import csv 
from pathlib import Path
from scraping import scrap , Site
from constants import RESULTS
import bisect
from import_logging import get_logger

logger = get_logger(__name__)

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
        "update the product best sites price from trob and return (ready to use in ui )queue of it "
        logger.info(f"Updating product: id='{self.id}'")
        sites = scrap(self.name ,self.id) 
        
        for site in sites[:RESULTS-1]:
            if "oldSP" == site.name:
                self.sites = sites[:RESULTS]
                break
        else:
            self.sites= sites[:RESULTS-1]
            bisect.insort(self.sites , Site("oldSP", self.price , suggest_price=False))

        while len(self.sites) < RESULTS:
            self.sites.append(Site(shop_name=None , price=0, badged=False, suggest_price=False))

        logger.debug(f"list of boxes (updated) to show in ui (len:{len(self.sites)}): {self.sites}")

        # #tst
        # self.sites = [
        #     Site(shop_name=f"Shop A ({self.name[0:3]})", price=self.price, badged=len(self.name) % 2 == 0),
        #     Site(shop_name=None, price=self.price * 0.95, badged=self.price > 100000 , suggest_price= False),
        #     Site(shop_name=f"Shop C ({self.name[2:5]})", price=self.price * 1.2, badged=self.active),
        #     Site(shop_name=f"Shop D ({self.name[-4:]})", price=self.price * 1.1, badged=self.number > 10),
        #     Site(shop_name=f"Shop E ({self.name[-3:]})", price=self.price * 1.5, badged=self.price_tax > 5000),
        # ]

    def chose_site (self , ch : Site) :
        self.chosen_site = ch
        logger.debug("chosen site saved in Data->self (RAM)")

class CsvData :
    """
        creat one object of this class for getting a Data list from csv and use it\n
        class contains a list[Data]
    """
    _instance = None
    __index = -1
    __list_data : list[Data]= []
    def __init__(self) :

        try:
            csvFolder = Path("input CSV folder")

            files = list(csvFolder.glob("*.csv"))
            if not files:
                raise FileNotFoundError("No CSV files found in the specified folder.")                
            
            csv_file_path = files[0]
            logger.info(f"Using CSV file: {csv_file_path}")

            # reading csv file
            with open(csv_file_path, 'r' , encoding='utf-8') as csvfile:

                csvreader = csv.reader(csvfile , delimiter=';')
                next(csvreader)
                for line in csvreader:
                    try:
                        # if not bool(int(line[8])): # False == active # fix 
                        if int(line[0]) in [14,18,23,32,33,41,63,64] :
                            self.__list_data.append(Data(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]))
                            logger.debug(f"Data adedd to list: {line}")
                    except Exception :
                        logger.exception(f"Error parsing line ")
        except Exception as e :
            logger.exception(f"error during CSV loading: ")
            raise

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
            logger.info(f"Current index of list: {self.__index} --refers to id='{curr.id}'")
            if curr.sites is None:
                curr.update()
            return curr
        except IndexError:
            logger.warning("No more data available.")
            return None  # Return None if the list is exhausted
        except Exception :
            logger.exception(f"Unexpected error in showData: ")
            return None
