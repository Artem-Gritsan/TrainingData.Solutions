import os
import cv2 as cv
import xml.etree.ElementTree as ET
import numpy as np
from PIL import ImageColor





def xml_parser():
    while True:
        try:
            start = input("Введите название файла или exit: ")
            if start == 'exit':
                break
            tree = ET.parse(f'{start}.xml')
            root = tree.getroot()
            get_colors(root)
        except FileNotFoundError:
            print('Что-то пошло не так. Попробуйте еще раз!')


def get_colors(root):
    colors = {}
    for tag in root.iter('label'):
        hex = tag.find('color').text
        rgb = ImageColor.getrgb(hex)
        colors[tag.find('name').text.lower()] = rgb
    return get_points(root, colors)

def get_points(root, colors):
    for image in root.findall('image'):
        shapes = {}
        ignore_shapes = []
        name_index = image.get('name').rfind('/')
        name = image.get('name')[name_index + 1:]
        for shape in image:
            color_class = shape.get('label').lower()
            color = colors[color_class] if color_class in colors else (255, 255, 255)
            points = shape.get('points').split(';')
            points = [list(map(float, x.split(','))) for x in points]
            if shape.get('label').lower() == 'ignore':
                ignore_shapes.append(points)
            else:
                if color not in shapes:
                    shapes[color] = [points]
                else:
                    shapes[color].append(points)
        create_black_image(name, shapes, ignore_shapes)
    os.remove('skin.png')
    print('Выполнено')


def create_black_image(name, shapes, ignore_shapes):
    photo = cv.imread(os.path.join('images', name))
    cv.imwrite('skin.png', np.zeros(photo.shape[:2], dtype='uint8'))
    skin = cv.imread('skin.png')
    for color, shape in shapes.items():
        for points in shape:
            pts = np.array(points, np.int32)
            cv.fillPoly(skin, pts=[pts], color=color)
    if ignore_shapes:
        for ignore in ignore_shapes:
            ignore_pts = np.array(ignore, np.int32)
            cv.fillPoly(skin, pts=[ignore_pts], color=0)
    os.mkdir('black_images') if not os.path.exists('black_images') else None
    cv.imwrite(os.path.join('black_images', f'black_{name}'), skin)
    return create_image(skin, photo, shapes, name)


def create_image(skin, photo, shapes, name):
    for color in shapes.keys():
        mask = cv.inRange(skin, color, color)
        cv.imwrite('skin.png', mask)
        mask = cv.imread('skin.png')
        photo[(mask == 255).all(-1)] = color
    new_name = 'marked_' + name
    os.mkdir('new_images') if not os.path.exists('new_images') else None
    cv.imwrite(os.path.join('new_images', new_name), photo)







if __name__ == '__main__':
    xml_parser()

