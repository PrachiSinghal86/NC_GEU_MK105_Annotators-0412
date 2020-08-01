from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    driver.set_window_size(1120, 1000)
    url = 'https://www.glassdoor.co.in/Job/india-ios-developer-jobs-SRCH_IL.0,5_IN115_KO6,19.htm'
    driver.get(url)
    jobs = []
    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)
        try:
            driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  # clicking to the X.
        except NoSuchElementException:
            pass

            # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name(
            "jl")  # jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)
            jobs.append({"Job Title": job_title,

                         "Job Description": job_description,

                         "Company Name": company_name,
                         "Location": location}
                        )
            # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                             len(jobs)))
            break
    return pd.DataFrame(jobs)
df = get_jobs(250, False)
df.to_csv('ios.csv', index = False)
