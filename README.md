# indeed-skill-scrape

* Selenium 4 has made many changes, current version will not work
* *indeed_scrape.py* works by itself
* *modular-scrape/indeed_scrape_client.py* AND *modular-scrape/scrape.py* work as a client-module, *scrape.py* is the module

## Summary
Simple Indeed job skill scrape. User decided which job to search for, how many pages to search, whether or not to search each individual job for certain skills (this takes longer, but is the intended use), and a list of skills as Strings to search for. The following images are results from:

* job = 'Data science'
* pages = 10
* skill_search = True
* skills = ['Python', 'SQL', ...], filled with the skills present on the graphs y axis

<img width="1410" alt="Skill Graph" src="https://user-images.githubusercontent.com/76178340/117382997-c6093700-aead-11eb-8379-d7d31cd7edc9.png">

When you are searching for a custom job, you may create a list full of skills or possible requirements for a specific job (e.g. technical skills, education requirements, such as those listed on the graph. If a skill is present in the description of a job, a +1 will be added to its occurence. For example, if we search 15 jobs, and 12/15 jobs have 'Python' in their description, python will have a value of 12 on the graph. This provides a good visual as to which skills are in demand or more widely used than others. Skills are NOT double counted, if it is present multiple times in a job description, it is only counted once.

<img width="1036" alt="ccsssvvv" src="https://user-images.githubusercontent.com/76178340/117383248-5a739980-aeae-11eb-883b-9be2100d4a17.png">

A CSV of all the data retrieved. Used for condensing the data instead of scrolling through pages and clicking on each one. You can also see which skills are present in each job at a quick glance. If one catches your eye, the full description is present in the last column, or you may use the link to go to job posting online.

<br/>

## How is this different than Indeed???

1. **SKILLS**: indeed cannot quickly show you which skills each job requires
2. **TIME**: while the program itself takes time to run, you do not need to sit there scrolling through pages. Let the program run and come back in seconds to a minute (depending on how many pages you search) and have all the data infront of you. If a job in the CSV requires skills you do not have, you can brush past it in a split second.
3. **INSIGHT**: The graph shows you which skills are used the most. Students can use this information to find out which skills they should learn to increase the likelyhood of having the skills a future internship or job requires

<br/>

## Instructions, technical use
Before using, make sure:
* You have Chromedriver installed
* You have Selenium installed
* You have bs4 installed
* You change the path to Chromedriver on YOUR computers path

How to:
* Selenium: open terminal, 'pip install selenium'
* bs4: open terminal, 'pip install bs4'
* Chromdriver: setup, https://chromedriver.chromium.org/getting-started
* Change path: varies, eg. '/Users/YourUserName/Desktop/Chromedriver', if it is on desktop

To start, call the main method with your desired arguments. The parameters are described in the functions docstrings. The data must be change in the code. 

The function will return:
* A CSV file on the directory it is saved in
* A matplotlib graph with the number of occurences for each skill (if skill_search==True)
* The following data:
  * Job 
  * Company
  * Location
  * Skills
  * Salary
  * Rating
  * Link
  * Description
  * n/a if any data is not present 

Intended uses:
* bar graph gives you a good visual of which skills are more used than others, perhaps you should choose to learn the skills with the most mentions first
* The csv file allows you to quickly see all the important data, condensed. A link is provided to go to the specific job listing

Note:
* The location variable does not currently work, detailed in comments

Possible Confusions
* Three 'link' lists: Can be ignored, this is for functionality. Sometimes the link retrived from the 'All Listings' pages vs the specific listings page are different. skill_search = True provides a link that is much more likely to be valid.

Future improvement:
* front end work; Website/webapp, Tkinter, etc?
* Eventually work with more data
* Fix location entry
* Different job sites; glassdoor, monster?
* look into use of regex, for example; the programming language R is hard to search for because any word with an r in it will count as a mention. ' R ' with spaces on each side could work, but in many jobs HTML, it is present as '\nR' or '\*R'. while this will count as a mention, '\nRead' would yield a mention as well becuase '\nR' is present. We could list each one, but that would give us a graph with R mentioned 3+ times!

Project notes:
* focus changed from job scrape to skill scrape, job scrape is too basic and overused, searching for in demand skills is not
