"""
网页解析器

: 先解析 Html
: 获取其中的有效链接，存入 Url_manager
: 解析有效数据，并把数据存入 excel

政务公开 权责清单/
"""
from bs4 import BeautifulSoup
from lxml import etree
from json import loads
from downloader import fetch_json, build_post_body, fetch_html

# from bs4 import BeautifulSoup
#
# def parse_html(html_doc: str) -> BeautifulSoup:
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     return soup


def res_json(fetch_func):
    def wrapped_fetch_func(*args, **key_word):
        json_str = fetch_func(*args, **key_word)

        if json_str is None:
            raise ValueError()
        dic = loads(json_str)
        assert isinstance(dic, dict)
        return dic

    return wrapped_fetch_func


def res_html(fetch_func):
    def wrapped_fetch_func(*args, **key_word):
        html_str = fetch_func(*args, **key_word)
        if html_str is None:
            raise ValueError()
        return etree.HTML(html_str)
    return wrapped_fetch_func


@res_html
def fetch_affairs_public_duty_list_(region: 'str' = '440000', dept_code: 'str' = '006940386') -> BeautifulSoup:
    return fetch_html(f'https://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region={region}&deptCode={dept_code}')


@res_json
def fetch_gdbs_nav_(region: 'str' = '440000', dept_code: 'str' = '006940386') -> dict:
    """
    获取权责清单的查找依据： 根据部门， 类型，或地市

    :return: json | None
    """
    return fetch_json(
        'https://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/index',
        refer=f'https://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region={region}&deptCode={dept_code}',
        content_type='application/x-www-form-urlencoded; charset=UTF-8',
        post_body=build_post_body({
            'regCode': region,  # region code 区域代码
            'responsibility': '1'  # 责任
        })
    )


@res_json
def fetch_par_sum_(region: 'str' = '440000', dept_code: 'str' = '006940386'):
    """
    主要是为了获取 TASK_TYPE

    :return: json | None
    """
    return fetch_json(
        'https://www.gdzwfw.gov.cn/portal/item-event/getPowerandresponsibilitySum',
        refer=f'https://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region={region}&deptCode={dept_code}',
        content_type='application/x-www-form-urlencoded; charset=UTF-8',
        post_body=build_post_body({
            'regCode': region,  # region code 区域代码
            'responsibility': '1'  # 责任

        })
    )


@res_json
def get_power_and_responsibility(
        region: str = '440000',
        is_province: int = 0,
        page_num: int = 1,
        dept_code: str = '006940386',
        dept_codes: str = ('006939756,006940116,006939801,696453330,725107227,006940140,006940175,006940167,'
                           '006939991,553612461,MB2D02159,006940060,006939799,006939844,006941135,006939908,'
                           '096927520,MB2C87614,006940132,MB2D01906,758333079,006940028,MB2D02343,091785615,'
                           '006940124,00693981X,759214127,006939537,671392287,MB2C86400,671571488,006939916,'
                           '006940386,MB2D03442,006941127,MB2D0164X,748039589')
) -> dict:
    """
    获取权责清单主项
    """
    # 创建 body
    # post_body = build_body()
    # 获取到数据
    return fetch_json(
        "https://www.gdzwfw.gov.cn/portal/item-event/getPowerandresponsibility",
        content_type="application/x-www-form-urlencoded",
        refer=f"https://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region={region}&deptCode={dept_code}",
        post_body=build_post_body({
            'pageNum': page_num,
            'pageSize': 10,
            'DEPT_CODE': dept_code,
            'TASK_TYPE': '',
            'KEYWORD': '',
            'AREACODE': region,
            'ISPROVINCE': is_province,
            'DEPT_CODES': dept_codes
        })
    )


@res_json
def portal_custom_config_get_detail(region_code: str = 440000) -> dict:
    return fetch_json(
        'https://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail',
        content_type="application/x-www-form-urlencoded",
        refer=f"https://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region={region_code}",
        post_body=build_post_body({
            'regCode': region_code,
        })
    )


def fetch_par_(
        region: 'str' = '440000',
        dept_code: 'str' = '006940386',
        page_num: 'int' = 1,
        dept_codes: 'str' = ('006939756,006940116,006939801,696453330,725107227,006940140,006940175,006940167,'
                             '006939991,553612461,MB2D02159,006940060,006939799,006939844,006941135,006939908,'
                             '096927520,MB2C87614,006940132,MB2D01906,758333079,006940028,MB2D02343,091785615,'
                             '006940124,00693981X,759214127,006939537,671392287,MB2C86400,671571488,006939916,'
                             '006940386,MB2D03442,006941127,MB2D0164X,748039589')
):
    return get_power_and_responsibility(region, dept_code, page_num, dept_codes)


@res_json
def get_power_and_responsibility_xx(
        qzqd_code: 'str',
        dept_code: 'str'
) -> dict:
    """
    获取权责简要信息
    :param qzqd_code
    :param dept_code
    :return: json | None
    """

    return fetch_json(
        'https://www.gdzwfw.gov.cn/portal/item-event/getPowerandresponsibilityxx',
        # '/portal/item-event/getPowerandresponsibilityxx',
        refer=f"https://www.gdzwfw.gov.cn/portal/affairs-public-detail?qzqdCode={qzqd_code}&deptCode={dept_code}",
        content_type='application/x-www-form-urlencoded; charset=UTF-8',
        post_body=build_post_body({
            'ITEMGUID': qzqd_code,
            'DEPT_CODE': dept_code
        }),
    )


def get_par_list_(
        qzqd_code: 'str',
        dept_code: 'str'
):
    return get_power_and_responsibility_xx(qzqd_code, dept_code)


@res_json
def fetch_common_audit_item_(
        qzqd_code: 'str',
        dept_code: 'str',
        task_type: 'str',
        base_code: 'str',
        page_num: 'int' = 1,
) -> dict:
    """
    获取实施清单列表
    :return:
    """
    # qzqdCode = 'B09EA62464F2128AE0530A3D10ACF619'
    # deptCode = 'MB2D0164X'
    return fetch_json(
        'https://www.gdzwfw.gov.cn/portal/item/getCommonAuditItem',
        refer=f'https://www.gdzwfw.gov.cn/portal/affairs-public-detail?qzqdCode={qzqd_code}&deptCode={dept_code}',
        content_type='application/x-www-form-urlencoded; charset=UTF-8',
        post_body=build_post_body({
            'pageNum': page_num,
            'pageSize': 10,
            'DEPT_CODE': dept_code,
            'TASK_TYPE': task_type,
            'BASECODE': base_code,
            'KEY_WORD': '',
            'AREA_CODE': '',
            'ISLOCALLEVEL': '',
            'TASKTAG': '',
            'TYPE': '',
            'IS_ONLINE': ''
        })
    )


@res_html
def fetch_par_guide_(guid: 'str' = '11440000MB2D0164XH2440289876000'):
    """
    GET
    :return: html
    """
    return fetch_html(f'https://www.gdzwfw.gov.cn/portal/guide/{guid}')
