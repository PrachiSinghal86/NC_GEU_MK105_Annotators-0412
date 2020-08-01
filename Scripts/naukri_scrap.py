from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup


driver = webdriver.Chrome("./chromedriver")

df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Experience","Description"])

for i in range(0, 50):
    driver.get('https://www.naukri.com/cloud-computing-jobs-' + str(i))

    driver.implicitly_wait(4)

    for job in driver.find_elements_by_class_name('jobTuple'):


        soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')

        try:
            title = soup.find("a", class_="title").text.replace("\n", "").strip()

        except:
            title = 'None'

        try:
            location = soup.find(class_="subTitle").text
        except:
            location = 'None'

        try:
            company = soup.find(class_="company").text.replace("\n", "").strip()
        except:
            company = 'None'
        try:
            exp = soup.find(class_="experience").text
        except:
            exp = 'None'
        try:
            location = soup.find(class_="location").text.replace("\n", "").strip()
        except:
            location = 'None'
        try:
            salary = soup.find(class_="salary").text.replace("\n", "").strip()
        except:
            salary = 'None'
        job_desc=""
        try:
            for i in soup.find_all(class_="fleft"):
                job_desc+=" "+i.text


        except:
            job_desc=soup.find(class_="job-description").text.replace("\n", "").strip()



        df = df.append({'Title': title,'Location': location, 'Company': company, 'Salary': salary,'Experience':exp,
                        'Description': job_desc}, ignore_index=True)

df.to_csv("cloudnewnaukri.csv", index=False)