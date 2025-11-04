import requests  
from bs4 import BeautifulSoup
import json
from import_logging import get_logger
from pathlib import Path
import pandas as pd
import UI
import sys
from urllib.parse import urlparse
from sortedcontainers import SortedList
from constants import RESULTS, RESULTS_NUM, SITE_NAME
import undetected_chromedriver as uc
import time
from googlesearch import search
import re

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
            url = cls.shorten_torob_url(cls.url_map[name])
            if url.startswith("http://"):
                url = "https://" + url[len("http://"):]
            return url
        except KeyError:
            logger.warning(f"name='{name}' not founded in csv")
            return None
        

def search_google (data_name):
    try:
        query = data_name
        target_pattern = r"https://torob.com/"
        search_results = search(query , RESULTS_NUM)
        for result in search_results:
            if re.match(target_pattern,result):
                target = result
                break
        if not target:
            return None
        return target
    except Exception :
        logger.exception(f"Error during Google search:")
        return None


class RequestTorob :
    _session = None  
    
    @classmethod
    def _init_session(cls):
        if cls._session is None :
            cls._session = requests.Session()
            cls._session.headers.update(        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8,fr;q=0.6",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.bing.com/"
        })
        
    @classmethod
    def get_html(cls , url):# use sleep in updateAll if using this 
        cls._init_session()
        try:
            response = cls._session.get(url)
            response.raise_for_status()
            logger.debug(f'request Successed!')
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        except Exception as e:
            logger.error(f'some error occurred in requesting: {e}')
        return None


def get_html(url: str):
    try:
        options = uc.ChromeOptions()
        options.headless = True  # runs invisible : False for CAPTCHA input
        options.add_argument("--window-size=300,300")# Set viewport size for headless rendering
        driver = uc.Chrome(options=options)
        driver.set_window_position(10000, 0)
        driver.set_window_size(300, 300)
        driver.get(url)
        # input("If you see a CAPTCHA, solve it in the browser, then press Enter here...")
        time.sleep(2)  # Give page time to load
        html = driver.page_source
        driver.quit()
        logger.debug(f'request Successed!')
        return html.encode('utf-8')
    except Exception:
        logger.exception(f'some error occurred in requesting: ')
        return None


class Site :
    def __init__(self , shop_name  , price : int , city='', last_change='', score_text='', badged = False ) :
        self.name = shop_name
        self.price = int(price )
        self.badged = badged
        self.city = city
        self.last_change = last_change
        self.score_text = score_text
        if shop_name == SITE_NAME or price == 0:
            self.suggested_price = "dont change price"
        else:
            self.suggested_price = self._suggest()
        
    def __repr__(self):
        return (f"Site(name={self.name!r}, price={self.price}, "
                f"badged={self.badged}, suggested_price={self.suggested_price!r})")

    def __lt__(self, other):  # Define sorting rule = buy-box of Torob priority rule 
        if self.price == 0 or other.price == 0: # appending empty prices at end 
            return other.price == 0 and self.price != 0
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
        
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "badged": self.badged,
            "city": self.city,
            "last_change": self.last_change,
            "score_text": self.score_text
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            shop_name=data.get("name"),
            price=data.get("price", 0),
            city=data.get("city", ''),
            last_change=data.get("last_change", ''),
            score_text=data.get("score_text", ''),
            badged=data.get("badged", False)
        )


def get_all_sites (soup : BeautifulSoup): 
    try:
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if not script_tag or not script_tag.string:
            if soup.find("title", string="آیا شما یک ربات هستید؟‌ | ترب"):
                logger.error("Blocked by cloudflare")
            else:
                logger.error("Could not find the required script tag for product data.")
            return []
        json_data = json.loads(script_tag.string)

        products = json_data["props"]["pageProps"]["baseProduct"]["products_info"]["result"]
    except Exception as e:
        logger.error(f"Error parsing product data : {e}")
        raise
    sites = SortedList()
    shop = None
    for product in products[:RESULTS*2]:
        try:
            shop = product.get('shop_name')
            if product.get('availability') and not product.get('is_adv', False): # lookslike is_adv=true will have dupicate so this condition neccecery for delte one of them 
                price = int(''.join(filter(str.isdigit, product.get('price_text', '0'))))
                city = product.get('shop_name2', '')
                last_change = product.get('last_price_change_date', '')
                score_text = product.get('score_info', {}).get('score_text', '')
                badged = product.get('is_filtered_by_warranty', False)
                sites.add(Site(shop, price, city, last_change, score_text, badged))
        except Exception :
            logger.exception(f"Error processing product for site ={shop} : ")
    return sites

    

def scrap (data_name , url):
    """ request torob for a product and return buy-box and 'RESULTS' of sites in 'Site' object arranged by priority """
    if url is None :
        url = TorobURL.get_url(data_name)
    if url is None :
        url = search_google(data_name)
        logger.warning(f"url not was not avalable in csv for ='{data_name}'")
    if url is None :
        logger.warning(f"url also not found in search google")
        return SortedList() , None
    logger.info(f"requesting torob at url={url}")
    try :
        response = get_html(url)
        if response is None:
            logger.warning("Failed to get torob.com response")
            return SortedList() , url
        soup = BeautifulSoup(response, "html5lib")    
        sites = get_all_sites(soup) 
        if not sites :
            logger.warning(f"not any sites found at torob.result for product = {data_name}")
        else :
            logger.info(f"Final sites list(len:{len(sites)}): {sites}")
            return sites , url
    except Exception as e:
        logger.error(f"Error in scrap():{e}")
    return SortedList() , url
