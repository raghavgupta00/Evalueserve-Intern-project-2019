# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:33:57 2019

@author: Raghav Gupta

A script to scrape the homepage of various universities stored in an 
excel file. The first non-advertised page is pulled and stored in a list, which
is then appended to the dataframe of the universities.

These will be used to eliminate duplicates (by comparing website
names).

BUGS: sometimes pulls up incorrect pages (mostly Wikipedia). This is mostly
a non-issue, because the first search result of two universities with very 
similar pages would most likely still be the same website.
"""

# Libraries required
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import time
import random

# Displaying all columns
pandas.set_option('display.max_columns', None)

# Reading excel file of list of universities
uni_list = pandas.read_excel("D:\\CS Projects\\Python\\Evalueserve " \
							 "Project\\LinkedIn URLs.xlsx")
# Creating copy of data frame to store URL
uni_url = pandas.DataFrame.copy(uni_list, deep = True)

# Getting index of first nan row in the URL column
num = 0
'''
for i in range(uni_url.shape[0]):
	if pandas.isna(uni_url.loc[i, "URL"]):
		num = i
		break
'''
# Initializing webdriver for chrome
chrome_driver = webdriver.Chrome(
		"D:\CS Projects\Chrome webdriver\chromedriver.exe")
'''
# For loop to create a list of university URLs
# Code using Google search. Not very reliable, because it detects bot 
# behaviour, despite usage of the sleep function
for i in range(num, uni_url.shape[0]): # uni_list.shape[0] gives number of rows
	# Text to insert in the google search bar 
	curr_search = uni_list.loc[i, "Institution"] + " " + \
	uni_list.loc[i, "Country"] + " homepage"
	# Using google's American website for better results
	# chrome_driver.get("https://www.google.com/?gl=us&hl=en&pws=0&gws_rd=cr")
	chrome_driver.get("https://www.google.com/")
	time.sleep(2)
	chrome_driver.find_element_by_xpath(
			'//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input'). \
			send_keys(curr_search)
	chrome_driver.find_element_by_xpath(
			'//*[@id="tsf"]/div[2]/div/div[3]/center/input[1]').click()
	soup = BeautifulSoup(chrome_driver.page_source, "lxml")
	uni_url.loc[i, "URL"] = soup.find("cite", {"class": "iUh30"}).text
	time.sleep(2)
	# Saving new dataset to excel file
	uni_url.to_excel("D:\\CS Projects\\Python\\Evalueserve Project\\" \
				  "duplicates.xlsx", index = False)  
'''

# Search using DuckDuckGo 
for i in range(num, uni_url.shape[0]): # uni_list.shape[0] gives number of rows
	# Text to insert in the google search bar 
	if "linkedin.com/school/" not in uni_url.loc[i, "URL"]:
		curr_search = uni_list.loc[i, "Institution"] + \
		" site:https://www.linkedin.com/school"
		# Using google's American website for better results
		chrome_driver.get("https://www.duckduckgo.com")
		chrome_driver.find_element_by_name("q").send_keys(curr_search)
		time.sleep(random.uniform(3, 6))
		chrome_driver.find_element_by_name("q").submit()
		soup = BeautifulSoup(chrome_driver.page_source, "lxml")
		uni_url.loc[i, "URL"] = soup.find(
		"span", {"class": "result__url__domain"}).text + soup.find(
		"span", {"class": "result__url__full"}).text
		# Saving new dataset to excel file
		time.sleep(random.uniform(3, 6))
		uni_url.to_excel("D:\\CS Projects\\Python\\Evalueserve Project\\" \
					  "LinkedIn URLs.xlsx", index = False)

'''
# Search using Bing
for i in range(num, uni_url.shape[0]): # uni_list.shape[0] gives number of rows
	# Text to insert in the google search bar 
	curr_search = uni_list.loc[i, "Institution"] + " homepage"
	# Using google's American website for better results
	chrome_driver.get("https://www.bing.com")
	chrome_driver.find_element_by_name("q").send_keys(curr_search)
	chrome_driver.find_element_by_name("q").submit()
	soup = BeautifulSoup(chrome_driver.page_source, "lxml")
	uni_url.loc[i, "URL"] = soup.find(
			"li", {"class": "b_algo"}).find("cite").text
	# Saving new dataset to excel file
	uni_url.to_excel("D:\\CS Projects\\Python\\Evalueserve Project\\" \
				  "duplicates.xlsx", index = False)  
'''   