#import libraries
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 

#define multiple urls for scraping
url_nasa = 'https://mars.nasa.gov/news/'
url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' 
url_weather = 'https://twitter.com/marswxreport?lang=en'
url_facts= 'https://space-facts.com/mars/'
url_imgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#start up our browser extracted so we can use multiple times
def start_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    #init browser for scraping 
    browser = start_browser()

    # All info goes in this info dict 
    info = {}

    ####### News #######
    browser.visit(url_nasa)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #find & define
    news_title = soup.select_one('.content_title').a.get_text(strip=True)
    news_p = browser.find_by_css('.article_teaser_body').first.text

    info['news_title'] = news_title
    info['news_p'] = news_p

    #######Featured image #######
    # browser = start_browser()
    browser.visit(url_jpl)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    #find & define
    browser.click_link_by_id('full_image')
    browser.is_element_present_by_css(('a.button')[2], wait_time=2)
    browser.find_by_css('a.button')[2].click()
    browser.find_by_css('figure').first.click()
    fiu = browser.find_by_css('img').first['src']
    
    info['fiu'] = fiu

    ####### Weather #######
    # browser = start_browser()
    browser.visit(url_weather)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

     #find & define
    mars_weather = browser.find_by_css('div.js-tweet-text-container').first.text

    info['mars_weather'] = mars_weather

    ####### Facts #######
    # browser = start_browser()
    browser.visit(url_facts)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # find & define

    df = pd.read_html(url_facts, attrs={'id': 'tablepress-p-mars'})[0]
    df = df.set_index(0).rename(columns={1: "value"})
    del df.index.name
    mars_facts = df.to_html(header="true", table_id="table")
    #jinja in template to access 
    
    info['mars_facts'] = mars_facts

    ####### Images #######
    # browser = start_browser()
    browser.visit(url_imgs)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # find & define
    # Img 1 
    t1 = browser.find_by_tag('h3')[0].text
    browser.find_by_css('.thumb')[0].click()
    img1 = browser.find_by_text('Sample')['href']
    # print(img1) # debug
    browser.back()
    #Img 2 
    t2 = browser.find_by_tag('h3')[1].text
    browser.find_by_css('.thumb')[1].click()
    img2 = browser.find_by_text('Sample')['href']
    # print(img2) # debug
    browser.back()

    # Img 3 
    t3 = browser.find_by_tag('h3')[2].text
    browser.find_by_css('.thumb')[2].click()
    img3 = browser.find_by_text('Sample')['href']
    # print(img3) # debug
    browser.back()

    # Img 4 
    t4 = browser.find_by_tag('h3')[3].text
    browser.find_by_css('.thumb')[3].click()
    img4 = browser.find_by_text('Sample')['href']
    # print(img4) # debug
    browser.quit()

    # return the images and titles for dislay
    info['t1'] = t1 
    info['img1'] = img1

    info['t2'] = t2 
    info['img2'] = img2

    info['t3'] = t3 
    info['img3'] = img3

    info['t4'] = t4 
    info['img4'] = img4
    
    #return that info dict
    return info
    
