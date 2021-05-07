# indeed-job-scrape

Simple Indeed job scrape. User decided which job to search for, how many pages to search, whether or not to search each individual job for certain skills (this takes longer), and a list of skills as Strings to search for. The following images are results from:

* job = 'Data science'
* pages = 10
* skill_search = True
* skills = ['Python', 'SQL', ...], filled with the skills present on the graphs y axis

<img width="1410" alt="Skill Graph" src="https://user-images.githubusercontent.com/76178340/117382997-c6093700-aead-11eb-8379-d7d31cd7edc9.png">

Skills are NOT double counted, if it is present multiple times in a job description, it is only counted once.

<img width="1036" alt="ccsssvvv" src="https://user-images.githubusercontent.com/76178340/117383248-5a739980-aeae-11eb-883b-9be2100d4a17.png">

A CSV of all the data retrieved.

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
* bar graph gives you a good visual of which skills are more used than others, perhaps you should choose to learn the more used skills
* The csv file allows you to quickly see all the important data, condensed. A link is provided to go to the specific job listing

Warnings:
* The location variable does not currently work, detailed in comments

Possible Confusions
* Two link lists: sometimes the link retrived from the 'All Listings' pages vs the specific listings page are different. skill_search = True provides a link that is much more likely to be valid.

Future improvement:
* Eventually work with more data
* Fix location entry
* Different job sites; glassdoor, monster?
* front end work; Website/webapp, Tkinter?
