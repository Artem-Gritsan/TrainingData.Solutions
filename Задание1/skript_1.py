import os
import sys
import xml.etree.ElementTree as ET
import random


def get_all_images(root):
    count_images = len(root.findall('image'))
    if not count_images:
        print('В файле нет нужных данных!')
        os.execl(sys.executable, sys.executable, *sys.argv)
    return f'1.Всего изображений: {count_images}'

def marked_images(root, counter=0, counter1=0):
    for mark in root.iter('image'):
        if mark:
            counter += 1
        else:
            counter1 += 1
    return f'\n2.Размечено: {counter}' + (f'\n3.Не размечено: {counter1}' if counter1 != 0 else '')

def all_shapes(root):
    shapes = len(root.findall('./image/'))
    return f'\n5.Всего фигур: {shapes}'

def image_shape(root, max_images, min_images, max_size=0, min_size=99999,):
    for image in root.iter('image'):
        width = int(image.get('width'))
        height = int(image.get('height'))
        sum = width + height
        if sum > max_size:
            max_size = sum
            max_images.clear()
            max_images.append(image)
        elif sum == max_size:
            max_images.append(image)
        if sum < min_size:
            min_size = sum
            min_images.clear()
            min_images.append(image)
        elif sum == min_size:
            min_images.append(image)
    max_image = max_images[random.randrange(len(max_images))]
    min_image = min_images[random.randrange(len(min_images))]
    return f'\n6.Самое большое: name={min_image.get("name")}, ' \
           f'width={max_image.get("width")}, ' \
           f'height={max_image.get("height")}' + (f' Количество={len(max_images)}\n' if len(max_images) > 1 else None) + \
           f'  Самое маленькое: name={min_image.get("name")},' \
           f' width={min_image.get("width")},' \
           f' height={min_image.get("height")}' + (f' Количество={len(min_images)}\n' if len(min_images) > 1 else '')



def main():
    while True:
        try:
            start = input("Введите название файла или exit: ")
            if start == 'exit':
                break
            tree = ET.parse(f'{start}.xml')
            root = tree.getroot()
            print(get_all_images(root), marked_images(root), all_shapes(root), image_shape(root, [], []))
        except FileNotFoundError:
            print('Файл не найден.')










if __name__ == '__main__':
    main()