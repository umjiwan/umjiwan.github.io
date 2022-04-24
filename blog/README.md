# ulog
작성날짜 2022-04-24<br>

<img src="https://cdn.discordapp.com/attachments/925359064211402775/967612316067709028/2022-04-24_11.25.14.png">

블로그 입니다.<br>

`md/` 폴더에 마크다운 확장자의 파일을 넣고 <br>
`deploy.py`프로그램을 실행시키면 자동으로 html 파일을 만들어줍니다.<br>

## 사용방법 
1. `md/` 폴더에 양식에 맞는 마크다운 확장자의 파일을 넣어줍니다.<br>

마크다운 파일의 조건은<br>
`확장자가 .md 아닌것`<br>
`중복된 이름의 파일명`<br>
`양식의 맞지 않는 파일내용`<br>
은 불가능 합니다.<br>

양식
```
{
title: 제목
subtitle: 부제목/설명
date: 2022-04-22
hidden: false
tags: tag1, tag2, tag3
}

글 내용(html 가능)
```

옵션 설명<br>
`title`: 제목<br>
`subtitle`: 부제목/설명<br>
`date`: 표기날짜(0000-00-00)<br>
`hidden`: 이 파일을 html로 변환할지 안할지(숨길지 안숨길지)<br>
`tags`: 원하는 태그 ,(쉼표) 로 구분 태그는 자동생성<br>

2. `deploy.py` 파일을 실행 (테스트 파이썬 버전: 3.8)<br>
(추후 자동 업로드 기능 추가 예정)

## 커스텀 방법
커스텀은 `template/` 폴더안에 있는 파일<br>
`static/` 폴더안에 있는 파일들에서 가능합니다.<br>

파일리스트 (괄호한 파일은 추가 예정 파일)<br>

template/<br>
`\_index.html`: blog 홈화면 ~/blog/ 에 표시되는 html<br>
`list.html`: blog 홈화면에 글 리스트를 나타내는 html<br>
`post.html`: blog 글(특정X) 에 들어갔을때 보여지는 html<br>

static/<br>
`style.css`: 모든 template의 적용되는 css<br>
`script.js`: 모든 template의 적용되는 javascript<br>

template html 파일들은 변수가 들어갈 위치를 커스텀 할 수 있습니다.<br>

사용가능한 변수<br>

`{title}` : 해당 글의 제목을 표시해줍니다.<br>
`{subtitle}` : 해당 글의 부제목/설명 을 표시해줍니다.<br>
`{date}` : 해당 글의 표기날짜 를 표시해줍니다.<br>
`{tags}` : 해당 글의 태그들을 표시해줍니다.<br>
`{content}` : 해당 글의 내용을 표시해줍니다.<br>
`{post_name}` : 해당 글의 .md를 제외한 마크다운 파일 명을 표시해줍니다.<br>
`{..}` : 해당 글의 필요한 경우 ../ 를 추가 해 줍니다. (경로상의 문제)<br>
`{dd}` : 현재 해당하는 태그페이지에 대한 태그를 보여줍니다 (True일때)<br>

## deploy.py 의 작동방식과 원리

deploy.py 의 작동순서 및 함수별 설명<br>

1. getFileContent
```python3
def getFileContent(fileName):
    with open(f"md/{fileName}", "r") as file:
        content = file.read()
    return content
```
파일명을 입력받으면 md/ 폴더에 있는 해당 파일의 내용을 불러온다.<br>

2. getPostContent
```python3
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
```
`getFileContent` 에서 얻은 파일의 내용을 input으로 받는다.<br>
받은 파일 내용에서 옵션을 제외한 진짜 파일의 내용을 추출하여 return한다.<br>

3. getOption
```python3
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
```
`getFileContent` 에서 추출한 content를 input으로 받는다.<br>
그리고 content에서 `option` 을 추출하여 return 한다.<br>

4. getPostList
```python3
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
```
input을 받지 않습니다.<br>
`md/` 폴더에 있는 markdown 파일들의 리스트를 날짜순으로 내림차순 정렬합니다.<br>
정렬한 리스트를 return 합니다.<br>

5. removeFile
```python3
def removeFile(library):
    removeList = os.listdir(library)
    for remove in removeList:
        os.remove(f"{library}/{remove}")
```
경로 라이브러리를 input 값으로 받습니다.<br>
해당 경로의 있는 모든 파일을 삭제합니다.<br>


6. getListTemplate
```python3
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
```
option, post, dd 를 input 값으로 받습니다.<br>
작성된 `template/` 폴더의 `list.html` 의 파일 내용을 불러와<br>
작성된 변수 값들을 변환하여 return 합니다.<br>

7. getTagList
```python3
def getTagList(option, route):
    tagList = []
    for tag in option["tags"]:
        tagList.append(f"<a class='tag' href='{route}{tag}.html'>{tag}</a>")
    tagList = ", ".join(tagList)

    return tagList
```
option, route 를 input으로 받는다.<br>
option에서 tag를 추출하여 리스트를 만든다.<br>
그 리스트를 return한다.

8. createIndex
```python3
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
```
listTemplate, route, dd 를 input값으로 받는다.<br>
`index.html`, `tag/{tag}.html` 파일을 생성해준다.<br> 

9. createPost
```python3
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
```
content, option, post 를 input값으로 받는다.<br>
글 파일 `0000-00-00-filename.html` 파일을 생성해준다.<br>

10. createTagFile
```python3
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
```
tagList, tagPostList 를 input으로 받는다.<br>
tag file 즉 `tag/{tag}.html` 파일을 생성한다.<br>

+ main 함수
```python3
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
```
메인함수이다.<br>
말 그대로다.<br>

## 전체코드
(기준 : 2022-04-24 14:30)
```python3
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
```

## \_print 옵션이 true 일때 나타나는 화면 예시
```yml
(base) ulhangry:blog/ (black) $ python3 deploy.py                                                                                                                      [16:00:07]
start!

post list : epepepepe.md, hmm.md, 0416sat.md, thank_lesh.md, test.md


file : epepepepe.md
['date', '2022-04-17']
['title', '파이썬 Hello World! 출력']
['subtitle', '가장 기본적인 출력이라는 걸 배워보자']
['hidden', 'false']
['tags', '파이썬, 테스트, 공부']


file : hmm.md
['date', '2022-04-14']
['title', '안녕하세요!']
['subtitle', '저를 소개할게요']
['hidden', 'false']
['tags', '인사, 테스트']


file : 0416sat.md
['date', '2022-04-16']
['title', '4월 16일 어느날']
['subtitle', '그날 나에게 엄청난 일이 일어났다.']
['hidden', 'false']
['tags', '일상, 테스트']


file : thank_lesh.md
['title', '레쉬님 감사합니다.']
['subtitle', '정말정말정말정말정말정말정말정말정말']
['hidden', 'false']
['tags', '정말, 감사, 테스트']
['date', '2022-04-21']


file : test.md
['date', '2022-04-07']
['title', '이 세상에서 가장 무서운 것']
['subtitle', '난 그것을 찾아 떠나기로 하였다.']
['hidden', 'false']
['tags', '소설, 공부, 테스트']

post date list : ['20220421-thank_lesh.md', '20220417-epepepepe.md', '20220416-0416sat.md', '20220414-hmm.md', '20220407-test.md']

post/2022-04-17-epepepepe.html removed
post/2022-04-21-thank_lesh.html removed
post/2022-04-07-test.html removed
post/2022-04-16-0416sat.html removed
post/2022-04-14-hmm.html removed


get list template : thank_lesh.md
write post : post/2022-04-21-thank_lesh.html

get list template : epepepepe.md
write post : post/2022-04-17-epepepepe.html

get list template : 0416sat.md
write post : post/2022-04-16-0416sat.html

get list template : hmm.md
write post : post/2022-04-14-hmm.html

get list template : test.md
write post : post/2022-04-07-test.html


removed index.html

tag/파이썬.html removed
tag/일상.html removed
tag/공부.html removed
tag/감사.html removed
tag/소설.html removed
tag/테스트.html removed
tag/인사.html removed
tag/정말.html removed

write index : index.html

['date', '2022-04-14']
['title', '안녕하세요!']
['subtitle', '저를 소개할게요']
['hidden', 'false']
['tags', '인사, 테스트']

write index : tag/인사.html

['date', '2022-04-17']
['title', '파이썬 Hello World! 출력']
['subtitle', '가장 기본적인 출력이라는 걸 배워보자']
['hidden', 'false']
['tags', '파이썬, 테스트, 공부']
['date', '2022-04-07']
['title', '이 세상에서 가장 무서운 것']
['subtitle', '난 그것을 찾아 떠나기로 하였다.']
['hidden', 'false']
['tags', '소설, 공부, 테스트']

write index : tag/공부.html

['date', '2022-04-17']
['title', '파이썬 Hello World! 출력']
['subtitle', '가장 기본적인 출력이라는 걸 배워보자']
['hidden', 'false']
['tags', '파이썬, 테스트, 공부']

write index : tag/파이썬.html

['title', '레쉬님 감사합니다.']
['subtitle', '정말정말정말정말정말정말정말정말정말']
['hidden', 'false']
['tags', '정말, 감사, 테스트']
['date', '2022-04-21']

write index : tag/정말.html

['date', '2022-04-07']
['title', '이 세상에서 가장 무서운 것']
['subtitle', '난 그것을 찾아 떠나기로 하였다.']
['hidden', 'false']
['tags', '소설, 공부, 테스트']

write index : tag/소설.html

['title', '레쉬님 감사합니다.']
['subtitle', '정말정말정말정말정말정말정말정말정말']
['hidden', 'false']
['tags', '정말, 감사, 테스트']
['date', '2022-04-21']

write index : tag/감사.html

['title', '레쉬님 감사합니다.']
['subtitle', '정말정말정말정말정말정말정말정말정말']
['hidden', 'false']
['tags', '정말, 감사, 테스트']
['date', '2022-04-21']
['date', '2022-04-17']
['title', '파이썬 Hello World! 출력']
['subtitle', '가장 기본적인 출력이라는 걸 배워보자']
['hidden', 'false']
['tags', '파이썬, 테스트, 공부']
['date', '2022-04-16']
['title', '4월 16일 어느날']
['subtitle', '그날 나에게 엄청난 일이 일어났다.']
['hidden', 'false']
['tags', '일상, 테스트']
['date', '2022-04-14']
['title', '안녕하세요!']
['subtitle', '저를 소개할게요']
['hidden', 'false']
['tags', '인사, 테스트']
['date', '2022-04-07']
['title', '이 세상에서 가장 무서운 것']
['subtitle', '난 그것을 찾아 떠나기로 하였다.']
['hidden', 'false']
['tags', '소설, 공부, 테스트']

write index : tag/테스트.html

['date', '2022-04-16']
['title', '4월 16일 어느날']
['subtitle', '그날 나에게 엄청난 일이 일어났다.']
['hidden', 'false']
['tags', '일상, 테스트']

write index : tag/일상.html

done ;)
total elapsed time : 0.01149296760559082sec
```

감사합니다.<br>

## 추가할 예정인 기능
1. 도메인을 ulhangry.com 으로 변경
2. 커스텀 기능 더욱더 활성화
3. yml 파일로 커스텀 활성화
4. 댓글기능 단독생성
