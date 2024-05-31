"""
aim: take an url, save a csv containing products sl no, name, price, image url, reviews
"""

import os
import requests
import shutil
import pandas as pd
import numpy as np
from requests_html import HTML # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))




def url_to_txt(url, filename="details.html", save = False):
    r= requests.get(url)
    if r.status_code==200:
        html_text= r.text
        if save:
            with open("details.html", "w") as f :
                f.write(html_text)
        return html_text
    else:
        return print("Page not found!!")
    
def parse_and_extract(url, name =None):
    html_text = url_to_txt(url)

    re_html = HTML(html =html_text)

    re_brands= re_html.find(".iW697U")
    
 
    re_names= re_html.find(".wjcEIp")
    re_price= re_html.find(".Nx9bqj")
    re_rating= re_html.find(".Y1HWO0")

    # print(len(re_names), len(re_price))
    assert len(re_names)==len(re_price)==len(re_rating)
    table_data=[]
    header_names=["Sl No", "Product Name", "Price", "Rating"]
    
    sl_no= 1
    for pr_name, pr_price, re_rating in zip(re_names, re_price, re_rating):
        pr_name= pr_name.text
        pr_price= int(pr_price.text.split("₹")[1].replace(",", ""))
        re_rating= re_rating.text
        table_row= [sl_no, pr_name, pr_price, re_rating]
        table_data.append(table_row)
        sl_no +=1
        

    
    # print(header_names)
    # for item in table_data:
    #     print(item)
    #saving data in a csv file
    df = pd.DataFrame(table_data, columns=header_names)
    path = os.path.join(BASE_DIR, "Products")
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join("Products", f'{name}.csv')
    df.to_csv(file_path, index=False)
    return True
    

if __name__ =="__main__":
    parse_and_extract(url= "https://www.flipkart.com/mobile-phones-store?fm=neo%2Fmerchandising&iid=M_a76c5c1f-341e-4223-8a51-5fdd08c3d89b_1_372UD5BXDFYS_MC.ZRQ4DKH28K8J&otracker=hp_rich_navigation_2_1.navigationCard.RICH_NAVIGATION_Mobiles_ZRQ4DKH28K8J&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_2_L0_view-all&cid=ZRQ4DKH28K8J", name ="mobiles_4")

