import os
import re
# import xml.etree.ElementTree as ET
from lxml import etree

text = """Welcome to the Regex Training Center! Let's start with some dates:
01/02/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20, and 2021.07.04. You can
also find dates with words: March 14, 2022, and December 25, 2020. 

Now let's move on to some phone numbers:
(123) 456-7890, +1-800-555-1234, 800.555.1234, 800-555-1234, and 123.456.7890. 
Other formats include international numbers: +44 20 7946 0958, +91 98765 43210.

Here are some email addresses to find:
john.doe@example.com, jane_doe123@domain.org, support@service.net, info@company.co.uk, 
and contact.us@my-website.com. You might also find these tricky: weird.address+spam@gmail.com,
"quotes.included@funny.domain", and this.one.with.periods@weird.co.in.

Need some URLs to extract? Try these:
http://example.com, https://secure.website.org, http://sub.domain.co, 
www.redirect.com, and ftp://ftp.downloads.com. Don't forget paths and parameters:
https://my.site.com/path/to/resource?param1=value1&param2=value2, 
http://www.files.net/files.zip, https://example.co.in/api/v1/resource, and 
https://another-site.org/downloads?query=search#anchor. 

Hexadecimal numbers appear in various contexts:
0x1A3F, 0xBEEF, 0xDEADBEEF, 0x123456789ABCDEF, 0xA1B2C3, and 0x0. You might also find these: 
#FF5733, #C70039, #900C3F, #581845, #DAF7A6, and #FFC300. RGB color codes can be tricky: 
rgb(255, 99, 71), rgba(255, 99, 71, 0.5).

For those interested in Social Security numbers, here's some data:
123-45-6789, 987-65-4321, 111-22-3333, 555-66-7777, and 999-88-7777. Note that Social 
Security numbers might also be written like 123 45 6789 or 123456789.

Let's throw in some random sentences for good measure:
- The quick brown fox jumps over the lazy dog.
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Jack and Jill went up the hill to fetch a pail of water.
- She sells seashells by the seashore.

Finally, let's include some special characters and numbers:
1234567890, !@#$%^&*()_+-=[]{}|;':",./<>?, 3.14159, 42, and -273.15.

That's it! I hope you find this useful for your regex training."""


def parse_date():
    patern = r'\b(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}[./-]\d{1,2}[./-]\d{1,2}|(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})\b'
    dates = re.findall(patern, text)
    print(dates)


def parse_mail():
    patern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    mails = re.findall(patern, text)
    print(mails)


def parse_xpath_xml_text_input_what(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()

    tree = etree.HTML(html)
    input_elements = tree.xpath("//input[@id='text-input-what']")

    placeholders = [element.get('placeholder') for element in input_elements]
    print(placeholders)


def parse_xpath_xml_text_input_where(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()

    tree = etree.HTML(html)
    input_elements = tree.xpath("//input[@id='text-input-where']")

    placeholders = [element.get('placeholder') for element in input_elements]
    print(placeholders)


def parse_xpath_xml_text_input_what_where_button(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()

    tree = etree.HTML(html)
    input_elements = tree.xpath("//form[@id='jobsearch']//button[@type='submit']")

    placeholders = [element.text for element in input_elements]
    print(placeholders)


if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)
    html_file_path = os.path.join(current_dir, 'data', 'br_indeed_com.html')

    # parse_date()
    # parse_mail()
    # parse_xpath_xml_text_input_what(html_file_path)
    # parse_xpath_xml_text_input_where(html_file_path)
    parse_xpath_xml_text_input_what_where_button(html_file_path)
