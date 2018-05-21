from bs4 import BeautifulSoup
import requests
import time,re

headers = {
'Host': 'http://store.steampowered.com/',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate',
'Referer': 'http://store.steampowered.com/',
'Connection': 'keep-alive',
 'Cache-Control': 'max-age=0',

}

def read_id(file_name):
	'''
	从gameid.csv中读取id并且生成集合
	'''
	file=open(file_name,"r",encoding='utf-8')
	id_list=file.read().split("\n")
	id_set=set(id_list)
	print("目前共有{}个游戏id".format(len(id_set)-1))
	return id_set

def get_id(id_set,csv_path,start_num=1,page_num=2):
	'''
	params:id_set用于去重,start_num指定开始的页数
	从服务器接口处获取html
	'''
	start_url="http://store.steampowered.com/search/results?category1=998&page="
	count=0
	for i in range(start_num,page_num):
		url=start_url+str(i)
		id_list=[]
		req=requests.get(url,headers=headers)
		if req.status_code==200:
			parser=BeautifulSoup(req.text,"lxml")
			game_list=parser.find_all("div",attrs={"class":"col search_capsule"})
			if len(game_list)==0:
				print("此时没有获取到数据...")
			for game in game_list:
				id=game.find("img").get("src").split("/")[5]
				if id not in id_set:
					id_list.append(id)
		else:
			assert ValueError("No response...")
		with open(csv_path,"a",encoding="utf-8") as file:
			for id in id_list:
				file.write(id+"\n")
				count+=1
		print("{} 次,共获取到{}条数据...".format(i,len(id_list)))
		time.sleep(2)
		if i % 20==0:
			time.sleep(10)
	print("此次数据爬完了,共有{}条数据".format(count))

if __name__=="__main__":
	id_set=read_id("./data/game_id.csv")
	get_id(id_set,"./data/game_id.csv",start_num=1,page_num=900)


