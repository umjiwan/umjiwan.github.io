import os
import re

post_list = os.listdir("md/")

# vsc 오류 제거용---
title = 0
subtitle = 0
date = 0
hidden = 0

# 기존 파일 제거
rm_list = os.listdir("post/")
for rm in rm_list:
    os.remove("post/" + rm)
os.remove("index.html")
f = open("index.html", "w"); f.close()

# html 파일 생성
for post in post_list:
    with open("md/" + post, "r") as file:
        post_content = file.read()
    
    option_find = re.compile("[{].*[}]", re.DOTALL)
    option_list = option_find.findall(post_content)
    option_list = option_list[0][option_list[0].find("{")+1:option_list[0].find("}")-1]
    option_list = option_list.split("\n")[1:]
    
    for option in option_list: # option 추출
        option = option.split(":")
        if option[1][0] == " ":
            option[1] = option[1][1:]
        globals()[option[0]] = option[1]

    if hidden == "true":
        continue
    
    content = post_content[post_content.find("}") + 1:]
    content_list = []
    
    for i in content:
        content_list.append(i)

    for i in range(len(content_list)):
        if content_list[i] == "\n":
            content_list[i] = ""
        else:
            break
    
    content = "".join(content_list)
    title = title.replace(" ", "_")

    with open("template/list.html", "r") as file:
        index_content = file.read()

    post_name = post.replace(".md", "")

    index_content = index_content.replace("{title}", title)
    index_content = index_content.replace("{subtitle}", subtitle)
    index_content = index_content.replace("{date}", date)
    index_content = index_content.replace("{content}", content)
    index_content = index_content.replace("{post_name}", post_name)

    
    """# {date} 문자열을 date의 값으로 바꾸기
    index_date = index_content.find("{date}")
    while index_date != -1:
        index_content_list = []
        for i in index_content:
            index_content_list.append(i)
        index_content_list[index_date:index_date+len("{date}")] = ""
        for i in date:
            index_content_list.insert(index_date, i)
            index_date += 1
        index_content = "".join(index_content_list)
        index_date = index_content.find("{date}")

    # {title} 문자열을 title의 값으로 바꾸기
    index_title = index_content.find("{title}")
    while index_title != -1:
        index_content_list = []
        for i in index_content:
            index_content_list.append(i)
        index_content_list[index_title:index_title+len("{title}")] = ""
        for i in title:
            index_content_list.insert(index_title, i)
            index_title += 1
        index_content = "".join(index_content_list)
        index_title = index_content.find("{title}")

    # {subtitle} 문자열을 title의 값으로 바꾸기
    index_subtitle = index_content.find("{subtitle}")
    while index_subtitle != -1:
        index_content_list = []
        for i in index_content:
            index_content_list.append(i)
        index_content_list[index_subtitle:index_subtitle+len("{subtitle}")] = ""
        for i in subtitle:
            index_content_list.insert(index_subtitle, i)
            index_subtitle += 1
        index_content = "".join(index_content_list)
        index_subtitle = index_content.find("{subtitle}")
        
    
    하... replace 있는거 까먹고 이렇게 짰다..
    """

    with open("index.html", "a") as file:
        file.write(index_content)

    with open("template/post.html", "r") as file:
        post_content = file.read()

    post_content = post_content.replace("{title}", title)
    post_content = post_content.replace("{subtitle}", subtitle)
    post_content = post_content.replace("{date}", date)
    post_content = post_content.replace("{content}", content)
    post_content = post_content.replace("{post_name}", post_name)

    content = post_content

    
    with open(f"post/{date}-{post_name}.html", "w") as file:
        file.write(content) 
    

    
    

    
    
