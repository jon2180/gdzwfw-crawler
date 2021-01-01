import json
from model import PowerAndResponsibility


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
            if len(p_info) > 0:
                for i in range(len(p_info)):
                    p_info[i] = p_info[i].replace('\r', '').replace('\t', '').replace('\n', '').replace('\xa0', '')
                deleteNullInList(p_info)
                if len(p_info) > 0:
                    content_info.append(p_info[0])
                else:
                    content_info.append('')
            else:
                content_info.append('')
            # p_info = p.xpath(" ./p/a/text() | ./p/text() | ./a/text() | ./text()")
            # if len(p_info) > 0:
            #     for i in range(len(p_info)):
            #         p_info[i] = p_info[i].replace('\r', '').replace('\t', '').replace('\n', '').replace('\xa0', '')
            #     deleteNullInList(p_info)
            #     content_info.append(p_info[0])
            # else:
            #     content_info.append('')
            # p_info = p.xpath(" ./p/a/text() | ./p/text() | ./a/text() | ./text()")
            # # print(p_info)
            # # p_info[0] = p_info[0].replace('\r','').replace('\t','').replace('\n','').replace('\xa0','')
            # # print(p_info[0])
            # if len(p_info) > 1:
            #     p_info = p_info[1:2]
            #     # print(p_info)
            # p_info[0] = p_info[0].replace('\r', '').replace('\t', '').replace('\n', '').replace('\xa0', '')
            # content_info.append(p_info[0])
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
            # TODO 减一缩进会报错
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
            if len(p) < 2:
                continue
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


# 消除list中\t和\n和' '
def deleteSlashTandNinList(lists):
    for i in range(len(lists)):
        lists[i] = lists[i].replace('\t', '').replace('\n', '').replace(' ', '')


# 消除list中的空值
def deleteNullInList(lists):
    i = 0
    while i < len(lists):
        if lists[i] == '':
            del lists[i]
            i -= 1
        i += 1


def getInfo(dom, s, div, par_model):
    if s == "基本信息":
        admin_basic_info = div
        basic_tr_list = admin_basic_info.xpath('./table/tbody/tr')
        table_list = admin_basic_info.xpath('./div/table')
        table_name_list = admin_basic_info.xpath('./div/h3/text()')
        # 基本信息
        basicInfo = getDictInfo(basic_tr_list, admin_basic_info.xpath('./h2/text()')[0])
        # print("基本信息：", basicInfo)
        for i in range(len(table_name_list)):
            for j in range(len(table_list)):
                if i == j:
                    if table_name_list[i] == "跨域通办":
                        # 跨域通办
                        kytbInfo = getTrAsNameInfo(table_list[i], table_name_list[j])
                        # print("跨域通办：", kytbInfo)
                    elif table_name_list[i] == "审批信息":
                        # 审批信息
                        spxxInfo = getDictInfo(table_list[i].xpath('./tbody/tr'), table_name_list[j])
                        # print("审批信息：", spxxInfo)
                    elif table_name_list[i] == "审批结果":
                        # 审批结果
                        spjgInfo = getTheadAsNameInfo(table_list[i], table_name_list[j])
                        # print("审批结果：", spjgInfo)
                    elif table_name_list[i] == "编码代码":
                        # 编码代码
                        bmdmInfo = getDictInfo(table_list[i].xpath('./tbody/tr'), table_name_list[j])
                        # print("编码代码：", bmdmInfo)
                    elif table_name_list[i] == "特别程序":
                        # 特别程序
                        tbcxInfo = getTrAsNameInfo(table_list[i], table_name_list[j])
                        # print("特别程序：", tbcxInfo)
                    elif table_name_list[i] == "中介服务":
                        # 中介服务
                        zjfwInfo = getTrAsNameInfo(table_list[i], table_name_list[j])
                        # print("中介服务：", zjfwInfo)
                    elif table_name_list[i] == "其他信息":
                        # 其他信息
                        qtxxInfo = getDictInfo(table_list[i].xpath('./tbody/tr'), table_name_list[j])
                        # print("其他信息：", qtxxInfo)
                    else:
                        print("basic info error!")
        basicInfo = basicInfo.get('基本信息', '无基本信息')
        # pk_region 区域 应该从前面json里取

        if basicInfo != '无基本信息':
            # 标题应该取前面一页取
            # par_model.title = basicInfo.get('事项名称','无')

            # par_model.publisher = basicInfo.get('实施主体','无')
            par_model.pk_org_name = basicInfo.get('实施主体', '') + basicInfo.get('审批部门', '') + basicInfo.get('实施机构',
                                                                                                          '') + basicInfo.get(
                '办理部门', '') + basicInfo.get('受理机构', '') + basicInfo.get('部门名称', '') + basicInfo.get('实施部门', '')
            # 发布者publisher和pk_org_name 行使主体  一致
            par_model.publisher = par_model.pk_org_name
            par_model.pk_mplementer_kind = basicInfo.get('实施主体性质', '') + basicInfo.get('主体性质', '')
            # pk_field 篇扩领域应该默认为空 而不应为事项类型
            # par_model.pk_field = basicInfo.get('事项类型','无')
            par_model.pk_commitment_time = basicInfo.get('承诺办结时限', '') + basicInfo.get('承诺办理时限', '') + basicInfo.get(
                '承诺时限', '') + basicInfo.get('承诺期限', '')
            par_model.pk_declare_type = basicInfo.get('办件类型', '') + basicInfo.get('办理类型', '') + basicInfo.get('办理类型',
                                                                                                              '事项类别')
            par_model.pk_legal_time = basicInfo.get('法定办结时限', '') + basicInfo.get('法定办理时限', '') + basicInfo.get('法定时限',
                                                                                                                '') + basicInfo.get(
                '法定期限', '')
            par_model.pk_presence_num = basicInfo.get('到办事现场次数', '') + basicInfo.get('到现场次数', '') + basicInfo.get(
                '到办理现场次数', '') + basicInfo.get('到现场窗口次数', '') + basicInfo.get('到现场办理的次数', '')
            # ?
            par_model.pk_item_type = basicInfo.get('事项类型', '') + basicInfo.get('权力类别', '') + basicInfo.get('事项性质',
                                                                                                           '') + basicInfo.get(
                '权力类型', '') + basicInfo.get('职权类型', '')
            par_model.pk_process_form = basicInfo.get('办理形式', '') + basicInfo.get('办理方式', '')
            par_model.pk_presence_reason = basicInfo.get('必须现场办理原因', '') + basicInfo.get('必须现场办理原因说明', '')
            par_model.pk_exercise_content = basicInfo.get('服务内容', '') + basicInfo.get('审批内容', '') + basicInfo.get(
                '行使内容', '') + basicInfo.get('处罚内容', '') + basicInfo.get('违法程度', '') + basicInfo.get('违法情节',
                                                                                                    '') + basicInfo.get(
                '处罚种类', '') + basicInfo.get('处罚裁量标准', '') + basicInfo.get('处罚的行为、种类、幅度', '') + basicInfo.get('征收类型',
                                                                                                             '') + basicInfo.get(
                '征收种类', '') + basicInfo.get('是否涉及征收(税)费减免的审批', '') + basicInfo.get('强制类型', '')
            par_model.pk_is_charge = basicInfo.get('是否收费', '') + basicInfo.get('许可收费', '') + basicInfo.get('审批收费',
                                                                                                           '') + basicInfo.get(
                '收费内容', '') + basicInfo.get('收费情况', '')
            par_model.pk_online_processing = basicInfo.get('是否网办', '') + basicInfo.get('是否可以在线申报', '')
            par_model.pk_online_processing_depth = basicInfo.get('网上办理深度', '') + basicInfo.get('网办深度', '')
            par_model.pk_online_payment = basicInfo.get('是否支持网上支付', '') + basicInfo.get('网上支付', '')
            par_model.pk_appointment = basicInfo.get('是否支持预约办理', '') + basicInfo.get('支持预约办理', '') + basicInfo.get(
                '是否支持网上预约办理', '') + basicInfo.get('预约办理', '')
            par_model.pk_logistics_express = basicInfo.get('是否支持物流快递', '') + basicInfo.get('支持物流快递',
                                                                                           '') + basicInfo.get(
                '是否支持结果快递', '') + basicInfo.get('是否物流', '') + basicInfo.get('物流快递', '')
        spxxInfo = spxxInfo.get('审批信息', '无审批信息')
        if spxxInfo != '无审批信息':
            par_model.pk_exe_level = spxxInfo.get('行使层级', '无')
            par_model.pk_item_source = spxxInfo.get('权力来源', '无')
            par_model.pk_approval_mode = spxxInfo.get('审批服务形式', '') + spxxInfo.get('审批模式', '')
            # par_model对象里差事项版本号
            par_model.pk_version = spxxInfo.get('事项版本号', '')
        kytbInfo = kytbInfo.get('跨域通办', '无跨域通办')
        if kytbInfo != '无跨域通办':
            for i in kytbInfo:
                tbqy = kytbInfo[i].get('通办区域', '')
                if tbqy == '':
                    continue
                if tbqy == '查看区域':
                    continue
                # 通办范围
                par_model.pk_operation_scope = tbqy
        # 审批结果名称
        par_model.pk_result_name = str(spjgInfo)
        # 篇扩结果样本 篇扩结果类型 篇扩结果领取方式 都无空 应该都是存在审批结果名称中

        zjfwInfo = zjfwInfo.get('中介服务', '无中介服务')
        if zjfwInfo != '无中介服务':
            par_model.pk_intermediary = str(zjfwInfo)
        else:
            par_model.pk_intermediary = ''

        tbcxInfo = tbcxInfo.get('特别程序', '无特别程序')
        if tbcxInfo == '无特别程序':
            par_model.pk_special_procedure = str(tbcxInfo)
        else:
            par_model.pk_special_procedure = ''
    elif s == "受理标准":
        # 受理标准
        slbz_info = div
        # print(*slbz_info)
        # 受理范围
        slfwInfo = getDictInfo(slbz_info.xpath('./table/tbody/tr'), slbz_info.xpath('./h3/text()')[0])
        # print("受理范围：", slfwInfo)
        # 受理条件
        sltjInfo = getSLTJinfo(slbz_info, slbz_info.xpath('./h3/text()')[1])
        # print("受理条件：", sltjInfo)
        slfwInfo = slfwInfo.get('受理范围', '无受理范围')
        if slfwInfo != '无受理范围':
            par_model.classify = slfwInfo.get('事项分类', '') + slfwInfo.get('办事主题', '') + slfwInfo.get('服务主题分类',
                                                                                                    '') + slfwInfo.get(
                '法人主题分类', '') + slfwInfo.get('自然人主题分类', '') + slfwInfo.get('面向法人事项主题分类', '') + slfwInfo.get(
                '面向自然人事项主题分类', '')
            par_model.pk_service_objects = slfwInfo.get('申请内容', '') + slfwInfo.get('适用范围', '') + slfwInfo.get('涉及的内容',
                                                                                                              '')
            par_model.pk_implementation_object = slfwInfo.get('服务对象', '') + slfwInfo.get('审批对象', '') + slfwInfo.get(
                '办理对象', '') + slfwInfo.get('申报对象', '') + slfwInfo.get('服务对象及领域', '')
        sltjInfo = sltjInfo.get('受理条件', '无受理条件')
        if sltjInfo != '无受理条件':
            par_model.pk_requirements = str(sltjInfo)
    elif s == "办理流程":
        # 办理流程
        bllc_info = div
        # print(*bllc_info)
        bllcInfo = getBLLCinfo(bllc_info)
        # print("办理流程：", bllcInfo)
        bllcInfo = bllcInfo.get('办理流程', '')

        par_model.pk_procedures = str(bllcInfo)
    elif s == "申请材料":
        # 申请材料
        sqcl_info = div
        # print(*sqcl_info)
        table = sqcl_info.xpath('./div/div/div/table')
        # print(type(table))
        if len(table) > 0:
            sqclInfo = getTheadAsNameInfo(table[0], sqcl_info.xpath('./h2/text()'))
            par_model.pk_materials = str(sqclInfo)
        # print("申请材料：", sqclInfo)
        else:
            par_model.pk_materials = ''

        # 中介服务
        table = sqcl_info.xpath('./table')[0]
        name = sqcl_info.xpath('./h3/text()')[0]
        zjfwInfo = getTrAsNameInfo(table, name)
        # print("中介服务：", zjfwInfo)
    elif s == "咨询监督":
        # 咨询监督
        zxjd_info = div
        name_list = zxjd_info.xpath('./div/div/h3/text()')
        # 咨询方式和监督投诉方式
        zxfsInfo = getZXJDinfo(zxjd_info, name_list)
        # print("咨询方式和监督投诉方式：", zxfsInfo)

        zxfs = str(zxfsInfo.get('咨询方式', '')) + str(zxfsInfo.get('咨询电话', '')) + str(zxfsInfo.get('联系电话', '')) + str(
            zxfsInfo.get('咨询联系电话', ''))
        par_model.pk_consultation_ways = str(zxfs)
        jdts = str(zxfsInfo.get('监督投诉方式', '')) + str(zxfsInfo.get('监督方式', '')) + str(zxfsInfo.get('投诉电话', '')) + str(
            zxfsInfo.get('投诉监督电话', '')) + str(zxfsInfo.get('监督电话', '')) + str(zxfsInfo.get('监督和投诉电话', '')) + str(
            zxfsInfo.get('监督投诉渠道', ''))
        par_model.pk_monitor_ways = str(jdts)

    elif s == "窗口办理":
        # 窗口办理
        ckbl_info = div
        ckblInfo = getPAsInfo(ckbl_info)
        # print("窗口办理：", ckblInfo)

        ckblInfo = ckblInfo.get('窗口办理', '')
        if len(ckblInfo) > 0:
            par_model.pk_process_time = ckblInfo[3]
            par_model.pk_process_place = ckblInfo[1]
        else:
            par_model.pk_process_time = ""
            par_model.pk_process_place = ""

    elif s == "收费项目信息":
        sfxmxx_info = div
        sfxmxxInfo = getPAsInfo(sfxmxx_info)
        # print("收费项目信息：", sfxmxxInfo)

        sfxmxxInfo = sfxmxxInfo.get('收费项目信息', '无收费项目信息')
        if sfxmxxInfo != '无收费项目信息':
            par_model.pk_charge_standard = str(sfxmxxInfo)
    elif s == "法律依据":
        flyjInfo = getflyjInfo(dom)
        # print("法律依据：", flyjInfo)
        par_model.pk_basis = str(flyjInfo)
    else:
        print("getInfo error")


def parse_guide_detail(dom, par_model: PowerAndResponsibility):
    div_list = dom.xpath('//div[@class="matters-content-part"]')

    for div in div_list:
        h2 = div.xpath('./h2/text() | ./div[1]/text()')
        # print(type(h2))
        deleteSlashTandNinList(h2)
        deleteNullInList(h2)
        if len(h2) > 0:
            getInfo(dom, h2[0], div, par_model)
