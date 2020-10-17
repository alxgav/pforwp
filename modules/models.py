from modules import db_connect
from datetime import datetime

mydb = db_connect.db_connect()


mycursor = mydb.cursor()

wp_post_insert = '''INSERT INTO wp_posts (post_author,
                                    post_date, 
                                    post_date_gmt,
                                    post_content,
                                    post_title, 
                                    post_status,
                                    comment_status, 
                                    ping_status,
                                    post_name, 
                                    post_modified, 
                                    post_modified_gmt, 
                                    post_parent,
                                    guid,
                                    menu_order, 
                                    post_type, 
                                    comment_count, 
                                    post_excerpt,
                                    to_ping,
                                    pinged, 
                                    post_content_filtered,
                                    post_mime_type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
wp_postmeta_insert = """INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (%s,%s,%s)"""

wp_term_relationships_insert = """INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) VALUES (%s, %s)"""

# insert to category and city
def insert_wp_term_relationships(post_id, city):
    # 274 modelle
    terms_cursor = mydb.cursor()
    terms_cursor.execute(f"SELECT wp_terms.term_id, wp_terms.name FROM wp_terms WHERE wp_terms.name = '{city}' ")
    terms = terms_cursor.fetchone()
    mycursor.execute(
        f"DELETE from wp_term_relationships where object_id={post_id}")
    mydb.commit()
    if terms:
        wp_value = [(post_id, 274), (post_id, terms[0])]
        mycursor.executemany(wp_term_relationships_insert, wp_value)
        mydb.commit()
    else:
        print ('fff')

def translateD(text):
    letter = {'ö': 'o', 'ä': 'e', 'ü': 'u', 'ß': 'ss'}
    for key, value in letter.items():
        if key in text:
            return text.replace(key, value)
    return text


def insert_wp_posts_stmt(data, post_author, post_parent=0):

    post_name = f'{post_author}-{translateD("".join(data["title"].lower().split()))}'

    wp_post_value = (post_author,
                     datetime.today(),
                     datetime.today(),
                     data['description'],
                     data['title'].upper(),
                     'publish',
                     'open',
                     'closed',
                     post_name,
                     datetime.today(),
                     datetime.today(),
                     post_parent,
                     '',
                     0,
                     'place',
                     0, '', '', '', '', '')
    mycursor.execute(wp_post_insert, wp_post_value)
    mydb.commit()
    return mycursor.lastrowid


def insert_wp_postmeta(id,  id_image, x_coord, y_coord, location, phone, nikname):
    wp_postmeta_values = [(id, '_vc_post_settings', 'a:1:{s:10:"vc_grid_id";a:0:{}}'),
                          (id, 'et_featured', '0'),
                          (id, 'et_full_location', location),
                          (id, 'et_location_lat', x_coord),
                          (id, 'et_location_lng', y_coord),
                          (id, 'de_realestate_stretch', nikname),
                          (id, 'de_realestate_child_room', '1'),
                          (id, 'de_realestate_furnish', '0'),
                          (id, 'de_realestate_notes', phone),
                          (id, 'rating_score', '0'),
                          (id, 'et_payment_package', '1003'),
                          (id, 'et_claimable', '1'),
                          (id, '_thumbnail_id', id_image)]

    mycursor.executemany(wp_postmeta_insert, wp_postmeta_values)
    mydb.commit()


def insert_wp_posts_image(image, url, post_author, post_parent=0):
    wp_post_value = (post_author,
                     datetime.today(),
                     datetime.today(),
                     '',
                     image,
                     'inherit',
                     'open',
                     'closed',
                     image.replace('.', '-'),
                     datetime.today(),
                     datetime.today(),
                     post_parent,
                     url,
                     0,
                     'attachment',
                     0, '', '', '', '', 'image/jpg')
    mycursor.execute(wp_post_insert, wp_post_value)
    mydb.commit()
    return mycursor.lastrowid


def insert_wp_postmeta_images(id, imageName):
    images = {
        'imageName': imageName,
        'imgs': imageName.split('.')[0]
    }
    imagesData = ['''a:5:{s:5:"width";i:1000;s:6:"height";i:700;''',
                  '''s:4:"file";s:13:"clubs/imgs/{imageName}";s:5:"sizes";'''.format(
                      **images),
                  '''a:9:{s:6:"medium";a:4:{s:4:''',
                  '''"file";s:13:"{imgs}-500x350.jpg"'''.format(**images),
                  ''';s:5:"width";i:500;s:6:"height";i:350;s:9:"mime-type";s:9:"image/jpg";}s:9:"thumbnail";a:4:{s:''',
                  '''4:"file";s:13:"{imgs}-400x400.jpg";s:5:"width";i:400;s:6:"height";i:400;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}s:12:"medium_large";a:4:{s:4:"file";s:''',
                  '''13:"{imgs}-768x538.jpg";s:5:"width";i:768;s:6:"height";i:538;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}s:18:"big_post_thumbnail";a:4:{s:4:"file";s:13:''',
                  '''"{imgs}-270x280.jpg";s:5:"width";i:270;s:6:"height";i:280;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}s:21:"medium_post_thumbnail";a:4:{s:4:"file";s:13:''',
                  '''"{imgs}-200x175.jpg";s:5:"width";i:200;s:6:"height";i:175;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}s:20:"small_post_thumbnail";a:4:{s:4:"file";s:11:''',
                  '''"{imgs}-70x65.jpg";s:5:"width";i:70;s:6:"height";i:65;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}s:21:"review_post_thumbnail";a:4:{s:4:"file";s:13:''',
                  '''"{imgs}-255x160.jpg";s:5:"width";i:255;s:6:"height";i:160;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}s:19:"place_cover_preview";a:4:{s:4:"file";s:13:''',
                  '''"{imgs}-286x200.jpg";s:5:"width";i:286;s:6:"height";i:200;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}s:21:"slide_place_thumbnail";a:4:{s:4:"file";s:13:''',
                  '''"{imgs}-858x600.jpg";s:5:"width";i:858;s:6:"height";i:600;s:9:"mime-type";s:9:"image/jpg";'''.format(
                      **images),
                  '''}}s:10:"image_meta";a:12:{s:8:"aperture";s:1:"0";s:6:"credit";s:0:"";s:6:"camera";s:0:"";s:7:"caption";s:0:"";s:17:"created_timestamp";s:1:"0";s:9:"copyright";s:0:"";s:12:"focal_length";s:1:"0";s:3:"iso";s:1:"0";s:13:shutter_speed";s:1:"0";s:5:"title";s:0:"";s:11:"orientation";s:1:"0";s:8:"keywords";a:0:{}}}''']

    wp_postmeta_values = [(id, '_wp_attached_file', f'clubs/imgs/{imageName}'),  # f'{year}/{month}/{imageName}'
                          (id, '_wp_attachment_metadata', ''.join(imagesData)),
                          (id, 'type_image', 'image_post')
                          ]

    mycursor.executemany(wp_postmeta_insert, wp_postmeta_values)
    mydb.commit()


def delete_posts(post_author=42):
    post_cursor = mydb.cursor()
    postmeta_cursor = mydb.cursor()
    post_cursor.execute(
        f"SELECT ID FROM wp_posts where post_author={post_author}")
    posts = post_cursor.fetchall()
    for x in posts:
        postmeta_cursor.execute(
            f"DELETE from wp_postmeta where post_id={x[0]}")
        mydb.commit()
    post_cursor.execute(
        f"DELETE from wp_posts where post_author={post_author}")
    mydb.commit()
    print(f'posts {post_author} deleted')

#  get all clubs
def getClubs():
    club_cursor = mydb.cursor()
    club_id = mydb.cursor()
    club_id.execute(
        """select wp_users.ID from wp_users where wp_users.ID >1""")
    clubs = club_id.fetchall()
    club_data = []
    for i in clubs:

        club_dict = {}
        # id = i[0]

        club_cursor.execute(f"""select wp_users.ID, 
                                      wp_usermeta.meta_key,
                                      wp_usermeta.meta_value from
                                      wp_users, wp_usermeta  
                                      where wp_users.ID = {i[0]} AND wp_usermeta.user_id = {i[0]}""")
        club = club_cursor.fetchall()
        # print ('======================================================')
        club_dict.update({'id': i[0]})
        for e in club:
            if e[1] == 'twitter':
                if len(e[2]) != 0:
                    club_dict.update({'url': e[2].split('#')[0]})
                    club_dict.update(
                        {'et_location_lat': e[2].split('#')[1].split(',')[0]})
                    club_dict.update(
                        {'et_location_lng': e[2].split("#")[1].split(',')[1].split(';')[0]})
                    club_dict.update(
                        {'stadt': e[2].split("#")[1].split(',')[1].split(';')[1]})
            if e[1] == 'location':
                club_dict.update({'location': e[2]})
            if e[1] == 'phone':
                club_dict.update({'phone': e[2]})
            if e[1] == 'nickname':
                club_dict.update({'nikname': e[2]})
        club_data.append(club_dict)
    return club_data
