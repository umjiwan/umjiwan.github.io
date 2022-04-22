# ulog
작성날짜 2022-04-22<br>

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
커스텀은 `template/` 폴더안에 있는 폴더들에서 가능합니다.<br>

파일리스트 (괄호한 파일은 추가 예정 파일)<br>
```
_index.html # blog 홈화면 ~/blog/ 에 표시되는 html
index.css # blog 홈화면에 적용되는 css
list.html # blog 홈화면에 글 리스트를 나타내는 html
post.html # blog 글(특정X) 에 들어갔을때 보여지는 html
post.css # blog 글에 적용되는 css
(tag.html) # blog 태그 ~/blog/tag/(tag).html 에 보여질 html
(tag_list.html) # blog 태그에 태그리스트를 나타내는 html
(tag.css) # blog 태그에 적용되는 css
```
template html 파일들은 변수가 들어갈 위치를 커스텀 할 수 있습니다.<br>

사용가능한 변수<br>
```
{title} : 해당 글의 제목을 표시해줍니다.
{subtitle} : 해당 글의 부제목/설명 을 표시해줍니다.
{date} : 해당 글의 표기날짜 를 표시해줍니다.
{tags} : 해당 글의 태그들을 표시해줍니다.
{content} : 해당 글의 내용을 표시해줍니다.
{post_name} : 해당 글의 .md를 제외한 마크다운 파일 명을 표시해줍니다.
```

## deploy.py 의 작동방식과 원리

deploy.py 내용 (기준 : 2022-04-22 18:02)
```python3
import os
import re

post_list = os.listdir("md/")

# vsc 오류 제거용---
title = 0
subtitle = 0
date = 0
hidden = 0
tags = 0
index = ""

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

    af_tags = []
    af_tags_p = []
    for i in tags:
        af_tags.append(f"<a href='tag/{i}.html' class='tag'>{i}</a>")
        af_tags_p.append(f"<a href='../tag/{i}.html' class='tag'>{i}</a>")

    index_content = index_content.replace("{title}", title)
    index_content = index_content.replace("{subtitle}", subtitle)
    index_content = index_content.replace("{date}", date)
    index_content = index_content.replace("{content}", content)
    index_content = index_content.replace("{post_name}", post_name)
    index_content = index_content.replace("{tags}", " ".join(af_tags))

    index += index_content

    with open("template/post.html", "r") as file:
        post_content = file.read()

    post_content = post_content.replace("{title}", title)
    post_content = post_content.replace("{subtitle}", subtitle)
    post_content = post_content.replace("{date}", date)
    post_content = post_content.replace("{content}", content)
    post_content = post_content.replace("{post_name}", post_name)
    post_content = post_content.replace("{tags}", ", ".join(af_tags_p))

    content = post_content

    with open(f"post/{date}-{post_name}.html", "w") as file:
        file.write(content)

# index.html
with open("template/_index.html", "r") as file:
    _index_content = file.read()

_index_content = _index_content.replace("{list}", index)

with open("index.html", "w") as file:
    file.write(_index_content)
```

deploy.py 의 작동순서<br>
1. `md/`폴더의 파일들을 파일명 리스트로 변수에 저장 합니다.
```python3
post_list = os.listdir("md/")
```

2. 저장한 리스트를 반복하여 글마다 작업을 합니다.<br>

3. 먼저 파일 내용에서 옵션을 뽑아옵니다<br>
옵션은 {} 로 둘러쌓여있기 때문에 `re` 모듈 즉 정규 표현식으로 옵션을 추출합니다.

```python3
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
```
`globals()[]`는 특정 변수의 값이 변수이름으로 정의 할 수 있는 용도로 사용하였습니다.<br>
예)
```python3
a = "hello"
globals()[a] = 1
print(hello)
```
`hello`를 정의한적이 없지만 알아서 1이라는 값이 출력 됩니다.<br>

`post_name` 옵션도 추출해줍니다.
```python3
post_name = post.replace(".md", "")
```

4. 추출한 옵션을 템플릿 파일의 적용하여 html 파일을 생성합니다.<br>
먼저 `list` 템플릿 파일을 불러옵니다. (글 리스트)<br>
불러온 `list` 템플릿에서 가공전 옵션 `{옵션명}` 을 `{옵션값}` 으로 변환합니다.

```python3
with open("template/list.html", "r") as file:
        index_content = file.read()

index_content = index_content.replace("{title}", title)
index_content = index_content.replace("{subtitle}", subtitle)
index_content = index_content.replace("{date}", date)
index_content = index_content.replace("{content}", content)
index_content = index_content.replace("{post_name}", post_name)
index_content = index_content.replace("{tags}", " ".join(af_tags))
```
변경된 `index_content` 를 저장합니다
```python3
index += index_content
```

그 다음 post (글 내용 템플릿)을 불러와 옵션을 적용합니다.<br>
```python3
with open("template/post.html", "r") as file:
        post_content = file.read()

post_content = post_content.replace("{title}", title)
post_content = post_content.replace("{subtitle}", subtitle)
post_content = post_content.replace("{date}", date)
post_content = post_content.replace("{content}", content)
post_content = post_content.replace("{post_name}", post_name)
post_content = post_content.replace("{tags}", ", ".join(af_tags_p))
```

그리고 가공된 post_content를 html 파일로 찍어냅니다.<br>
```python3
content = post_content

with open(f"post/{date}-{post_name}.html", "w") as file:
    file.write(content)
```

5. 저장했던 index_content를 index.html 템플릿 파일에 적용후 html 파일을 생성합니다.<br>
```python3
# index.html
with open("template/_index.html", "r") as file:
    _index_content = file.read()

_index_content = _index_content.replace("{list}", index)

with open("index.html", "w") as file:
    file.write(_index_content)
```
6. 추출한 태그를 태그 파일로 만들어줍니다 (추후 추가 예정)

## 추가할 예정인 기능
1. 파일리스트를 표기날짜 순으로 내림차순/오름차순 정렬
2. 태그 기능
3. 댓글 기능
4. 도메인을 ulhangry.com 으로 변경

감사합니다.
