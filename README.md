# 爬虫程序 For [广东政务服务](https://www.gdzwfw.gov.cn/portal/affairs-public-duty-city?region=440000)

## 分层部分

- HTML/Json 下载器
    - html_downloader
- HTML/Json 解析器
    - html_parser
- URL 管理器 （为多线程、多进程准备的，目前用不着）
    - url_manager
- 爬虫派遣
    - gdzwfw_crawler
- 工具函数
    - api 用于包裹接口
    - excel_writer 输出 excel
    - config 配置
    - data_conversion 数据转化，把页面数据转化为表格需要的数据
- 模型
    - model/PowerAndResponsibility
    
## 对于 gdzwfw_crawler

总体分为三个页面

其中

- [目录页](https://www.gdzwfw.gov.cn/portal/affairs-public-duty-city?region=440000)
- [职权清单页](https://www.gdzwfw.gov.cn/portal/affairs-public-detail?qzqdCode=A924E8C8F3711194E0530C3D10ACF992&deptCode=007482575)
 
为纯 json 获取

第三个页面

- [具体办事指南](https://www.gdzwfw.gov.cn/portal/guide/11440100007482575H3440118009000)

为纯 html 解析

