import xml.etree.ElementTree as ET



def edit_id(start, root, tree, id=0):
    if root.find('image').get('id') != '0':
        for child in root.iter('image'):
            child.set('id', str(id))
            id += 1
    else:
        id = int(root.findall('image')[-1].get('id'))
        for child in root.iter('image'):
            child.set('id', str(id))
            id -= 1
    tree.write(f'{start}_copy.xml')
    return 'Файл изменен'


def edit_extension(root, tree, start):
    for child in root.iter('image'):
        index = child.get('name').rfind('.')
        name = child.get('name')[:index+1] + 'png'
        child.set('name', name)
    tree.write(f'{start}_copy.xml')
    return 'Файл изменен'

def edit_path(root, tree, start):
    for child in root.iter('image'):
        index = child.get('name').rfind('/')
        name = child.get('name')[index+1:]
        child.set('name', name)
    tree.write(f'{start}_copy.xml')
    return 'Файл изменен'


def main():

    while True:
        try:
            start = input("Введите название файла или exit: ")
            if start == 'exit':
                break
            tree = ET.parse(f'{start}.xml')
            root = tree.getroot()
            while True:
                number = input('Введите нужный вам пункт(7-9) или exit: ')
                if number == '7':
                    print(edit_id(start, root, tree))
                elif number == '8':
                    print(edit_extension(root, tree, start))
                elif number == '9':
                    print(edit_path(root, tree, start))
                elif number == 'exit':
                    break
                else:
                    print('Что-то не так. Попробуйте еще раз')

        except FileNotFoundError:
            print('Что-то пошло не так. Попробуйте еще раз!')











if __name__ == '__main__':
    main()