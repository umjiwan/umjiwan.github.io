import os
import re

post_list = os.listdir("md/")

# vsc 오류 제거용---
title = 0
subtitle = 0
date = 0
hidden = 0
tags = 0

# 기존 파일 제거
rm_list = os.listdir("post/")
for rm in rm_list:
    os.remove("post/" + rm)
os.remove("index.html")
f = open("index.html", "w"); f.close()

# html 파일 생성
tag_list = []
post_tag_list = []
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

    tags = tags.split(",")
    post_tag_list += [[post.replace(".md", ""), title, subtitle, date, tags]]

    for i in range(len(tags)):
        if tags[i][0] == " ":
            tags[i] = tags[i][1:]

    tag_list += tags
    
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

    with open("template/list.html", "r") as file:
        index_content = file.read()

    post_name = post.replace(".md", "")

    index_content = index_content.replace("{title}", title)
    index_content = index_content.replace("{subtitle}", subtitle)
    index_content = index_content.replace("{date}", date)
    index_content = index_content.replace("{content}", content)
    index_content = index_content.replace("{post_name}", post_name)
    index_content = index_content.replace("{tags}", ", ".join(tags))

    with open("index.html", "a") as file:
        file.write(index_content)

    with open("template/post.html", "r") as file:
        post_content = file.read()

    post_content = post_content.replace("{title}", title)
    post_content = post_content.replace("{subtitle}", subtitle)
    post_content = post_content.replace("{date}", date)
    post_content = post_content.replace("{content}", content)
    post_content = post_content.replace("{post_name}", post_name)
    post_content = post_content.replace("{tags}", ", ".join(tags))

    content = post_content

    with open(f"post/{date}-{post_name}.html", "w") as file:
        file.write(content)
 
# tag

# rm tag_file
tag_file_list = os.listdir("tag/")
for tag_file in tag_file_list:
    os.remove("tag/" + tag_file)

# write tag/index.html
with open("tag/index.html", "w") as file:
    for tag in list(set(tag_list)):
        file.write(f"<a href='{tag}.html'>{tag}</a><br>\n")

# write tag_file
print(post_tag_list[0])

for tag in list(set(tag_list)):
    for post_tag in post_tag_list:
        if tag in post_tag[-1]:
            with open(f"tag/{tag}.html", "a") as file:
                file.write(f"<a href='../post/{post_tag[3]}-{post_tag[0]}.html'>{post_tag[1]}</a><br>\n")






    
    

    
    
