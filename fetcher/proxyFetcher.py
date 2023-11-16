# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import re
import json
from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        for i in range(1,10):
            target_url = "https://www.zdaye.com/free/"+str(i)+"/"
            _tree = WebRequest().get(target_url).tree
            for tr in _tree.xpath("//table//tr"):
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port)
            sleep(5)

    @staticmethod
    def freeProxy02():
        """
        代理66 http://www.66ip.cn/
        """
        url = "http://www.66ip.cn/"
        resp = WebRequest().get(url, timeout=10).tree
        for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
            if i > 0:
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy03():
        """ 开心代理 """
        target_urls = ["http://www.kxdaili.com/dailiip.html", "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in target_urls:
            tree = WebRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy04():
        """ FreeProxyList https://www.freeproxylists.net/zh/ """
        url = "https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50"
        tree = WebRequest().get(url, verify=False).tree
        from urllib import parse

        def parse_ip(input_str):
            html_str = parse.unquote(input_str)
            ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', html_str)
            return ips[0] if ips else None

        for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
            ip = parse_ip("".join(tr.xpath('./td[1]/script/text()')).strip())
            port = "".join(tr.xpath('./td[2]/text()')).strip()
            if ip:
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=1):
        """ 快代理 https://www.kuaidaili.com """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy06():
        """ FateZero http://proxylist.fatezero.org/ """
        url = "http://proxylist.fatezero.org/proxy.list"
        try:
            resp_text = WebRequest().get(url).text
            for each in resp_text.split("\n"):
                json_info = json.loads(each)
                #if json_info.get("country") == "CN":
                    #yield "%s:%s" % (json_info.get("host", ""), json_info.get("port", ""))
                yield "%s:%s" % (json_info.get("host", ""), json_info.get("port", ""))
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy07():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        """ 小幻代理 """
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=1):
        """ 免费代理库 """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url, verify=False).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy10():
        """ 89免费代理 """
        r = WebRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            yield ':'.join(proxy)

    @staticmethod
    def freeProxy11():
        """ 稻壳代理 https://www.docip.net/ """
        r = WebRequest().get("https://www.docip.net/data/free.json", timeout=10)
        try:
            for each in r.json['data']:
                yield each['ip']
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy12():
        """
        PzzQz https://pzzqz.com/
        """
        from requests import Session
        from lxml import etree
        session = Session()
        try:
            index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
            x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
            if x_csrf_token:
                data = {"http": "on", "ping": "3000", "country": "cn", "ports": ""}
                proxy_resp = session.post("https://pzzqz.com/", verify=False,
                                          headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
                tree = etree.HTML(proxy_resp["proxy_html"])
                for tr in tree.xpath("//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()"))
                    port = "".join(tr.xpath("./td[2]/text()"))
                    yield "%s:%s" % (ip, port)
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy13():
        """
        墙外网站 cn-proxy
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy14():
        """
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
        request = WebRequest()
        import base64
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    @staticmethod
    def freeProxy15():
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy16():
        urls = [
            'http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&country=CN',
            'http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&country=',
            'http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&country=SG',
            'http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&country=US',
            'http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&country=CZ',
            'http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&country=AR',
        ]
        request = WebRequest()

        for url in urls:
            r = request.get(url, timeout=20)
            proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)', r.text)
            for proxy in proxies:
                yield proxy

    @staticmethod
    def freeProxy17():
        urls = [
            'https://openproxylist.xyz/http.txt',
            'http://pubproxy.com/api/proxy?limit=3&format=txt&http=true&type=https',
            'https://www.proxy-list.download/api/v1/get?type=https',
            'https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt'
        ]
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=20)
            for proxy in r.text.split('\n'):
                if proxy:
                    yield proxy
    @staticmethod
    def freeProxy18():
        """
        米扑代理 https://proxy.mimvp.com/
        :return:
        """
        url_list = [
            'https://proxy.mimvp.com/freeopen',
            'https://proxy.mimvp.com/freeopen?proxy=in_tp'
        ]
        port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                        'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                        'DgwODE': '8081', 'Dk5OTk': '9999'}
        for url in url_list:
            html_tree = WebRequest().get(url).tree
            for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
                try:
                    ip = ''.join(tr.xpath('./td[2]/text()'))
                    port_img = ''.join(tr.xpath('./td[3]/img/@src')).split("port=")[-1]
                    port = port_img_map.get(port_img[14:].replace('O0O', ''))
                    if port:
                        yield '%s:%s' % (ip, port)
                except Exception as e:
                    print(e)
    @staticmethod
    def freeProxy19():
        """
        神鸡代理 http://www.shenjidaili.com/
        :return:
        """
        url = "http://www.shenjidaili.com/product/open/"
        tree = WebRequest().get(url).tree
        for table in tree.xpath("//table[@class='table table-hover text-white text-center table-borderless']"):
            for tr in table.xpath("./tr")[1:]:
                proxy = ''.join(tr.xpath("./td[1]/text()"))
                yield proxy.strip()
                
    @staticmethod
    def freeProxy20(page=2):
        """
        极速代理 https://www.superfastip.com/
        :return:
        """
        url = "https://api.superfastip.com/ip/freeip?page={page}"
        for i in range(page):
            page_url = url.format(page=i + 1)
            try:
                resp_json = WebRequest().get(page_url).json
                for each in resp_json.get("freeips", []):
                    yield "%s:%s" % (each.get("ip", ""), each.get("port", ""))
            except Exception as e:
                print(e)
    @staticmethod
    def freeProxy21():
        """
        http://www.xiladaili.com/
        西拉代理
        :return:
        """
        urls = ['http://www.xiladaili.com/']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", r.text)
            for ip in ips:
                yield ip.strip()

if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy01():
        print(_)

##
