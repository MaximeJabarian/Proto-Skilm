import time
import pandas as pd
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.by import By


def format_url_string(job_name, country_name):
    job_url = "%20".join(job_name.split(" "))
    country_url = "%20".join(country_name.split(" "))
    country_url = country_url.replace("é", "%C3%A9")
    return f"https://www.linkedin.com/jobs/search/?currentJobId=3439429730&geoId=&keywords={job_url}&location={country_url}"


def scroll_jobs_page(driver, jobs_num):
    i = 2
    click_count = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while i <= 1: #int(jobs_num / 5) + 1:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i += 1
        print(f"Current at: {i}, Percentage at: {((i + 1) / (int(jobs_num / 2) + 1)) * 100}%", end="\r")

        try:
            infinite_scroller_button = driver.find_element(By.XPATH, ".//button[@aria-label='Voir plus offres d’emploi']")
            infinite_scroller_button.click()
            time.sleep(0.8)

        except:
            time.sleep(0.5)
            pass

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height is not None and new_height != last_height:
            click_count = 0
        else:
            click_count += 1
            print(f"Clicked the button {click_count} times")

        if click_count >= 9:
            break

        last_height = new_height

    return driver


# Rest of the code for extracting job details and creating a pandas DataFrame

def extract_job_details(job_name, driver):
    job_lists = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
    jobs = job_lists.find_elements(By.TAG_NAME, "li")
    pattern = r'[^\w\s]'
    job_details = []
    previous_job_description = None
    ct = 0
    
    for job in jobs:
        details = {}
        
        details['job_target'] = job_name

        try:
            details['date'] = job.find_element(By.CSS_SELECTOR, "div>div>time").get_attribute("datetime")
        except:
            details['date'] = None

        try:
            details['location'] = job.find_element(By.CSS_SELECTOR, "div>div>span").get_attribute("innerText")
        except:
            details['location'] = None

        try:
            details['job_title'] = job.find_element(By.CSS_SELECTOR, "h3").get_attribute("innerText")
        except:
            details['job_title'] = None

        try:
            details['company_name'] = job.find_element(By.CSS_SELECTOR, "h4").get_attribute("innerText")
        except:
            details['company_name'] = None

        #__________________________________________________________________________ JOB Industry
        industry_path='/html/body/div/div/section/div/div/section/div/ul/li[4]/span'

        try:
            details['Industry'] = job.find_element(By.XPATH,industry_path).get_attribute('innerText')
        except:
            details['Industry'] = None
            pass
            
        try:
            details['job_link'] = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            details['job_link'] = None
            
        try:
            job_click_path = f'/html/body/div/div/main/section/ul/li[{jobs.index(job) + 1}]/div/a'
            job.find_element(By.XPATH, job_click_path).click()
            time.sleep(2)

            jd_path = '/html/body/div/div/section/div/div/section/div/div/section/div'
            details['job_description'] = job.find_element(By.XPATH, jd_path).get_attribute('innerText')
        except:
            details['job_description'] = None
            
        if previous_job_description is not None: 
            
            #if details['job_description'].replace('\n\n', ' ').replace('\n', '')[10] == previous_job_description.replace('\n\n', ' ').replace('\n', '')[10]:
            if re.sub(pattern, '', details['job_description'].replace('\n\n', ' ').replace('\n', ' ')).strip()[:10] == re.sub(pattern, '', previous_job_description.replace('\n\n', ' ').replace('\n', ' ')).strip()[:10]:
                job_click_path = f'/html/body/div/div/main/section/ul/li[{jobs.index(jobs[ct-1]) + 1}]/div/a'
                jobs[ct-1].find_element(By.XPATH, job_click_path).click()
                time.sleep(2)
                job_click_path = f'/html/body/div/div/main/section/ul/li[{jobs.index(job) + 1}]/div/a'
                job.find_element(By.XPATH, job_click_path).click()
                time.sleep(2)
                jd_path = '/html/body/div/div/section/div/div/section/div/div/section/div'
                details['job_description'] = job.find_element(By.XPATH, jd_path).get_attribute('innerText')

        previous_job_description = details['job_description']
        
        ct+=1
        job_details.append(details)

    return job_details


def main(job_name, country_name):

    # Country to select
    Countries = ["Canada", "France", "Erevan Armenia", "Turkey", "Spain", "Italy", "United-Kingdom", "Portugal",
            'United States', 'China', 'India', 'Brazil', 'Indonesia', 'Nigeria', 'Pakistan', 'Bangladesh',
             'Russia', 'Japan']   
    
    # Starting url creation to scrap
    url = format_url_string(job_name, country_name)
    driver = webdriver.Chrome("./chromedriver")
    driver.get(url)

    jobs_num = driver.find_element(By.CSS_SELECTOR, "h1>span").get_attribute("innerText")
    jobs_num = int(jobs_num.replace('\u202f', '').replace(',', ''))
    driver = scroll_jobs_page(driver, jobs_num)
    job_details = extract_job_details(job_name, driver)
    driver.quit()


    # Create a pandas DataFrame from the job_details list
    job_data = pd.DataFrame(job_details)

    # Save the job_data DataFrame to a CSV file or further process the data as needed
    job_name = job_name.replace(" ", "_")
    #job_data.to_csv(f"SKILMI/Dataset_{job_name}_{country_name}.csv", index=False)
    #job_data.to_csv("SKILMI/Job_descriptions.csv", index=False)
    
    # Append the new DataFrame to the existing CSV file
    job_data.to_csv('SKILMI/Job_descriptions.csv', mode='a', header=False, index=False)
    
    
"""
Job target

- Business Developer
- Sales development representative
- Product owner
- Customer success
- Chargé.e de projet marketing et communication
- Chargé de projet intelligence artificielle
- Account manager
- Business Development Representative
- Operations Manager
- Growth Marketing
- Chef de Projet

"""
