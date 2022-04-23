import os
import re

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

    return content

def getOption(content):
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

    option["tags"] = option["tags"].replace(" ", "")
    option["tags"] = option["tags"].split(",")

    return option

def getPostList():
    postList = os.listdir("md/")
    postDateList = []

    for post in postList:
        fileContent = getFileContent(post)
        option = getOption(fileContent)

        postDateList.append(f"{option['date'].replace('-', '')}-{post}")

    postDateList.sort(reverse=True)
    postList = []
    for post in postDateList:
        postList.append(post.split("-")[1])

    return postList

def removeFile(library):
    removeList = os.listdir(library)
    for remove in removeList:
        os.remove(f"{library}/{remove}")

def getListTemplate(option, post, dd=False):
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

    return listTemplate

def getTagList(option, route):
    tagList = []
    for tag in option["tags"]:
        tagList.append(f"<a class='tag' href='{route}{tag}.html'>{tag}</a>")
    tagList = ", ".join(tagList)

    return tagList

def createIndex(listTemplate, route="index.html", dd=False):
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

    with open(route, "w") as file:
        file.write(indexTemplate)

def createPost(content, option, post):
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

def createTagFile(tagList, tagPostList):
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
            option = getOption(fileContent)

            listTemplate += getListTemplate(option, post, dd=True)
        createIndex(listTemplate, route=f"tag/{tag}.html", dd=True)
def main():
    postList = getPostList()
    listTemplate = ""
    tagList = []
    tagPostList = {}

    removeFile("post/")

    for post in postList:
        fileContent = getFileContent(post)
        content = getPostContent(fileContent)
        option = getOption(fileContent)

        if option["hidden"] == "true":
            continue

        listTemplate += getListTemplate(option, post)
        createPost(content, option, post)

        tagList += option["tags"]
        tagPostList[post] = option["tags"]

    if os.path.isfile("index.html"):
        os.remove("index.html")

    removeFile("tag/")

    createIndex(listTemplate)
    createTagFile(tagList, tagPostList)
        
if __name__ == "__main__":
    main()