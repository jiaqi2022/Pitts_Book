from bs4 import BeautifulSoup as bs

import re
import urllib
import requests
import numpy as np
import pandas as pd


def restaurants_html_to_df():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

    rs_table = {'name': [], 'rating':[], 'type':[], 'area':[], 'href': []}

    # there are total of 24 pages of result
    i = 0
    while i < 240:
        url='https://www.yelp.com/search?find_desc=Restaurants&find_loc=Pittsburgh%2C+PA&start='+str(i)
        response=requests.get(url,headers=headers)
        soup = bs(response.content,'lxml')

        rates = [x for x in soup.find_all('span', {'class':'css-gutk1c', 'data-font-weight':'semibold'})]
        if rates == [] or rates[3].getText() == '':
            continue

        if len(rates)==14:
            for rate in rates[3:-1]:
                rs_table['rating'].append(float(rate.getText()))
        elif len(rates)==13:
            for rate in rates[2:-1]:
                rs_table['rating'].append(float(rate.getText()))

        # By filtering the redirect link we will remove the Sponsored Results,
        # since the href for Ads does not begin with '/biz'.
        for name in soup.find_all('a', class_="css-1m051bw", href=re.compile("^/biz")):
            rs_table['name'].append(urllib.parse.unquote(name['name']))
            rs_table['href'].append(urllib.parse.unquote(name['href']))

        for detail in [x for x in soup.find_all('p', {'class':'css-dzq7l1'})][2:-1]:
            types = detail.find_all('span', {'class':'css-11bijt4'})
            rs_table['type'].append([type.getText() for type in types])

            area = detail.find('span', {'class':'css-chan6m'})
            rs_table['area'].append(area.getText())
        i += 10
    

    df = pd.DataFrame(data=rs_table)

    df.loc[df['area'] == '$', 'area'] = ''
    df.loc[df['area'] == '$$', 'area'] = ''
    return df


def get_types(df):
    restraunt_arr = np.array([item for sublist in df['type'] for item in sublist])
    restraunt_arr = np.unique(restraunt_arr)
    return restraunt_arr.tolist()


def get_areas(df):
    area_lst = np.unique(np.array(df['area'])).tolist()
    try:
        area_lst.remove('')
    except ValueError:
        print('Item \'\' not found in the Area list')
    return area_lst


