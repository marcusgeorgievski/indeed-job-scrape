"""
Simple Indeed web scraper module

Tools: Python, Selenium, BeautifulSoup, pandas, matplotlib

Created on Fri, May 7 2021
@author: Marcus Georgievski
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def clean(text):
	'''
	Returns the edited String.

	Parameters:
		text (str):The string which is to be edited.

	Returns:
		text(str):The string which is edited.   
	'''
	# \n seems to be present in many Strings, this function fixes that
	if '\n' in text:
		text = text.replace('\n','')
		return text


def graph(my_skills, df):
	'''
	Returns Matplotlib graph.

	Parameters:
		skill_search (boolean):Condtion to search skills.
		my_skills (list):List of skills to search.
		df (DataFrame):All listing data.
		
	Variables:
		ds (dict):Skill data sorted
		n (list):Skills
		o (int):Occurences

	Returns:
		figure (obj):Skills graph
		'''
	d = {i:0 for i in my_skills} # initialized skill dict
	
	# Pairs skill with num of occurences, does so my search 'skills' DataFrame column
	for i in range(len(df)):
		for skill in my_skills:
			if skill in df.iloc[i]['Skills']:
				d[skill] += 1

	# Sorts dict, stores values and keys in seperate lists
	ds = {k: v for k, v in (sorted(d.items(), key=lambda item: item[1]))}
	n = list(ds.keys())
	o = list(ds.values())
	
	# graph
	plt.rcParams.update({'font.size': 10}) # font size is low to fit long skill lists
	plt.figure(figsize=(20,5))
	plt.barh(n,o)
	plt.ylabel('Skill')
	plt.xlabel('Number of jobs mentioned in')
	plt.title('Skill Mentions')
	
	for index, value in enumerate(o):
		plt.text(value, index, str(value)) # plot value for each bar

	plt.savefig('skill_graph') # saves graph
	plt.show() # displays fig


def get_skills_and_desc(lk,sks, desc, links2, my_skills,driver):
	driver.get(lk) # opens page
	links2.append(driver.current_url) # appends links of job listing
	posting = BeautifulSoup(driver.page_source, 'html.parser') # parse new page

	# Grabs description, rarely a NoneType, so the following prevents error
	try:
		desc = posting.find('div', {'id':'jobDescriptionText'}).get_text()
	except:
		desc = 'n/a'
	
	# Checks if skill is present (at least once) in the description 
	for skill in my_skills:
		if skill.lower() in desc.lower():
			sks += skill+', '

	return sks[0:-2], desc


def create_dataframe(jobs,companies,locations,skills,salaries,ratings,links0,descriptions):
	df = pd.DataFrame({
		'Job':jobs,
		'Company':companies,
		'Location':locations,
		'Skills':skills,
		'Salary':salaries,
		'Rating':ratings,
		'Link':links0,
		'Descriptions':descriptions,
		})
	df.to_csv('indeed_jobs.csv')

	return df


def get_job(li):
	try:
		j = clean(li.find('h2').find('a').get_text()) 
	except:
		j = 'n/a'

	return j

def get_salary(li):
	try:
		s = clean(li.find('span',{'class':'salaryText'}).get_text()) 
	except:
		s = 'n/a'

	return s

def get_company(li):
	try:
		c = clean(li.find('span',{'class':'company'}).get_text())
	except:
		c = 'n/a'

	return c

def get_location(li):
	try:
		l = li.find('span',{'class':'location accessible-contrast-color-location'}).get_text() 
	except:
		try:
			l = li.find('div',{'class':'location accessible-contrast-color-location'}).get_text() 
		except:
			l = 'n/a'

	return l

def get_rating(li):
	try:
		r = clean(li.find('span',{'class':'ratingsContent'}).get_text())
	except:
		r = 'n/a'

	return r

def get_link(li,URL):
	try:
		lk = URL+li.h2.a.get('href')[1:] 
	except:
		lk = 'n/a'

	return l