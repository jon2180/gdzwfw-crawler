#!/usr/bin/python3

from excel_writer import PARExcelWriter
from gdzwfw_crawler import crawl_per_county
from model import PowerAndResponsibility

if __name__ == '__main__':
    # 爬取一个区县镇
    crawl_per_county(
        org_name='广州市',
        country_org_sub_name='越秀区-北京街道',
        departments=[],
        org_area_code='440104003000'
    )
# 440113007000