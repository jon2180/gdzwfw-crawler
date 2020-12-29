import requests
import json
import time
from lxml import etree
# from package import tool
# import re

headers = {
    # "Accept": "application/json, text/javascript, */*; q=0.01",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9",
    # "Connection": "keep-alive",
    # "Content-Length": "14",
    # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Cookie": "portal=BA77EF5E4B37AAF4BE24E7E671AFE103; _horizon_uid=0e1700ce-5aa1-425e-ad5c-9c3ca7a17da7; _horizon_sid=e1bc7672-c10d-4873-b964-535de2df63d4",
    # "Host": "www.gdzwfw.gov.cn",
    # "Origin": "https://www.gdzwfw.gov.cn",
    "Referer": "https://www.gdzwfw.gov.cn/portal/affairs-public-duty-city?region=440000",
    # "sec-ch-ua": 'Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    # "sec-ch-ua-mobile": "?0",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    # "X-Requested-With": "XMLHttpRequest"
}

# id = 0
# belongDomainList = "外交|国防|发展和改革|教育|科学技术|工业和信息化|民族事务|公安|国家安全|民政|司法|财政|人力资源和社会保障|自然资源|生态环境|住房和城乡建设|交通运输|水利|农业农村|商务|文化和旅游|卫生健康|退役军人事务|应急管理|人民银行|审计|国有资产监督管理|海关|税务|市场监督管理|广播电视|体育|统计|国际发展合作|医疗保障|参事|国家机关事务管理|港澳事务|研究|新华通讯|科学|社会科学|工程|发展研究|广播电视|气象|银行保险监督管理|证券监督管理|信访|粮食和物资储备|能源|国防科技工业|烟草专卖|移民|林业和草原|铁路|民用航空|邮政|文物|中医药管理|煤矿安全监察|外汇管理|药品监督管理|知识产权"


def GetWeb(url, params):
    page = requests.get(url=url, params=params, headers=headers)
    return page


# 11.主题分类
# url = "https://www.gdzwfw.gov.cn/portal/guide/11440300MB2D0722464440127028001"
# page_text = GetWeb(url, "").text
# time.sleep(1)
# tree = etree.HTML(page_text)


# 获取键值对形式的信息
def getDictInfo(tr_list, name):
    # print(name)
    info_list = dict()
    info = dict()
    for th in tr_list:
        th_info = th.xpath("./th/text()")
        td = th.xpath("./td")
        content_info = list()
        for p in td:
            p_info = p.xpath(" ./p/a/text() | ./p/text() | ./a/text() | ./text()")
            # print(p_info)
            # p_info[0] = p_info[0].replace('\r','').replace('\t','').replace('\n','').replace('\xa0','')
            # print(p_info[0])
            if len(p_info) > 1:
                p_info = p_info[1:2]
                # print(p_info)
            p_info[0] = p_info[0].replace('\r', '').replace('\t', '').replace('\n', '').replace('\xa0', '')
            content_info.append(p_info[0])
        # print(th_info)
        # print(content_info)
        for i in range(len(th_info)):
            # ALlinfo[th_info[i]] = content_info[i]
            info_list[th_info[i]] = content_info[i]
    info[name] = info_list
    return info


# 获取跨域通办信息
def getTrAsNameInfo(table, name):
    tr_list = table.xpath('./tbody/tr')
    name_list = tr_list[0].xpath('./th/div/text()')
    tr_list = tr_list[1:]
    # print(*tr_list[1])
    Info = dict()
    all_kytb_list = dict()
    num = 0
    for tr in tr_list:
        td_list = tr.xpath('./td/a/text() |./td/text() ')
        i = 0
        num += 1
        kytb_list = dict()
        for td in td_list:
            td = td.replace('\n', '').replace('\t', '').replace(' ', '')
            if td == '':
                continue
            kytb_list[name_list[i]] = td
            i += 1
        all_kytb_list[num] = kytb_list
        # print(all_kytb_list)
    # print(all_kytb_list)
    # ALlinfo["跨域通办"] = all_kytb_list
    Info[name] = all_kytb_list
    return Info


def getTheadAsNameInfo(table, name):
    info = dict()
    th_list = table.xpath('./thead/tr/th/div/text()')
    name_list = th_list
    tr_list = table.xpath('./tbody/tr')
    all_info_list = dict()
    num = 0
    for tr in tr_list:
        td_list = tr.xpath('./td/p/a/text() |./td/p/text() |./td/text()')
        i = 0
        num += 1
        info_list = dict()
        for td in td_list:
            td = td.replace('\n', '').replace('\t', '').replace(' ', '')
            if td == '':
                continue
            info_list[name_list[i]] = td
            i += 1
        all_info_list[num] = info_list
    info = all_info_list
    return info


def getSLTJinfo(slbz_info, name):
    info = dict()
    sltjInfo = slbz_info.xpath('./p/text()')
    s = ''
    for i in range(len(sltjInfo)):
        s += sltjInfo[i]
    info[name] = s
    return info


def getBLLCinfo(bllc_info):
    bllcinfo = dict()
    info = dict()
    div_list = bllc_info.xpath('./div[2]/div[2]/div')
    for div in div_list:
        a = div.xpath('./div/a/@data-attach')
        # a为lxml.etree._ElementUnicodeResult格式 转化为 list
        for item in a:
            item_json = json.loads(item)
        bllcinfo[item_json[0]["ATTACHNAME"].replace('.png', '')] = item_json[0]["FILEPATH"]
    info["办理流程"] = bllcinfo
    return info


def getZXJDinfo(zxjd_info, name_list):
    info = dict()
    i = 0
    div_list = zxjd_info.xpath('./div/div')
    for div in div_list:
        li_list = div.xpath('./ul/li')
        infolist = dict()
        for li in li_list:
            p = li.xpath('./p/text()')
            infolist[p[0]] = p[1]
            # print(infolist)
        info[name_list[i]] = infolist
        i += 1
    return info


def getPAsInfo(div):
    info = dict()
    name = div.xpath('./h2/text()')[0]
    # print(name)
    content = div.xpath('./p/text() | ./div/p/text()')
    for i in range(len(content)):
        content[i] = content[i].replace('\n', '').replace('\t', '')
    info[name] = content
    return info


def getflyjInfo(dom):
    info = dict()
    flyj_list = dict()
    tr_list = dom.xpath('//*[@id="tab3"]/div/table/tr')
    for tr in tr_list:
        name_list = tr.xpath('./th/text()')
        td_list = tr.xpath('./td/text() | ./td/a/text() | ./td/p/text()')
        if len(name_list) > 1:
            name = name_list[0]
            name_list = name_list[1:]
        flyj_list[name_list[0]] = td_list[0]
        info[name] = flyj_list
    return info


def parse_guide_detail(dom, ):
    # ALlinfo = dict()
    div_list = dom.xpath('//div[@class="matters-content-part"]')
    # 行政许可基本信息
    # print(div_list)
    # 行政基本信息
    admin_basic_info = div_list[0]
    # print(*admin_basic_info)
    basic_tr_list = admin_basic_info.xpath('./table/tbody/tr')
    table_list = admin_basic_info.xpath('./div/table')
    table_name = admin_basic_info.xpath('./div/h3/text()')
    print(table_list)
    # 基本信息
    basicInfo = getDictInfo(basic_tr_list, admin_basic_info.xpath('./h2/text()')[0])
    print("基本信息：", basicInfo)
    # 跨域通办
    kytbInfo = getTrAsNameInfo(table_list[0], table_name[0])
    print("跨域通办：", kytbInfo)
    # 审批信息
    spxxInfo = getDictInfo(table_list[1].xpath('./tbody/tr'), table_name[1])
    print("审批信息：", spxxInfo)
    # 审批结果
    spjgInfo = getTheadAsNameInfo(table_list[2], table_name[2])
    print("审批结果：", spjgInfo)
    # 编码代码
    bmdmInfo = getDictInfo(table_list[3].xpath('./tbody/tr'), table_name[3])
    print("编码代码：", bmdmInfo)
    # 特别程序
    tbcxInfo = getTrAsNameInfo(table_list[4], table_name[4])
    print("特别程序：", tbcxInfo)
    # 中介服务
    zjfwInfo = getTrAsNameInfo(table_list[5], table_name[5])
    print("中介服务：", zjfwInfo)
    # 其他信息
    qtxxInfo = getDictInfo(table_list[6].xpath('./tbody/tr'), table_name[6])
    print("其他信息：", qtxxInfo)

    # 受理标准
    slbz_info = div_list[1]
    # print(*slbz_info)
    # 受理范围
    slfwInfo = getDictInfo(slbz_info.xpath('./table/tbody/tr'), slbz_info.xpath('./h3/text()')[0])
    print("受理范围：", slfwInfo)
    # 受理条件
    sltjInfo = getSLTJinfo(slbz_info, slbz_info.xpath('./h3/text()')[1])
    print("受理条件：", sltjInfo)

    # 办理流程
    bllc_info = div_list[2]
    # print(*bllc_info)
    bllcInfo = getBLLCinfo(bllc_info)
    print("办理流程：", bllcInfo)

    # 申请材料
    sqcl_info = div_list[3]
    # print(*sqcl_info)
    table = sqcl_info.xpath('./div/div/div/table')[0]
    # print(type(table))
    sqclInfo = getTheadAsNameInfo(table, sqcl_info.xpath('./h2/text()'))
    print("申请材料：", sqclInfo)
    # 中介服务
    table = sqcl_info.xpath('./table')[0]
    name = sqcl_info.xpath('./h3/text()')[0]
    zjfwInfo = getTrAsNameInfo(table, name)
    print("中介服务：", zjfwInfo)

    # 咨询监督
    zxjd_info = div_list[4]
    name_list = zxjd_info.xpath('./div/div/h3/text()')
    # 咨询方式和监督投诉方式
    zxfsInfo = getZXJDinfo(zxjd_info, name_list)
    print("咨询方式和监督投诉方式：", zxfsInfo)

    # 窗口办理
    ckbl_info = div_list[5]
    ckblInfo = getPAsInfo(ckbl_info)
    print("窗口办理：", ckblInfo)

    # 收费项目信息
    sfxmxx_info = div_list[6]
    sfxmxxInfo = getPAsInfo(sfxmxx_info)
    print("收费项目信息：", sfxmxxInfo)

    # 法律依据
    flyj_info = div_list[7]
    # print(flyj_info.xpath('./div[2]/text()'))
    # print(tree.xpath('//*[@id="li_tab3"]/a/text()'))
    # print(tree.xpath('//*[@id="tab3"]/div/table/tr/th/text()'))
    flyjInfo = getflyjInfo(dom)
    print("法律依据：", flyjInfo)

    # 权力与义务
