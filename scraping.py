import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from json import loads
from bs4.element import Tag 

from constants import RESULTS , RESULTS_NUM

def search_google (data_name ,data_id):
    print("searching google for ", data_id, ":")
    try:
        from googlesearch import search
        import re
        query = data_name
        targets = []
        target_pattern = r"https://torob.com/"
        with open("searchResult_ME.txt","w") as file: #tst
            for result in search(query , RESULTS_NUM):
                file.write(f"\n{result}\n")
                if re.match(target_pattern,result):
                    targets.append( result)
        
        print("prinring all search results (first url will be used) :")
        print(targets)
        return targets
    except Exception as e:
        print(f"Error during Google search: {e}")
        return []

def get_html(url : str ) -> requests.Response:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url=url , headers=headers)
        response.raise_for_status()
    except HTTPError as err:
        print(f'HTTP error occurred: {err}')  
        return None
    except Exception as err:
        print(f'Other error occurred: {err}') 
        return None
    else:
        print('Success! no expection with url : ' ,response.url) 
        return response


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
from sortedcontainers import SortedList
import json # tst 
def get_all_sites (soup : BeautifulSoup)-> tuple[list[Site],list[Site],list[Site]]: 
    try:
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if not script_tag or not script_tag.string:
            print("Could not find the required script tag for product data.")
            return [], []
        json_data = loads(script_tag.string)  

        with open("test_data.json", "w", encoding="utf-8") as j: #tst
            json.dump(json_data, j, ensure_ascii=False, indent=4)
    
        products = json_data["props"]["pageProps"]["baseProduct"]["products_info"]["result"]
    except Exception as e:
        print(f"Error parsing product data: {e}")
        return [], []

    # (info@) 
    badged_sites = []
    unbadged_sites = []
    try:
       with open("other_sites.txt" , "w" , encoding='utf-8')as f : #tst (not all of down)
            for product in products[:RESULTS-2]: # 2 = 1(buy-box ) + 1 ((may be)old price)
                shop = product.get('shop_name', '')
                try:
                    if product.get('availability') and not product.get('is_adv', False):
                        price = int(''.join(filter(str.isdigit, product.get('price_text', '0'))))
                        badged = product.get('is_filtered_by_warranty', False)
                        if "اسپارک" in shop :
                            badged_sites.append(Site(None, price, True, False ))  
                            continue
                        if badged :
                            badged_sites.append(Site(shop  , price, True ))  
                        else:
                            unbadged_sites.append(Site(shop  , price , False ))                   

                        f.write(f"------{shop} ----------- {product.get('price_text', '')}  \n") # tst
                    else:
                        f.write(f"{shop} ----------- {product.get('price_text', '')} \n") # tst
                except Exception as e:
                    print(f"Error processing product {shop}: {e}")
    except Exception as e:
        print(f"Error writing to other_sites.txt: {e}")
    return badged_sites , unbadged_sites 

    

def scrap (data_name,data_id):
    """ search torob for a product and return buy-box and 'RESULTS' of sites in 'Site' object arranged by priority """
    try:
        results = search_google(data_name ,data_id)
        if not results:
            print("No search results found.")
            return []
        print("searching torob :")
        response = get_html(results[0]) # targets[0] = first torob result(url)
        if response is None:
            print("Failed to fetch Torob page.")
            return []
        soup = BeautifulSoup(response.content , "html5lib")    

        with  open("TorobResult3.html" , "w" , encoding='utf-8') as file  : #tst
            file.write(soup.prettify())

        badged_sites , unbadged_sites = get_all_sites(soup) # sites  = all sites 
        sites = sorted(badged_sites + unbadged_sites)
        
        return sites
    except Exception as e:
        print(f"Error in scrap(): {e}")
        return []
    # fix : aya "sites" ke dare kharej mishe be tartibe gheymate ? ---- bayad be tartib gheymat bashe ta algorithm man dorost kar kne

    # return  badged_sites , unbadged_sites ,  sites , box  # age badged_sites , unbadged_sites  mikhaym 
