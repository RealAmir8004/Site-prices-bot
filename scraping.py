import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from json import loads
from bs4.element import Tag 

from import_logging import get_logger
from pathlib import Path
import pandas as pd
import UI
import sys
from urllib.parse import urlparse

logger = get_logger(__name__)

class TorobURL :
    _instance = False  
    @classmethod
    def _load_data(cls):
        try :
            input_folder = Path("input torob")
            csv_file_path = next(input_folder.glob("*.csv"))
            logger.info(f"Using torob-csv file: {csv_file_path}")
        except StopIteration:
            e = "No csv files found in the 'input torob' folder"
            logger.error(e+" → sys.exit(1) called")
            UI.critical_message(e)
            sys.exit(1)

        df = pd.read_csv(csv_file_path,encoding='utf-16',sep='\t')
        cls.url_map = dict(zip(df['نام کالا'], df['لینک ترب']))
        cls._instance = True

    @classmethod
    def shorten_torob_url(cls ,url):
        parsed = urlparse(url)
        parts = parsed.path.strip("/").split("/") # path='/p/8a99b150-...(ID)/long-title(uneccecery)'
        if len(parts) > 2 and parts[0] == "p":
            short_path = f"/p/{parts[1]}/"
            return f"{parsed.scheme}://{parsed.netloc}{short_path}"
        else:
            logger.warning(f"url skiped from shorten_torob_url() :url='{url}'")
            return url
        
    @classmethod
    def get_url(cls , name):
        if not cls._instance :
            cls._load_data()
        try :
            return cls.shorten_torob_url(cls.url_map[name])
        except KeyError:
            logger.warning(f"name='{name}' not founded in csv")
            return None
        


class RequestTorob :
    _session = None  
    
    @classmethod
    def _init_session(cls):
        if cls._session is None :
            cls._session = requests.Session()
            cls._session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
        
    @classmethod
    def get_html(cls , url):
        cls._init_session()
        if url.startswith("http://"):
            url = "https://" + url[len("http://"):]
        try:
            response = cls._session.get(url)
            response.raise_for_status()
            logger.debug(f'request Successed!')
            return response
        except Exception:
            logger.exception(f'some error occurred in requesting: ')
            return None


class Site :
    def __init__(self , shop_name  , price : int , badged : bool = False ) :
        self.name = shop_name
        self.price = int(price )
        self.badged = badged
        if shop_name == "اسپارک دیجی" or price == 0:
            self.suggested_price = "dont change price"
        else:
            self.suggested_price = self._suggest()
        
    def __repr__(self):
        return (f"Site(name={self.name!r}, price={self.price}, "
                f"badged={self.badged}, suggested_price={self.suggested_price!r})")

    def __lt__(self, other):  # Define sorting rule = buy-box of Torob priority rule 
        if self.badged == other.badged:
            return self.price < other.price
        if self.badged and not other.badged:
            return self.price < (other.price * 105) / 100
        if not self.badged and other.badged:
            return (self.price * 105) / 100 < other.price
        return False
    
    def _suggest(self) -> int:
        susuggested = self.price
        if self.badged: # ckeck if guarantee_badge !!!!!!!!! mohem : in behtarin halate  bekhate algoritm buy_box torob
            mod = self.price % 10_000
            if mod <= 4000: # baraye inke age masalan ::  mod==0  bod price faghat 1000 ta kam nashe (zaye mishe)
                mod += (4000-mod)
            susuggested = self.price - (mod + 1000)  # fix me : we can upgrade to new versions later (price_reduce->from after-csv-faze1 (commit) )
        
        else : # is NOT badged 
            temp = ( self.price *105 ) / 100 - 1000 
            mod = temp % 10_000
            if mod < 9000 and  self.price>=200_000  :
                temp =  temp - (mod + 1000)  # we can upgrade to ...
            susuggested = temp    
        return int(susuggested)
        
    
# (info@) : rah haye mokhtalefi baraye sort bodan  list ha hast 
    # 1 - if : product['is_adv']  delete konim -> list ha khodeshon sort shode mian biron (vali ye data hazf mishe) 
    # 2 - sortedList
def get_all_sites (soup : BeautifulSoup)-> tuple[list[Site],list[Site],list[Site]]: 
    try:
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if not script_tag or not script_tag.string:
            logger.error("Could not find the required script tag for product data.")
            return [], []
        json_data = loads(script_tag.string)  

        products = json_data["props"]["pageProps"]["baseProduct"]["products_info"]["result"]
    
    except Exception :
        logger.exception(f"Error parsing product data ")
        return [], []

    # (info@) 
    badged_sites = []
    unbadged_sites = []
    try:
        for product in products: # 2 = 1(buy-box ) + 1 ((may be)old price)
            shop = product.get('shop_name', '')
            try:
                if product.get('availability') and not product.get('is_adv', False): # lookslike is_adv=true will have dupicate so this condition neccecery for delte one of them 
                    price = int(''.join(filter(str.isdigit, product.get('price_text', '0'))))
                    if product.get('is_filtered_by_warranty', False) :
                        badged_sites.append(Site(shop  , price, True ))  
                    else:
                        unbadged_sites.append(Site(shop  , price , False ))                   
            except Exception :
                logger.exception(f"Error processing product {shop} : ")
    except Exception :
        logger.exception(f"Error writing to other_sites.txt: ")
    logger.debug(f"Badged sites (len:{len(badged_sites)}): {badged_sites}")
    logger.debug(f"Unbadged sites (len:{len(unbadged_sites)}): {unbadged_sites}")
    return badged_sites , unbadged_sites 

    

def scrap (data_name):
    """ request torob for a product and return buy-box and 'RESULTS' of sites in 'Site' object arranged by priority """
    url = TorobURL.get_url(data_name)
    if url is None :
        logger.warning(f"url not was not avalable in csv for ='{data_name}'")
        return []
    logger.info(f"requesting torob at url={url}")
    try :
        response = RequestTorob.get_html(url)
        if response is None:
            logger.error("Failed to fetch Torob page.")
            return []
        soup = BeautifulSoup(response.content , "html5lib")    

        badged_sites , unbadged_sites = get_all_sites(soup) 
        sites = sorted(badged_sites + unbadged_sites)
        
        logger.info(f"Final sites list(len:{len(sites)}): {sites}")
        return sites
        # fix in new version if needed  :
        # code : age sites[0] bdard nemikhord
        #   sites[0] = sites[1] 
    except Exception :
        logger.exception(f"Error in scrap():")
        return []

    # return  badged_sites , unbadged_sites ,  sites , box  # age badged_sites , unbadged_sites  mikhaym 
