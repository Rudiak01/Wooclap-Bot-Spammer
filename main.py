# -*- coding: utf-8 -*-
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import signal
import random
import string
import time
from selenium.webdriver.firefox.options import Options
import re
# Global variables
url="" #get the url
num_browsers=0 #choose a number of instances
option=0
emoji_option=0 #chosse the emoji
pool=None

# Signal handler
def signal_handler(signal, frame):
    print("\n\nSortir...")
    pool.terminate()
    pool.join()
    exit(0)

def get_room_code():
    global url
    room_code = " "
    while url.startswith('https://app.wooclap.com/public?missingSlug=') or room_code == " ":
        if url.startswith('https://app.wooclap.com/public?missingSlug=') or room_code == "":
            print("Invalid room code, please try again.")
        room_code = ""
        while room_code == "" or ' ' in room_code :
            print("Please enter the room code:")
            room_code = input("Code: ").upper()
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f'https://app.wooclap.com/')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.sc-hlindT.hAPWLm'))).send_keys(room_code)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.sc-gWrJbu.gDCSKR'))).click()
        time.sleep(1)
        url = driver.current_url
        driver.quit()

def generate_random_user(driver):
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    # Find the input field and enter the username
    input_field = driver.find_element(By.CSS_SELECTOR, 'input.sc-dCBTtU.drRDKD')
    input_field.send_keys(username)
    # Find the button and click it
    button = driver.find_element(By.CSS_SELECTOR, 'button.sc-geWqxS.fFvTET')
    button.click()

# Functions
def spam_emoji(args):
    url, emoji_option = args
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(f'{url}')
    time.sleep(1)
    if len(driver.find_elements(By.CSS_SELECTOR, 'input.sc-dCBTtU.drRDKD')) > 0:
        generate_random_user(driver)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.jwFq2'))).click()
    while True:
        try:
            if len(driver.find_elements(By.CSS_SELECTOR, 'textarea.sc-hPvlKq.dVDOSf')) > 0 and len(driver.find_elements(By.CSS_SELECTOR, 'button.sc-hLseeU.sc-eDDNvR.sc-gLDzan.TfzXa.ieVmah.gNRcrj')) > 0:
                text = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                # Find the input field and enter the username
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea.sc-hPvlKq.dVDOSf'))).click()
                input_field = driver.find_element(By.CSS_SELECTOR, 'textarea.sc-hPvlKq.dVDOSf')
                input_field.send_keys(text)
                driver.find_element(By.CSS_SELECTOR, 'button.sc-hLseeU.sc-eDDNvR.sc-gLDzan.TfzXa.ieVmah.gNRcrj').click()
            elif len(driver.find_elements(By.CSS_SELECTOR, 'ul.G_s3z')) > 0 and len(driver.find_elements(By.CSS_SELECTOR, 'button.sc-hLseeU.sc-eDDNvR.sc-gLDzan.TfzXa.ieVmah.gNRcrj')) > 0:
                while len(driver.find_elements(By.CSS_SELECTOR, 'ul.G_s3z')) > 0 and len(driver.find_elements(By.CSS_SELECTOR, 'button.sc-hLseeU.sc-eDDNvR.sc-gLDzan.TfzXa.ieVmah.gNRcrj')) > 0:
                    parent_element = driver.find_element(By.CSS_SELECTOR,'ul.G_s3z')
                    child_elements = parent_element.find_elements(By.TAG_NAME, "li")
                    number_of_child_elements = len(child_elements)
                    button = random.randint(1,number_of_child_elements)
                    button_selector = f'li:nth-child({button}) div button.zOWQM.u7G_O.s2MaS.WiTUI'
                    selected_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
                    driver.execute_script("arguments[0].scrollIntoView();", selected_button)
                    selected_button.click()
                    driver.find_element(By.CSS_SELECTOR, 'button.sc-hLseeU.sc-eDDNvR.sc-gLDzan.TfzXa.ieVmah.gNRcrj').click()
                    driver.quit()
                    options = Options()
                    options.add_argument("-headless")
                    driver = webdriver.Firefox(options=options)
                    driver.get(f'{url}')
                    time.sleep(1)
                    if len(driver.find_elements(By.CSS_SELECTOR, 'input.sc-dCBTtU.drRDKD')) > 0:
                        generate_random_user(driver)
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.jwFq2'))).click()
            elif len(driver.find_elements(By.CSS_SELECTOR, 'button.sc-eoqJBP.iGKvaI')) > 0:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-eoqJBP.iGKvaI'))).click()
                while True:
                    if emoji_option == 6:
                        button_selector = f'div.sc-gxJnBp.cwFwAU button:nth-child({random.randint(1, 5)})'
                    else:
                        button_selector = f'div.sc-gxJnBp.cwFwAU button:nth-child({emoji_option})'
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))).click()
            else:
                print("Nothing to do, waiting...")
                time.sleep(5)
        except (StaleElementReferenceException, TimeoutException):
            print("Element became stale or timed out, refreshing page...")
            driver.refresh()
            time.sleep(5)  # Wait for page to reload
            continue

        
def spam_user(args):
    url, _ = args
    while True:
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f'{url}')
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(driver, 5).until(element_present)
            driver.quit()
        except TimeoutException:
            driver.quit()
        
def menu():
    global num_browsers, option, emoji_option
    print("=== Wooclap Spammer | by Rudiak ===")
    while 0>=option or option>2:
        print("Choisi une option: ")
        print("\t1. Spam Emoji / Questions")
        print("\t2. Spam Users")
        option = int(input("Option: "))
    if option == 1:
        while 0>=emoji_option or emoji_option>6:
            print("Choose an emoji: ")
            print("\t1. 👍")
            print("\t2. 💙")
            print("\t3. 🔥")
            print("\t4. 😯")
            print("\t5. 🎉")
            print("\t6. Random")
            emoji_option = int(input("Option: "))
    while num_browsers<=0:
        print("Enter the number of instances (more instances ==> more lag)")
        num_browsers = int(input("Number of instances: "))
    get_room_code()
    print("Running...")

def switch_function(i):
    global pool
    args = [(url,emoji_option)] * num_browsers
    switcher = {
        1: lambda: pool.map(spam_emoji, args),
        2: lambda: pool.map(spam_user, args)
    }
    func = switcher.get(i, lambda: None)
    func()

# Main
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    menu()
    pool = Pool(num_browsers)
    switch_function(option)
    
