import urllib2
import cookielib

cookie = cookielib.CookieJar()  # 声明CookieJar对象实例来保存cookie
# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)  # 通过handler构建opener
opener.open(r'http://online.hhgrace.com')
for item in cookie:
    print(item)
