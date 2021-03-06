class PowerAndResponsibility:
    libNum: 'str' = ''
    """
    资源库编号 统一 qzqdk
    """
    catalogId: 'str' = ''
    """
    目录编号：按目录设置逐级填写，如采集的是上海市商务委的权责清单，则目录编号为：地方政府-上海市-市级-上海市商务委。目录设置参照附件一《权责清单库目录设置》，导入系统时可自动按目录编号生成目录。
    """

    title: 'str' = ''
    """
    标题：提取该事项的名称。
    
    常见名称实例：职权名称;事项名称
    """

    issuedNum: 'str' = ''
    """
    颁布文号：不填。
    """

    publisher: 'str' = ''
    """
    发布者

    发布者：提取实施主体、实施部门等。与扩展属性“行使主体”内容一致。见附件二《权责清单属性设置》
    
    常见名称示例：实施主体;审批部门;实施机构;办理部门;受理机构;部门名称;实施部门
    """

    publishDate: 'str' = ''
    """
    发布日期
    
    提取网页上的发布日期或更新日期。若无填写采集日期
    
    类型：日期
    """

    belongDomain: 'str' = ''
    """
    归属领域
    
    归属领域：领域划分主要与机构或部门相对应，一般填二级领域，如采集的是上海市商务委的权责事项，则领域为“政府-商务”，见附件三《领域清单》。
    """

    genre: 'str' = ''
    """
    体裁
    
    体裁：统一填写“清单”。
    """

    source: 'str' = ''
    """
    来源
    
    ：填写来源网站名称，如“广东政务服务网”。
    """

    creatorName: 'str' = ''
    """
    创建人
    
    创建人名称：采集人员的名称。
    """

    classify: 'str' = ''
    """
    主题分类
    
    主题分类：提取事项分类、办事主题，见附件二《权责清单属性设置》。
    
    常见名称示例：事项分类;办事主题;服务主题分类;法人主题分类;自然人主题分类;面向法人事项主题;面向自然人事项主题
    """

    originalAddress: 'str' = ''
    """
    原文地址(应该为 url)
    
    原文地址：该事项的网址
    """

    htmlContent: 'str' = ''
    """
    html 内容
    
    长文本
    """

    # field: 'str' = ''
    # """
    # 领域
    # """
    #
    # industry: 'str' = ''
    # """
    # 行业
    # """
    #
    # fastTime: 'str' = ''
    # """
    # """
