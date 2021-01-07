#!/usr/bin/python3

from gdzwfw_crawler import start_by_city

if __name__ == '__main__':
    # 单线程作业
    start_by_city()
    # par_excel_writer = PARExcelWriter('template/template.xlsx')
    # crawler = Crawler(par_excel_writer)
    # crawler.start_by_dept()
    # crawler.start_by_city()
    # par_excel_writer.save('downloads/output.xlsx')
