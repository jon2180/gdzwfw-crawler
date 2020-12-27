"""
url 管理器
"""


class URLManager:
    visited_addr = set()
    waiting_addr = set()

    def get_url(self):
        """
        从 waiting_addr 中获取一个 url
        并保证该 url 没有在 visited_url 中
        """
        if not self.waiting_addr:
            return None
        addr = self.waiting_addr.pop()
        if addr in self.visited_addr:
            return self.get_url()
        return addr

    def finished_parse_url(self, url):
        """
        表示已经完成了一个 url 解析
        将此 url 从 waiting_addr 中取出，并放入 visited_addr
        """
        # 表示此 url 已经解析完毕
        if url in self.visited_addr and url not in self.waiting_addr:
            return

        # step 1: 检查这个链接是否在 waiting_addr 中，如果是，移除
        if url in self.waiting_addr:
            self.waiting_addr.remove(url)

        # step 2: 添加进 visited_addr
        self.visited_addr.add(url)

    def push_url(self, url):
        """
        表示把此链接放入 waiting_addr 集合
        """

        # 如果此链接已经被处理
        if url in self.visited_addr and url not in self.waiting_addr:
            return

        # step 1: 检查这个链接是否在 visited_addr 中，如果是，移除
        if url in self.visited_addr:
            self.visited_addr.remove(url)

        # step 2: 添加进 visited_addr
        self.waiting_addr.add(url)
