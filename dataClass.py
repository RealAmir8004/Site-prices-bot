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
        logger.info("Scraping for product ...")
        # sites = scrap(self.name) 
        
        # for site in sites[:RESULTS-1]:
        #     if "oldSP" == site.name:
        #         self.sites = sites[:RESULTS]
        #         break
        # else:
        #     self.sites= sites[:RESULTS-1]
        #     bisect.insort(self.sites , Site("oldSP", self.price , suggest_price=False))

        # while len(self.sites) < RESULTS:
        #     self.sites.append(Site(shop_name=None , price=0, badged=False, suggest_price=False))

        # logger.debug(f"list of boxes (updated) to show in ui (len:{len(self.sites)}): {self.sites}")

        #tst
        self.sites = [
            Site(shop_name=f"Shop A ({self.name[0:3]})", price=self.price, badged=len(self.name) % 2 == 0),
            Site(shop_name="oldSP", price=self.price , badged=self.price > 100000 , suggest_price= False),
            Site(shop_name=f"Shop B ({self.name[2:5]})", price=self.price * 1.2, badged=True),
            Site(shop_name=f"Shop C ({self.name[2:5]})", price=self.price * 1.2, badged=False),
            Site(shop_name=f"Shop D ({self.name[-4:]})", price=self.price * 1.1, badged=True),
            Site(shop_name=f"Shop E ({self.name[-3:]})", price=self.price * 1.5, badged=False),
        ]


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
            # filteering table to Only select "id_product", "name", "price" from "active" rows :
            filtered = df.loc[df["active"] == 1, ["id_product", "name", "price"]]
            self.__list_data = [Data(row.id_product, row.name, row.price) for row in filtered.itertuples()]
            logger.debug("list_data exported from xlsx is = "+str([{'id': d.id, 'name': d.name, 'price': d.price} for d in self.__list_data])) 
            # fix (if later needed): we can use __repr__ in Data instead of prevous line 
        except StopIteration:
            logger.error("No xlsx files found in the input xlsx folder")
            raise FileNotFoundError("No files found in the specified folder")
        except Exception as e :
            logger.exception(f"error during xlsx loading: ")
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

    def saveData(self) :
        """Save all of changes maded untill now from memory to xlsx file"""
        try:
            df = pandas.read_excel(self.output_path)
            # Remove all active == 0 :
            inactive_ids = set(df.loc[df["active"] == 0, "id_product"])
            df = df[~df["id_product"].isin(inactive_ids)]
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
                    remain = False
                    continue  # Remove
                row_dict = row._asdict()
                if isinstance(chosen, str):
                    site = data.sites[int(chosen)]
                    if isinstance(site.suggested_price, str): # "dont change price"
                        remain = False
                        continue
                    updated_price = site.suggested_price
                elif isinstance(chosen, int): # custom price 
                    updated_price = chosen 
                row_dict["price"] = updated_price 
                remain = True
                new_rows.append(row_dict)
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