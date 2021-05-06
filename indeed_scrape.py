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
        j -> lk (str):Temp vars to append to listing data
        
        listings (list):List of div's for each job listing on current page
        
        *Unlisted vars are mostly Selenium vars for automation, explained in comments
        
    Functions:
        clean():Cleans text data from listings
        graph():Graphs skills data by number of mentions in all listings
    
    Returns:
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
    
    
    
    # Function to clean text 
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



    # Sorted Bar graph to visualize number of skills mentioned
    def graph(my_skills, df):
        '''
        Returns Matplotlib graph.
    
        Parameters:
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
        
    

    # Data retrieval
    for page in range(pages): # loop for each page

        # Parse 
        soup = BeautifulSoup(driver.page_source, 'html.parser') # current page parse
        listings = soup.find_all('div',{'class':'jobsearch-SerpJobCard unifiedRow row result clickcard'}) # listings parse

        # Parse data for each listing
        for li in listings:
            # Job
            try:
                j = clean(li.find('h2').find('a').get_text()) 
            except:
                j = 'n/a'

            # Salary
            try:
                s = clean(li.find('span',{'class':'salaryText'}).get_text()) 
            except:
                s = 'n/a'

            # Company
            try:
                c = clean(li.find('span',{'class':'company'}).get_text())
            except:
                c = 'n/a'

            # Location, searches two locations
            try:
                l = li.find('span',{'class':'location accessible-contrast-color-location'}).get_text() 
            except:
                try:
                    l = li.find('div',{'class':'location accessible-contrast-color-location'}).get_text() 
                except:
                    l = 'n/a'
                    
            # Rating
            try:
                r = clean(li.find('span',{'class':'ratingsContent'}).get_text())
            except:
                r = 'n/a'
                
            # Job link, the link may not always be valid
            try:
                lk = URL+li.h2.a.get('href')[1:] 
            except:
                lk = 'n/a'
                
            # If skil_search: this block opens the listing page, checks and saves description
            sks = ''
            desc = ''
            if skill_search:
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

            # All data appended to list after each listing
            jobs.append(j) 
            salaries.append(s)
            companies.append(c)
            locations.append(l)
            ratings.append(r)
            links1.append(lk)
            skills.append(sks[0:-2])
            descriptions.append(desc)

            # Which links list is used
            if skill_search:
                links0 = links2.copy()
            else:
                links0 = links1.copy()
            
            # DataFrame 
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

            
        # This selects the next page, breaks if link is not present/no more pages
        try:
            link = URL+soup.find('ul',{'class':'pagination-list'}).find_all('li')[-1].find('a').get("href")
        except:
            break
            

        driver.get(link)
        sleep(1) 


    driver.quit() # Exits webpage

    if skill_search:
        graph(my_skills, df)
    
    
    
datasci_skills = ['python', 'SQL', 'tensorflow','sci-kit','pyTorch','aws','azure','artificial intelligence', ' AI ',
             'machine learning','deep learning', 'neural network', 'bachelor','masters','phd',
             'statistic','math'] 

sofdev_skills = ['HTML','CSS','JavaScript','React','angular','mongoDB','SQL','Python','AWS','Azure','bachelor',
                'masters','statistic','math','artificial intelligence']

main('Data Science', True, 1, datasci_skills)


