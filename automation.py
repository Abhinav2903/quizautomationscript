
import time
import csv
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebScraper:
    def __init__(self):
        self.driver = None
        self.settings = None
#read configuration
    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.settings = config['Settings']

    def initialize_driver(self):
        self.driver = webdriver.Chrome()

#question answer pages script
    def question_answer(self, wait, writer):
        response_mapping = {'a': 1, 'b': 2, 'c': 3}
        button_index = 1  # it starts from 1
        while True:
            question_text_xpath = f"/html/body/div[1]/div/main/section/div/div/div[1]/ol/li[{button_index}]/div/div/div/div[1]/p"
            question_text = self.driver.find_element(By.XPATH, question_text_xpath).text
            print("Question:", question_text)
            # Take user response
            response_value = input("Enter your response (a, b, or c): ").lower()
            response_value_numeric = response_mapping.get(response_value)
            
            if response_value_numeric is None:
                print("Invalid response. Please enter 'a', 'b', or 'c', so taking option a as response")
                response_value_numeric = 1
            response_button_xpath = f"/html/body/div[1]/div/main/section/div/div/div[1]/ol/li[{button_index}]/div/div/div/div[2]/ul/li[{response_value_numeric}]/button/span[1]"
            response_button = wait.until(EC.element_to_be_clickable((By.XPATH, response_button_xpath)))
            response_value_text = response_button.text
            #click selected option
            response_button.click()
            # Write question and response to CSV
            writer.writerow([question_text, response_value_text])
            if button_index == 38:
                break
            button_index += 1
            time.sleep(2)
#information page script
    def writer_function(self, wait, writer):
        button_index = 1
        while True:
            heading_text_xpath = f"/html/body/div[1]/div/main/section/form/div/ol/li[{button_index}]/div[2]/div[1]/h2/button/span[2]"
            answer_text_xpath = f"/html/body/div[1]/div/main/section/form/div/ol/li[{button_index}]/div[2]/div[2]/p"
            response_button = wait.until(EC.element_to_be_clickable((By.XPATH, heading_text_xpath)))
            response_button.click()
            response_button_text = self.driver.find_element(By.XPATH, heading_text_xpath).text
            # Add a delay before capturing main_text
            time.sleep(1)  # Adjust this delay as needed
            #wait untill it is visbile
            main_text_element = wait.until(EC.visibility_of_element_located((By.XPATH, answer_text_xpath)))
            main_text =  main_text_element.text
             # Write info & response to CSV
            writer.writerow([response_button_text, main_text])
            if button_index == 38:
                break
            button_index += 1
            time.sleep(2)

    def navigate_and_capture_results(self):
        wait = WebDriverWait(self.driver, 20)
        self.driver.get(self.settings['url'])
        time.sleep(2) 
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button--big")))
        start_button = self.driver.find_element(By.CLASS_NAME, "button--big")
        start_button.click()
        time.sleep(2)
        # Open CSV file for storing results
        with open('results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Question", "Response"])
            self.question_answer(wait, writer)
            self.writer_function(wait, writer)

    def run(self):
        self.read_config()
        self.initialize_driver()
        self.navigate_and_capture_results()
        self.driver.quit()


if __name__ == "__main__":
    scraper = WebScraper()
    scraper.run()
