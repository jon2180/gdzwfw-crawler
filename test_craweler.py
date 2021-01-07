import unittest
from gdzwfw_crawler import crawl_per_county, start_portal_guide
from model.PARExcelWriter import PARExcelWriter
from model import PowerAndResponsibility


class MyTestCase(unittest.TestCase):
    def test_crawl_guide(self):
        # 爬取一个页面
        par_excel_writer = PARExcelWriter('template/template.xlsx')
        start_portal_guide(
            par_excel_writer=par_excel_writer,
            par_model=PowerAndResponsibility(),
            guid='11440300MB2D0722464440127028001'
        )
        par_excel_writer.save('downloads/output.xlsx')
        self.assertTrue(True)

    def test_crawl_single_town_1(self):
        # 爬取一个区县镇
        crawl_per_county(
            org_name='云浮市',
            country_org_sub_name='云安区-石城镇',
            departments=[],
            org_area_code='445323109000'
        )
        self.assertTrue(True)

    def test_crawl_single_town_2(self):
        # 爬取一个区县镇
        crawl_per_county(
            org_name='广州市',
            country_org_sub_name='越秀区-北京街道',
            departments=[],
            org_area_code='440104003000'
        )
        self.assertTrue(True)

    def test_crawl_single_town_3(self):
        # 爬取一个区县镇
        crawl_per_county(
            org_name='广州市',
            country_org_sub_name='番禺区-市桥街',
            departments=[],
            org_area_code='440113007000'
        )
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
