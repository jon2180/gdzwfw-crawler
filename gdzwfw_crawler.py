"""
爬虫主流程，数据获取及数据保存
"""

import api
from excel_writer import PARExcelWriter
from model import PowerAndResponsibility


class Crawler:
    _excel_writer: PARExcelWriter

    def __init__(self, excel_writer: PARExcelWriter):
        self._excel_writer = excel_writer

    def start_by_city(self):
        """
        从这个链接 https://www.gdzwfw.gov.cn/portal/affairs-public-duty-city?region=440000 开始爬取，即以地市为入口

        大致逻辑是 先获取到所有市，再获取到各个区，（可以考虑在加个村，目前没做），然后在根据市区为参数开始获取具体的职权列表
        """
        dict_detail = api.portal_custom_config_get_detail()

        # TODO 遍历市级
        for city in dict_detail['data']['data']['city']:

            org_area_code = city['ORGAREACODE']
            org_name = city['ORGNAME']
            org_sub_name = city['ORGSNAME']  # 纯市名，类似于 广州市 等市名字
            print(f'开始爬取 {org_name}')

            # TODO 遍历区县级
            dict_details = api.portal_custom_config_get_detail(region_code=org_area_code)
            for country in dict_details['data']['data']['country']:

                country_org_name = country['ORGNAME']
                country_org_sub_name = country['ORGSNAME']
                print(f'开始爬取 {country_org_name}')

                # TODO 按区写入 excel
                par_excel_writer = PARExcelWriter('template/template.xlsx')
                xlsx_name = f'{org_name}-{country_org_sub_name}.xlsx'


                # TODO 根据以上参数来获取具体的 每一个区 的权责列表
                arr = []
                for dept in dict_details['data']['data']['department']:
                    arr.append(dept['ORGNUMBER'])

                dic_par = api.get_power_and_responsibility(
                    dept_code='',
                    dept_codes=','.join(arr),
                    region=org_area_code,
                    is_province=1,
                    page_num=1
                )

                # 获取到数据
                page_info = dic_par['data']['custom']['PAGEINFO']

                idx = 1

                # 分页
                pages_num = int((int(page_info['TOTALNUM']) - 1) / int(page_info['PAGESIZE'])) + 2
                print(f'pages_num:\t{pages_num - 1}')

                for page_index in range(
                        1,
                        1
                        # TODO 这里作了弊，不让它继续执行，为了快速检查excel是否有问题
                        # int((int(page_info['TOTALNUM']) - 1) / int(page_info['PAGESIZE'])) + 2
                ):
                    # 获取到数据
                    if page_index >= 2:
                        dic_par = dic_par = api.get_power_and_responsibility(
                            dept_code='',
                            dept_codes=','.join(arr),
                            region=org_area_code,
                            is_province=1,
                            page_num=page_index
                        )

                    for item in dic_par['data']['custom']['PowerandresponsibilityList']:
                        par_model = PowerAndResponsibility()
                        par_model.libNum = 'qzqdk'
                        par_model.source = '广东政务服务网'
                        par_model.genre = '清单'
                        # TODO
                        par_model.creatorName = 'zhangjun'
                        par_model.catalogId = item['CATALOG_ID']

                        # 主要是用于做 referer 的值
                        qzqd_code = item['ROWGUID']  # B09EA62464F2128AE0530A3D10ACF619
                        dept_code = item['DEPT_CODE']  # MB2D0164X
                        catelog_id = item['CATALOG_ID']

                        # print(qzqd_code)
                        # print(dept_code)
                        # print(catelog_id)
                        prefix = f'权责清单#{idx}'
                        print(prefix)
                        print('dept_code: ', item['DEPT_CODE'])
                        print('row_guid : ', item['ROWGUID'])  # 关键值，url 拼接可用
                        print('task_name: ', item['TASK_NAME'])
                        print('dept_name: ', item['DEPT_NAME'])
                        print('laws     : ', item['LAWS'])
                        print('catalog_id: ', item['CATALOG_ID'])
                        print('responsibility: ', item['RESPONSIBILITY'])
                        print()

                        # 针对每一条数据进行操作
                        # self.start_affairs_public_detail(
                        #     par_model=par_model,
                        #     dept_code=dept_code_outer,
                        #     qzqd_code=qzqd_code,
                        #     prefix=prefix
                        # )
                        idx += 1
                        print()

                # todo 写入到 excel
                par_excel_writer.save(f'downloads/{xlsx_name}')

    def start_by_dept(
            self,
            dept_code_outer: str = '006939756',
            region_outer: str = '440000',
    ):
        # 获取到数据
        dic_par = api.get_power_and_responsibility(dept_code=dept_code_outer, region=region_outer)
        page_info = dic_par['data']['custom']['PAGEINFO']

        idx = 1

        for page_index in range(
                1,
                int((int(page_info['TOTALNUM']) - 1) / int(page_info['PAGESIZE'])) + 2
        ):
            # 获取到数据
            if page_index >= 2:
                dic_par = api.get_power_and_responsibility(
                    dept_code=dept_code_outer,
                    region=region_outer,
                    page_num=page_index
                )

            for item in dic_par['data']['custom']['PowerandresponsibilityList']:
                par_model = PowerAndResponsibility()
                par_model.libNum = 'qzqdk'
                par_model.source = '广东政务服务网'
                par_model.genre = '清单'
                # TODO
                par_model.creatorName = 'zhangjun'
                par_model.catalogId = item['CATALOG_ID']

                # 主要是用于做 referer 的值
                qzqd_code = item['ROWGUID']  # B09EA62464F2128AE0530A3D10ACF619
                dept_code = item['DEPT_CODE']  # MB2D0164X
                catelog_id = item['CATALOG_ID']

                # print(qzqd_code)
                # print(dept_code)
                # print(catelog_id)
                prefix = f'权责清单#{idx}'
                print(prefix)
                # print('dept_code: ', item['DEPT_CODE'])
                # print('row_guid : ', item['ROWGUID'])  # 关键值，url 拼接可用
                # print('task_name: ', item['TASK_NAME'])
                # print('dept_name: ', item['DEPT_NAME'])
                # print('laws     : ', item['LAWS'])
                # print('catalog_id: ', item['CATALOG_ID'])
                # print('responsibility: ', item['RESPONSIBILITY'])
                # print()

                # 针对每一条数据进行操作
                self.start_affairs_public_detail(
                    par_model=par_model,
                    dept_code=dept_code_outer,
                    qzqd_code=qzqd_code,
                    prefix=prefix
                )
                idx += 1
                print()
        return True

    def start_affairs_public_detail(
            self,
            par_model: PowerAndResponsibility,
            qzqd_code: str = 'B09EA62464F2128AE0530A3D10ACF619',
            dept_code: str = 'MB2D0164X',
            prefix: str = ''
    ):
        # 第一个链接
        # 获取到的是简要信息（没有分页信息）
        main_detail = api.get_power_and_responsibility_xx(
            qzqd_code=qzqd_code,
            dept_code=dept_code
        )

        # print(main_detail['data']['custom']['POWERANDRESPONSIBILITYLIST'])
        # print(item['CATALOG_ID'])
        # print(item['ROWGUID'])

        dic_useful = main_detail['data']['custom']['POWERANDRESPONSIBILITYLIST']
        par_model.publisher = dic_useful['DEPT_NAME']
        par_model.classify = dic_useful['TASK_TYPE']
        par_model.belongDomain = '政府-xxx'
        base_code = dic_useful['XKSXBM']

        dic_audit_item = api.fetch_common_audit_item_(
            base_code=base_code,
            task_type=dic_useful['TASK_TYPE'],
            qzqd_code=dept_code,  # TODO
            dept_code=dic_useful['DEPT_CODE'],
            page_num=1
        )

        idx = 1

        page_info = dic_audit_item['data']['CUSTOM']['PAGEINFO']
        for page_index in range(
                1,
                int((int(page_info['TOTALNUM']) - 1) / int(page_info['PAGESIZE'])) + 2):
            # 第二个链接
            if page_index >= 2:
                dic_audit_item = api.fetch_common_audit_item_(
                    base_code=base_code,
                    task_type=dic_useful['TASK_TYPE'],
                    qzqd_code=dept_code,  # TODO
                    dept_code=dic_useful['DEPT_CODE'],
                    page_num=page_index
                )
            for item in dic_audit_item['data']['CUSTOM']['AUDIT_ITEMLIST']:
                print(f'{prefix} - 实施清单#{idx}')

                # print('guid:         ', item['ITEMGUID'])
                # print('catalog_name: ', item['parentCatalogName'])
                # print('task_code:    ', item['TASK_CODE'])

                guid = item['TASK_CODE']
                par_model.originalAddress = f'https://www.gdzwfw.gov.cn/portal/guide/{guid}'

                self.start_portal_guide(
                    par_model=par_model,
                    guid=guid
                )
                idx += 1

    def start_portal_guide(
            self,
            par_model: PowerAndResponsibility,
            guid: str
    ):
        # TODO 在这里获取核心数据
        soup_main_guide_html = api.fetch_par_guide_(guid=guid)

        tag_list = soup_main_guide_html.select('.matters-truncate')
        title = tag_list[0]
        classify = tag_list[2]
        par_model.title = title.string
        par_model.classify = classify.string

        for key, val in par_model.__dict__.items():
            print(f'{key}:\t{val}')

        # self._excel_writer.write_row(par_model)
