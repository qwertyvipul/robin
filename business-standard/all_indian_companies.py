import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

base_url = "https://www.business-standard.com"
a2z_url = base_url + "/stocks/stock-quote-list"

res = requests.get(a2z_url)
if res.status_code != 200:
    raise Exception("Page not found " + a2z_url)
    
soup = BeautifulSoup(res.text, "html.parser")
a2z_ul = soup.find("ul",{"class":"A-Z-links"})
a2z_lis = a2z_list.find_all("li", {"class":"pT5"})

a2z_links = []
for li in a2z_lis:
    a2z_links.append([li.a.string, base_url + li.a.get("href")])
    
df = pd.DataFrame(a2z_links, columns=["A-Z", "Link"])
df.to_csv("data/a2z_links.csv", index=None)

a2z_queue = []
crawled = []
companies = []
    
for az_link in a2z_links:
    az_path = "data/" + az_link[0]
    az_url = az_link[1] + "/1"
    if not os.path.isdir(path):
        os.mkdir(path)
        
    az_res = requests.get(az_url)
    if az_res.status_code != 200:
        raise Exception("Page not found " + az_url)
        
    az_soup = BeautifulSoup(az_res.text, "html.parser")
    az_next = az_soup.find("div", {"class":"next-colum"})
    az_queue = []
    az_queue.append(az_url)
    next_btn = az_next
    
    while next_btn != None:
        next_url = base_url + next_btn.a.get("href")
        print(next_url)
        az_queue.append(next_url)
        next_res = requests.get(next_url)
        next_soup = BeautifulSoup(next_res.text, "html.parser")
        next_btn = next_soup.find("div", {"class":"next-colum"})
    
    a2z_queue.extend(az_queue)
    
df = pd.DataFrame(a2z_queue, columns=["Links"])
df.to_csv("data/a2z_queue.csv", index=None)

all_companies = []
for i, link in enumerate(a2z_queue):
    if i < 364:
        continue
    print(i+1)
    page_url = link
    page_res = requests.get(page_url)
    page_soup = BeautifulSoup(page_res.text, "html.parser")
    main_cont = page_soup.find("div", {"class":"main-cont-left"})
    table = main_cont.find("table")
    trs = table.find_all("tr")
    
    for tr in trs[1:]:
        tds = tr.find_all("td")
        all_companies.append([
                tds[0].string, 
                tds[1].string if tds[1].string != None else "", 
                tds[2].string if tds[2].string != None else "",
                base_url + tds[0].a.get("href")])
    
df = pd.DataFrame(all_companies, columns=["COMPANY NAME", 
                                          "BSE CODE",
                                          "NSE SYMBOL",
                                          "BS LINK"])
    
df.to_csv("data/all_companies.csv", index=None)
    
    
    