import os
import sys
import datetime
import requests
import pandas as pd
from requests_html import HTML # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def url_to_txt(url, filename="world.html", save = False):
    r= requests.get(url)
    if r.status_code==200:
        html_text= r.text
        if save:
            with open("world.html", "w") as f :
                f.write(html_text)
        return html_text
    else:
        return print("Page not found!!")
    
def parse_and_extract(url, name ="new file"):
    html_text = url_to_txt(url) #return an html file
    if html_text==None:
        return print("No html text found!!")

    r_html = HTML(html = html_text)
    table_class = ".imdb-scroll-table" # a-section of a class; ".class", "#table"\
    r_table= r_html.find(table_class)
    # print(r_table[0].text)

    #to store table datas in a nesteted list
    table_data=[]
    parsed_table =r_table[0] #object form
    rows = parsed_table.find("tr")
    header_row = rows[0]
    # print(header_row.text)
    header_cols = header_row.find("th") # <class 'list'> or list object
    header_names=[x.text for x in header_cols ]
    # print(header_names)
    for row in rows[1:]: # excluding 0 index i.e. header names
        cols= row.find("td")   # td = cell/ block
        row_data=[]
        for col in cols:
            row_data.append(col.text)
        table_data.append(row_data)

    # print(header_names)
    # print(table_data)

    #saving data in a csv file
    df = pd.DataFrame(table_data, columns=header_names)
    path = os.path.join(BASE_DIR, "Data")
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join("Data", f'{name}.csv')
    df.to_csv(file_path, index=False)
    return True

#using the code for different times
def run(start_year=None, years_ago= None):
    if start_year==None:
        now= datetime.datetime.now()
        start_year = now.year
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f'{start_year}')==4
    for i in range(0, years_ago +1):
        url =f"https://www.boxofficemojo.com/year/world/{start_year}/"
        finished = parse_and_extract(url=url, name =start_year)
        if finished:
            print(f'Finished {start_year}')
        else:
            print(f'{start_year} not finished.')
        start_year -=1



if __name__=="__main__":
    try:
        start= int(sys.argv[1])
    except:
        start= None
    
    try:
        count= int(sys.argv[2])
    except:
        count =0
    run(start_year=start, years_ago=count)
    

