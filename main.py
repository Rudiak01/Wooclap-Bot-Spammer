# -*- coding: utf-8 -*-
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)
import signal
import random
import string
import time
from selenium.webdriver.firefox.options import Options
import re

# Global variables
url = ""  # get the url
num_browsers = 0  # choose a number of instances
option = 0
emoji_option = -1  # chosse the emoji
is_spam_word_cloud = False
is_questions_spam = False
is_lost = False
num_browsers = -1
pool = None


# Signal handler
def signal_handler(signal, frame):
    print("\n\nSortir...")
    pool.terminate()
    pool.join()
    exit(0)


def get_room_code():
    global url
    room_code = " "
    while (
        url.startswith("https://app.wooclap.com/public?missingSlug=")
        or room_code == " "
    ):
        if (
            url.startswith("https://app.wooclap.com/public?missingSlug=")
            or room_code == ""
        ):
            print("Invalid room code, please try again.")
        room_code = ""
        while room_code == "" or " " in room_code:
            print("Please enter the room code:")
            room_code = input("Code: ").upper()
        print("Starting up...")
        options = Options()
        # options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f"https://app.wooclap.com/")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form>div>div>div>input"))
        ).send_keys(room_code)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form>button"))
        ).click()
        time.sleep(1)
        url = driver.current_url
        driver.quit()


def generate_random_user(driver):
    username = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    # Find the input field and enter the username
    input_field = driver.find_element(By.CSS_SELECTOR, "form>div>div>div>input")
    input_field.send_keys(username)
    # Find the button and click it
    button = driver.find_element(By.CSS_SELECTOR, "main>div>div>div>div>button")
    button.click()


def Lost(driver):
    # met que le joueur est perdu
    if (
        len(
            driver.find_elements(
                By.CSS_SELECTOR, "header>div>div:nth-child(3)>button:nth-child(1)"
            )
        )
    ):
        driver.find_element(
            By.CSS_SELECTOR, "header>div>div:nth-child(3)>button:nth-child(1)"
        ).click()


# Functions
def spam_emoji(args):
    url, emoji_option, is_spam_word_cloud, is_questions_spam, is_lost = args
    options = Options()
    # options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(f"{url}")
    time.sleep(1)
    # si le champ utilisateur existe, générer un username et click sur c'est parti
    if len(driver.find_elements(By.CSS_SELECTOR, "form>div>div>div>input")) > 0:
        generate_random_user(driver)
    if(is_lost == True):
        Lost(driver)
    while True:
        try:
            # si l'erreur "veuillez choisir au moins 1 réponse" cliquer sur ok
            if (
                len(driver.find_elements(By.CSS_SELECTOR, "main>div>div>div>header>h3"))
                > 0
            ):
                driver.find_element(
                    By.CSS_SELECTOR,
                    "main>div>div>div>div>button",
                ).click()
                time.sleep(1)
            # nuage de mot spam
            if (
                len(
                    driver.find_elements(
                        By.CSS_SELECTOR, "main>div>div>div>div>div>div>div>textarea"
                    )
                )
                > 0
                and len(
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "nav>div>div>div>button",
                    )
                )
                > 0
                and is_spam_word_cloud == True
            ):
                text = "".join(
                    random.choices(string.ascii_letters + string.digits, k=20)
                )
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "main>div>div>div>div>div>div>div>textarea")
                    )
                ).click()
                input_field = driver.find_element(
                    By.CSS_SELECTOR, "main>div>div>div>div>div>div>div>textarea"
                )
                input_field.send_keys(text)
                driver.find_element(
                    By.CSS_SELECTOR,
                    "nav>div>div>div>button",
                ).click()
            # Question auto spam
            elif (
                len(
                    driver.find_elements(
                        By.CSS_SELECTOR, "main>div>div:nth-child(2)>div>ul"
                    )
                )
                > 0
                and len(
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "main>div>div:nth-child(2)>div>ul>li>div>button",
                    )
                )
                > 0
                and is_questions_spam == True
            ):
                while (
                    len(
                        driver.find_elements(
                            By.CSS_SELECTOR, "main>div>div:nth-child(2)>div>ul"
                        )
                    )
                    > 0
                    and len(
                        driver.find_elements(
                            By.CSS_SELECTOR,
                            "main>div>div:nth-child(2)>div>ul>li>div>button",
                        )
                    )
                    > 0
                ):  # vérifie que au moins 1 réponse est présente
                    parent_element = driver.find_element(
                        By.CSS_SELECTOR, "main>div>div>div>ul"
                    )  # list comprenant les réponses
                    child_elements = parent_element.find_elements(By.TAG_NAME, "li")
                    number_of_child_elements = len(child_elements)
                    button = random.randint(1, number_of_child_elements)
                    button_selector = f"li:nth-child({button})>div>button"
                    selected_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
                    )
                    driver.execute_script(
                        "arguments[0].scrollIntoView();", selected_button
                    )
                    selected_button.click()
                    driver.find_element(
                        By.CSS_SELECTOR,
                        "nav>div>div>div>button",
                    ).click()
                    # relance le navigateur entrer le plus de réponses possibles
                    driver.quit()
                    options = Options()
                    options.add_argument("-headless")
                    driver = webdriver.Firefox(options=options)
                    driver.get(f"{url}")
                    time.sleep(1)
                    if (
                        len(
                            driver.find_elements(
                                By.CSS_SELECTOR, "form>div>div>div>input"
                            )
                        )
                        > 0
                    ):
                        generate_random_user(driver)

            # click emoji
            elif (
                len(
                    driver.find_elements(
                        By.CSS_SELECTOR, "main>div:nth-child(2)>button"
                    )
                )
                > 0
                and emoji_option > 0
            ):  # cherche si l'icône pour afficher tout les emojis existe
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "main>div:nth-child(2)>button")
                    )
                ).click()  # click sur le bouton emoji pour voir la liste de tout les emojis
                while True:
                    if emoji_option == 6:
                        button_selector = f"main>div:nth-child(3)>button:nth-child({random.randint(1, 5)})"  # sélectionne aléatoirement sur un emoji
                    else:
                        button_selector = f"main>div:nth-child(3)>button:nth-child({emoji_option})"  # sélectionne l'émoji choisi
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
                    ).click()  # click sue l'émoji selectionner
            else:
                print("Nothing to do, waiting...")
                time.sleep(5)
        except (
            StaleElementReferenceException,
            TimeoutException,
            NoSuchElementException,
        ):
            print("Element became stale or timed out, refreshing page...")
            driver.refresh()
            time.sleep(5)  # Wait for page to reload
            continue


def spam_user(args):
    url, _, _, _, is_lost = args
    while True:
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f"{url}")
        try:
            element_present = EC.presence_of_element_located((By.ID, "main"))
            WebDriverWait(driver, 5).until(element_present)
            if(is_lost == True):
                # si le champ utilisateur existe, générer un username et click sur c'est parti
                if len(driver.find_elements(By.CSS_SELECTOR, "form>div>div>div>input")) > 0:
                    generate_random_user(driver)
                Lost(driver)
            driver.quit()
        except TimeoutException:
            driver.quit()


def menu():
    global num_browsers, option, emoji_option, is_questions_spam, is_spam_word_cloud, is_lost
    questions_option = -1
    spam_word_cloud = -1
    lost_option = -1
    print("=== Wooclap Spammer | by Rudiak ===")
    while 0 >= option or option > 2:
        print("\tChoisi une option: ")
        print("\t1. Spam Emoji / Questions")
        print("\t2. Spam Users")
        try:
            option = int(input("Option: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    if option == 1:
        while emoji_option < 0 or emoji_option > 6:
            print("\tChoose an emoji: (0)")
            print("\t1. 👍")
            print("\t2. 💙")
            print("\t3. 🔥")
            print("\t4. 😯")
            print("\t5. 🎉")
            print("\t6. Random")
            print("\t0. Deactivate Emoji Spam")

            try:
                emoji_option = int(input("Option: "))
            except ValueError:
                emoji_option = 0
                break

        while True:
            print("\tActivate question random response: (0) ")
            print("\t1. Yes")
            print("\t0. No")
            try:
                questions_option = int(input("Option: "))
                if questions_option == 1:
                    is_questions_spam = True
                    break
                elif questions_option == 0:
                    is_questions_spam = False
                    break
            except ValueError:
                is_questions_spam = False
                break

        while True:
            print(
                "\tActivate word cloud flooding (/!\\ WARNING will probably crash the Wooclap session): (0) "
            )
            print("\t1. Yes")
            print("\t0. No")
            try:
                spam_word_cloud = int(input("Option: "))
                if spam_word_cloud == 1:
                    is_spam_word_cloud = True
                    break
                elif spam_word_cloud == 0:
                    is_spam_word_cloud = False
                    break
            except ValueError:
                is_spam_word_cloud = False
                break

        while True:
            print("\tActivate 'is lost': (0) ")
            print("\t1. Yes")
            print("\t0. No")
            try:
                lost_option = int(input("Option: "))
                if lost_option == 1:
                    is_lost = True
                    break
                elif lost_option == 0:
                    is_lost = False
                    break
            except ValueError:
                is_lost = False
                break
    else:
        while True:
            print("\tActivate 'is lost': (0) ")
            print("\t1. Yes")
            print("\t0. No")
            try:
                lost_option = int(input("Option: "))
                if lost_option == 1:
                    is_lost = True
                    break
                elif lost_option == 0:
                    is_lost = False
                    break
            except ValueError:
                is_lost = False
                break
    if emoji_option == 0 and not is_questions_spam and not is_questions_spam:
        print("nothing to run... Quiting")
        num_browsers = 0
    else:
        while num_browsers <= 0:
            print(
                "Enter the number of instances (more instances ==> more resource intensive)"
            )
            num_browsers = int(input("Number of instances: "))
        get_room_code()
        print("Running...")


def switch_function(i):
    global pool
    args = [
        (url, emoji_option, is_questions_spam, is_spam_word_cloud, is_lost)
    ] * num_browsers
    switcher = {
        1: lambda: pool.map(spam_emoji, args),
        2: lambda: pool.map(spam_user, args),
    }
    func = switcher.get(i, lambda: None)
    func()


# Main
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    menu()
    if num_browsers != 0:
        pool = Pool(num_browsers)
        switch_function(option)
