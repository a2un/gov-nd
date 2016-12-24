import requests.exceptions
from urlparse import urlparse
from collections import deque 
import re
import csv
from bs4 import BeautifulSoup
import pdb
def clean_emails(str):
	re.sub('<*?>', '', str)

with open("ODlist.csv",'r') as csvfile:
	reader=csv.DictReader(csvfile)
	with open('email.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=' ',
		quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for row in reader:
			url =  (row['Website'])
			try:
				#url="https://www.linkedin.com/in/gauri-nigudkar-a946385"
				compare="http"
				if url.find(compare)==-1:
					url="http://"+url
				new_urls = deque([url])
				processed_urls = set()
				emails = set()  
				# print ' url from file: ', url
				while (len(new_urls))>0:
					#writer.write("\n")
					# print 'new: ', new_urls
					url = new_urls.popleft()
					processed_urls.add(url)
					# print 'processed url : ',processed_urls
					#print 'processed: ', processed_urls		
					#print processed_urls
					parts = urlparse(url)
					# print "parts: " ,parts
					base_url = "{0.scheme}://{0.netloc}".format(parts)
					# print "base_url: ",base_url
					path = url[:url.rfind('/')+1] if'/' in parts.path else url 
					# print "path: " ,path
					orig_url=base_url[7:]
					#print 'hey
					# print("Processing %s" %url)
					#processed_urls = []
					#print 'path ', path
					try:
						response = requests.get(path)
						#print response
					except requests.exceptions.RequestException as e:
						#parint e
						# print e
						pass
					# response.text=str(response.text)
					f = open('myfile','w')
					f.write(response.text.encode('utf8')) # python will convert \n to os.linesep
					f.close() # you can omit in most cases as the destructor will call it
					# print response.text
					new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\+-_]+[\.[a-z]+",response.text,re.I))
					#pdb.set_trace()
					#print response
					new_emails=str(new_emails)
					#new_emails = clean_emails(new_emails)
					if new_emails is not None:
						emails.update(new_emails)
					#print "no:" ,len(new_urls)
					soup =BeautifulSoup(response.text,"lxml")
					#print "soup: ",soup
					for anchor in soup.find_all("a"):
				 		link=anchor.attrs["href"] if "href" in anchor.attrs  else ''
					 	print "link: ",link
					 	print 'new_emails: ', new_emails
					 	if link.find(orig_url)!=-1 or link.find(".html")!=-1:	
					 		# print "yes"
					 		if link.startswith('/'):
					 			link = base_url + link
					 		elif not link.startswith('http'):
					 			link = path + link
					 		if not link in new_urls and not link in processed_urls :
					 			new_urls.append(link)
						#print 'email:' ,emails

						#print 'processed urls: ', processed_urls
						#print 'new_emails: ', new_emails
					#print 'emails: ' ,emails
					
					#clean_emails
				row_arr=[]
				if url is not None:
					row_arr.append(url)
				# for email in list(emails):
				# 	if emails is not None:
				# 		row_arr.append(email)
				print url, list(emails)
				row_arr.extend(list(emails))
				writer.writerow(row_arr)
			except requests.exceptions.ConnectionError:
				print 'Max retries exceeded with url ', url

