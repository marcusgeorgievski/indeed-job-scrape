#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Indeed web scraper

Tools: Python, Selenium, BeautifulSoup, pandas, matplotlib

Created on Sat Apr 24 2021
@author: Marcus Georgievski
"""
from selenium import webdriver
# next two lines are for use in jupyter if youd like
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import scrape

def main(job, skill_search, pages, my_skills):
	'''
	Main function.
	
	Parameters:
		job (str):The job to search for on Indeed.
		skill_search (bool):The condition to search for skills or not (takes longer).
		pages (int):Number of Indeed pages to search (~14 listings per page)
		my_skills (list[str]):List of skills to search for, Strings
	
	Variables:
		driver (obj):Web automation
		location (str):DO NOT USE, location to search for
		
		jobs -> skills (lists):Lists to store listing data
		
		listings (list):List of div's for each job listing on current page
		
		*Unlisted vars are mostly Selenium vars for automation, explained in comments
		
	Functions:
		scrape.py (module):Contains all functions
	
	Returns/Prints/Creates:
		df (DataFrame):DataFrame for all data.   
		fig (obj):Skills graph
		'''
		
	# Initiate ChromeDriver and open page
	driver = webdriver.Chrome('/Users/marcus/Desktop/indeed-data-scrape/chromedriver') # change according to your machine
	URL = 'https://ca.indeed.com/' # may need changing depending on country
	# The following commented line can be use for Jupyer 
	# driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get(URL)
	
	# Search data
	location = '' # ! LEAVE BLANK FOR NOW !, location to search, this autfofills and .clear() does not seem to work

	# Get search bars
	job_search = driver.find_element_by_id('text-input-what')
	location_search = driver.find_element_by_id('text-input-where')
	
	# Search bars input
	job_search.send_keys(job)
	location_search.send_keys(location)
	
	# Click submit button
	search_button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
	search_button.click()
	
	# Lists of data to store
	jobs = []
	salaries = []
	companies = []
	locations = []
	ratings = []
	links0 = [] # list of links based on search condition, copy of one of the following:
	links1 = [] # used when skill_search == False
	links2 = [] # used when skill_search == True
	skills = []
	descriptions = []

	# Data retrieval
	for page in range(pages): # loop for each page

		# Parse 
		soup = BeautifulSoup(driver.page_source, 'html.parser') # current page parse
		listings = soup.find_all('div',{'class':'jobsearch-SerpJobCard unifiedRow row result clickcard'}) # listings parse

		# Data for each listing
		for li in listings:
				
			# If skil_search: this function opens the listing page, checks and saves description and skills
			sks = ''
			desc = ''
			if skill_search:
				sks, desc = scrape.get_skills_and_desc(scrape.get_link(li,URL), sks, desc, links2, my_skills, driver)


			# All data appended to list for each listing
			jobs.append(scrape.get_job(li)) 
			salaries.append(scrape.get_salary(li))
			companies.append(scrape.get_company(li))
			locations.append(scrape.get_location(li))
			ratings.append(scrape.get_rating(li))
			links1.append(scrape.get_link(li,URL))
			skills.append(sks)
			descriptions.append(desc)

			# Which links list is used
			if skill_search:
				links0 = links2.copy()
			else:
				links0 = links1.copy()
			
			# DataFrame 
			df = scrape.create_dataframe(jobs,companies,locations,skills,salaries,ratings,links0,descriptions)
			
		# This selects the next page, breaks if link is not present/no more pages
		try:
			link = URL+soup.find('ul',{'class':'pagination-list'}).find_all('li')[-1].find('a').get("href")
		except:
			break
			
		# Opens next page
		driver.get(link) 
		sleep(1) 


	driver.quit() # Exits webpage

	if skill_search:
		scrape.graph(my_skills, df)
	
	
	
datasci_skills = ['python', 'SQL', 'tensorflow','sci-kit','pyTorch','aws','azure','artificial intelligence', ' AI ',
			 'machine learning','deep learning', 'neural network', 'bachelor','masters','phd',
			 'statistic','math'] 

sofdev_skills = ['HTML','CSS','JavaScript','React','angular','mongoDB','SQL','Python','AWS','Azure','bachelor',
				'masters','statistic','math','artificial intelligence']

main('Data Science', True, 1, datasci_skills)
