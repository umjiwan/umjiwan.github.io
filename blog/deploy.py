import os
import re

post_list = os.listdir("md/")

# vsc 오류 제거용---
title = 0
subtitle = 0
date = 0
hidden = 0
# ---------------

# 기존 파일 제거
rm_list = os.listdir("post/")
for rm in rm_list:
    os.remove("post/" + rm)
os.remove("index.html")

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

    if bool(hidden):
        pass
    
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

    with open("index.html", "a") as file:
        file.write(f'<a href="post/{date}-{title}.html">{title}</a><br>\n')

    with open(f"post/{date}-{title}.html", "w") as file:
        file.write(f"{title}<br>{date}")
        file.write(f"<p>{content}</p>")

    

    
    

    
    
