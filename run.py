import pprint
import requests
import os
# from requests_html import HTMLSession


from modules import  parcers, models


# constants

path_image = '/home/servizio/domains/6perlen.de/public_html/wp-content/uploads/clubs/imgs/'
if not os.path.exists(path_image):
    os.makedirs(path_image)



#  images
def insertToBase(data, post_author,x_coord, y_coord, location, phone, nikname, city):
    # pprint.pprint (data)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    make_post = models.insert_wp_posts_stmt(data, post_author)
    models.insert_wp_term_relationships(make_post[0], city)

    print(make_post[0], 'post_id')
    post_id_images = ''
    for i in data['images']:
        responce = requests.get(i, headers=headers)
        if responce.status_code == 200:
            imageName = i.split('/')[-1]
            print(imageName, make_post[0])
            # imgName = models.translateD("".join(data["title"].lower().split()))
            f = open(f'{path_image}{make_post[1]}{imageName}', 'wb')
            f.write(responce.content)
            f.close()
            post_id_images = models.insert_wp_posts_image(
                make_post[1]+imageName, f'https://www.6perlen.de/wp-content/uploads/clubs/imgs/{make_post[1]}{imageName}', post_author, make_post[0])
            print(post_id_images, 'post_id_images')
            models.insert_wp_postmeta_images(post_id_images, make_post[1]+imageName)
            print(post_id_images)
            models.insert_wp_postmeta(make_post[0], post_id_images, x_coord, y_coord, location, phone, nikname)



#  https://www.rotelaterne.de/
def parcerRotelaterne(url, post_author, x_coord, y_coord, location, phone, gen_url, className, nikname, city):
    soup = parcers.getContent(url)
    id = 1
    data = {}
    for link in soup.select(className):
        link = f"{gen_url}{link.get('href')}"
        print(link, id)
        data = parcers.getDataRotelaterne(link)
        insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)
        id += 1

#   "https://www.pearls24-muenchen.de" id37

def parcerPearl24(url, post_author, x_coord, y_coord, location, phone, nikname, city):
    soup = parcers.getContent(url)
    id = 1
    # print (soup)
    for link in soup.select('article.grid-item.one-third.girl.sizeify'):
        if 'https://model' in link.select_one('a').get('href'):
            # print (link)
            data = {}
            images = f"{link.select_one('div.image').get('style').replace('background-image: url(','').replace(');','')}"
            data.update({'images': [images]})
            data.update({'description': ''})
            data.update({'title': link.select_one('div.inside').text.strip()})
        
            insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)
            # pprint.pprint (data)
            id +=1

            #  https://www.leierkasten.sexy/Girls id38 id39 id47 id51 
def parcerLeierkasten(url, post_author, x_coord, y_coord, location, phone, className, nikname, city ):
    soup = parcers.getContent(url)
    id = 1
    data = {}
    for link in soup.select(className):
        link = f"{link.get('href')}"
        
        data = parcers.parsingData(url=link, 
                name ='span.display-inline-block.text-gradient',
                descr = 'div.text-left.gap-bottom-big',
                serv = 'div#Service',
                imgs = 'div.flex-image img' )
        insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)
        id += 1


 #  http://www.lustmolche.com/lustratorinnen/ladys/ id43
def parcerLustmolche(url, post_author, x_coord, y_coord, location, phone, className, nikname, city ):
    soup = parcers.getContent(url)
    id = 1
    data = {}
    for link in soup.select(className):
        link = f"{link.get('href')}"
        print (link)
        data = parcers.parsingData(url=link, 
                name ='div.lustmolche-lustratorin-text-left h1',
                descr = 'div.lustmolche-lustratorin-text p',
                serv = 'div.lustmolche-lustratorin-text ul',
                imgs = 'div.lustmolche-lustratorin-bilder a')
        insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)
        id += 1
#  https://lady-discreet.de/damen/ id48

def parcerLadyDiscreet(url, post_author, x_coord, y_coord, location, phone, className, nikname, city ):
    soup = parcers.getContent(url)
    id = 1
    data = {}
    for link in soup.select(className):
        link = f"{link.get('href')}"
        print (link)
        data = parcers.parsingData(url=link, 
                name ='h1.h2.up.mb-0',
                descr = 'div.single_model-desc',
                serv = 'div#single-tab1',
                imgs = 'div.item a')
        insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)
   
        id += 1

# https://www.royal-eros.de/aktuelle-girls/ id52
def parcerRoyal(url, post_author, x_coord, y_coord, location, phone, nikname, city):
    soup = parcers.getContent(url)
    id = 1
    
    for link in soup.select('div.imgDiv'):
        data = {}
        images = f"{link.select_one('img').get('src')}"
        data.update({'images': [images]})
        data.update({'description': ''})
        data.update({'title': link.select_one('figcaption').text.split(',')[0]})
        
        insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)
        id +=1


    

# https://hauptstadtnummer.com/inserate-bordell-berlin.html id 44
def parcerHauptstadtnummer(url, post_author, x_coord, y_coord, location, phone,  nikname, city ):
    soup = parcers.getContent_text('https://hauptstadtnummer.com/inserate-bordell-berlin.html')
    for link in soup.select('ul#m1 a'):
        l = link.get('href')
        data = {}
        if len(l) >10 and 'gaestebuch' not in l and 'arbeiten' not in l :
            try:
                title = link.text
            except:
                title = ''
            soup = parcers.getContent_text(f'https://hauptstadtnummer.com/{l}')
            try:
                descr = soup.find('meta', property="og:description")['content']
            except:
                descr = ''
            try:
                img = soup.find('meta', property="og:image")['content']
            except:
                img = ''
            data.update({'title': title})
            data.update({'description': descr})
            data.update({'images': [img]})
            insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)

# https://fkk-club-6himmel.com/category/clubgirls id45
def parcerHimmel(post_author, x_coord, y_coord, location, phone, nikname, city):
    
   links=['https://fkk-club-6himmel.com/category/clubgirls', 'https://fkk-club-6himmel.com/category/clubgirls/page/2']
   for i in links:
        soup = parcers.getContent_text(i)
        
        for l in soup.select('a.bg-link'):
            data = {}
            images = []
            soup = parcers.getContent_text(l.get('href'))
            try:
                title = soup.select_one('h1.entry-title').text.split(' ')[0]
            except:
                title = ''
            try:
                descr = soup.select_one('ul.tags').text
            except:
                descr = ''
            try:
                for i in soup.select('li.blocks-gallery-item img'):
                    img = i.get('src')
                    if 'http' in img:
                        images.append(i.get('src'))
            except:
                images = []
            data.update({'title': title})
            data.update({'description': descr})
            data.update({'images': images})
            insertToBase(data,post_author,x_coord, y_coord, location, phone, nikname, city)


if __name__ == "__main__":
    CLUBS =["https://www.rotelaterne.de/", 
            'https://www.pearls24-muenchen.de', 
            'https://www.leierkasten.sexy/Girls', 
            'https://www.caesars-world.de/Girls',
            'http://www.lustmolche.com/lustratorinnen/ladys/',
            'https://www.cherry-ladies.de/Hoferstrasse',
            'https://www.cherry-ladies.de/Machtlfingerstrasse',
            'https://lady-discreet.de/damen/',
            'https://www.royal-eros.de/aktuelle-girls/',
            'https://fkk-club-6himmel.com/category/clubgirls', #id45
            'https://hauptstadtnummer.com/' #id44
            ]
    # pprint.pprint(models.getClubs())
    for i in models.getClubs():
        if len(i) > 3:
            print (i['id'], i['nikname'], i['url'], i['stadt'])
            if CLUBS[0] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerRotelaterne(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], CLUBS[0], 'div.nickname a', i['nikname'], i['stadt'])
            if CLUBS[1] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerPearl24(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], i['nikname'], i['stadt'])
            if CLUBS[2] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerLeierkasten(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], 'a.list-website-name', i['nikname'], i['stadt'])  
            if CLUBS[3] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerLeierkasten(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], 'a.list-website-name', i['nikname'], i['stadt']) 
            if CLUBS[4] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerLustmolche(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], 'div.lustmolche-lustratorinnen-query-result a', i['nikname'], i['stadt'])  
            if CLUBS[5] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerLeierkasten(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], 'a.list-website-name', i['nikname'], i['stadt'])        
            if CLUBS[6] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerLeierkasten(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], 'a.list-website-name', i['nikname'], i['stadt'])
            if CLUBS[7] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerLadyDiscreet(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], 'a.card-link', i['nikname'], i['stadt'])
            if CLUBS[8] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerRoyal(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"],  i['nikname'], i['stadt'])
            if CLUBS[9] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerHimmel( i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"], i['nikname'], i['stadt'])
            if CLUBS[10] in i['url']:
                print (i['id'], i['nikname'], i['url'])
                models.delete_posts(i['id'])
                parcerHauptstadtnummer(i['url'], i['id'], i["et_location_lat"], i["et_location_lng"], i["location"], i["phone"],  i['nikname'], i['stadt'])
              
