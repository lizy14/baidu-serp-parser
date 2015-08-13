import xml.dom.minidom
import http.client
import html
import urllib.parse
import sys
def BaiduSERP(keyword):
	conn = http.client.HTTPConnection("m.baidu.com")
	try:
		conn.request("GET", "/s?word="+keyword)
	except:
		print('Connection Failed')
		return
		
	resp = conn.getresponse()

	if resp.status==200:
		
		page = str(resp.read(), 'UTF-8')
		
		#xml规范化
		page=page.replace('<?xml version="1.0" encoding="utf-8"?>','')
		page=page.replace('<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">','')
		page=page.replace('&#160;','')
		page=page.replace('&nbsp;',': ')
		
		#去除附加格式
		page=page.replace('<em>','')
		page=page.replace('</em>','')
		
		dom=xml.dom.minidom.parseString(page).documentElement
		divs=dom.getElementsByTagName('div')

		def getInnerText(obj):
			if obj.nodeType==obj.TEXT_NODE :
				return html.unescape(obj.data)
			ret=""
			delim=" "
			if obj.tagName=='style':
				return ""		
			if (obj.tagName=='em'):
				delim=""
			elif (obj.tagName=='div'):
				delim="\n"
			else:
				delim=' '
			for child in obj.childNodes:
				ret=ret+getInnerText(child)
			return ret+delim

		for div in divs:
			if div.getAttribute('class')=='resitem':
				print(getInnerText(div))
				
	else:
		print('HTTP CODE '+resp.status+': '+resp.reason)
	conn.close()
def main():
	while True:
		keyword = urllib.parse.quote(input('keyword>'))
		BaiduSERP(keyword)
		if '-1' in sys.argv:
			break
main()