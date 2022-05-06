def getFileContent(fileName):
    with open(f"md/{fileName}", "r") as file:
        content = file.read()
    return content

def getPostContent(fileContent):
    content = fileContent[fileContent.find("}") + 1:]
    content_list = []
    
    for i in content:
        content_list.append(i)

    for i in range(len(content_list)):
        if content_list[i] == "\n":
            content_list[i] = ""
        else:
            break
    
    content = "".join(content_list)
    content = markdown.markdown(content)

    return content

def getOption(content, _print=False):
    optionFind = re.compile("[{].*[}]", re.DOTALL)
    optionList = optionFind.findall(content)
    optionList = optionList[0][optionList[0].find("{")+1:optionList[0].find("}")-1]
    optionList = optionList.split("\n")[1:]

    option = {}
    for optionVar in optionList:
        optionVar = optionVar.split(":")
        if optionVar[1][0] == " ":
            optionVar[1] = optionVar[1][1:]
        option[optionVar[0]] = optionVar[1]
        if _print:
            print(optionVar)

    option["tags"] = option["tags"].replace(" ", "")
    option["tags"] = option["tags"].split(",")

    return option

def getPostList(_print=False):
    postList = os.listdir("md/")
    postDateList = []

    if _print:
        print("post list : " + ", ".join(postList))

    for post in postList:
        if _print:
            print("\n")
            print("file : " + post)
        fileContent = getFileContent(post)
        option = getOption(fileContent, _print=_print)


        postDateList.append(f"{option['date'].replace('-', '')}-{post}")

    postDateList.sort(reverse=True)
    postList = []
    for post in postDateList:
        postList.append(post.split("-")[1])
    if _print:
        print(f"\npost date list : {postDateList}\n")
    return postList

def removeFile(library, _print=False):
    removeList = os.listdir(library)
    for remove in removeList:
        os.remove(f"{library}/{remove}")
        if _print:
            print(f"{library}{remove} removed")

def getListTemplate(option, post, dd=False, _print=False):
    with open("template/list.html", "r") as file:
        listTemplate = file.read()
    
    listTemplate = listTemplate.replace("{title}", option["title"])
    listTemplate = listTemplate.replace("{subtitle}", option["subtitle"])
    listTemplate = listTemplate.replace("{date}", option["date"])

    postName = post.replace(".md", "")
    listTemplate = listTemplate.replace("{post_name}", postName)

    if dd:
        dd = "../"
    else:
        dd = ""

    tagList = getTagList(option, f"{dd}tag/")
    listTemplate = listTemplate.replace("{tags}", tagList)

    if dd:
        listTemplate = listTemplate.replace("{..}", "../")
    else:
        listTemplate = listTemplate.replace("{..}", "")

    if _print:
        print("get list template : " + post)

    return listTemplate

def getTagList(option, route):
    tagList = []
    for tag in option["tags"]:
        tagList.append(f"<a class='tag' href='{route}{tag}.html'>{tag}</a>")
    tagList = ", ".join(tagList)

    return tagList

def createIndex(listTemplate, settings, route="index.html", dd=False, _print=False):
    with open("template/_index.html", "r") as file:
        indexTemplate = file.read()
    
    if dd:
        dd = "../"
        tag = route.replace("tag/", "")
        tag = tag.replace(".html", "")
        indexTemplate = indexTemplate.replace("{dd}", f" - {tag}")
    else:
        dd = ""
        indexTemplate = indexTemplate.replace("{dd}", "")
        
    indexTemplate = indexTemplate.replace("{list}", listTemplate)
    indexTemplate = indexTemplate.replace("{..}", dd)
    indexTemplate = indexTemplate.replace("{username}", settings["username"])
    indexTemplate = indexTemplate.replace("{github}", settings["github"])

    with open(route, "w") as file:
        file.write(indexTemplate)

    if _print:
        print("\nwrite index : " + route + "\n")

def createPost(content, option, post, _print=False):
    with open("template/post.html", "r") as file:
        postTemplate = file.read()
    
    postTemplate = postTemplate.replace("{title}", option["title"])
    postTemplate = postTemplate.replace("{subtitle}", option["subtitle"])
    postTemplate = postTemplate.replace("{date}", option["date"])
    postTemplate = postTemplate.replace("{content}", content)

    tagList = getTagList(option, "../tag/")

    postTemplate = postTemplate.replace("{tags}", tagList)

    with open(f"post/{option['date']}-{post.replace('.md', '')}.html", "w") as file:
        file.write(postTemplate)

    if _print:
        print("write post : " + f"post/{option['date']}-{post.replace('.md', '')}.html\n")

def createTagFile(tagList, tagPostList, settings, _print=False):
    tagList = list(set(tagList))
    tagFileList = {}

    for tag in tagList:
        tagFile = []
        for tagPost in tagPostList:
            if tag in tagPostList[tagPost]:
                tagFile.append(tagPost)
        tagFileList[tag] = tagFile

    for tag in tagFileList:
        postList = tagFileList[tag]
        listTemplate = ""

        for post in postList:
            fileContent = getFileContent(post)
            option = getOption(fileContent, _print=_print)

            listTemplate += getListTemplate(option, post, dd=True)
        createIndex(listTemplate, settings, route=f"tag/{tag}.html", dd=True, _print=_print)

def getSettingJson(filename="settings.json"):
    with open(filename, "r") as file:
        settingJson = json.loads(file.read())

    return settingJson

def main(_print=False):
    startTime = time.time()
    if _print:
        print("start!\n")
    
    postList = getPostList(_print=_print)
    settings = getSettingJson()

    listTemplate = ""
    tagList = []
    tagPostList = {}

    removeFile("post/", _print=_print)
    if _print:
        print("\n")

    for post in postList:
        fileContent = getFileContent(post)
        content = getPostContent(fileContent)
        option = getOption(fileContent)

        if option["hidden"] == "true":
            continue

        listTemplate += getListTemplate(option, post, _print=_print)
        createPost(content, option, post, _print=_print)

        tagList += option["tags"]
        tagPostList[post] = option["tags"]

    if os.path.isfile("index.html"):
        os.remove("index.html")
        if _print:
            print("\nremoved index.html\n")

    removeFile("tag/", _print=_print)

    createIndex(listTemplate, settings, _print=_print)
    createTagFile(tagList, tagPostList, settings, _print=_print)

    if _print:
        print("done ;)")
        print("total elapsed time : " + str(time.time() - startTime) + "sec")

import os
import re
import time
import sys
import json
import markdown

if __name__ == "__main__":
    argList = sys.argv[1:]

    _print = True

    if "_print=False" in argList:
        _print = False

    main(_print=_print)