from lxml import html
import requests
import sqlite3
import bs4
from bs4 import BeautifulSoup as soup
import sqlite3
from urllib2 import urlopen as uReq
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def my_function():
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/', 
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/']

	for url in my_url:

		page = requests.get(url)
		tree = html.fromstring(page.content)


		#This will create master list containing SwellSize, SwellInterval, & Airtemp
		intervals = tree.xpath('//*[@class="nomargin font-sans-serif heavy"]/text()')
		#Navigating through master list, breaking down 3 data categories into variables
		swellsizeft = intervals[0::5]
		swellintervalsec = intervals[2::5]
		airtempdegrees = intervals[4::5]

		# Next we will need to iterate through our per category lists, and add to DB!

		# ['A', 'B', 'C', 'D']
		# ['Swell Size', 'Junk', 'SwellInterval', 'Junk', 'Airtemp']
		# ['  2', '  ', '  11', '  ', '38', ]

		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE IF NOT EXISTS SurfReport(ID INTEGER PRIMARY KEY, SwellSizeFt TEXT, SwellIntervalSec TEXT, AirTemp TEXT )')

		for x, y, z in zip(swellsizeft, swellintervalsec, airtempdegrees):
				conn = sqlite3.connect('SurfSend.db')
				cursor = conn.cursor()
				# cursor.execute("INSERT INTO SurfReport VALUES (?,?,?)", (x,y,z))
				cursor.execute("INSERT INTO SurfReport (SwellSizeFt, SwellIntervalSec, AirTemp) VALUES (?,?,?)", (x,y,z,))
				conn.commit()
				cursor.close()
				conn.close()


def my_function2():
	#list of URLs to scrape from
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/', 
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/']
	# opening up connecting, grabbing the page

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS WindInfo(ID INTEGER PRIMARY KEY, WindMPH TEXT)')

	#iterate over list of URLS
	for url in my_url:
		#initiating python's ability to parse URL
		uClient = uReq(url)
	# this will offload our content in'to a variable
		page_html = uClient.read()
	# closes our client
		uClient.close()

	# html parsing
		#beautifulsoup magic
		page_soup = soup(page_html, "html.parser")
		#variable for soon to be parsed page
		wind = page_soup.findAll('td', class_=re.compile("text-center table-forecast-wind td-nowrap"))
		#prints the list of URLs we scraped from

	# iterates over parsed HTML
		for w in wind:
			#wavesize
			wi = w.find('span', class_='stacked-text text-right')
			winb = wi.text.strip()

			conn = sqlite3.connect('SurfSend.db')
			cursor = conn.cursor()
			# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
			cursor.execute("INSERT INTO WindInfo (WindMPH) VALUES (?)", (winb,))
			conn.commit()
			cursor.close()
			conn.close()

def my_function3():
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/', 
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/']

	for url in my_url:

		r = requests.get(url)

		html = r.text

		soup = BeautifulSoup(html, 'lxml')

		# wind_directions = soup.find_all('td', {"class":"text-center last msw-js-tooltip td-square background-success"})

		wind_dir = soup.find_all(class_=re.compile('^text-center last msw-js-tooltip td-square background-'))  

		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE IF NOT EXISTS WindDirection(ID INTEGER PRIMARY KEY, WindDescription TEXT)')

		for w in wind_dir:

			windd = w['title']
			print(w['title'])


			conn = sqlite3.connect('SurfSend.db')
			cursor = conn.cursor()
			# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
			cursor.execute("INSERT INTO WindDirection (WindDescription) VALUES (?)", (windd,))
			conn.commit()
			cursor.close()
			conn.close()


def my_function4():

	url = 'https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/'

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS IDGrab(ID INTEGER PRIMARY KEY, WindDescription TEXT)')

	r = requests.get(url)

	html = r.text

	soup = BeautifulSoup(html, 'lxml')

	# wind_directions = soup.find_all('td', {"class":"text-center last msw-js-tooltip td-square background-success"})

	wind_dir = soup.find_all(class_=re.compile('^text-center last msw-js-tooltip td-square background-'))  

	for w in wind_dir:

		windd = w['title']
		print(w['title'])


		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
		cursor.execute("INSERT INTO IDGrab (WindDescription) VALUES (?)", (windd,))
		conn.commit()
		cursor.close()
		conn.close()




my_function()
my_function2()
my_function3()
my_function4()

	#Executing this script should give us 616 rows