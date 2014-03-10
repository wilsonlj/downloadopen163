# -*- coding: utf-8 -*-
import urllib
import urllib2
import string

def checkLesson(url):
	try:
		web = urllib2.urlopen(url).read().decode('gbk','ignore').encode('utf-8').split('\n')
	except:
		print 'Check Error',url
		return 0
	count = 0
	for line in web:
		if '.mp4' in line:
			count += 1
			if count >= 2:
				return 2
	if count == 1:
		return 1
	return 0

def generateList(url):
	category = urllib.unquote(url[url.find('pl2') + 4:url.find('/default/fc')]).decode('gbk','ignore').encode('utf-8')
	if category == 'default':
		category = '全部'
	print category
	dic = {}
	
	page = 1
	url = url[:url.rfind('1.html')]
	while True:
		cURL = url + str(page) + '.html'
		try:
			web = urllib2.urlopen(cURL).read().decode('gbk','ignore').encode('utf-8').split('\n')
		except:
			print 'Web Error', cURL
			continue
		count = 0
		flag = 0
		for line in web:
			if flag == 1:
				lesson = line[line.find('>') + 1:line.rfind('<')]
				address = line[line.find('\"') + 1:line.find('\" target')]
				dic[lesson] = address
				flag = 0
			if 'contentArea-resultList-title cBlue' in line:
				count += 1
				flag = 1
		if count == 0:
			break
		else:
			page += 1
	
	fList = open(category + 'List.txt','w')
	fSpec= open(category + 'Spec.txt','w')
	fAll = open(category + 'All.txt','w')
	for lesson in dic:
		fAll.write('# ' + lesson + '\n')
		flag = checkLesson(dic[lesson])
		if flag == 0:
			fAll.write('# ')
		elif flag == 2:
			fList.write('# ' + lesson + '\n')
			fList.write(dic[lesson] + '\n')
		else:
			fSpec.write('# ' + lesson + '\n')
			fSpec.write(dic[lesson] + '\n')
		fAll.write(dic[lesson] + '\n')
	fSpec.close()
	fList.close()
	fAll.close()
	
	return

if __name__ == '__main__':
	
	generateList('http://so.open.163.com/movie/listpage/listprogram1/pl2/default/default/fc/ot/default/1.html')
	generateList('http://so.open.163.com/movie/listpage/listprogram1/pl2/%D5%DC%D1%A7/default/fc/ot/default/1.html')
	generateList('http://so.open.163.com/movie/listpage/listprogram1/pl2/TED/default/fc/ot/default/1.html')
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%CA%FD%D1%A7/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%D0%C4%C0%ED/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%D2%D5%CA%F5/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%BC%C6%CB%E3%BB%FA/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%C0%FA%CA%B7/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%CE%C4%D1%A7/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%C2%D7%C0%ED/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%C9%E7%BB%E1/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%B9%DC%C0%ED/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%B7%A8%C2%C9/default/fc/ot/default/1.html")	
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%BE%AD%BC%C3/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%D1%DD%BD%B2/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%D2%BD%D1%A7/default/fc/ot/default/1.html")
	generateList("http://so.open.163.com/movie/listpage/listprogram1/pl2/%BC%BC%C4%DC/default/fc/ot/default/1.html")
		
	print 'List Done'