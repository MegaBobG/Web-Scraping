import csv
import json
from pprint import pprint
import xml.etree.ElementTree as ET
import sqlite3

from sqlalchemy import create_engine, Column, Integer, String, Boolean, func
from sqlalchemy.orm import sessionmaker, declarative_base

# from credentials import NEON_PASSWORD

example = [
    ["Tom", "Smith", 80, True],
    ["Alice", "Johnson", 92, False],
    ["Bob", "Williams", 75, True],
    ["Emma", "Brown", 88, False],
    ["David", "Jones", 107, True]
]


def write_csv():
    filename = 'people.csv'
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['First name', 'Last name', 'Weigth', 'Is male'])
        writer.writerows(example)


def write_json():
    filename = 'people.json'
    data = [
        {'First name': First_name, 'Last_name': Last_name, 'Weigth': Weigth, 'Is male': Is_male}
        for First_name, Last_name, Weigth, Is_male in example
    ]
    pprint(data)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def write_xml():
    filename = 'people.xml'

    root = ET.Element('People')
    for entry in example:
        person = ET.SubElement(root, 'Person')
        ET.SubElement(person, 'First name').text = entry[0]
        ET.SubElement(person, 'Last name').text = entry[1]
        ET.SubElement(person, 'Weigth').text = str(entry[2])
        ET.SubElement(person, 'Is male').text = str(entry[3])

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


def write_sqlite():
    filename = 'people.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        create table if not exists people (
            id integer primary key,
            first_name text,
            last_name text,
            weight integer,
            is_male boolean
        )
    """
    cursor.execute(sql)

    for entry in example:
        cursor.execute("""
            insert into people (first_name, last_name, weight, is_male)
            values (?, ?, ?, ?)
        """, (entry[0], entry[1], entry[2], entry[3]))

    conn.commit()
    conn.close()


def read_sqlite():
    filename = 'people.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # 1. get all data
    sql = """
            select first_name, last_name
            from people
        """
    rows = cursor.execute(sql).fetchall()
    print(rows)

    # 2. get all male
    sql = """
        select first_name, last_name
        from people
        where is_male = true
    """
    rows = cursor.execute(sql).fetchall()
    print(rows)

    # 3. max / min weight
    sql = """
        select first_name, last_name
        from people
        where weight = (select min(weight) from people)
    """
    rows = cursor.execute(sql).fetchall()
    print(rows)

    conn.close()


def write_sqlalchemy():
    filename = 'people_sqlalchemy.db'
    engine = create_engine(f'sqlite:///{filename}')

    Base = declarative_base()

    class Person(Base):
        __tablename__ = 'person'

        id = Column(Integer, primary_key=True)
        first_name = Column(String)
        last_name = Column(String)
        weight = Column(Integer)
        is_male = Column(Boolean)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for entry in example:
        person = Person(first_name=entry[0], last_name=entry[1], weight=entry[2], is_male=entry[3])
        session.add(person)

    session.commit()
    session.close()


if __name__ == '__main__':
    # write_csv()
    # write_json()
    # write_xml()
    # write_sqlite()
    # read_sqlite()
    write_sqlalchemy()
