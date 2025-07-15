import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from json import loads
from bs4.element import Tag 

from constants import RESULTS , RESULTS_NUM
from import_logging import get_logger

logger = get_logger(__name__)

def search_google (data_name):
    try:
        from googlesearch import search
        import re
        query = data_name
        targets = []
        target_pattern = r"https://torob.com/"
        search_results = search(query , RESULTS_NUM)
        for result in search_results:
            if re.match(target_pattern,result):
                targets.append( result)
        if not targets:
            logger.warning(f"not any torob found in first {RESULTS_NUM}-- results of google: {search_results}")
            return []

        logger.debug(f"Google torob search result(s): {targets}")
        return targets
    except Exception :
        logger.exception(f"Error during Google search:")
        return []

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

def get_html(url: str):
    try:
        options = Options()
        options.headless = False  # Show browser so you can solve CAPTCHA
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        # input("If you see a CAPTCHA, solve it in the browser, then press Enter here...")
        time.sleep(2)  # Give page time to load after CAPTCHA
        html = driver.page_source
        driver.quit()
        logger.debug(f'request Successed!')
        return html.encode('utf-8')
    except Exception:
        logger.exception(f'some error occurred in requesting: ')
        return None
class Site :
    def __init__(self , shop_name  , price : int , badged : bool = False , suggest_price : bool = True) :
        """if Site.name is spark->suggest_price must be False """
        self.name = shop_name
        self.price = int(price )
        self.badged = badged
        if suggest_price :
            self.suggested_price = self._suggest()
        else:
            self.suggested_price = "dont change price"
        
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
                    badged = product.get('is_filtered_by_warranty', False)
                    if "اسپارک" in shop :
                        badged_sites.append(Site("oldSP", price, True, False ))  
                        continue
                    if badged :
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
    """ search torob for a product and return buy-box and 'RESULTS' of sites in 'Site' object arranged by priority """
    try:
        results = search_google(data_name)
        if not results:
            return []
        logger.info(f"requesting torob at url={results[0]}")
        response = get_html(results[0]) # targets[0] = first torob result(url)
        if response is None:
            logger.error("Failed to fetch Torob page.")
            return []
        soup = BeautifulSoup(response , "html5lib")    

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
