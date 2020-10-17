import requests, os
from bs4 import BeautifulSoup



def getContent(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    return BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')

def getContent_text(url):
    return BeautifulSoup(requests.get(url).text, 'lxml')
    
# www.rotelaterne.de
def getDataRotelaterne(url='https://www.rotelaterne.de/bianca_caesars_'):
    soup = getContent(url)
    images = []
    try:
        title = soup.select_one('div#sedcard-main h1').text
    except:
        title = ''
    try:
        description = soup.select_one(
            'div#sedcard-main div.maincontent').text.replace('\'', '')
    except:
        description = ''
    try:
        service = soup.select_one('div.tablet-info-service').text
    except:
        service = ''

    for img in soup.select('ul.ad-thumb-list a'):
        images.append(f"https:{img.get('href')}")

    return {'title': title,
            'description': description+'\n'+service,
            'images': images,
            }

# https://www.leierkasten.sexy/Girls  id38 id 37 id39 43

def parsingData(**kwargs ):
    soup = getContent(kwargs['url'])
    images = []

    try:
        name = soup.select_one(kwargs['name']).text.strip().replace('\n','')
    except:
        name = ''
    try:
        description = soup.select_one(kwargs['descr']).text
    except:
        description = ''
    try:
        service = soup.select_one(kwargs['serv']).text.strip()
    except:
        service = ''
    try:
        tag = ''
        if kwargs['imgs'].split(' ')[1] == 'a':
            tag = 'href'
        else:
            tag = 'src'
        for i in soup.select(kwargs['imgs']):
            filename = i.get(tag)
            ext = os.path.splitext(filename)[1]
            if (ext == '.jpg' or ext == '.JPG'):
                images.append(filename)
    except :
        images = []
    
    return {'title': name,
            'description': description+'\n'+service,
            'images': images,
            # 'adress': adress,
            # 'telephone': telephone,
            }

# https://lady-discreet.de/damen/ id 48

def parsingPerls24(url='https://www.lustmolche.com/lustratorinnen/paula/', 
                name ='div.lustmolche-lustratorin-text-left h1',
                descr = 'div.lustmolche-lustratorin-text p',
                serv = 'div.lustmolche-lustratorin-text ul',
                imgs = 'div.lustmolche-lustratorin-bilder img', **kwargs ):
    soup = getContent(url)
    images = []

    try:
        name = soup.select_one(name).text.strip()
    except:
        name = ''
    try:
        description = soup.select_one(descr).text
    except:
        description = ''
    try:
        service = soup.select_one(serv).text.strip()
    except:
        service = ''
    try:
        tag = ''
        if imgs[:-1] == 'a':
            tag = 'href'
        else:
            tag = 'src'


        for i in soup.select(imgs):
            images.append(i.get('src'))
    except :
        images = []
    
    return {'title': name,
            'description': description+'\n'+service,
            'images': images,
            # 'adress': adress,
            # 'telephone': telephone,
            }
# https://hauptstadtnummer.com/inserate-bordell-berlin.html id 44

def parsingHauptstadtnummer(url='https://hauptstadtnummer.com/alexis-bordell-berlin.html', 
                name ='div.v76.ps293.s542.c259 h1',
                descr = 'div.anim.fadeIn.js355.v76.ps300.s549.c267',
                serv = 'div.anim.zoomIn.js352.v76.ps299.s548.c261',
                imgs = 'a.a7'):
    soup = getContent(url)
    images = []

    try:
        name = soup.select_one(name).text.split('-')[0].strip()
    except:
        name = ''
    try:
        description = soup.select_one(descr).text
    except:
        description = ''
    try:
        service = soup.select_one(serv).text.strip()
        # print(service, 'ss')
    except:
        service = ''
    try:
        for i in soup.select(imgs):
            images.append(f'{"https://hauptstadtnummer.com/"}{i.get("href")}')
    except :
        images = []
    
    return {'title': name,
            'description': description+'\n'+service,
            'images': images,
            # 'adress': adress,
            # 'telephone': telephone,
            }

# id 45 https://fkk-club-6himmel.com/category/clubgirls

def parsingHimmel(url= 'https://fkk-club-6himmel.com/anastasia-aus-russland'):
    soup = getContent(url)
    images = []
    title = soup.select_one('h1.entry-title')

    # try:
    #     title = soup.select_one('h1.entry-title').text
    # except:
    #     title = ''
    try:
        description = soup.select_one('ul.tags').text.strip()
    except:
        description = ''
    try:
        for i in soup.select('div.czr-wp-the-content img'):
            images.append(i.get('src'))
        images = soup.select_one('div.czr-wp-the-content img').get('src')
    except:
        images = []
    
    return{
        'title': title,
        'description': description,
        'images': images,
    }