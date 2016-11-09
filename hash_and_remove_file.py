import os
import glob
from PIL import Image

def dhash(image, hash_size = 8):
    image = image.convert('L').resize((hash_size + 1,hash_size), Image.ANTIALIAS)
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col,row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)


def check_unique_hash(hash,db,cursor):
    sql_get = "SELECT hash FROM hashes_duplicates WHERE hash = '%s'" % (hash)
    try:
        cursor.execute(sql_get)
        if not cursor.rowcount:
            return True
        else:
            return False
    except:
        pass


def update_image_process(id,db,cursor):
    sql_update = "UPDATE image_process SET is_hashed = 1 WHERE post_id = %s" % (id)
    try:
        cursor.execute(sql_update)
        db.commit()
    except:
        db.rollback()

def hash_to_mysql(hash,id,db,cursor):
    sql_insert = "INSERT INTO hashes (hash, post_id) VALUES ('%s', '%s')" % (hash, id)
    try:
        cursor.execute(sql_insert)
        db.commit()
        update_image_process(id,db,cursor)
    except:
        db.rollback()


def hash_images(db,cursor):
    for file in os.listdir("/home/kenneth/dlimage"):
        try:
            hash = dhash(Image.open("/home/kenneth/dlimage/"+file))
            hash_to_mysql(hash,file,db,cursor)
        except:
            pass
    filelist = glob.glob("/home/kenneth/dlimage/*")
    for f in filelist:
        os.remove(f)