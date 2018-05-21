#!/usr/bin/env Python
# coding=utf-8
import requests
import bs4
import csv

csvReader=csv.reader(open("./data/comments.csv","r",encoding="gbk"))
i=0
id_dict={}
print(len(id_dict))
for line in csvReader:
	if i==0:
		i=1
		continue
	curator_id=line[1]
	if curator_id in id_dict.keys():
		num=id_dict[curator_id]
	else:
		url="http://store.steampowered.com/curator/"+curator_id
		page=requests.get(url).text
		tree=bs4.BeautifulSoup(page,"lxml")
		try:
			num=tree.find(name="span",attrs={"id":"Recommendations_total"}).text.replace(",","").strip()
		except:
			num="None"
		id_dict[curator_id]=num
	with open("review_num.csv","a",encoding="utf-8") as file:
		file.write(",".join([curator_id,num]))
		file.write("\n")
		print(curator_id,num)

