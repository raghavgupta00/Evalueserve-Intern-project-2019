# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 22:30:49 2019

@author: Sony
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import time

# Importing excel file of LinkedIn URLs of universities
uni_url = pandas.read_excel("D:\\CS Projects\\Python\\Evalueserve " \
							 "Project\\University LinkedIn URLs.xlsx")

# Creating copy of data frame to store URL
alumni_url = pandas.read_excel("D:\\CS Projects\\Python\\Evalueserve " \
								 "Project\\Alumni LinkedIn URLs.xlsx")

# Initializing Chrome webdriver
chromedriver = webdriver.Chrome("D:\\CS Projects\\Chrome webdriver\\" \
		 "chromedriver.exe")
   
# Going to LinkedIn login page
chromedriver.get("https://www.linkedin.com/uas/login")

# Sending username
chromedriver.find_element_by_xpath('//*[@id="username"]'). \
send_keys("") # Enter email/mobile number here

# Sending password
chromedriver.find_element_by_xpath('//*[@id="password"]'). \
send_keys("") # Enter password here

# Clicking the "sign in" button
chromedriver.find_element_by_xpath(
		'//*[@id="app__container"]/main/div/form/div[3]/button').click()

start = 0 # Start point 
end = alumni_url.shape[1] # End point
for i in range(start, end):
	if pandas.isna(alumni_url.iloc[0, i]):
		start = i
		break

for i in range(start, end):      	  	
	# Searching for Indian alumni of the university by going to alumni page 
	# By appending "people/?keywords=indian" to website's name
	time.sleep(5)
	chromedriver.get(uni_url.loc[i, "URL"] + "people/?keywords=indian")  
	# Scrolling to get enough alumni names
	# The sleep function is to give time for loading more names
	while True:
		temp_soup = BeautifulSoup(chromedriver.page_source, "lxml")
		for j in range(5): 
			chromedriver.execute_script("window.scrollTo(0, 10000000);")
			time.sleep(5)
			
		alumni_soup = BeautifulSoup(chromedriver.page_source, "lxml")
		main_page = alumni_soup.find(
				"main", {"class": "org-grid__core-rail--wide"})
		alumni_names = main_page.find(
				"div", {"class": "org-people-profiles-module ember-view"})		
		alumni_list = list()
		for links in alumni_names.find_all(
				"a", {"data-control-name": "people_profile_card_image_link"}):
			alumni_list.append("https://www.linkedin.com" + links["href"])
			if len(alumni_list) >= 40:
				break
		if len(alumni_list) >= 40:
			break
		if temp_soup.text == alumni_soup.text:
			break
	alumni_url[alumni_url.columns[i]] = pandas.Series(alumni_list)
	if alumni_url[alumni_url.columns[i]].count() == 0:
		alumni_url.iloc[0, i] = "Nothing Found"
	# Save the data in the SAME excel file
	alumni_url.to_excel(
			"D:\\CS Projects\\Python\\Evalueserve Project\\Alumni " \
			"LinkedIn URLs.xlsx", 
			index = False)