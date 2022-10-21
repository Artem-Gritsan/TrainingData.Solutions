import os
import cv2 as cv
import xml.etree.ElementTree as ET
import numpy as np
from PIL import ImageColor





def xml_parser():
    tree = ET.parse('masks.xml')
    root = tree.getroot()
    for hex in root.iter('label'):
        if hex.find('name').text != 'Skin':
            continue
        hex = hex.find('color').text
        break
    count = 0
    for image in root.findall('image'):
        shapes = []
        ignore_shapes = []
        name_index = image.get('name').rfind('/')
        name = image.get('name')[name_index + 1:]
        for shape in image:
            points = shape.get('points').split(';')
            points = [list(map(float, x.split(','))) for x in points]
            if shape.get('label').lower() == 'ignore':
                ignore_shapes.append(points)
            else:
                shapes.append(points)
        count += 1

        image_mask(name, shapes, ignore_shapes, hex, count)
    return 'Выполнено'




def image_mask(name, points, ignore_points, hex, count):
    rgb = ImageColor.getrgb(hex)
    photo = cv.imread(f'images/{name}')
    ignore_pol = np.zeros(photo.shape[:2], dtype='uint8')
    skin = np.zeros(photo.shape[:2], dtype='uint8')
    for point in points:
        pts = np.array(point, np.int32)
        cv.fillPoly(skin, pts=[pts], color=255)
    if ignore_points:
        for ignore in ignore_points:
            ignore_pts = np.array(ignore, np.int32)
            cv.fillPoly(ignore_pol, pts=[ignore_pts], color=255)
            skin = cv.bitwise_xor(ignore_pol, skin)
    photo_copy = np.copy(photo)
    cv.imwrite(f'masks/{count}_material.png', skin)
    mask = black = cv.imread(f'masks/{count}_material.png')
    photo_copy[(mask == 255).all(-1)] = rgb
    black[(mask==255).all(-1)] = rgb
    new_name, black_name = 'marked_' + name, 'black_' + name
    cv.imwrite(f'new_images/{new_name}', photo_copy)
    cv.imwrite(f'black_images/{black_name}', black)







if __name__ == '__main__':
    print(xml_parser())

