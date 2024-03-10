import time
import csv
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


# Function to read config file
def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Settings']

def question_answer(wait,writer):
        response_mapping = {'a': 1, 'b': 2, 'c': 3}
        button_index = 1  # it starts from 1
        # Loop through questions
        while True:
            # Find and print the question text
            question_text_xpath =  "/html/body/div[1]/div/main/section/div/div/div[1]/ol/li[{0}]/div/div/div/div[1]/p".format(button_index)
            # response_button_xpath = "/html/body/div[1]/div/main/section/div/div/div[1]/ol/li[{0}]/div/div/div/div[2]/ul/li[1]/button/span[1]".format(button_index)
            question_text = driver.find_element(By.XPATH,question_text_xpath).text
            print("Question:", question_text)
            response_value = input("Enter your response (a, b, or c): ").lower()  # Taking user response
            response_value_numeric = response_mapping.get(response_value)
            if response_value_numeric is None:
                print("Invalid response. Please enter 'a', 'b', or 'c', so taking option a as response")
                response_value_numeric = 1
            response_button_xpath = "/html/body/div[1]/div/main/section/div/div/div[1]/ol/li[{0}]/div/div/div/div[2]/ul/li[{1}]/button/span[1]".format(button_index,response_value_numeric)
            # Simulate user's response (parameterization)
            response_button = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, response_button_xpath)))
            response_value_text = response_button.text
            # Click the button
            response_button.click()

            # Write question and response to CSV
            writer.writerow([question_text, response_value_text])
            if(button_index==38):
                break
            button_index += 1 
            # Wait for the page to load
            time.sleep(2)
            
def writer_function(writer,wait):
          button_index = 1
          while True:
            # Find and print the question text
            heading_text_xpath ="/html/body/div[1]/div/main/section/form/div/ol/li[{0}]/div[2]/div[1]/h2/button/span[2]".format(button_index)
            answer_text_xpath = "/html/body/div[1]/div/main/section/form/div/ol/li[{0}]/div[2]/div[2]/p".format(button_index)
            response_button = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, heading_text_xpath)))
             # Click the button
            response_button.click()
            response_button_text =driver.find_element(By.XPATH, heading_text_xpath).text
            main_text = driver.find_element(By.XPATH,answer_text_xpath).text
            # Write question and response to CSV
            writer.writerow([response_button_text,main_text])
            if(button_index==38):
                break
            button_index += 1 
            # Wait for the page to load
            time.sleep(2)
            

# Function to navigate through questions and capture results
def navigate_and_capture_results(url):
    # Wait for the element to be clickable
    wait = WebDriverWait(driver, 20) 
    # Open the webpage
    driver.get(url)

    # Wait for the page to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button--big")))

    # Locate and click the start button
    start_button = driver.find_element(By.CLASS_NAME,"button--big")
    start_button.click()

    # Wait for the page to load
    time.sleep(2)

    # Open CSV file for storing results
    with open('results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "Response"])
        question_answer(wait=wait,writer=writer)
        writer_function(wait=wait,writer=writer)


# Read settings from config file
settings = read_config()
# Initialize Chrome driver with the specified path
driver = webdriver.Chrome()
# Call the function to navigate and capture results
navigate_and_capture_results(url=settings['url'])
# Close the browser
driver.quit()
      
          
