# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import os
import argparse
import pathlib
import filedate
from pathvalidate import validate_filename, ValidationError

confstring = '''
 {"members": [
        {
            "memberName": "Ushio Sarina",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=2"
        },
        {
            "memberName": "Kageyama Yuka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=4"
        },
        {
            "memberName": "Kato Shiho",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=5"
        },
        {
            "memberName": "Saito Kyoko",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=6"
        },
        {
            "memberName": "Sasaki Kumi",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=7"
        },
        {
            "memberName": "Sasaki Mirei",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=8"
        },
        {
            "memberName": "Takase Mana",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=9"
        },
        {
            "memberName": "Takamoto Ayaka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=10"
        },
        {
            "memberName": "Higashimura Mei",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=11"
        },
        {
            "memberName": "Kanemura Miku",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12"
        },
        {
            "memberName": "Kawata Hina",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=13"
        },
        {
            "memberName": "Kosaka Nao",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=14"
        },
        {
            "memberName": "Tomita Suzuka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=15"
        },
        {
            "memberName": "Nibu Akari",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=16"
        },
        {
            "memberName": "Hamaigishi Hiyori",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=17"
        },
        {
            "memberName": "Matsuda Konoka",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=18"
        },
        {
            "memberName": "Miyata Manamo",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=19"
        },
        {
            "memberName": "Watanabe Miho",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=20"
        },
        {
            "memberName": "Kamimura Hinano",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=21"
        },
        {
            "memberName": "Takahashi Mikuni",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=22"
        },
        {
            "memberName": "Morimoto Marii",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=23"
        },
        {
            "memberName": "Yamaguchi Haruyo",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=24"
        },
        {
            "memberName": "POKA",
            "blogUrl": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=000"
        }
    ]}
'''

#region parse argument
parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--page", help="Define from which page to download.", type=int, default=1)
parser.add_argument(
    "-d", "--dir", help="Define where to save the images.", default=str(pathlib.Path(__file__).parent.resolve()))
parser.add_argument(
    "-a", "--allPages", help="Save image from all pages of each member's blog.", action='store_true')
args = parser.parse_args()
#endregion

def scrap_image(member, base_path, pages):
    is_success = True

    # main image scraper logic
    try:
        print("Downloading images from {0}'s blog.".format(
            member["memberName"]))        
        count = 0
        URL = member["blogUrl"]

        if pages > 1:            
            base_url = URL.split("?")[0]
            params = URL.split("?")[1].split("&")
            params.insert(1, "page={0}".format(str(pages)))
            params.append("cd=member")
            paramString = "&".join(params)
            URL = "?".join([base_url, paramString])

        print(URL)
        webpage = requests.get(URL)
        soup = BeautifulSoup(webpage.content, "html.parser")

        if soup.find("div", class_="l-contents--blog-list") is None:
            is_success = False

        if is_success:
            blog_article = soup.find_all("div", class_="p-blog-article")
            # latest_article_date_element = blog_article[0].find(
            #     "div", class_="c-blog-article__date").text.strip()
            name = blog_article[0].find("div", class_="c-blog-article__name")
            save_path = os.path.join(base_path, name.text.strip())

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            for article in blog_article:
                article_info = article.find(
                    "div", class_="p-blog-article__info")
                article_date = article_info.find("div", class_="c-blog-article__date")
                datetime_string = article_date.text.strip("\n").strip()
                article_body = article.find(
                    "div", class_="c-blog-article__text")
                images = article_body.find_all("img")
                count_image = 0
                for image in images:
                    src = image.get('src')
                    if src is not None and src != "" and "http" in src:
                        basename = os.path.basename(image["src"])

                        try:
                            validate_filename(basename)
                        except ValidationError as e:
                            file_ext = os.path.splitext(image['src'])[1]
                            basename = member["memberName"] + datetime_string.replace(" ","-").replace(":","-") + "_" + str(count_image) + file_ext
                            count_image += 1

                        full_path = os.path.join(save_path, basename)
                        
                        if not os.path.exists(full_path):
                            try:
                                print("Downloading {0}".format(image["src"]))
                                with open(full_path, "wb") as f:
                                    f.write(requests.get(image['src']).content)
                                file = filedate.File(full_path)
                                file.set(
                                    created = datetime_string+":00",
                                    modified = datetime_string+":00"
                                )
                                count += 1
                                is_success = True
                            except Exception as e:
                                # is_success = False
                                print("Problem downloading {0}".format(
                                    image["src"]))
                                print(str(e))

            if count > 0:
                print("Downloaded {0} images from {1}'s Blog.\n".format(
                    str(count), member["memberName"]))
            # elif is_success and count == 0:
            #     print("All images from {0}'s blog have been downloaded.\n".format(
            #         member["memberName"]))
            
            if count > 0:
                is_success = True
    except Exception as e:
        is_success = False
        print("Problem getting data of {0} \n".format(member["memberName"]))
        print(e)
    return is_success

config = json.loads(confstring)
BASE_PATH = args.dir

print("Save Path: {0}".format(BASE_PATH))
for member in config["members"]:
    page = args.page
    if args.allPages:
        while(scrap_image(member, BASE_PATH, page)):
            page += 1
    else:
        scrap_image(member, BASE_PATH, page)

    print("All images from {0}'s blog have been downloaded.\n".format(member["memberName"]))
