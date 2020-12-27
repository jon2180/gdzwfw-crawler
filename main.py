#!/usr/bin/python3

from excel_writer import PARExcelWriter
from gdzwfw_crawler import Crawler

if __name__ == '__main__':
    # 单线程作业
    par_excel_writer = PARExcelWriter('template/template.xlsx')
    crawler = Crawler(par_excel_writer)
    # crawler.start_by_dept()
    crawler.start_by_city()
    par_excel_writer.save('downloads/output.xlsx')
