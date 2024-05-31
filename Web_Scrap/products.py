"""
aim: take an url, save a csv containing products sl no, name, price, image url, reviews
"""

import os
import requests
import shutil
import pandas as pd
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

    re_names= re_html.find(".grid-product__title--body")
    re_price= re_html.find(".grid-product__price")
    # print(len(re_names), len(re_price))
    assert len(re_names)==len(re_price) 
    table_data=[]
    sl_no= 1
    for pr_name, pr_price in zip(re_names, re_price):
        pr_name= pr_name.text
        pr_price= pr_price.text.split(".00")[0].split("MRP: ₹ ")[1] + ".00"
        table_row= [sl_no, pr_name, pr_price]
        table_data.append(table_row)
        sl_no +=1
        

    
    header_names=["Sl No", "Product Name", "Price"]
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
    parse_and_extract(url= "https://scentido.com/", name ="perfume")
