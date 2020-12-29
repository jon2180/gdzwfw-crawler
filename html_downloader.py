"""
网页下载器

为多线程准备的
"""
import socket
import traceback
from http.client import HTTPResponse
from urllib import request, parse, error

from config import user_agent


def try_catch(cb):
    def wrapped_func(*args, **kw):
        try:
            data = cb(*args, **kw)
            return data
        except error.ContentTooShortError as e:
            # print(f'{args}: [ContentTooShort] download failed\n{e.reason}')
            traceback.print_exc()
            print('\n')
            return cb(*args, **kw)
        except error.HTTPError as e:
            # print(f'{url}: [HttpError] download failed\n{e.reason}')
            traceback.print_exc()
            print('\n')
            return cb(*args, **kw)
            # return fetch_html(url)
        except socket.timeout as e:
            # print(f'{url}: [SocketTimeout] download failed\n')
            traceback.print_exc()
            print('\n')
            return cb(*args, **kw)
            # return fetch_html(url)
        except error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                # print('socket timed out - URL %s', url)
                return cb(*args, **kw)
                # return fetch_html(url)
            else:
                print('some other error happened')
                # print(f'{url}: [URLError] download failed\n{e.reason}')
                traceback.print_exc()
                print('\n')
                return cb(*args, **kw)
                # return fetch_html(url)
        except Exception as e:
            # print(f'{url}: download failed\n')
            traceback.print_exc()
            print('\n')
            return None

    return wrapped_func


@try_catch
def fetch_html(url, timeout: float = 60):
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

    res = request.urlopen(req, timeout=60)
    assert isinstance(res, HTTPResponse)
    json_doc = res.read()
    res.close()
    return json_doc
