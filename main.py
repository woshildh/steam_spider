import requests
import bs4,time,re,chardet,random
import cookie,json,csv

cookies=cookie.get_cookie()
headers=cookie.headers

def get_id():
	with open("./data/game_id.csv","r",encoding="utf-8") as file:
		id_list=file.read().split("\n")
	id_list.remove("")
	return id_list

def get_info_page(id):
	url="http://store.steampowered.com/app/"+id+"/"
	while True:
		try:
			page=requests.get(url,headers=headers,cookies=cookies)
			return page.text
		except:
			time.sleep(40)
			continue


def get_review_page(id,num):
	url="http://store.steampowered.com/curators/ajaxgetcurators/render/?query=&start="+str(num)+"&count=10&filter=top_curators_reviewing&appid="+str(id)+"&new_browse=0"
	page=requests.get(url,headers=headers,cookies=cookies)
	#content=re.findall('results_html":"(.+?)"}',page.text)[0]
	content=json.loads(page.text)["results_html"]
	return content

def parse_review_page(id,text):
	'''
	解析鉴赏页面
	'''
	tree=bs4.BeautifulSoup(text,"lxml")

	all_review_info=tree.find_all("div",attrs={"class":"steam_curator_row_ctn"})
	if len(all_review_info)==0:  #表示这个游戏没有获取到鉴赏家评论
		return -1  
	all_reviews=[]

	for review_info in all_review_info:
		appid=id
		curator_id=review_info.find("a",attrs={"class":"steam_curator_row"}).get("data-clanid")
		curator_follower_num=review_info.find("div",attrs={"class":"num_followers"}).text.replace(",","")
		
		temp=review_info.find("div",attrs={"class":"recommendation_type_ctn"}).text
		#print(temp)
		if "Not" not in temp:
			rec=temp.split(" ")[0].strip()	
			date=temp.split(" ")[1].strip()
		else:
			rec=" ".join(temp.split(" ")[0:2]).strip()
			date=temp.split(" ")[2].strip()
		review=review_info.find("div",attrs={"class":"recommendation_desc"}).text.replace(",","，").replace("\n","")
		all_reviews.append([appid,curator_id,rec,date,curator_follower_num,review])
	return all_reviews
	#print([appid,curator_id,date,curator_follower_num,review])

def get_reviews(id):
	'''
	爬取这个游戏的所有评论
	'''
	num=0
	while True:
		print(num)
		page_text=get_review_page(id,num)

		info_list=parse_review_page(id,page_text)
		if info_list==-1:
			print(id,"爬完了...")
			return
		elif num==0:
			with open("./data/game_review_id.csv","a",encoding="utf-8") as file:
				file.write(id+"\n")
			with open("./data/comments.csv","a",encoding="utf-8") as file:
				for info in info_list:
					file.write("\n")
					file.write(",".join(info))
		else:
			with open("./data/comments.csv","a",encoding="utf-8") as file:
				for info in info_list:
					file.write("\n")
					file.write(",".join(info))
		num=num+10

def parse_info(id,text):
	"""
	解析游戏信息页面
	"""
	tree=bs4.BeautifulSoup(text,"lxml")
	text=tree.text
	try:
		appid=id
		name=tree.find("div",attrs={"class":"apphub_AppName"}).text
		#print(name)
		tag=re.findall("类型:(.+?)\n",text)[0].strip()
		#print(tag)
		try:
			developer=re.findall("开发商:\n\n(.+?)\n",text)[0].replace("\r","")
		except:
			developer=None
		print(developer)
		date=re.findall("发行日期:(.+?)\n",text)[0]
		print(date)
		try:
			price=re.findall("¥ (.+?)\n",text)[0].split("¥")[-1].strip()
		except:
			price=0
		#print(price)
		try:
			memory=re.findall("内存:(.+?)RAM",text)[0].strip()
		except:
			memory=None
		try:
			cpu=re.findall("处理器:(.+?)内存",text)[0].strip()
		except:
			cpu=None
		#print(cpu)
		
		try:
			curation_num=re.findall("\t(.+?)名鉴赏家",text)[0].strip().replace(",","")
		except:
			curation_num=0

		try:
			review_num=re.findall("\((.+?)篇评测",text)[0].replace(",","")
		except:
			review_num=0
	except:
		print(id,"爬取过程出错了")
		return -1
	return [appid,name,tag,developer,date,price,memory,cpu,curation_num,review_num]

def get_info(id):
	text=get_info_page(id)
	info_list=parse_info(id,text)
	print(info_list)
	if info_list!=-1:
		with open("./data/gameinfo.csv","a",newline="",encoding="utf-8") as file:
			writer=csv.writer(file)
			writer.writerow(info_list)
	else:
		with open("./data/error.csv","a",encoding="utf-8") as file:
			file.write(id)
	print(id,"信息收集完了..")

if __name__=="__main__":
	'''
	all_id_list=set(get_id())
	with open("./data/game_review_id.csv","r",encoding="utf-8") as file:
		finished=set(file.read().split("\n"))
	id_set=all_id_list-finished
	'''
	'''
	for i,id in enumerate(id_set):
		get_reviews(id)
		if i%40==0:
			time.sleep(3)
	'''
	
	with open("./data/game_review_id.csv","r",encoding="utf-8") as file:
		content=file.read()
	id_list=content.split("\n")
	if "" in id_list:
		id_list.remove("")
	with open("./data/finished_game_info.csv","r",encoding="utf-8") as file:
		content=file.read()

	finished_list=content.split("\n")
	if "" in finished_list:
		finished_list.remove("")
	
	id_set=set(id_list)-set(finished_list)
	print(len(id_set))
	
	
	for i,id in enumerate(id_set):
		get_info(id)
		time.sleep(random.randint(1,4))
		if i%20==0 and i!=0:
			time.sleep(random.randint(5,15))
	
