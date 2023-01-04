from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
import re
import time
import requests
from selenium.webdriver.common.keys import Keys
import random

import xml.etree.ElementTree as ET


#import selenium.webdriver as webdriver

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def webscraper():
    # get URL
    url = "https://en.wikipedia.org/wiki/List_of_hobbies"
    html = urllib.request.urlopen(url, context=ctx).read()

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    lst = []

    for tag in tags:

        if not tag.string is None:

            raw = tag.get('href', None)
            raw_x = raw.rstrip()
            # print(raw_x)
            if raw_x.startswith("/wiki") and len(raw_x) < 10:
                x = re.findall('/wiki/(.*)', raw_x)
                lst = lst + x
    return lst

    # print(lst)
    # all_words = soup.find_all('a')
    # print(all_words)


def web_search(search_term):
    url = "https://www.google.com/?gws_rd=ssl"
    #s = Service(r'F:\DS Project 1\Firefox GeckoDriver\geckodriver.exe')
    browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    # browser = webdriver.Firefox(executable_path=r'F:\DS Project 1\Firefox GeckoDriver\geckodriver.exe')
    browser.get(url)
    #search_box = browser.find_element_by_name('q')   #depreciated in update
    search_box = browser.find_element("name", "q")

    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)
    search_box.submit()
    time.sleep(5)
    url2 = browser.current_url
    page = requests.get(url2)

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())

    definition = soup.find("div", class_='BNeawe s3v9rd AP7Wnd').text
    hint = definition.split()[0:10]
    hint_string = ' '.join(hint)
    print(hint_string)

    # for definition in definitions:
    # print(definition.contents)
    # try:
    #     links = browser.find_elements_by_xpath("//ol[@class='w-gl w-gl--desktop w-gl--']//div//a")
    #     #links = browser.find_elements_by_xpath('//div//a')
    #     # links = browser.find_element_by_id('loginForm')
    # except:
    # print("not found")

    # links = browser.find_element_by_id("href")
    # links = browser.find_elements_by_xpath('//div//p//span')
    # results = []
    # print("check here mate")
    # href = links.get_attribute("href")
    # print(href)
    # for link in links:
    #     href = link.get_attribute("href")
    #
    #
    #     print(href)
    #     results.append(href)
    browser.close()
    return definition


# search_item = input("Enter word that needs hint ")

hangman_word_list = webscraper()
hangman_word = random.choice(hangman_word_list)
letter_list = list(hangman_word)
last_index = len(letter_list)
user_guess_list = ['_'] * last_index
attempt = 0

try:
    game_start = input("Play with hints? y or n ")
except ValueError:
    print("please type y or n!")

if game_start.lower() == "y":
    to_search = "define " + hangman_word
    web_search(to_search)








while attempt < 4:

    user_try = input("Guess a letter of the word ").lower()


    for i, letter in enumerate(letter_list):
        if user_try == letter and letter_list != user_guess_list:

            user_guess_list[i] = letter
            for k, let in enumerate(letter_list):
                if let == letter:
                    user_guess_list[k] = let

            print("Letter matched!")
            print(user_guess_list)

            break

        elif i == len(letter_list):
            attempt = attempt + 1
            print(f"Try again, Attempted {attempt} times")


        elif letter_list == user_guess_list:
            print("you won!")
            exit()


        else:

            continue

    continue

print("Game over")