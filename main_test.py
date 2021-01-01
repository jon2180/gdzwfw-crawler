#!/usr/bin/python3

from excel_writer import PARExcelWriter
from gdzwfw_crawler import start_portal_guide
from model import PowerAndResponsibility

if __name__ == '__main__':
    # 爬取一个页面
    par_excel_writer = PARExcelWriter('template/template.xlsx')
    start_portal_guide(
        par_excel_writer=par_excel_writer,
        par_model=PowerAndResponsibility(),
        guid='11440300MB2D0722464440127028001'
    )
    par_excel_writer.save('downloads/output.xlsx')
    # par_excel_writer = PARExcelWriter('template/template.xlsx')
    # crawler = Crawler(par_excel_writer)
    # crawler.start_by_dept()
    # crawler.start_by_city()
    # par_excel_writer.save('downloads/output.xlsx')
