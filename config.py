# import requests
# from bs4 import BeautifulSoup

# url = "https://proxy5.net/fa/free-proxy/iran"
# headers = {"User-Agent": "Mozilla/5.0"}

# resp = requests.get(url, headers=headers)
# if resp.status_code != 200:
#     raise RuntimeError(f"Failed to fetch page, status {resp.status_code}")

# soup = BeautifulSoup(resp.text, "html.parser")

# table = soup.find("table", class_="table-responsive")
# if not table:
#     raise RuntimeError("Proxy table not found")

# proxies = []

# for tr in table.find_all("tr")[1:]:
#     cols = tr.find_all("td")
#     if len(cols) < 5:
#         continue

#     ip       = cols[0].get_text(strip=True)
#     port     = cols[1].get_text(strip=True)
#     proto    = cols[2].get_text(strip=True).lower()
#     country_td = cols[4].select_one(".country-name strong")
#     country  = country_td.get_text(strip=True) if country_td else ""

#     if country == "ایران" and proto == "http":
#         proxies.append(f"{ip}:{port}")

# print("PROXIES = [")
# for p in proxies:
#     print(f'    "{p}",')
# print("]")

PROXIES = [
    "31.14.114.69:1081",
    "193.3.182.14:3128",
    "31.14.114.75:1081",
    "94.182.146.250:8080",
    "31.14.114.67:1081",
    "85.133.240.75:8080",
    "185.172.214.112:80",
    "84.241.30.214:8080",
    "31.14.114.77:1081",
    "78.39.10.11:3128",
    "185.88.177.197:8080",
    "194.39.254.35:80",
    "194.39.254.196:80",
    "31.14.114.68:1081",
    "185.105.102.189:80",
    "31.14.114.72:1081",
    "5.190.36.4:3128",
]

HEADERS_LIST =[
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.google.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8,fr;q=0.6",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.bing.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.7,ru;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://duckduckgo.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/114.0.1823.51",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.yahoo.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://m.google.com/"
        },
        {
            "User-Agent": "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
            "Accept": "text/html,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": "https://www.opera.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.apple.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.linkedin.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.reddit.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 12; en-US; SM-G975F Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.41 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": "https://www.android.com/"
        }
    ]

