#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from selenium import webdriver


def init_browser():
    executable_path = {"executable_path":"C:\chromedriver_win32\chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    #url of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p 


    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    
    mars_dict['featured_image'] = featured_image_url


    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html_weather = browser.html
    soup2 = bs(html_weather, 'html.parser')
    mars_weather = soup2.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    mars_dict['mars_weather'] = mars_weather


    url4 = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url4)
    mars_df = mars_table[0]
    mars_html = mars_df.to_html()
    mars_facts = mars_html.replace("\n", "")
    
    mars_dict['mars_facts'] = mars_facts


    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    html = browser.html
    soup4 = bs(html, 'html.parser')
    
    hemisphere_names = []
    names = soup4.find_all('h3')

    for name in names:
        hemisphere_names.append(name.text.replace(' Enhanced',''))
    
    url_ends = []
    enhanced_url = soup4.find_all('a', class_='itemLink product-item')

    for a in enhanced_url:
        url_ends.append(a.get('href'))
    
    unique_url = []

    for end in url_ends:
        if end not in unique_url:
            unique_url.append(end)

    hemisphere_links = []
    parent_url = "https://astrogeology.usgs.gov"
    
    for path in unique_url:
        hemisphere_links.append(parent_url + path)

    hemisphere_image = []

    for link in hemisphere_links:
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_link = soup.find('div', class_='downloads').find('a')['href']
        hemisphere_image.append(image_link)

    hemisphere_dicts = []

    for name, image in zip(hemisphere_names, hemisphere_image):
        hemisphere_dicts.append({"Title": name, "Image_Url": image})

    print(hemisphere_dicts)
    mars_dict['hemisphere_image'] = hemisphere_dicts


    return mars_dict
