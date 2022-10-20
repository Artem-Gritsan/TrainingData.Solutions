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
    for image in root.findall('image'):
        shapes = []
        name_index = image.get('name').rfind('/')
        name = image.get('name')[name_index + 1:]
        for shape in image:
            if shape.get('label') == 'Ignore':
                continue
            points = shape.get('points').split(';')
            points = [list(map(float, x.split(','))) for x in points]
            shapes.append(points)

        image_mask(name, shapes, hex)
    return 'Выполнено'




def image_mask(name, points, hex):
    rgb = ImageColor.getrgb(hex)
    photo = cv.imread(f'images/{name}')
    img = np.zeros(photo.shape[:2], dtype='uint8')
    for point in points:
        pts = np.array(point, np.int32)
        cv.fillPoly(photo, pts=[pts], color=rgb)
        cv.fillPoly(img, pts=[pts], color=255)
        masked = cv.bitwise_and(photo, photo, mask=img)
    new_name, black_name = 'marked_' + name, 'black_' + name
    cv.imwrite(f'new_images/{new_name}', photo)
    cv.imwrite(f'black_images/{black_name}', masked)







if __name__ == '__main__':
    print(xml_parser())

