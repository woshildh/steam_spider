import requests
import bs4
'''
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive',
 'Cache-Control': 'max-age=0',
}
'''
headers={"Accept": "text/html, application/xhtml+xml, image/jxr, */*",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
"Connection": "Keep-Alive",
"Host": "store.steampowered.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

def get_cookie():
	'''
	从cookie.txt里获取cookie
	'''
	content=open("./cookie.txt","r",encoding="utf-8").read()
	cookie=dict()
	content=content.split("\n")
	if "" in content:
		content.remove("")
	print(len(content))
	for c in content:
		x=c.split("=")
		cookie[x[0]]=x[1]
	return cookie

if __name__=="__main__":
	cookie=get_cookie()
	print(cookie)
