import os  
import csv 
from pathlib import Path
from scraping import scrap , Site

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
        self.sites : Site = None    

    def update(self) ->  tuple[Site ,list[Site]] :
        "update the product best sites price from trob and return+store it "
        self.sites = scrap(self.name ,self.id)


class CsvData :
    """
        creat one object of this class for getting a Data list from csv and use it\n
        class contains a list[Data] \n
        or\n 
        use .next function to return a object(Data)
    """
    _instance = None
    __index = -1
    __list_data = []
    def __init__(self) :

        if os.path.exists("active.txt"):  # tst
            os.remove("active.txt")  

        if os.path.exists("All.txt"):  # tst
            os.remove("All.txt")  

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



        with open("active.txt" , "w" , encoding='utf-8')as f: # tst
            temp = 0
            for d in self.__list_data:
                if   d.number ==0 and d.active == True: 
                    f.write(str(d.id))
                    f.write('\n')
                    temp+=1
            print("temp:", temp)

        with open("All.txt" , "w" , encoding='utf-8')as f: # tst
            for d in self.__list_data:
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
                
    def __next(self) -> Data:
        self.__index += 1 
        return self.__list_data[self.__index]
    
    def nextData(self) -> Data:
        " this will go forward in list and return (this will show list[0] for first use)"
        nxt = self.__next()
         # fix me :what if sites steel none
        if nxt.sites == None: 
            nxt.update() 
        return nxt
     