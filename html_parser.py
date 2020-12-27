"""
网页解析器

: 先解析 Html
: 获取其中的有效链接，存入 Url_manager
: 解析有效数据，并把数据存入 excel
"""
from json import loads
from lxml import etree

from bs4 import BeautifulSoup


def parse_html_by_etree(html_doc: str):
    return etree.HTML(html_doc)


def parse_html(html_doc: str) -> BeautifulSoup:
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def parse_json(json_str: str) -> dict:
    json_dic = loads(json_str)
    return json_dic
