# indeed-job-scrape

Simpled Indeed job scrape. Code is well documented and explains every step. 

Before using, make sure:
* You have Chromedriver installed
* You have Selenium installed
* You have bs4 installed
* You change the path to Chromedriver to YOUR computers path

To start, call the main method with your desired arguments. The parameters are described in the functions docstrings. The data must be change in the code. 

The function will return:
* A CSV file on the directory it is saved in
* A matplotlib graph with the number of occurences for each skill
* The following data:
  * Job 
  * Company
  * Location
  * Skills
  * Salary
  * Rating
  * Link
  * n/a if any data is not present 

Intended uses:
* bar graph gives you a good visual of which skills are more used than others, perhaps you should choose to learn the more used skills
* The csv file allows you to quickly see all the important data, condensed. A link is provided to go to the specific job listing

Warnings:
* The location variable does not currently work, detailed in comments

Future improvement:
* Eventually work with more data
* Fix location
* Different job sites
* front end work 
