import os 
import requests
import shutil
from requests_html import HTML # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

url ="https://beebom.com/naruto-sasori-facts/"



def saga(url):
    re = requests.get(url=url, stream=True)
    html_text = re.text
    re_html = HTML(html = html_text)
    re_div= re_html.find("h3")
    content_list=[]
    for obj in re_div:
        content= obj.text
        content_list.append(content)

    content_list= content_list[:-2]

    print("Saga in One Piece: \n")
    for item in content_list:
        print(item)
    print("----------------------")

def arc(url):
    re = requests.get(url=url, stream=True)
    html_text = re.text
    re_html = HTML(html = html_text)
    re_div= re_html.find("h4")
    content_list=[]
    for obj in re_div:
        content= obj.text
        content_list.append(content)

    content_list= content_list[:-5]

    print("Arc in One Piece: \n")
    for sl_no, item in enumerate(content_list):
        print(f"{sl_no +1} {item}")
    print("----------------------")

# arc()



    

def download(url, directory, fname=None):
    if not fname: # if filename is not given
        fname = os.path.basename(url)  #create a new name
    ul_downloaded_image_path = os.path.join(directory, fname)
    with requests.get(url, stream=True) as response:
        with open(ul_downloaded_image_path, 'wb') as file_obj: #wb for write bytes
            shutil.copyfileobj(response.raw,file_obj) #shutil.copy(source, destination, *, follow_symlinks = True)
    return ul_downloaded_image_path



def get_url_and_download(url):
    re = requests.get(url=url, stream=True)
    html_text = re.text
    re_html = HTML(html = html_text)
    re_class= re_html.find(".wp-block-image img")
    re_img_list=[]
    for img in range(0, len(re_class)):
        re_img = re_class[img].attrs["src"]
        re_img_list.append(re_img)
    
        # print(re_img) # image url
        img_url = re_img.split(".jpg")[0] +".jpg"
        # print(img_url)
        download(img_url, DOWNLOADS_DIR)
        print(f"Finisihed image {img+1}")

get_url_and_download(url)