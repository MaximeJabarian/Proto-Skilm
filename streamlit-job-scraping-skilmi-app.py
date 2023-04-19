import streamlit as st
import pandas as pd
#from selenium import webdriver
#from functions_job_scraping import main

# Configure the WebDriver
webdriver_path = "./chromedriver"  # Update this to the path of your WebDriver executable
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver
driver = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)

# Your existing Streamlit code
st.title("LinkedIn Job Scraper")

country_list = ["Canada", "France", "Erevan Armenia", "Turkey", "Spain", "Italy", "United-Kingdom", "Portugal",
                'United States', 'China', 'India', 'Brazil', 'Indonesia', 'Nigeria', 'Pakistan', 'Bangladesh',
                'Russia', 'Japan']

job_target_list = [
    "Business Developer",
    "Sales development representative",
    "Product owner",
    "Customer success",
    "Chargé.e de projet marketing et communication",
    "Chargé de projet intelligence artificielle",
    "Account manager",
    "Business Development Representative",
    "Operations Manager",
    "Growth Marketing",
    "Chef de Projet"
]

selected_country = st.selectbox("Select a country:", country_list)
selected_job_target = st.selectbox("Select a job target:", job_target_list)
num_pages = st.number_input("Select the number of pages to scrape:", min_value=1, value=1)

# if st.button("Scrape"):
#     job_data = main(selected_job_target, selected_country)
#     st.write(job_data.head(10))

