"""
网页下载器

为多线程准备的
"""
import traceback
from http.client import HTTPResponse
from urllib import request, parse

user_agent = ("Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / "
              "88.0.4321.0Safari / 537.36Edg / 88.0.702.0 ")
"""
用户代理设置
"""


def try_catch(cb):
    def wrapped_func(*args, **kw):
        for index in range(3):
            try:
                return cb(*args, **kw)
            except Exception as e:
                traceback.print_exc()
                continue
        return None

    return wrapped_func


@try_catch
def fetch_html(url, timeout: float = 5):
    req = request.Request(url)
    req.add_header("User-Agent", user_agent)
    res = request.urlopen(req, timeout=timeout)
    assert isinstance(res, HTTPResponse)
    html_doc = res.read()
    res.close()
    return html_doc


def build_post_body(query) -> bytes:
    post_body = parse.urlencode(query).encode('utf-8')
    return post_body


@try_catch
def fetch_json(url: str, post_body: bytes, refer: str, content_type: str):
    req = request.Request(url, post_body)
    req.add_header("User-Agent", ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                  " Chrome/87.0.4280.88 Safari/537.36"))
    req.add_header("Content-Type", content_type)
    req.add_header("Referer", refer)

    res = request.urlopen(req, timeout=5)
    assert isinstance(res, HTTPResponse)
    json_doc = res.read()
    res.close()
    return json_doc
