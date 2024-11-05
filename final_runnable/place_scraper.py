import pandas as pd
from email.mime import base
import requests
from bs4 import BeautifulSoup

def get_places_df():

    data = {
        "id": [],
        "name": [],
        "area": [],
        "description": [],
        "tag": []
    }

    base_url = "https://www.discovertheburgh.com/things-to-do-in-pittsburgh/#B"
    # Sending HTTP request
    req = requests.get(base_url)

    # Pulling HTTP data from internet
    sor = BeautifulSoup(req.text, "lxml")

    target_tag = ["B", "C"]
    count = 0
    for tag in target_tag:
        target_div = None
        div_list = sor.find_all("div")
        for div in div_list:
            a_B = div.find_all("a", {"name": tag})
            if a_B is not None and len(a_B) > 0:
                target_div = a_B[0].parent.parent
                break

        ul = target_div.find_all('ul')
        for li in ul:
            li_list = li.find_all('li')
            for l in li_list:
                name = l.find('a').text

                all_content = l.text
                # print(all_content)
                content = all_content.replace(name, "")
                content_arr = content.split('–')
                if len(content_arr) < 3:
                    area = ""
                    des = content_arr[1].strip()
                else:
                    area = content_arr[1].strip()
                    des = content_arr[2].strip()

                count = count + 1
                data["id"].append(count)
                data["name"].append(name)
                data["area"].append(area)
                data["description"].append(des)
                data["tag"].append(tag)

    #load data into a DataFrame object:
    df = pd.DataFrame(data)
    return df