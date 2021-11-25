# -*- coding: utf-8 -*-
import datetime
import requests
from bs4 import BeautifulSoup
import json
import os

# Logic baca file config. Isinya URL blog per member sama tanggal blog terbaru
configFile = open("config.json", "r", encoding='utf-8')
config = json.load(configFile)
BASE_PATH = config["basePath"]
print("Save Path: {0}".format(BASE_PATH))
for member in config["members"]:
    # main image scraper logic
    try:
        is_success = True
        count = 0
        URL = member["blogUrl"]
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        blog_article = soup.find_all("div", class_="p-blog-article")
        latest_article_date_element = blog_article[0].find("div", class_="c-blog-article__date").text.strip()
        latest_update = datetime.datetime.strptime(member["lastUpdate"], '%Y-%m-%d %H:%M:%S') if member["lastUpdate"] != "" else None
        latest_article_date = datetime.datetime.strptime(latest_article_date_element, '%Y.%m.%d %H:%M') if latest_article_date_element != "" else None
        name = blog_article[0].find("div", class_="c-blog-article__name")
        save_path = os.path.join(BASE_PATH,name.text.strip())
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        if(latest_update is None or (latest_update is not None and latest_article_date is not None and latest_article_date > latest_update)):
            for article in blog_article:
                article_info = article.find("div", class_="p-blog-article__info")
                # date = article_info.find("div", class_="c-blog-article__date")
                article_body = article.find("div", class_="c-blog-article__text")
                images = article_body.find_all("img")
                for image in images:
                    if image['src'] != "" and "http" in image['src']:
                        basename = os.path.basename(image["src"])
                        full_path = os.path.join(save_path,basename)
                        if not os.path.exists(full_path):
                            try:
                                print("Downloading {0}".format(image["src"]))
                                with open(full_path,"wb") as f:
                                    f.write(requests.get(image['src']).content)
                                count += 1
                            except Exception as e:
                                is_success = False
                                print("Problem downloading {0}".format(image["src"]))
                                print(str(e))
        if is_success and count > 0:
            print("Downloaded {0} images from {1}'s Blog.".format(str(count),member["memberName"]))
        elif is_success and count == 0:
            print("All images from {0}'s blog have been downloaded.".format(member["memberName"]))
        if is_success:
            member["lastUpdate"] = str(latest_article_date)
    except:
        print("Problem getting data of {0}".format(member["memberName"]))
configFile.close()

# write back config to file
json_object = json.dumps(config)
with open("config.json","w", encoding='utf-8') as out:
    out.write(json_object)
