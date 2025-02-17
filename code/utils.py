#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:59:08 2020

@author: ludivinelacour
"""

import requests
from bs4 import BeautifulSoup
import pymysql
from sqlalchemy import create_engine

def get_html(url):
    
    headers="user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    headers=dict([i.split(': ') for i in headers.split('\n')])
    
    html=requests.get(url,headers=headers).content
    soup=BeautifulSoup(html)
    
    return soup


def get_json(url,speciality,location,page_num):
    
    headers=f"""accept: application/json
    accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7
    cache-control: no-cache
    content-type: application/json; charset=utf-8
    cookie: __cfduid=d2b5aa87f9a6624d7b6d080621c78dd071584958668; ssid=c8003987149mac-5zfwbZlNIgv0; cookie_consent=true; esid=Hag6WnEswqPNmOsSdO6nq8Jg; last_place=%7B%22place_id%22%3A%22ChIJD7fiBh9u5kcRYJSMaMOCCwQ%22%2C%22name%22%3A%22Paris%22%7D; utm_b2b=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaUoxZEcxZmMyOTFjbU5sUFdScGNtVmpkQ1oxZEcxZmJXVmthWFZ0UFFZNkJrVlUiLCJleHAiOiIyMDIwLTA0LTEwVDExOjMwOjQ5LjM3MloiLCJwdXIiOiJjb29raWUudXRtX2IyYiJ9fQ%3D%3D--34c8fb3207d661d5f08f5fd3388cb219e6a450ca; _doctolib_session=Hhv7pWEDJwdnyCQyqr7ThfPEQcS62D9lKg7M%2Fvz8R0AIHipjT1Hu8SN0rhu51Urw8FXsHuPmX0L2UfmzU62ZifdY0%2Ful6siBegn1tBS9xIOE68s0L8WvzGo2NpZ3WtP8lg7du3f9lA%2BDUY9qvMjbXWQbsnHeE2GdX%2F46rLZZ%2FDvPRwaKV4ZcEYrliAJoVx%2BTeyLg634T5KloWv2A4kStpH7OzTg2A%2FQs8TpEaffKhJckYWtV7uE0BQYcDW14sU3N18VFz1X3RU3uXoAhQxw7%2FcQgncDD4sdPdsO%2FUY7ou2T0IOMmi%2FkJL%2B2sVlpGRgfv21I5BaJFK0fu9l3YgjDL5BuvupSKtAxlaw%3D%3D--jN4XvOBX1kwEvjNq--YuCqF8thsE1OjQaZOd%2B%2Fug%3D%3D
    referer: https://www.doctolib.fr/{speciality}/{location}?page={1 if page_num<2 else page_num-1}
    user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
    x-csrf-token: +AD1NNffpu2TUGR+i552cv/SJOdpo7KzgJOwVBys6r3/EBA3AwlvUidQ0R+FVeD3cUpNqeH+LYB2447FTjv7Rg=="""
    headers=dict([i.strip().split(': ') for i in headers.split('\n')])

    result=requests.get(url,headers=headers).json()
    
    return result


def get_specialities():
    # Get the list of specialities
    url='https://www.doctolib.fr/specialities'
    
    soup=get_html(url)
    
    list_of_specialities_slug=[i["href"].strip('/') for i in soup.select('h1+div a')]
    list_of_specialities=[i.text for i in soup.select('h1+div a')]
    
    return list_of_specialities_slug, list_of_specialities


def get_db_connexion(database, username='root',host='localhost', password=''):
    
    engine=create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')
    
    return engine