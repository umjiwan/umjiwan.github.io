import os
import re

post_list = os.listdir("post/")

# vsc 오류 제거용---
title = 0
subtitle = 0
date = 0
hidden = 0
# ---------------

for post in post_list:
    with open("post/" + post, "r") as file:
        post_content = file.read()
    
    option_find = re.compile("[{].*[}]", re.DOTALL)
    option_list = option_find.findall(post_content)
    option_list = option_list[0][option_list[0].find("{")+1:option_list[0].find("}")-1]
    option_list = option_list.split("\n")[1:]
    
    for option in option_list:
        option = option.split(":")
        if option[1][0] == " ":
            option[1] = option[1][1:]
        globals()[option[0]] = option[1]

    print(title)
    print(subtitle)
    print(date)
    print(hidden)
    
