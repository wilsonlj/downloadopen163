# -*- coding: utf-8 -*-
import urllib2
import os
import string
import time
import platform
import multiprocessing

def download(fname, url):
	if os.path.exists(fname):
		print 'Exist',fname
		return
	error = 0
	while True and error < 3:
		try:
			print 'Downloading',fname
			start = time.time()
			content = urllib2.urlopen(url).read()
			f = open(fname, 'wb')
			f.write(content)
			f.close()
			end = time.time()
			size = float(os.path.getsize(fname)) / 1024.0 / 1024.0
			print 'Completed', fname, ' | Time: %.2f' %((end-start) / 60),'min Size: %.2f' %size,'MB Speed: %.2f' %(size / (end-start)),'MB/S'
			break
		except:
			print 'MP4 Error', fname, url
			if error == 2:
				ferror = open('Error.txt','a')
				ferror.write(fname + '\t' +url + '\n')
				ferror.close()
			error += 1

def analyze(url):
	system = platform.system()
	target = {}
	while True:
		try:
			web = urllib2.urlopen(url).read().decode('gbk','ignore').encode('utf-8').split('\n')
			break
		except:
			print 'Web Error'
	flag = 0
	num = 0
	for line in web:
		if flag == 1:
			lesson = line[line.find('>') + 1:line.rfind('<')]
			if system == 'Windows':
				lesson = lesson.decode('utf-8','ignore').encode('gbk')
			flag = 0
		if '<title>' in line:
			course = line[line.find('>') + 1:line.find('_')]
			if system == 'Windows':
				course = course.decode('utf-8','ignore').encode('gbk')
			try:
				os.mkdir(course)
			except:
				print 'Exist', course
			else:
				print course
			continue
		if '[第' in line:
			no = string.atoi(line[line.find('[') + 4:line.find(']') - 3])
			flag = 1
		if 'downbtn' in line:
			mp4 = line[line.find('http'):line.rfind('.mp4') + 4]
			if no > num:
				print no, lesson
				num = no
				fname = course + '/' + str(no) + '_' + lesson.replace("/", "_") + '.mp4'
				target[fname] = mp4
	print
	return target

if __name__ == '__main__':
	# Set Courses List
	'''
	lists = open('Catalog/计算机List.txt').read().split('\n')
	lists += open('Catalog/历史List.txt').read().split('\n')
	lists += open('Catalog/经济List.txt').read().split('\n')
	lists += open('Catalog/伦理List.txt').read().split('\n')
	lists += open('Catalog/心理List.txt').read().split('\n')
	lists += open('Catalog/哲学List.txt').read().split('\n')
	lists += open('Catalog/社会List.txt').read().split('\n')
	lists += open('Catalog/艺术List.txt').read().split('\n')
	lists += open('Catalog/演讲List.txt').read().split('\n')
	lists += open('Catalog/文学List.txt').read().split('\n')
	lists += open('Catalog/管理List.txt').read().split('\n')
	'''
	# lists = ['http://v.163.com/special/opencourse/cancerprevention.html']
	lists = open('Catalog/csList.txt').read().split('\n')

	#  Get Download URLs 
	targets = {}
	for line in lists:
		if len(line) == 0 or line[0] == "#":
			continue
		target = analyze(line)
		targets = dict(targets,**target)

	# Start Concurrent Download
	print
	print 'Download Start.'
	pool = multiprocessing.Pool(processes=10) # MultiProcessor
	for fname in targets:
		pool.apply_async(download,(fname,targets[fname],))
	pool.close()
	pool.join()
	print 'Download End.'