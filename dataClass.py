from pathlib import Path
from scraping import scrap , Site
from constants import RESULTS
import bisect
from import_logging import get_logger
import pandas 
import shutil
from os import chmod
from  stat import S_IWRITE
from openpyxl import load_workbook
from time import sleep
import random  

logger = get_logger(__name__)

class Data :
    def __init__(self, id, name, price):
        self.id = int(id)
        self.name = str(name)
        self.price = int(price)
        self.sites : list[Site] = None
        self.chosen_site = None

    def update(self):
        "update the product best sites price from trob and return (ready to use in ui )queue of it "
        logger.info(f"Scraping for product (id='{self.id}')...")
        sites = scrap(self.name) 
        while len(sites) < RESULTS:
            sites.append(Site(shop_name=None , price=0, badged=False, suggest_price=False))
        
        for site in sites[:RESULTS-1]:
            if "oldSP" == site.name:
                self.sites = sites[:RESULTS]
                break
        else:
            self.sites= sites[:RESULTS-1]
            bisect.insort(self.sites , Site("oldSP", self.price , suggest_price=False))
        logger.debug(f"list of boxes (updated) to show in ui (len:{len(self.sites)}): {self.sites}")


class DataList :
    """
        creat one object of this class for getting a Data list from xlsx and use it\n
        class contains a list[Data]
    """
    _instance = None
    __index = -1
    __list_data : list[Data]= []
    def __init__(self) :
        try:
            input_folder = Path("input xlsx")
            xlsx_file_path = next(input_folder.glob("*.xlsx"))
            logger.info(f"Using xlsx file: {xlsx_file_path}")
            
            # Copy xlsx file to output folder
            output_folder = Path("output xlsx")
            if output_folder.exists():
                shutil.rmtree(output_folder , onerror=lambda func, path, _: (chmod(path, S_IWRITE), func(path)))
            output_folder.mkdir(exist_ok=True)
            self.output_path = output_folder / xlsx_file_path.name
            shutil.copy(xlsx_file_path, self.output_path)
            logger.info(f"Copied xlsx file to: {self.output_path}")

            # reading xlsx file
            df = pandas.read_excel(xlsx_file_path)
            
            active_products = df.groupby("id_product")["active"].apply(lambda a: (a == 1).any())
            active_products = active_products[active_products].index
            df_active = df["id_product"].isin(active_products)

            availables_products = df.groupby("id_product")["quantity"].apply(lambda q: (q > 0).any())
            availables_products = availables_products[availables_products].index            
            df_availables =df["id_product"].isin(availables_products)

            logger.info(f"Original file: {len(set(df["id_product"]))} ids in '{len(df)}' rows --> actives : '{len(active_products)}' ids in '{df_active.sum()}' rows --> availables : '{len(availables_products)}' ids in '{df_availables.sum()}' rows ")
            # saving self.output_df to "ram" for using in saveData :
            self.output_df = df[df_active & df_availables]
            
            # filteering table to Only select "id_product", "name", "price" from "active" rows :
            filtered = df.loc[(df["active"] == 1) & df_availables , ["id_product", "name", "price"]]
            self.__list_data = [Data(row.id_product, row.name, row.price) for row in filtered.itertuples()]
            self.len = len(self.__list_data)
            logger.debug(f"list_data exported from xlsx is = (len= {self.len}) "+str([{'id': d.id, 'name': d.name, 'price': d.price} for d in self.__list_data])) 
            # fix (if later needed): we can use __repr__ in Data instead of prevous line 
        except StopIteration:
            logger.error("No xlsx files found in the input xlsx folder")
            raise FileNotFoundError("No files found in the specified folder")
        except Exception as e :
            logger.exception(f"error during initing DataList: ")
            raise

    def current(self)-> Data :
        return self.__list_data[self.__index]
    
    def updateAll(self , bar):
        logger.info("→→→→→→→→→ 'All prudacts Updating'")
        for i, d in enumerate(self.__list_data):
            d.update()
            canceled = bar.progress(i)
            if canceled:
                logger.info(f"Canceled!")
                break
            sleep(random.uniform(2, 4))
        logger.info(f"→→→→→→→→→ 'All prudacts Updating' : procces ended : '{i}' of '{self.len}' prudacts update called")

    def showData(self , is_next : bool) -> Data:
        """This will go forward in the list and return the next Data object."""
        try:
            if is_next :
                self.__index += 1
            else :    
                self.__index -= 1
            if self.__index < -self.len:
                self.__index = self.len -1
            elif self.__index >= self.len:
                self.__index = 0
            curr = self.current()
            logger.info(f"Current index of list: {self.__index} --refers to id='{curr.id}'")
            if curr.sites is None:
                curr.update()
            return curr , self.__index
        except Exception :
            logger.exception(f"Unexpected error in showData: ")
            return None

    def saveData(self) :
        """Save all of changes maded untill now from memory to xlsx file"""
        try:
            df = self.output_df
            # filter unchangeds & include changes :
            new_rows = []
            data_map = {d.id: d for d in self.__list_data}
            remain = None
            prev_id = None
            for row in df.itertuples(index=False):
                curr_id = row.id_product
                if prev_id == curr_id : # combination row
                    if remain :
                        new_rows.append(row._asdict())
                    continue
                prev_id = curr_id
                data = data_map.get(curr_id)
                chosen = data.chosen_site
                if chosen is None: # radio not checked before save button 
                    logger.warning(f"id='{curr_id}' deleted from xlsx becuase: radio not checked before save button")
                    remain = False
                    continue  # Remove
                row_dict = row._asdict()
                if isinstance(chosen, str):
                    site = data.sites[int(chosen)]
                    if isinstance(site.suggested_price, str): # "dont change price"
                        logger.debug(f"id='{curr_id}' deleted from xlsx becuase: radio = 'dont change price'")
                        remain = False
                        continue
                    updated_price = site.suggested_price
                elif isinstance(chosen, int): # custom price 
                    updated_price = chosen 
                row_dict["price"] = updated_price 
                remain = True
                new_rows.append(row_dict)
                logger.info(f"id='{curr_id}' remained in xlsx : price updated to {updated_price}")
            # Save (without extra changings (header style)) :
            wb = load_workbook(self.output_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row)  # keep header, remove all rows
            for row_idx, row in enumerate(new_rows, start=2):
                for col_idx, col_name in enumerate(df.columns, start=1):
                    ws.cell(row=row_idx, column=col_idx, value=row.get(col_name))
            wb.save(self.output_path)
            logger.info(f"Successfully new xlsx saved to {self.output_path}")
        except Exception as e:
            logger.exception("Error during saving data to xlsx: ")
            raise e


if __name__ == "__main__":
    print("this file is only class mudule and can not be runed")