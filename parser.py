from bs4 import BeautifulSoup
from requests import get
from time import sleep
from math import ceil
import re
import shutil
import os


fin = open('links_all.txt', 'r')
fout = open('pics_url.txt', 'w')
image_pattern = re.compile("^.*img\/items\/m.*\.jpg$")
prefix = "http://www.onlinetrade.ru"
used_imgs=set()
cnt = 1

for line in fin:
    url = line
    print("looking page %s" % url)
    page = get(prefix + url)
    soup = BeautifulSoup(page.content, 'html.parser')

    imgs = set([x['src'] for x in soup.findAll(
            attrs={'src': image_pattern})]) - used_imgs

    for img in imgs:
        img_link = prefix + img
        response = get(img_link, stream=True)
        img_dir = img[1:img.rfind("/")]
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        with open(img[1:], 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        used_imgs.add(img)
        fout.write(img_link + "\n")
        print(str(cnt) + " Saved image: %s" % img)
        cnt += 1

    del soup
    del page

    sleep(1)
