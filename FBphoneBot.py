#!/usr/bin/env python
# -*- coding: utf-8 -*

import time, requests, sys
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')


def fb_login(user, passwd):
	driver = webdriver.Firefox()
	driver.get("https://www.facebook.com/login.php")
	driver.implicitly_wait(5)
	driver.find_element_by_xpath("//*[@name='email']").send_keys(user)
	driver.find_element_by_xpath("//*[@name='pass']").send_keys(passwd)
	driver.find_element_by_xpath("//*[@id='loginbutton']").click()
	time.sleep(3)
	return driver

def find_user(t):
	next=False
	url="https://www.facebook.com/search/people/?q="+t
	driver.get(url)
	time.sleep(5)
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	if soup.find("div",{"id":"empty_result_error"}):
		return driver, None
	div = soup.find("div",{"id":"contentArea"})
	if div != None:
		if "No hemos encontrado" in div.text and "resultado para" in div.text:
			return driver, None
		for a in div.findAll("a"):
			if next == True:
				break
			if a.get("href") == "#":
				next=True
	else:
		div = soup.find("div",{"id":"BrowseResultsContainer"})
		if "No hemos encontrado" in div.text and "resultado para" in div.text:
			return driver, None
		for a in div.findAll("a"):
			if next == True:
				break
			if a.get("href") == "#":
				next=True
	return driver, a.get("href")

def get_name(url_user):
	driver.get(url_user)
	time.sleep(2)
	soup = BeautifulSoup(driver.page_source, "html.parser")
	name = soup.find("span", {"id":"fb-timeline-cover-name"}).text
	return driver, name

def check_user(driver, phone):
	driver, url_user=find_user(phone)
	if url_user:
		return driver,True
	else:
		return driver,False

def menu():
	print """

______             _                 _            _                        _           _   
|  ___|           | |               | |          | |                      | |         | |  
| |_ __ _  ___ ___| |__   ___   ___ | | __  _ __ | |__   ___  _ __   ___  | |__   ___ | |_ 
|  _/ _` |/ __/ _ \ '_ \ / _ \ / _ \| |/ / | '_ \| '_ \ / _ \| '_ \ / _ \ | '_ \ / _ \| __|
| || (_| | (_|  __/ |_) | (_) | (_) |   <  | |_) | | | | (_) | | | |  __/ | |_) | (_) | |_ 
\_| \__,_|\___\___|_.__/ \___/ \___/|_|\_\ | .__/|_| |_|\___/|_| |_|\___| |_.__/ \___/ \__|
                                           | |                                             
                                           |_|                                             
-------------------------------------------------------------------------------------------
##### ##### ##### ##### AUTHOR QUANTIKA14 TEAM
###### ###### ###### ###### BLOG.QUANTIKA14.COM | github.com/Quantika14
####### ####### ####### ####### **FACEBOOK PHONE SEARCH AUTOMATIC BOT **
-------------------------------------------------------------------------------------------
"""
	print "***Default Directory log: log.txt***"

if __name__ == "__main__":
	menu()
	user = raw_input(str("Input Facebook user: "))
	passwd = raw_input(str("Input Facebook password: "))
	i = 1
	driver=fb_login(user, passwd)
	arch = open("log.txt","r")
	for line in arch.readlines():
		t=line.split("tlf:")[1].replace("\n","")
	arch.close()
	driver, bol=check_user(driver, t= int(t)+1)
	if bol:
		arch = open("log.txt","a")
		for a in range(20):
			t = int(t)+1
			t = str(t)
			driver, url_user=find_user(t)
			if url_user != None:
				driver, name = get_name(url_user)
				arch.write("url:"+url_user+"||name:"+name+"||phone:"+t+"\n")
			else:
				arch.write("url:None||name:None||phone:"+t+"\n")
				i+=1
				continue
			i+=1
	else:
		pass
	arch.close()
	driver.close()
