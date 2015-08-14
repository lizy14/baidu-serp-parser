import re
import http.client
import urllib.parse
import sys
from html import unescape

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
	
def parseHTML(html):
	html=html.replace('&#160;',' ')
	html=unescape(html)
	
	html=re.sub('<style[^>]*>[^>]*</style>','',html)
	html=re.sub('<br ?/?>','\n',html)
	html=re.sub('</p>','\n',html)
	html=re.sub('</?\w+[^>]*>','',html)

	html=html.strip()
	return html
	
def parseItem(item):
	
	title = (re.search('<a[^>]*>(.*?)</a>', item))
	title = parseHTML(title.group(1)) if title else ''
	content = (re.search('<div class="abs">(.*)</div>', item))
	content = parseHTML(content.group(1)) if content else ''
	
	site = (re.search('<span class="site" ?>(.*?)</span>', item))
	site = (site.group(1)) if site else ''
	date = (re.search('<span class="date" ?>(.*?)</span>', item))
	date = (date.group(1)) if date else ''
	excerpt = (re.search('<div class="abs">(.*?)<span class="site" ?>', item))
	
	content = parseHTML(excerpt.group(1)) if excerpt else content
	
	item_ = {'title': title, 'content': content, 'site': site, 'date': date}
	
	return item_
	
	
def parseBaiduSERP(page):
		
		results=[]
		
		try:
			match = re.search('<div class="reswrap">(.+)</div><div class="pagenav" >',page)
			items = match.group(1)
			match = re.findall('<div class="resitem"[^>]*?>(.+?</div>)</div>',items)
		except:
			print('Parse Error')
			
		for item in match:
			results.append(parseItem(item))

		
		return results

def outputFilter(text):
	#handle UnicodeEncodeError
	return  text.encode('GBK', 'ignore').decode('GBK')
	
def getKeywordFromArgv():
	flag=False
	for arg in sys.argv:
		if flag:
			return arg
		if arg in ['-k', '-keyword']:
			flag=True
	return None
	
def main():
	
	while True:
		keywordFromArgv = getKeywordFromArgv()
		if keywordFromArgv:
			keyword = keywordFromArgv
		else:
			keyword = (input('keyword>'))
		
		results = parseBaiduSERP(getBaiduSERP(keyword))
		for result in results:
			print(outputFilter(result['title']))
			print(outputFilter(result['content']))
			if result['site'] or result['date']:
				print(outputFilter(result['site']+', '+result['date']))
			print()
			
		if '-1' in sys.argv or keywordFromArgv:
			break
main()