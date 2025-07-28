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
from constants import RESULTS
import random
from config import HEADERS_LIST , PROXIES

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
        


class RequestTorob :
    _session = None
    _proxies = PROXIES.copy()
    _headers_list = HEADERS_LIST.copy()
    _proxy_index = 0
    _header_index = 0

    @classmethod
    def _init_session(cls):
        if cls._session is None:
            cls._session = requests.Session()
            random.shuffle(cls._proxies)
            cls._proxies = cls._validate_proxies(cls._proxies)
            if not cls._proxies:
                logger.warning("No valid proxies available after validation.")
            random.shuffle(cls._headers_list)

    @classmethod
    def _validate_proxies(cls, proxy_list, test_url="https://httpbin.org/ip", timeout=5):
        valid = []
        logger.info("checkng validation of proxies...")
        for proxy in proxy_list:
            proxy_cfg = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            try:
                resp = requests.get(test_url, proxies=proxy_cfg, timeout=timeout)
                logger.warning(f"Proxy {proxy} returned status {resp.status_code}")
                if resp.status_code == 200:
                    valid.append(proxy)
            except Exception as e:
                logger.warning(f"Proxy {proxy} failed validation: {e}")
        logger.info("checkng validation of proxies finifshed...")
        return valid

    @classmethod
    def _get_next_proxy(cls):
        if not cls._proxies:
            return None
        proxy = cls._proxies[cls._proxy_index % len(cls._proxies)]
        cls._proxy_index += 1
        return {"http": f"http://{proxy}","https": f"http://{proxy}",}

    @classmethod
    def _get_next_headers(cls):
        if not cls._headers_list:
            return {}
        headers = cls._headers_list[cls._header_index % len(cls._headers_list)]
        cls._header_index += 1
        return headers

    @classmethod
    def get_html(cls, url, max_retries=1, timeout=10):
        cls._init_session()
        for attempt in range(1, max_retries + 1):
            proxy = cls._get_next_proxy()
            hdrs = cls._get_next_headers()
            proxy_ip = proxy.get("http") if proxy else "No Proxy"
            try:
                response = cls._session.get(url,proxies=proxy,headers=hdrs,timeout=timeout)
                snippet = response.text[:5000].lower()
                if not response.text.strip() or any(blk in snippet for blk in ("access denied", "verify you are human", "blocked", "captcha")):
                    logger.warning(f"Attempt {attempt}: blocked or empty via proxy={proxy}, Using IP = {proxy_ip}, headers={hdrs.get('User-Agent')}")
                    continue
                response.raise_for_status()
                logger.debug(f"Attempt {attempt}: success via proxy={proxy}, Using IP = {proxy_ip}, headers={hdrs.get('User-Agent')}")
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt} failed with proxy={proxy}, Using IP = {proxy_ip}, headers={hdrs.get('User-Agent')}: {e}")
        logger.error("All attempts failed.")
        return None


class Site :
    def __init__(self , shop_name  , price : int , city='', last_change='', score_text='', badged = False ) :
        self.name = shop_name
        self.price = int(price )
        self.badged = badged
        self.city = city
        self.last_change = last_change
        self.score_text = score_text
        if shop_name == "اسپارک دیجی" or price == 0:
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
            logger.error("Could not find the required script tag for product data.")
            return [], []
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
        logger.warning(f"url not was not avalable in csv for ='{data_name}'")
        return SortedList() , None
    logger.info(f"requesting torob at url={url}")
    try :
        response = RequestTorob.get_html(url)
        if response is None:
            logger.warning("Failed to get torob.com response")
            return SortedList() , url
        soup = BeautifulSoup(response.content , "html5lib")    
        sites = get_all_sites(soup) 
        if not sites :
            logger.warning(f"not any sites found at torob.result for product = {data_name}")
        else :
            logger.info(f"Final sites list(len:{len(sites)}): {sites}")
            return sites , url
    except Exception as e:
        logger.error(f"Error in scrap():{e}")
    return SortedList() , url
