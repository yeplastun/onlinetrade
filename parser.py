from bs4 import BeautifulSoup
from requests import get
from time import sleep
from multiprocessing import Process
import re
import shutil
import os

def walk_site():
    fin = open('links_all.txt', 'r')
    fout = open('pics_url.txt', 'w')
    image_pattern = re.compile("^.*img\/items\/m.*\.jpg$")
    prefix = "http://www.onlinetrade.ru"
    #used_imgs=set()
    
    for line in fin:
        url = line
        print("looking page %s" % url[:-1])
        page = get(prefix + url)
        soup = BeautifulSoup(page.content, 'html.parser')
    
        imgs = set([x['src'] for x in soup.findAll(
                attrs={'src': image_pattern})]) #- used_imgs
    
        p = Process(target=load_imgs, args=(imgs,fout))
        p.start()

        del soup
        del page
    
        sleep(1)

def load_imgs(imgs, fout):
    prefix = "http://www.onlinetrade.ru"
    for img in imgs:
        img_link = prefix + img
        response = get(img_link, stream=True)
        img_dir = img[1:img.rfind("/")]
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        with open(img[1:], 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        #used_imgs.add(img)
        fout.write(img_link + "\n")
        print("\tSaved image: %s" % img[1:])


if __name__ == "__main__":
    walk_site()
