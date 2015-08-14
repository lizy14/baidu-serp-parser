import re
import http.client
import urllib.parse
import sys

def getBaiduSERP(keyword):
	conn = http.client.HTTPConnection("m.baidu.com")
	try:
		conn.request("GET","/s?word="+urllib.parse.quote(keyword))
	except:
		print('Connection Failed')
		conn.close()
		return ''
		
	resp = conn.getresponse()
	
	if resp.status==200:
		page = str(resp.read(), 'UTF-8')
		conn.close()
		return page
	else:
		print('HTTP CODE '+resp.status+': '+resp.reason)
		conn.close()
		return ''
	

def parseItem(item):
	
	site = (re.search('<span class="site" ?>(.*?)</span>', item))
	site = site.group(1) if site else ''
	date = (re.search('<span class="date" ?>(.*?)</span>', item))
	date = date.group(1) if date else ''
	title = (re.search('<a[^>]*>(.*?)</a>', item))
	title = title.group(1) if title else ''
	excerpt = (re.search('<div class="abs">(.*?)<span class="site" ?>', item))
	excerpt = excerpt.group(1) if excerpt else ''
	item_ = {'title': title, 'excerpt': excerpt, 'site': site, 'date': date}
	
	return item_
	
	
def parseBaiduSERP(page):
		
		results=[]
		
		try:
			match = re.search('<div class="reswrap">(.+)</div><div class="pagenav" >',page)
			items = match.group(1)
			match = re.findall('<div class="resitem"[^>]*?>(.+?</div>)</div>',items)
			for item in match:
				results.append(parseItem(item))
		except:
			print('Parse Error')
		
		return results
	
def main():
	
	while True:
		keyword = (input('keyword>'))
		
		results = parseBaiduSERP(getBaiduSERP(keyword))
		for result in results:
			print(result['title'])
			print(result['excerpt'])
			print(result['site']+' '+result['date'])
			print()
			
		if '-1' in sys.argv:
			break
main()