import requests
from lxml import etree
import re
import os
import openpyxl

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

id = 0
belongDomainList = "外交|国防|发展和改革|教育|科学技术|工业和信息化|民族事务|公安|国家安全|民政|司法|财政|人力资源和社会保障|自然资源|生态环境|住房和城乡建设|交通运输|水利|农业农村|商务|文化和旅游|卫生健康|退役军人事务|应急管理|人民银行|审计|国有资产监督管理|海关|税务|市场监督管理|广播电视|体育|统计|国际发展合作|医疗保障|参事|国家机关事务管理|港澳事务|研究|新华通讯|科学|社会科学|工程|发展研究|广播电视|气象|银行保险监督管理|证券监督管理|信访|粮食和物资储备|能源|国防科技工业|烟草专卖|移民|林业和草原|铁路|民用航空|邮政|文物|中医药管理|煤矿安全监察|外汇管理|药品监督管理|知识产权"


def GetWeb(url, params):
    page = requests.get(url=url, params=params, headers=headers)
    return page


def PostWeb(url, data):
    page = requests.post(url=url, data=data, headers=headers)
    return page


def GetUrlFromXpath(page_text, xpath):
    tree = etree.HTML(page_text)
    url = tree.xpath(xpath)[0]
    url = "https:" + url
    return url


def SelectCityAndGetOrgareaCode(url, data, int):
    page_json = PostWeb(url, data).json()
    orgareaCode = page_json["data"]["data"]["city"][int]["ORGAREACODE"]
    print(page_json["data"]["data"]["city"][int]["ORGNAME"])
    return orgareaCode


def GetAllPage(totalNum, pageSize):
    if totalNum % pageSize > 0:
        totalPage = totalNum // pageSize + 2
    else:
        totalPage = totalNum // pageSize + 1
    return totalPage


def SelectCountryAndGetOrgareaCode(url, data, int):
    page_json = PostWeb(url, data).json()
    orgareaCode = page_json["data"]["data"]["country"][int]["ORGAREACODE"]
    print(page_json["data"]["data"]["country"][int]["ORGSNAME"])
    return orgareaCode


def timestampToTime(time):
    t = time.localtime(time)
    strTime = time.strftime("%Y%m/%d %H:%M:%S", t)
    return strTime


def getAllCityInfo(url, data):
    page_json = PostWeb(url, data).json()
    return page_json["data"]["data"]["city"]


def chooseOneCity(allCityInfo, str):
    l = len(allCityInfo)
    # print(l)
    for n in range(0, l):
        if allCityInfo[n]["ORGNAME"] == str:
            return allCityInfo[n]
    print("city name err")


def getAllCountryInfoByCity(url, data, city):
    page_json = PostWeb(url, data).json()
    return page_json["data"]["data"]["country"]


def getCountryPageInfo(url, data):
    page_json = PostWeb(url, data).json()
    return page_json["data"]["custom"]["PAGEINFO"]


def getAllDepartment(url, data):
    page_json = PostWeb(url, data).json()
    return page_json["data"]["data"]["department"]


def getPowerResponsibilityList(url, data):
    page_json = PostWeb(url, data).json()
    return page_json["data"]["custom"]["PowerandresponsibilityList"]


def getInplementListInfo(url, data):
    page_json = PostWeb(url, data).json()
    return page_json["data"]["CUSTOM"]["PAGEINFO"]


def getAUDIT_ITEMLIST(url, data):
    page_json = PostWeb(url, data).json()
    return page_json["data"]["CUSTOM"]["AUDIT_ITEMLIST"]


def getPublishTime(url, data):
    page_json = PostWeb(url, data).josn()
    return page_json["data"]["serverTime"]


def getbelongDomain(str):
    result = re.findall(belongDomainList, str)
    l = len(result)
    if l == 0:
        return ""
    else:
        return "政府-" + result[0]


def file_is_exit(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        print("创建成功:", dirs)
    else:
        print("已存在：", dirs)


def excel_is_exit(city, country):
    dirs = city + "/" + city + "-" + country + ".xlsx"
    if not os.path.exists(dirs):
        book = openpyxl.Workbook()
        sh = book.active
        sh.title = city + "-" + country
        book.save(dirs)
        print("创建成功：", dirs)
    else:
        print("已存在:", dirs)
