import requests  
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
with  open("input-here.txt", "r") as txtfile :
    curl = txtfile.read()
data = {  
    "curl-code" : curl
}  

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

try:
    response = requests.post("https://curlconverter.com/python/", data=data , headers=headers)
    response.raise_for_status()
except HTTPError as err:
    print(f'HTTP error occurred: {err}')  
except Exception as err:
    print(f'Other error occurred: {err}') 
else:
    print('Success! no expection')

with  open("resCURL.html" , "w" ,) as file  :
    file.write(response.text)


curlSoup = BeautifulSoup(response.text , 'html.parser')
code = curlSoup.find(id="generated-code")
results = code.find_all(class_="hljs-string")
for res in results :
    print(res.text)


#last news :  the site isnt handling any request ...its just js 