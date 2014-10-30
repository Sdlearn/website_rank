#encoding=utf-8

import urllib2
import sys
import re
import cookielib


class RankCrawler():
    def __init__(self, site):
        self.site = site.strip()
        cookiejar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        self.opener.addheaders = [('Referer', 'http://pr.chinaz.com/?PRAddress=' + site)]

    def get_html(self, url):
        for i in range(3):    # 3 times at most
            try:
                return self.opener.open(url).read().decode('utf-8')
            except Exception, e:
                print 'Exception in get_html: %s' % str(e)
        raise Exception('Fail to open url %s' % url)

    def get_rank(self, url, patten):
        html_doc = self.get_html(url)
        match = re.search(patten, html_doc)
        if match:
            rank = match.group(1)
        else:
            rank = 0
        return rank

    def run(self):
        try:
            html_doc = self.get_html('http://pr.chinaz.com/?PRAddress=' + self.site)
            google_url = re.search("ajaxget\('(.*?)','pr'\);", html_doc).group(1)
            sogou_url = re.search("ajaxget\('(.*?)','sougoupr'\);", html_doc).group(1)

            google_pr = self.get_rank('http://pr.chinaz.com/' + google_url, '/Rank_(\d).gif')
            print 'Google PR:\t %s' % google_pr

            sogou_pr = self.get_rank('http://pr.chinaz.com/' + sogou_url, '/sRank_(\d).gif')
            print 'Sogou PR:\t %s' % sogou_pr

            baidu_rank = self.get_rank('http://mytool.chinaz.com/baidusort.aspx?host=%s&sortType=0' % self.site,
                                  u'百度权重：<font color="blue">(\d)</font>')
            print 'Baidu Rank:\t %s' % baidu_rank

            alexa_rank = self.get_rank('http://alexa.chinaz.com/?domain=%s' % self.site,
                                  u'全球综合排名第 <b><font color="#FFFF00">(\d+)</font></b> 位，中文排名第')
            print 'Alexa Rank:\t %s' % alexa_rank
        except Exception, e:
            print 'Exception: %s' % str(e)


if len(sys.argv) == 1:
    print '%s www.site.com' % sys.argv[0]
    sys.exit(0)
else:
    RankCrawler(sys.argv[1]).run()