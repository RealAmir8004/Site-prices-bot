import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from json import loads
from bs4.element import Tag 

from constants import RESULTS , RESULTS_NUM

def search_google (data_name ,data_id):
    print("searching google for ", data_id, ":")
    from googlesearch import search
    import re
    query = data_name
    targets = []
    target_pattern = r"https://torob.com/"
    with open("searchResult_ME.txt","w") as file:
        for result in search(query , RESULTS_NUM):
            file.write(f"\n{result}\n")
            if re.match(target_pattern,result):
                targets.append( result)
    
    print("prinring all search results (first url will be used) :")
    print(targets)
    return targets

def get_html(url : str ) -> requests.Response:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url=url , headers=headers)
        response.raise_for_status()
    except HTTPError as err:
        print(f'HTTP error occurred: {err}')  
    except Exception as err:
        print(f'Other error occurred: {err}') 
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

    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    
    json_data = loads(script_tag.string)  

    with open("test_data.json", "w", encoding="utf-8") as j: #tst
        json.dump(json_data, j, ensure_ascii=False, indent=4)
    
    products = json_data["props"]["pageProps"]["baseProduct"]["products_info"]["result"]

    # (info@) 
    badged_sites = []
    unbadged_sites = []
    with open("other_sites.txt" , "w" , encoding='utf-8')as f : #tst (not all of down)

        for product in products[:RESULTS-2]: # 2 = 1(buy-box ) + 1 ((may be)old price)
            shop = product['shop_name']
                                
            if product['availability'] and product['is_adv'] == False :

                price = int(''.join(filter(str.isdigit, product['price_text'])))

                badged = product['is_filtered_by_warranty']

                if "اسپارک" in shop :
                    badged_sites.append(Site(None, price, True, False ))  
                    continue
                if badged :
                    badged_sites.append(Site(shop  , price, True ))  
                else:
                    unbadged_sites.append(Site(shop  , price , False ))

                f.write(f"------{shop} ----------- {product['price_text']}  \n") # tst
            else :
                f.write(f"{shop } ----------- {product['price_text']} \n") # tst
    return badged_sites , unbadged_sites 

    

def scrap (data_name,data_id):
    """ search torob for a product and return buy-box and 'RESULTS' of sites in 'Site' object arranged by priority """
    results = search_google(data_name ,data_id)
    print("searching torob :")
    response = get_html(results[0]) # targets[0] = first torob result(url)

    soup = BeautifulSoup(response.content , "html5lib")    
    
    with  open("TorobResult3.html" , "w" , encoding='utf-8') as file  : #tst
        file.write(soup.prettify())

        #def get_sites (soup : BeautifulSoup):  
    
    buy_box : Tag= soup.find('div', class_='Showcase_buy_box__q4cpD') # class = Showcase_buy_box__q4cpD # badge =.Showcase_guarantee_badge_text__Kz3AW
    # code : age buy_box bdard nemikhord
    #   buy_box = olaviat ydone  badish jaygozin she 

    badged_sites , unbadged_sites = get_all_sites(soup) # sites  = all sites 
    
    box_name , box_price = buy_box.find_all('div' , class_='Showcase_buy_box_text__otYW_ Showcase_ellipsis__FxqVh')  
    box = Site( box_name.get_text(strip=True)[8:] ,  int(''.join(filter(str.isdigit, box_price.get_text(strip=True)))) ) # ye object 'Site' az 'buy_box' misaze
    if box.name in [site.name for site in badged_sites]: # ckeck if guarantee_badge !!!!!!!!! mohem : in behtarin halate  bekhate algoritm buy_box torob
        box.badged = True
    print(f"buy box = {box.price}", end=" ") #tst
    
    sites = sorted(badged_sites + unbadged_sites)
    sites.insert(0, box)
    return sites

    # fix : aya "sites" ke dare kharej mishe be tartibe gheymate ? ---- bayad be tartib gheymat bashe ta algorithm man dorost kar kne

    # return  badged_sites , unbadged_sites ,  sites , box  # age badged_sites , unbadged_sites  mikhaym 
