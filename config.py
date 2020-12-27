"""
配置文件，存放一般不会改变的内容
"""
import os

# initial_url = "https://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region=440000&deptCode=MB2D0164X"
initial_url = "https://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region=440000&deptCode=006940386"
"""
初始链接：获取内容为 广东省政务服务网 -> 政务公开 -> 省级权责清单（按部门） -> 省中医药局 、 省医保局
"""

user_agent = ("Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / "
              "88.0.4321.0Safari / 537.36Edg / 88.0.702.0 ")
"""
用户代理设置
"""

download_dir = os.path.split(os.path.realpath(__file__))[0]
# download_dir = os.path.join(os.getcwd(), "downloads")
"""
下载路径
"""

fetch_timeout = 1000
"""
下载超时
"""
