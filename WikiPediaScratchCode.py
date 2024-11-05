
import pandas as pd
from email.mime import base
import requests
from bs4 import BeautifulSoup
import re

def get_wiki_des(wiki_url):
  wiki_req = requests.get(wiki_url)
  wiki_sor = BeautifulSoup(wiki_req.text, "lxml")
  for div in wiki_sor.find_all("div", {'class':'thumb tright'}): 
    # remove 'class':'thumb tright'
    div.decompose()

  wiki_name_item = wiki_sor.find("span", {"class":"mw-page-title-main"})
  wiki_all_item = wiki_sor.find("div", {"id":"mw-content-text"})
  wiki_start_item = wiki_sor.find("table", {"class":re.compile(r"infobox(\s\w+)?")})
  wiki_end_item = wiki_sor.find("div", {"id":"toc"})
  wiki_all_item_txt = wiki_all_item.text
  wiki_name_item_txt = wiki_name_item.text

  if wiki_start_item is not None and wiki_end_item is not None:
    wiki_start_item_txt = wiki_start_item.text
    wiki_end_item_txt= wiki_end_item.text
    start_id = wiki_all_item_txt.find(wiki_start_item_txt) + len(wiki_start_item_txt)
    end_id = wiki_all_item_txt.find(wiki_end_item_txt)

    if start_id > end_id:
      start_id = 0
    description = wiki_all_item_txt[start_id:end_id].replace("\n", "")
  else:
    description = wiki_all_item_txt.replace("\n", "")

  return wiki_name_item_txt, description

data = {
  "id": [],
  "Site": [],
  "Description": [],
  "url": []
}

# base_url = "https://www.google.com/travel/things-to-do?g2lb=2502548,2503771,2503781,4258168,4270442,4284970,4291517,4306835,4518326,4597339,4718358,4723331,4757164,4810789,4810790,4814050,4816977,4826689,4852066,4854899,4856937,4858541,4861687,4865307,4868440,26483160&hl=en-US&gl=us&ssta=1&dest_mid=/m/068p2&dest_state_type=main&dest_src=ts&sa=X&ved=2ahUKEwiAy-Sjrcf6AhWGkIkEHV3ACOsQuL0BegQIGhAy"
# all top sight
base_url = "https://www.google.com/travel/things-to-do/see-all?g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4518326%2C4597339%2C4718358%2C4723331%2C4757164%2C4810789%2C4810790%2C4814050%2C4816977%2C4826689%2C4852066%2C4854899%2C4856937%2C4858541%2C4861687%2C4865307%2C4868440%2C26483160&hl=en-US&gl=us&ssta=1&dest_mid=%2Fm%2F068p2&dest_state_type=sattd&dest_src=ts&sa=X&ved=2ahUKEwiAy-Sjrcf6AhWGkIkEHV3ACOsQuL0BegQIGhAy"

# Sending HTTP request
req = requests.get(base_url)

# Pulling HTTP data from internet
sor = BeautifulSoup(req.text, "lxml")

item_list = sor.find_all("div", {"class":"Ld2paf", "jscontroller":"RVAT1"})
print("total size: ", len(item_list))

item_list = item_list[:50]  # top 50
print("select top 50: ", len(item_list))

for i in range(len(item_list)):
    item = item_list[i]
    sub_url = item['data-href']

    # print(sub_url)
    sub_req = requests.get(sub_url)
    sub_sor = BeautifulSoup(sub_req.text, "lxml")
   
    sub_item_list = sub_sor.find_all("a")
    # print(len(sub_item_list))
    for sub_item in sub_item_list:
        if sub_item.text.find('Wikipedia') > -1:
            wiki_url = sub_item['href']
            start_id = 7 # "/url?q="
            end_id = wiki_url.find("&")
            wiki_url = wiki_url[start_id:end_id]
            wiki_url = wiki_url.replace("%25", "%")
            site_name, description = get_wiki_des(wiki_url)
            print(i, site_name, wiki_url)

            data["id"].append(i)
            data["Site"].append(site_name)
            data["Description"].append(description)
            data["url"].append(wiki_url)


#load data into a DataFrame object:
df = pd.DataFrame(data)

print(df)

output_path = "./WikiPedia_Data.csv"
df.to_csv(output_path, sep='\t', encoding='utf-8')

print("saved!")
