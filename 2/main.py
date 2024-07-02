import json
import xml.etree.ElementTree as ET


def parse_xml_1():
    result = []

    tree = ET.parse('cats.xml')
    root = tree.getroot()

    for child in root:
        for grandchild in child:
            if grandchild.tag == 'fact':
                result.append(grandchild.text)

    with open('cat_result.txt', 'w') as f:
        f.write('\n'.join(result))


def parse_xml_2():
    result = []
    tree = ET.parse('cats.xml')
    root = tree.getroot()
    for info in root.findall('info'):
        fact = info.find('fact').text
        result.append(fact)

    with open('cat_result_2.txt', 'w') as f:
        f.write('\n'.join(result))


def parse_xml_to_json():
    result_dict = {}
    tree = ET.parse('cats.xml')
    root = tree.getroot()
    for number, info in enumerate(root.findall('info')):
        fact = info.find('fact').text
        result_dict[number] = fact

    print(result_dict, type(result_dict))

    with open('cat_result.json', 'w') as f:
        json.dump(result_dict, f)

    with open('cat_result.json', 'r') as f:
        result_from_json = json.load(f)

    print(result_from_json, type(result_from_json))

    print(result_dict == result_from_json)


def parse_json():
    with open('cats.json') as f:
        data = json.load(f)

    print(data.get('fact'))


if __name__ == '__main__':
    # parse_xml_1()
    # parse_xml_2()
    # parse_xml_to_json()
    parse_json()
