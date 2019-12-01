# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 17:54:58 2019

@author: Sony
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pandas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

alumni_url = pandas.read_excel(
		'D:\\Computer Science\\Projects\\Evalueserve 2019\\' \
		'LinkedIn Scraping\\Alumni LinkedIn URLs.xlsx')       
        
'''
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('browser.privatebrowsing.autostart', True)
driver = webdriver.Firefox(
        firefox_profile = firefox_profile,
        executable_path = \
        'D:\\CS Projects\\Firefox webdriver\\geckodriver.exe')
'''

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
driver = webdriver.Chrome(
        options = chrome_options,
        executable_path = \
        'D:\\Computer Science\\Webdrivers\\chromedriver.exe')

driver.get("https://www.linkedin.com/uas/login")
driver.find_element_by_xpath('//*[@id="username"]').send_keys(
        '') # Enter username
driver.find_element_by_xpath('//*[@id="password"]').send_keys(
        '') # Enter password
driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/' \
                             'div[3]/button').click()

html1=list()
soup1=list()

uni_start = 0 # Start point
uni_end = 40 # End point

alumni_start = 0 # Alumni start point. 
# WARNING: If set to anything other than 0, make sure that difference 
# between uni_start and uni_end is 1 (i.e. only one university should be done)

for i in range(uni_start, uni_end):
    if (alumni_url.iloc[40, i] == 0) or \
	(alumni_url.iloc[0, i] == "Nothing Found"):
        uni_start = i
        break
	
for i in range(uni_start, uni_end):
    # Default value at end of range
	# alumni_url[alumni_url.columns[i]].count() - 1
    # Only change the end value of range when difference between uni_start and
    # uni_end is 1 (i.e. only one university should be done)
    for j in range(alumni_start,
				   alumni_url[alumni_url.columns[i]].count() - 1):
        k = alumni_url.iloc[j, i]
        # Enter any of your connection profile link 
        driver.get("{}".format(k)) 
        elm = driver.find_element_by_tag_name('html')
        elm.send_keys(Keys.HOME)
        time.sleep(5)
        elm.send_keys(Keys.END)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 10000000);")
        time.sleep(3)
        last_height = driver.execute_script(
                "return document.body.scrollHeight")
        time.sleep(3)
        driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-2000);")
        # Wait to load the page.           
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 10000000);")         
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 5000);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 10000000);") 
        time.sleep(3)   
        driver.execute_script("window.scrollTo(0, 5000);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 10000);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 2500);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(3)
        elements = \
        driver.find_elements_by_class_name(
                "pv-profile-section__card-action-bar pv-skills-" \
                "section__additional-skills artdeco-container-card-action-" \
                "bar artdeco-button artdeco-button--tertiary artdeco-" \
                "button--3 artdeco-button--fluid")
        for e in elements:
            e.click()
        html2 = driver.execute_script(
                "return document.documentElement.innerHTML;")
        html2 = str(html2)
        html1.append(html2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = str(soup)
        soup1.append(soup)

# htmlsoup=pd.DataFrame({'html1':html1,'soup1':soup1})
# htmlsoup.to_excel('C:\\Users\\dpksh\\Desktop\\Htmlandsoup.xlsx')
# soup1=pd.read_excel('C:\\Users\\dpksh\\Desktop\\Htmlandsoup.xlsx')
# soup1=soup1.loc[:,'soup1']
# soup1=list(soup1)

length = len(soup1)
num_uni = uni_start
count = 0
data_you_need = pandas.read_excel(
		'D:\\Computer Science\\Projects\\Evalueserve 2019\\' \
		'LinkedIn Scraping\\Alumni data.xlsx')
		 		      
for i in range(length):          
    university = list()
    country = list()
    name = list()
    company = list()
    location = list()
    experience = list()
    education = list()
    top3skills = list()
    allskills = list()
    soup = soup1[i]
    soup = BeautifulSoup(soup, 'lxml')
    # Name
    for table in soup.findAll('div', {'class' : 'flex-1 mr5'} ):
        links = table.findAll(
                'li', class_ = 'inline t-24 t-black t-normal break-words')   
    for i in links:
        name.append(i.text)
    n = pandas.DataFrame({'Name':name})
    # Institution   
    count += 1
    if alumni_url.iloc[0, num_uni] == "Nothing Found":
        count = 0
        num_uni += 1
    elif count <= (alumni_url[alumni_url.columns[num_uni]].count() - 1):
        alumni_url.iloc[40, num_uni] = count
        alumni_url.to_excel(
				'D:\\Computer Science\\Projects\\Evalueserve 2019\\' \
				'LinkedIn Scraping\\Alumni LinkedIn URLs.xlsx', index = False)
    elif count > (alumni_url[alumni_url.columns[num_uni]].count() - 1):
        count = 0  
        num_uni += 1
    university.append(alumni_url.columns[num_uni])
    u = pandas.DataFrame({'University' : university})   
    # Company
    for table in soup.findAll('div', {'class' : 'flex-1 mr5'}):
        links = table.findAll('h2',class_ = 'mt1 t-18 t-black t-normal')   
    for i in links:
        company.append(i.text)
    c = pandas.DataFrame({'Company' : company})
    # Location
    for table in soup.findAll('div', {'class' : 'flex-1 mr5'}):
        links = table.findAll('li', 
                              class_ = 't-16 t-black t-normal inline-block')   
    for i in links:
        location.append(i.text)
    l = pandas.DataFrame({'Location' : location})
    # Experience
    for table in soup.findAll('section',
                              {'class' : 'pv-profile-section experience-' \
          'section ember-view'}):
        links = table.findAll('div',
                              class_ = 'display-flex flex-column full-width')
    for i in links:
        experience.append(i.text)
    ex = pandas.DataFrame({'Experience' : experience})
    # Education
    for table in soup.findAll('section',
                              {'class' : 'pv-profile-section ' \
          'education-section ember-view'}):
                                          
        links = table.findAll('div',
                              class_ = 'pv-profile-section__sortable-' \
                              'card-item pv-education-entity pv-profile-' \
                              'section__card-item ember-view')
    for i in links:
        education.append(i.text)
    ed = pandas.DataFrame({'Education' : education})
    # Top 3 skills
    for table in soup.findAll('ol',
                              {'class':'pv-skill-categories-section__top-' \
          'skills pv-profile-section__section-info section-info pb1'}):
        links = table.findAll('span',
                              class_ = 'pv-skill-category-entity__name-text ' \
                              't-16 t-black t-bold')
    for i in links:
        top3skills.append(i.text)
    s1 = pandas.DataFrame({'Skills3' : top3skills})
    # All skills
    for table in soup.findAll('div',
                              {'class' : 'pv-skill-categories-' \
          'section__expanded'}):
        links = table.findAll('span',
                              class_ = 'pv-skill-category-entity__name-text ' \
                              't-16 t-black t-bold')
    for i in links:
        allskills.append(i.text)
    s2 = pandas.DataFrame({'Skillsall' : allskills})
    
    data = pandas.concat([u, n, c, l, ex, ed, s1, s2], axis=1)
    data_you_need = data_you_need.append(data, ignore_index = True)
    
data_you_need.to_excel(
		'D:\\Computer Science\\Projects\\Evalueserve 2019\\'
		'LinkedIn Scraping\\Alumni Data.xlsx', index = False)
		
